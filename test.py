from sqlmodel import Session, select

from app.core.db import create_db_and_tables, engine
from app.core.models import User

create_db_and_tables()

with Session(engine) as sess:
	all_users = sess.exec(select(User)).all()
	print(all_users)
