from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes.admin import router as admin_router
from .api.routes.auth import router as auth_router
from .api.routes.crops import router as crops_router
from .api.routes.evaporation import router as evaporation_router
from .api.routes.scenarios import router as scenarios_router
from .api.routes.specialist import router as specialist_router
from .api.routes.water import router as water_router
from .config import get_settings
from .db import Base, engine
from .models import *  # noqa: F401,F403

settings = get_settings()
from contextlib import asynccontextmanager
from sqlalchemy import text

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown

app = FastAPI(title=settings.app_name, version='1.0.0', docs_url='/docs', lifespan=lifespan)

if settings.cors_enabled:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[origin.strip() for origin in settings.allowed_origins.split(',') if origin.strip()],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

app.include_router(auth_router)
app.include_router(evaporation_router)
app.include_router(crops_router)
app.include_router(water_router)
app.include_router(scenarios_router)
app.include_router(specialist_router)
app.include_router(admin_router)

@app.get('/health')
def health() -> dict:
    db_status = 'ok'
    try:
        with engine.connect() as conn:
            conn.execute(text('SELECT 1'))
    except Exception:
        db_status = 'error'
    
    return {
        'status': 'ok' if db_status == 'ok' else 'degraded', 
        'app': settings.app_name,
        'database': db_status
    }
