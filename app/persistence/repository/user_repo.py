from domain.model.user_detail import UserDetail


class UserRepo:
    def __init__(self):
        self.db = "db"

    def create_user(self, user_name: str, password: str) -> UserDetail:
        return UserDetail(user_id="1", name=user_name)
