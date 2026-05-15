from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers import flotteurs_router, humain_results_router, operations_router, operation_stats_router, ingest_router
from routers.audit import router as audit_router
from audit import register_audit_listeners
from database import engine
from models import Base, Operation
from sqlalchemy.orm import Session

Base.metadata.create_all(engine)
register_audit_listeners()


@asynccontextmanager
async def lifespan(app: FastAPI):
    with Session(engine) as session:
        if session.query(Operation).first() is None:
            print("📭 No data found in DB — running getData.py...")
            import runpy
            runpy.run_path("getData.py")
            print("✅ getData.py completed.")
    yield


app = FastAPI(title="CRUD CROSS API", version="0.1.0", lifespan=lifespan)

app.include_router(ingest_router)
app.include_router(operations_router)
app.include_router(flotteurs_router)
app.include_router(humain_results_router)
app.include_router(operation_stats_router)
app.include_router(audit_router)


@app.get("/")
def root():
    return {"message": "CRUD CROSS API is running"}
