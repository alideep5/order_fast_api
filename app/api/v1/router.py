from fastapi import APIRouter
from api.v1.controller.user_controller import router as user_router
from api.v1.controller.todo_controller import router as todo_router

router = APIRouter(prefix="/v1")

router.include_router(user_router, tags=["user"])
router.include_router(todo_router, tags=["todo"])