from dataclasses import dataclass
from typing import List

from app.domain.entity.user import User


@dataclass
class UserList:
    users: List[User]
