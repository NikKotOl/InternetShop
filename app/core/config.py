from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    SECRET_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )


settings = Settings(POSTGRES_DB="internet_shop", 
                    POSTGRES_USER="postgres", 
                    POSTGRES_PASSWORD="postgres", 
                    POSTGRES_HOST="localhost",
                    POSTGRES_PORT=5432,
                    SECRET_KEY="KvW3EdQQlb87WFEhSYRYb3DabK8EseU_iASBjQDs1HY")
