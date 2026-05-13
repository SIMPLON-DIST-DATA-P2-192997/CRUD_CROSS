from fastapi import FastAPI
from routers import flotteurs_router, humain_results_router, operations_router, operation_stats_router, ingest_router

app = FastAPI(title="CRUD CROSS API", version="0.1.0")

app.include_router(ingest_router)
app.include_router(operations_router)
app.include_router(flotteurs_router)
app.include_router(humain_results_router)
app.include_router(operation_stats_router)


@app.get("/")
def root():
    return {"message": "CRUD CROSS API is running"}
