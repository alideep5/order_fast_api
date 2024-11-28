from dataclasses import dataclass


@dataclass
class LoginUser:
    id: str
    username: str
    token: str
