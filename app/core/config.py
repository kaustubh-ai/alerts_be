from typing import Annotated, Any

from pydantic import (AnyUrl, BeforeValidator, computed_field)
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(v: Any) -> list[str] | str:
	if isinstance(v, str) and not v.startswith('['):
		return [i.strip() for i in v.split(',')]
	elif isinstance(v, list | str):
		return v
	raise ValueError(v)


class Settings(BaseSettings):
	model_config = SettingsConfigDict(env_file='.env', env_ignore_empty=True, extra='ignore')
	
	API_VERSION: str = '/api/v1'
	SECRET_KEY: str
	ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
	FRONTEND_HOST: str = 'http://localhost:5173'
	BACKEND_CORS_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)] = []
	CRYPTO_URL: str
	CRYPTO_API_KEY: str
	
	@computed_field
	@property
	def all_cors_origins(self) -> list[str]:
		return [str(origin).rstrip('/') for origin in self.BACKEND_CORS_ORIGINS] + [self.FRONTEND_HOST]
	
	PROJECT_NAME: str = 'Alerts'
	
	SQLALCHEMY_DATABASE_URI: str = 'sqlite:///./test.db'
	ZOHO_TOKEN: str


settings = Settings()