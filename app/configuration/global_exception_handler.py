from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.common.model.error_response import ErrorResponse
from app.common.error.response_exception import BaseResponseException
from app.common.app_logger import AppLogger


class GlobalExceptionHandler:
    def __init__(self, log: AppLogger):
        self.log = log

    async def handle_exception(self, request: Request, exc: Exception) -> JSONResponse:
        if isinstance(exc, BaseResponseException):
            return await self.handle_base_exception(request, exc)

        if isinstance(exc, RequestValidationError):
            return await self.validation_exception_handler(request, exc)

        self.log.error(
            f"Unexpected error occurred while processing request '{request.url} {exc}'"
        )
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(error="Internal Server Error").model_dump(),
        )

    async def handle_base_exception(
        self, request: Request, exc: BaseResponseException
    ) -> JSONResponse:
        self.log.error(
            f"{exc.status_code} Error occurred while processing request '{request.url}': {exc.message}"
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(error=exc.message).model_dump(),
        )

    async def validation_exception_handler(
        self, request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        error_details = ", ".join(
            [f"{err['loc'][-1]}: {err['msg']}" for err in exc.errors()]
        )
        self.log.error(
            f"Validation error occurred while processing request '{request.url}': {error_details}"
        )
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(error=f"{error_details}").model_dump(),
        )
