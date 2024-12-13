import threading
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.core.config import settings
from app.core.db import create_db_and_tables
from app.utils import monitor_alerts


@asynccontextmanager
async def lifespan(application: FastAPI):
	create_db_and_tables()
	threading.Thread(target=monitor_alerts, daemon=True).start()
	yield


app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f'{settings.API_VERSION}/openapi.json', lifespan=lifespan)
if settings.all_cors_origins:
	app.add_middleware(CORSMiddleware, allow_origins=settings.all_cors_origins, allow_credentials=True,
	                   allow_methods=['*'], allow_headers=['*'])

app.include_router(api_router, prefix=settings.API_VERSION)


@app.get('/')
async def root():
	return {'message': 'Alerts v1'}


if __name__ == '__main__':
	uvicorn.run(app, host='localhost', port=8004)
