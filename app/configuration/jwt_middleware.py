from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp
from app.common.model.error_response import ErrorResponse
from app.common.error.response_exception import (
    BaseResponseException,
    UnauthorizedException,
)
from app.common.model.user_info import UserInfo
from app.common.util.jwt_util import JWTUtil
from typing import Callable, Awaitable, Optional, Sequence
from app.common.app_logger import AppLogger


class JWTMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        jwt_util: JWTUtil,
        log: AppLogger,
        exempt_routes: Optional[Sequence[str]] = None,
    ) -> None:
        super().__init__(app)
        self.jwt_util = jwt_util
        self.log = log
        self.exempt_routes = exempt_routes or []

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        try:
            path: str = request.url.path

            if any(
                path.startswith(exempt_route) for exempt_route in self.exempt_routes
            ):
                return await call_next(request)

            auth_header: Optional[str] = request.headers.get("Authorization")
            if not auth_header:
                raise UnauthorizedException(message="Missing Authorization token")

            if not auth_header.startswith("Bearer "):
                raise UnauthorizedException(
                    message="Invalid Authorization header format"
                )

            token: str = auth_header[7:].strip()

            if not self.jwt_util.validate_token(token=token):
                raise UnauthorizedException(message="Invalid Authorization token")

            user: Optional[UserInfo] = self.jwt_util.get_user(token=token)
            if not user:
                raise UnauthorizedException(message="Invalid Authorization token")

            request.state.user = user

            response: Response = await call_next(request)
            return response

        except BaseResponseException as baseResponseException:
            self.log.error(
                f"{baseResponseException.status_code} Error occurred while processing request '{request.url}': {baseResponseException.message}"
            )

            return JSONResponse(
                status_code=baseResponseException.status_code,
                content=ErrorResponse(error=baseResponseException.message).model_dump(),
            )

        except Exception as exception:
            self.log.error(
                f"Unexpected error occurred while processing request '{request.url} {exception}'"
            )

            return JSONResponse(
                status_code=500,
                content=ErrorResponse(error="Internal Server Error").model_dump(),
            )
