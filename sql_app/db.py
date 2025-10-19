import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str

    class Config:
        env_file = ".env"

    @property
    def sqlalchemy_url(self) -> str:
        return(
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

settings = Settings()
engine = create_async_engine(settings.sqlalchemy_url, echo=False)
AsyncSession = async_sessionmaker(engine, expire_on_commit=False)