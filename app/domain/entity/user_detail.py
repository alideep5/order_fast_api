from dataclasses import dataclass


@dataclass
class UserDetail:
    id: str
    username: str
    password: str
