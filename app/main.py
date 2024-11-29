from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from app.api.dto.error_response import ErrorResponse
from app.api.middleware.jwt_middleware import JWTMiddleware
from app.config.app_container import AppContainer
from app.domain.error.response_exception import BaseResponseException
from fastapi.responses import JSONResponse

app_container = AppContainer()

app = FastAPI(root_path="/api")


@app.exception_handler(BaseResponseException)
async def handle_base_exception(
    request: Request, exc: BaseResponseException
) -> JSONResponse:
    print(
        f"{exc.status_code} Error occurred while processing request '{request.url}': {exc.message}"
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(error=exc.message).model_dump(),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    error_details = ", ".join(
        [f"{err['loc'][-1]}: {err['msg']}" for err in exc.errors()]
    )

    print(
        f"Validation error occurred while processing request '{request.url}': {error_details}"
    )

    return JSONResponse(
        status_code=400,
        content=ErrorResponse(error=f"{error_details}").model_dump(),
    )


@app.exception_handler(Exception)
async def handle_unexpected_exception(request: Request, exc: Exception) -> JSONResponse:
    print(f"Unexpected error occurred while processing request '{request.url}': {exc}")

    return JSONResponse(
        status_code=500,
        content=ErrorResponse(error="Internal Server Error").model_dump(),
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

app.include_router(app_container.v1_router())
