from fastapi import APIRouter
from app.api.routes import operations, auth, reports

router = APIRouter()

router.include_router(operations.router, prefix="/operations", tags=["operations"])
router.include_router(auth.router, prefix="/auth", tags=["authentication"])
router.include_router(reports.router, prefix="/reports", tags=["reports"])
