from fastapi import APIRouter
from app.api.routes import operations

router = APIRouter()

router.include_router(operations.router, prefix="/operations")
