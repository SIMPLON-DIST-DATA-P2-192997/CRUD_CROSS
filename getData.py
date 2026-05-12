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
    "operation_stats": OperationStatsSchema,
    "flotteurs": FlotteurSchema,
    "operations": OperationSchema,
}

ORM_MODELS = {
    "human_result": HumainResult,
    "operation_stats": OperationStats,
    "flotteurs": Flotteur,
    "operations": Operation,
}

urls = [
  {
    "name" : "human_result",
    "url" : "https://www.data.gouv.fr/api/1/datasets/r/8eb7f207-1ce5-460c-b941-5f1761a79c46"
  },
  {
    "name" : "operation_stats",
    "url" : "https://www.data.gouv.fr/api/1/datasets/r/5d3c65fb-c861-4b22-b8aa-1eab58e3d9db"
  },
  {
    "name" : "flotteurs",
    "url" : "https://www.data.gouv.fr/api/1/datasets/r/ae0e17e4-7117-45f0-80c4-b11b38f31c5c"
  },
  {
    "name" : "operations",
    "url" : "https://www.data.gouv.fr/api/1/datasets/r/fae6bc13-fe4c-4838-b281-b16628b7babe"
  }
]

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

for item in urls:
    res = requests.get(item["url"], headers=headers)
    res.raise_for_status()
    df = pd.read_csv(StringIO(res.content.decode("utf-8")), sep=",", low_memory=False)

    schema = SCHEMAS[item["name"]]
    schema.validate(df)
    print(f"✅ {item['name']}: validation passed")

    df.to_csv(f'./data/{item["name"]}.csv', index=False)

    orm_model = ORM_MODELS[item["name"]]
    records: list[dict[str, object]] = [
        {str(k): v for k, v in row.items()}
        for row in df.where(pd.notnull(df), other=None).to_dict(orient="records")  # type: ignore[arg-type]
    ]
    with engine.begin() as conn:
        conn.execute(orm_model.__table__.delete())
        conn.execute(orm_model.__table__.insert(), records)  # type: ignore[arg-type]
    print(f"📥 {item['name']}: {len(records)} rows inserted into PostgreSQL")

