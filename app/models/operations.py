from pydantic import BaseModel
from datetime import date
from decimal import Decimal
from app.services.model_enum import OperationKind


class OperationModel(BaseModel):
	id: int
	date: date
	kind: OperationKind
	amount: Decimal
	description: str | None = None

	class Config:
		orm_mode = True
