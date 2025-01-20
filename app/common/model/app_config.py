from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    database_url: str
    jwt_secret: str
    jwt_expiration_time: float
    cloudflare_pem: str
    customer_id: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        populate_by_name = True
        extra = "allow"
