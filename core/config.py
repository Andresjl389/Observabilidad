from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DB_PORT: str
    DB_ENGINE: str
    DB_NAME: str

    @property
    def DATABASE_URL(self) -> str:
        return f"{self.DB_ENGINE}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = Path(__file__).resolve().parent.parent / ".env"
        env_file_encoding = "utf-8"

# Instancia global
settings = Settings()

# Validación visual
if __name__ == "__main__":
    print("✅ DB_HOST:", settings.DB_HOST)
    print("✅ DATABASE_URL:", settings.DATABASE_URL)
