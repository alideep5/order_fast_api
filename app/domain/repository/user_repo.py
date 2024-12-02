from typing import Any, List, Optional, Protocol
from app.domain.entity.user import User
from app.domain.entity.user_detail import UserDetail
from app.domain.unit_of_work.transaction import ITransaction


class IUserRepo(Protocol):
    async def create_user(
        self, transaction: ITransaction[Any], username: str, password: str
    ) -> User:
        pass

    async def find_by_username(
        self, transaction: ITransaction[Any], username: str
    ) -> Optional[UserDetail]:
        pass

    async def is_username_exists(
        self, transaction: ITransaction[Any], username: str
    ) -> bool:
        pass

    async def find_by_id(
        self, transaction: ITransaction[Any], user_id: str
    ) -> Optional[User]:
        pass

    async def get_all_users(self, transaction: ITransaction[Any]) -> List[User]:
        pass
