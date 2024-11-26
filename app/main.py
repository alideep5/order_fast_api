from fastapi import FastAPI
from app.api.v1.v1_router import V1Router
from app.config.app_container import AppContainer

app = FastAPI(root_path="/api")

app_container = AppContainer()

app.include_router(app_container.v1_router())
