from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from app.configuration.jwt_middleware import JWTMiddleware
from app.app_container import AppContainer
from app.configuration.swagger_config import SwaggerConfig

app_container = AppContainer()

app = FastAPI(root_path="/api")
app.add_exception_handler(Exception, app_container.exception_handler().handle_exception)
app.add_exception_handler(
    RequestValidationError, app_container.exception_handler().handle_exception
)

app.add_middleware(
    JWTMiddleware,
    jwt_util=app_container.jwt_util(),
    log=app_container.app_logger(),
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
