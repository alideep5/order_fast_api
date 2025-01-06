from typing import List, Optional, Protocol
from app.domain.entity.user import User
from app.domain.entity.user_detail import UserDetail


class IUserRepo(Protocol):
    async def create_user(self, username: str, password: str) -> User:
        pass

    async def find_by_username(self, username: str) -> Optional[UserDetail]:
        pass

    async def is_username_exists(self, username: str) -> bool:
        pass

    async def find_by_id(self, user_id: str) -> Optional[User]:
        pass

    async def get_all_users(self) -> List[User]:
        pass
