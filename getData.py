import os
import requests
import pandas as pd
from io import StringIO
from dotenv import load_dotenv
from sqlalchemy import create_engine

from models import Base, Flotteur, HumainResult, Operation, OperationStats
from schemas.flotteur import FlotteurSchema
from schemas.humain_results import HumainResultSchema
from schemas.operations import OperationSchema
from schemas.operations_stats import OperationStatsSchema

load_dotenv()

DB_URL = (
    f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST', 'localhost')}:{os.getenv('POSTGRES_PORT', '5432')}"
    f"/{os.getenv('POSTGRES_DB')}"
)
engine = create_engine(DB_URL)
Base.metadata.create_all(engine)

SCHEMAS = {
    "human_result": HumainResultSchema,
    "operation_stat": OperationStatsSchema,
    "flotteur": FlotteurSchema,
    "operation": OperationSchema,
}

ORM_MODELS = {
    "operation": Operation,
    "human_result": HumainResult,
    "operation_stat": OperationStats,
    "flotteur": Flotteur,
}

urls = [
  {
    "name" : "operation",
    "url" : "https://www.data.gouv.fr/api/1/datasets/r/fae6bc13-fe4c-4838-b281-b16628b7babe"
  },
  {
    "name" : "human_result",
    "url" : "https://www.data.gouv.fr/api/1/datasets/r/8eb7f207-1ce5-460c-b941-5f1761a79c46"
  },
  {
    "name" : "operation_stat",
    "url" : "https://www.data.gouv.fr/api/1/datasets/r/5d3c65fb-c861-4b22-b8aa-1eab58e3d9db"
  },
  {
    "name" : "flotteur",
    "url" : "https://www.data.gouv.fr/api/1/datasets/r/ae0e17e4-7117-45f0-80c4-b11b38f31c5c"
  }
]

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

# Quarantined columns: present in source but excluded from DB seeding
# - seconde_autorite (operation): 96% null, marginal value
# - cross_sitrep (operation): unique free-text per row, not analytical
# - numero_immatriculation (flotteur): 57% null, values are SHA-1 hashes (anonymised)
QUARANTINE: dict[str, list[str]] = {
    "operation": ["seconde_autorite", "cross_sitrep"],
    "flotteur": ["numero_immatriculation"],
}

# Fetch and validate all CSVs before touching the DB
datasets: dict[str, pd.DataFrame] = {}
for item in urls:
    res = requests.get(item["url"], headers=headers)
    res.raise_for_status()
    df = pd.read_csv(StringIO(res.content.decode("utf-8")), sep=",", low_memory=False)

    schema = SCHEMAS[item["name"]]
    schema.validate(df)
    print(f"✅ {item['name']}: validation passed")

    quarantine_cols = [c for c in QUARANTINE.get(item["name"], []) if c in df.columns]
    if quarantine_cols:
        quarantine_df = df[["operation_id"] + quarantine_cols] if "operation_id" in df.columns else df[quarantine_cols]
        quarantine_df.to_csv(f'./quarantine/{item["name"]}.csv', index=False)
        print(f"🔒 {item['name']}: quarantined {quarantine_cols} → quarantine/{item['name']}.csv")

    db_df = df.drop(columns=quarantine_cols)
    db_df.to_csv(f'./data/{item["name"]}.csv', index=False)
    datasets[item["name"]] = db_df

# Delete in child-first order to respect FK constraints, then insert
# Delete order: children first, parent last
# Insert order: parent first, children after
DELETE_ORDER = ["operation_stat", "human_result", "flotteur", "operation"]
INSERT_ORDER = ["operation", "flotteur", "human_result", "operation_stat"]

with engine.begin() as conn:
    for name in DELETE_ORDER:
        conn.execute(ORM_MODELS[name].__table__.delete())
        print(f"🗑️  {name}: table cleared")

    for name in INSERT_ORDER:
        df = datasets[name]
        records: list[dict[str, object]] = [
            {str(k): v for k, v in row.items()}
            for row in df.where(pd.notnull(df), other=None).to_dict(orient="records")  # type: ignore[arg-type]
        ]
        conn.execute(ORM_MODELS[name].__table__.insert(), records)  # type: ignore[arg-type]
        print(f"📥 {name}: {len(records)} rows inserted")

