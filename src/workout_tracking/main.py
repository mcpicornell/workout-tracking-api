from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqladmin import Admin

from .admin import ADMIN_VIEWS, get_authentication_backend
from .infra.db.database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

admin = Admin(app, engine, authentication_backend=get_authentication_backend())

for view in ADMIN_VIEWS:
    admin.add_view(view)


@app.get("/")
def read_root():
    return {"message": "Welcome to Workout Tracking API"}
