from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / 'certs' / 'jwt-private.pem'
    public_key_path: Path = BASE_DIR / 'certs' / 'jwt-public.pem'
    algorithm: str = 'RS256'
    access_token_expire_minutes: int = 30


class Settings(BaseSettings):

    AUTH_HOST: str = 'db_auth'
    AUTH_PORT: int = 5432
    AUTH_DB: str = 'auth'
    AUTH_USER: str = 'user'
    AUTH_PASSWORD: str = '1111'

    auth_jwt: AuthJWT = AuthJWT()

    @property
    def DATABASE_URL(self):
        return (
            f'postgresql+asyncpg://{self.AUTH_USER}:'
            f'{self.AUTH_PASSWORD}@{self.AUTH_HOST}:'
            f'{self.AUTH_PORT}/{self.AUTH_DB}'
        )

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
