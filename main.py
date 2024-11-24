from fastapi import FastAPI
from api.user_controller import router as user_router
from api.todo_controller import router as todo_router

app = FastAPI(root_path="/api")

app.include_router(user_router, tags=["user"])
app.include_router(todo_router, tags=["todo"])