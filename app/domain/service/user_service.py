from app.domain.entity.user import User
from app.domain.unit_of_work.transaction_manager import ITransactionManager
from app.persistence.repository.user_repo import UserRepo


class UserService:
    def __init__(self, unit_of_work: ITransactionManager, user_repo: UserRepo) -> None:
        self.unit_of_work = unit_of_work
        self.user_repo = user_repo

    async def create_account(self, user_name: str, password: str) -> User:
        async with self.unit_of_work.get_transaction() as transaction:
            user: User = await self.user_repo.create_user(
                transaction=transaction, username=user_name, password=password
            )
            await transaction.commit()

            return user
