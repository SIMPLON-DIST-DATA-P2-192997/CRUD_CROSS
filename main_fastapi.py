from fastapi import FastAPI
from routers import flotteurs_router, humain_results_router, operations_router, operation_stats_router, ingest_router
from routers.audit import router as audit_router
from audit import register_audit_listeners
from database import engine
from models import Base

Base.metadata.create_all(engine)
register_audit_listeners()

app = FastAPI(title="CRUD CROSS API", version="0.1.0")

app.include_router(ingest_router)
app.include_router(operations_router)
app.include_router(flotteurs_router)
app.include_router(humain_results_router)
app.include_router(operation_stats_router)
app.include_router(audit_router)


@app.get("/")
def root():
    return {"message": "CRUD CROSS API is running"}
