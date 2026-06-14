from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    
    database_username: str = ""
    database_hostname: str = ""
    database_port: str = ""
    database_password: str = ""
    database_name: str = ""
    secret_key: str = ""
    algorithm: str = ""
    access_token_expire_minutes: int = 100
    rate_limit_enabled: bool = True
    rate_limit_capacity: int = 60
    rate_limit_refill_rate: float = 1.0

    model_config = {"env_file": ".env"}

settings = Settings()
