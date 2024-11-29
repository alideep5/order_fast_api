from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp
from app.domain.error.response_exception import (
    ForbiddenException,
    UnauthorizedException,
)
from app.domain.util.jwt_util import JWTUtil
from typing import Callable, Awaitable, Optional, Sequence


class JWTMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        jwt_util: JWTUtil,
        exempt_routes: Optional[Sequence[str]] = None,
    ) -> None:
        super().__init__(app)
        self.jwt_util = jwt_util
        self.exempt_routes = exempt_routes or []

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        path: str = request.url.path

        if any(path.startswith(exempt_route) for exempt_route in self.exempt_routes):
            return await call_next(request)

        token: Optional[str] = request.headers.get("Authorization")
        if not token:
            raise ForbiddenException()

        try:
            user_id: str = self.jwt_util.get_user_id(token=token)
            request.state.user = user_id
        except Exception:
            raise UnauthorizedException()

        response: Response = await call_next(request)
        return response
