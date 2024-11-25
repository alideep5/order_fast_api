from fastapi import FastAPI
from api.v1.v1_router import V1Router

app = FastAPI(root_path="/api")

app.include_router(V1Router())
