from domain.model.user_detail import UserDetail
from persistence.repository.user_repo import UserRepo


class UserService:
    def __init__(self):
        self.user_repository = UserRepo()

    def create_account(self, user_name: str, password: str) -> UserDetail:
        return self.user_repository.create_user(user_name=user_name, password=password)
