from typing import Any

from fastapi import APIRouter, HTTPException

from app import crud
from app.api.deps import SessionDep
from app.core.models import UserIn, UserPublic

router = APIRouter(prefix='/signup', tags=['signup'])


@router.post('/', response_model=UserPublic)
def signup_user(session: SessionDep, user_in: UserIn) -> Any:
	user = crud.get_user_by_email(session=session, email=user_in.email)
	if user:
		raise HTTPException(status_code=400, detail='User already exists')
	
	user_create = UserIn.model_validate(user_in)
	user = crud.create_user(session=session, user_create=user_create)
	
	return user
