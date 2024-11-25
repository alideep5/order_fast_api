from domain.model.user_detail import UserDetail
from persistence.db_session_manager import DbSessionManager
from persistence.orm.user import User


class UserRepo:
    def __init__(self):
        self.db_session_manager = DbSessionManager()

    async def create_user(self, username: str, password: str) -> UserDetail:
        user = User(username=username, password=password)

        async with self.db_session_manager.get_session() as session:
            session.add(user)
            await session.commit()
            await session.refresh(user)

        return UserDetail(user_id=user.id, name=user.username)
