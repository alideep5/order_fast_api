from domain.model.user_detail import UserDetail
from persistence.session_manager import SessionManager
from persistence.orm.user import User


class UserRepo:
    def __init__(self) -> None:
        self.session_manager = SessionManager()

    async def create_user(self, username: str, password: str) -> UserDetail:
        user = User(username=username, password=password)

        async with self.session_manager.get_session() as session:
            session.add(user)
            # await session.flush()
            await session.commit()
            await session.refresh(user)

        return UserDetail(user_id=user.id, name=user.username)
