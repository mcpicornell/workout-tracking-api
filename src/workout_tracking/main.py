from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqladmin import Admin

from .dependencies import get_dependencies
from .infra.admin.admin_views import ADMIN_VIEWS
from .infra.db.database import Base, engine, AsyncSessionLocal
from .infra.admin.admin_auth import AdminAuth
from .settings import get_settings



@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


dependencies = None
app = FastAPI(lifespan=lifespan)

settings = get_settings()
admin_auth = AdminAuth(
    secret_key=settings.SECRET_AUTH_KEY,
    session_factory=AsyncSessionLocal,
)

admin = Admin(
    app,
    engine,
    authentication_backend=admin_auth,
)

for view in ADMIN_VIEWS:
    admin.add_view(view)


@app.get("/")
def read_root():
    return {"message": "Welcome to Workout Tracking API"}
