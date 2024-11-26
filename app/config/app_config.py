from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    db: str
    datasource_username: str
    datasource_password: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        populate_by_name = True
