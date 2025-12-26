from fastapi import FastAPI
from backend.routes.data_api import router as data_router
from backend.routes.health import router as health_router
from backend.routes.file_api import router as file_router

app = FastAPI(title="LMT Dashboard API")

# Health routes
app.include_router(health_router)

# Data + Files routes
app.include_router(data_router)

app.include_router(file_router)

# Run using:
# uvicorn backend.app:app --reload
