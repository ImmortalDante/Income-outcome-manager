from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import StreamingResponse

from app.models.auth import UserModel
from app.services.auth_service import get_current_user
from app.services.reports import ReportService

router = APIRouter()


@router.post("/import")
def import_csv(
		file: UploadFile = File(...),
		user: UserModel = Depends(get_current_user),
		reports_service: ReportService = Depends()
):
	"""Загрузка в базу данных значений из csv файла"""
	reports_service.import_csv(user_id=user.id, file=file.file)


@router.get("/export")
def export_csv(
		user: UserModel = Depends(get_current_user),
		reports_service: ReportService = Depends()
):
	report = reports_service.export_csv(user_id=user.id)
	return StreamingResponse(report, media_type="text/csv", headers={
		"Content-Disposition": "attachment; filename=report.csv"
	})
