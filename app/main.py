from fastapi import FastAPI
from app.config.app_config import AppConfig
from app.config.app_container import AppContainer

app_config = AppConfig()

app = FastAPI(root_path="/api")

app_container = AppContainer()

app.include_router(app_container.v1_router())
