from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL

REPO_ROOT = Path(__file__).resolve().parents[3]
DOTENV_PATH = REPO_ROOT / ".env"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=DOTENV_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    KNOWLEDGE_BASE_DIR: Path = REPO_ROOT / "knowledge_base"
    ACCESS_POLICY_VERSION: str = "v1.0"
    EMBEDDING_DIM: int = 384

    def get_database_url(self, database: str | None = None) -> URL:
        return URL.create(
            drivername="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            database=database or self.POSTGRES_DB,
        )

    @property
    def database_url(self) -> URL:
        return self.get_database_url()

settings = Settings()
