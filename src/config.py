from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: bool = False
    log_format: str = "[%(asctime)s]-[%(levelname)s]-[%(name)s]: %(message)s"
    version: str = "1.0"

    # Set when behind reverse proxy with path prefix (e.g. /backend/salary-index)
    root_path: str = ""

    secret_key: str = "secret_key"

    domclick_api_url: str = "domclick_api_url"
    user_agent: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    data_file_path: str = "data/cities_sqm_price.json"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
