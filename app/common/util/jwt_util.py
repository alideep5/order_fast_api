import json
from typing import Optional
import jwt
from datetime import datetime, timezone, timedelta
from app.common.configuration.app_config import AppConfig
from app.common.model.user_info import UserInfo


class JWTUtil:
    def __init__(self, app_config: AppConfig) -> None:
        self.jwt_secret = app_config.jwt_secret_key
        self.jwt_expiration_time = app_config.jwt_expiration_time

    def generate_token(self, user: UserInfo) -> str:
        now = datetime.now(timezone.utc)
        expiration_date = now + timedelta(seconds=self.jwt_expiration_time)
        payload = {
            "sub": user.model_dump_json(),
            "iat": int(now.timestamp()),
            "exp": int(expiration_date.timestamp()),
        }
        return jwt.encode(payload, self.jwt_secret, algorithm="HS256")

    def get_user(self, token: str) -> Optional[UserInfo]:
        try:
            decoded = jwt.decode(token, self.jwt_secret, algorithms=["HS256"])
            user_data = json.loads(decoded.get("sub"))
            return UserInfo(**user_data)
        except Exception:
            return None

    def validate_token(self, token: str) -> bool:
        try:
            jwt.decode(
                token,
                self.jwt_secret,
                algorithms=["HS256"],
                options={"verify_exp": True},
            )
            return True
        except Exception:
            return False
