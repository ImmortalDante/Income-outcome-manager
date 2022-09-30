from fastapi import APIRouter
from app.api.routes import operations, auth

router = APIRouter()

router.include_router(operations.router, prefix="/operations")
router.include_router(auth.router, prefix="/auth")
