import uuid
from typing import Any

from fastapi import APIRouter
from sqlmodel import select

from app.api.deps import CurrentUser, SessionDep
from app.core.models import Alert, AlertCreate, AlertsPublic

router = APIRouter(prefix='/alerts', tags=['alerts'])


@router.get('/', response_model=AlertsPublic)
def get_alerts(session: SessionDep, current_user: CurrentUser) -> Any:
	statement = select(Alert).where(Alert.created_by == current_user.email)
	alerts = session.exec(statement).all()
	
	return AlertsPublic(data=alerts)


@router.post('/')
def create_alert(*, session: SessionDep, current_user: CurrentUser, alert_in: AlertCreate) -> Any:
	alert = Alert.model_validate(alert_in, update={'created_by': current_user.email})
	session.add(alert)
	session.commit()
	session.refresh(alert)
	
	return {'id': alert.alert_id}


@router.put('/{alert_id}')
def update_alert(*, session: SessionDep, current_user: CurrentUser, alert_id: uuid.UUID, alert_in: AlertCreate) -> Any:
	alert = session.get(Alert, alert_id)
	if not alert:
		return {'message': 'Alert not found'}
	
	alert_data = alert_in.model_dump()
	for key, value in alert_data.items():
		setattr(alert, key, value)
	
	alert.created_by = current_user.email
	
	session.add(alert)
	session.commit()
	session.refresh(alert)
	
	return {'id': alert.alert_id}
