from app.common.error.response_exception import UnauthorizedException
from app.common.model.user_info import UserInfo
from fastapi import Request


class RequestUtil:
    @staticmethod
    def get_auth_user(request: Request) -> UserInfo:
        user: UserInfo = request.state.user
        if not user:
            raise UnauthorizedException(message="Invalid Authorization token")
        return user
