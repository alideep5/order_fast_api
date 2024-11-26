from app.domain.entity.user import User
from app.persistence.session_manager import SessionManager
from app.persistence.table.user_table import UserTable


class UserRepo:
    def __init__(self, session_manager: SessionManager) -> None:
        self.session_manager = session_manager

    async def create_user(self, username: str, password: str) -> User:
        user = UserTable(username=username, password=password)

        async with self.session_manager.get_session() as session:
            session.add(user)
            # await session.flush()
            await session.commit()
            await session.refresh(user)

        return User(user_id=user.id, name=user.username)
