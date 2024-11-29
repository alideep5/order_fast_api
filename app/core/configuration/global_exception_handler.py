from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.core.model.error_response import ErrorResponse
from app.core.error.response_exception import BaseResponseException


class GlobalExceptionHandler:
    @staticmethod
    async def handle_exception(request: Request, exc: Exception) -> JSONResponse:
        if isinstance(exc, BaseResponseException):
            return await GlobalExceptionHandler.handle_base_exception(request, exc)

        if isinstance(exc, RequestValidationError):
            return await GlobalExceptionHandler.validation_exception_handler(
                request, exc
            )

        print(
            f"Unexpected error occurred while processing request '{request.url} {exc}'"
        )
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(error="Internal Server Error").model_dump(),
        )

    @staticmethod
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

    @staticmethod
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
