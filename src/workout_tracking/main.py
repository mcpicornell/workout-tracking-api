from fastapi import FastAPI
from sqladmin import Admin
from .infra.db.database import engine, Base
from .admin import ADMIN_VIEWS
from .auth import AdminAuth
from .dependencies import get_dependencies
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

authentication_backend = AdminAuth(secret_key="change-this-to-a-secure-random-string")
admin = Admin(app, engine, authentication_backend=authentication_backend)

for view in ADMIN_VIEWS:
    admin.add_view(view)

@app.get("/")
def read_root():
    return {"message": "Welcome to Workout Tracking API"}
