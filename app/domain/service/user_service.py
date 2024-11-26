from app.domain.entity.user import User
from app.persistence.repository.user_repo import UserRepo


class UserService:
    def __init__(self) -> None:
        self.user_repository = UserRepo()

    async def create_account(self, user_name: str, password: str) -> User:
        return await self.user_repository.create_user(
            username=user_name, password=password
        )
