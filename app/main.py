from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from app.core.middleware.jwt_middleware import JWTMiddleware
from app.app_container import AppContainer
from app.core.config.global_exception_handler import GlobalExceptionHandler
from app.core.config.swagger_config import SwaggerConfig

app_container = AppContainer()

app = FastAPI(root_path="/api")

app.add_exception_handler(Exception, GlobalExceptionHandler.handle_exception)
app.add_exception_handler(
    RequestValidationError, GlobalExceptionHandler.handle_exception
)

app.add_middleware(
    JWTMiddleware,
    jwt_util=app_container.jwt_util(),
    exempt_routes=[
        "/docs",
        "/api/openapi.json",
        "/api/v1/account/login",
        "/api/v1/account/create-account",
    ],
)

swagger_config = SwaggerConfig(app)
swagger_config.add_security_scheme()

app.include_router(app_container.v1_router())
