import jwt
from datetime import datetime, timezone, timedelta
from app.config.app_config import AppConfig


class JWTUtil:
    def __init__(self, app_config: AppConfig) -> None:
        self.jwt_secret = app_config.jwt_secret_key
        self.jwt_expiration_time = app_config.jwt_expiration_time

    def generate_token(self, user_id: str) -> str:
        now = datetime.now(timezone.utc)
        expiration_date = now + timedelta(seconds=self.jwt_expiration_time)
        payload = {
            "sub": user_id,
            "iat": int(now.timestamp()),
            "exp": int(expiration_date.timestamp()),
        }
        return jwt.encode(payload, self.jwt_secret, algorithm="HS256")

    def get_user_id(self, token: str) -> str:
        decoded = jwt.decode(token, self.jwt_secret, algorithms=["HS256"])
        user_id = decoded.get("sub")
        if not isinstance(user_id, str):
            raise ValueError("Token does not contain 'sub' claim")
        return user_id

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
