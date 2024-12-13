from fastapi import APIRouter

from app.api.routes import alerts, quotes, signin, signup

api_router = APIRouter()
api_router.include_router(quotes.router)
api_router.include_router(alerts.router)
api_router.include_router(signin.router)
api_router.include_router(signup.router)
