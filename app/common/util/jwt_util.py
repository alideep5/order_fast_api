import json
from typing import Optional
import jwt
from datetime import datetime, timezone, timedelta
from app.common.model.app_config import AppConfig
from app.common.model.user_info import UserInfo
from app.common.app_logger import AppLogger


class JWTUtil:
    def __init__(self, app_config: AppConfig, log: AppLogger) -> None:
        self.app_config = app_config
        self.log = log

    def generate_token(self, user: UserInfo) -> str:
        now = datetime.now(timezone.utc)
        expiration_date = now + timedelta(seconds=self.app_config.jwt_expiration_time)
        payload = {
            "sub": user.model_dump_json(),
            "iat": int(now.timestamp()),
            "exp": int(expiration_date.timestamp()),
        }
        return jwt.encode(payload, self.app_config.jwt_secret, algorithm="HS256")

    def get_user(self, token: str) -> Optional[UserInfo]:
        try:
            decoded = jwt.decode(
                token, self.app_config.jwt_secret, algorithms=["HS256"]
            )
            user_data = json.loads(decoded.get("sub"))
            return UserInfo(**user_data)
        except Exception as ex:
            self.log.error(f"Error while decoding token: {ex}")

            return None

    def validate_token(self, token: str) -> bool:
        try:
            jwt.decode(
                token,
                self.app_config.jwt_secret,
                algorithms=["HS256"],
                options={"verify_exp": True},
            )
            return True
        except Exception as ex:
            self.log.error(f"Error while validate token: {ex}")
            return False
