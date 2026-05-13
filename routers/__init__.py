from routers.flotteurs import router as flotteurs_router
from routers.humain_results import router as humain_results_router
from routers.operations import router as operations_router
from routers.operation_stats import router as operation_stats_router
from routers.ingest import router as ingest_router

__all__ = [
    "flotteurs_router",
    "humain_results_router",
    "operations_router",
    "operation_stats_router",
    "ingest_router",
]
