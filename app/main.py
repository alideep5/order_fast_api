from fastapi import FastAPI
from api.v1.router import router

app = FastAPI(root_path="/api")

app.include_router(router)