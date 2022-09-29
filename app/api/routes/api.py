from fastapi import APIRouter

from app.api.routes import message

router = APIRouter()

router.include_router(message.router, tags=["message"], prefix="/message")
