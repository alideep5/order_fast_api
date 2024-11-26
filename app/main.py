from fastapi import FastAPI
from app.config.app_container import AppContainer

app_container = AppContainer()

app = FastAPI(root_path="/api")

app.include_router(app_container.v1_router())
