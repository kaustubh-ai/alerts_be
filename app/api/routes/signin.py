from datetime import timedelta

from fastapi import APIRouter, HTTPException

from app import crud
from app.api.deps import SessionDep
from app.core import security
from app.core.config import settings
from app.core.models import Token, UserIn

router = APIRouter(prefix='/signin', tags=['signin'])


@router.post('/')
def signin_user(session: SessionDep, user_in: UserIn) -> Token:
	user = crud.authenticate(session=session, email=user_in.email, password=user_in.password)
	if not user:
		raise HTTPException(status_code=400, detail='Incorrect email or password')
	
	access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
	access_token = security.create_access_token(user.email, expires_delta=access_token_expires)
	
	return Token(access_token=access_token)
