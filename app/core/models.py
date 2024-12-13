import uuid

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class Quotes(SQLModel):
	quotes: dict[str, float]


class Prices(SQLModel, table=True):
	symbol: str = Field(max_length=255, primary_key=True)
	price: float


class AlertBase(SQLModel):
	token: str
	condition: str = Field(max_length=255)
	price: float


class AlertCreate(AlertBase):
	pass


class Alert(AlertBase, table=True):
	alert_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
	created_by: EmailStr = Field(foreign_key='user.email', nullable=False, ondelete='CASCADE')


class AlertPublic(AlertBase):
	created_by: EmailStr
	alert_id: uuid.UUID


class AlertsPublic(SQLModel):
	data: list[AlertPublic]


class User(SQLModel, table=True):
	email: EmailStr = Field(unique=True, max_length=255, primary_key=True)
	hashed_password: str


class UserIn(SQLModel):
	email: str
	password: str


class UserPublic(SQLModel):
	email: str


class Token(SQLModel):
	access_token: str
	token_type: str = 'bearer'


class TokenPayload(SQLModel):
	sub: str | None = None
