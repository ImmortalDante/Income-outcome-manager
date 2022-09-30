from pydantic import BaseModel
from datetime import date
from decimal import Decimal
from app.services.model_enum import OperationKind


class OperationBase(BaseModel):
	date: date
	kind: OperationKind
	amount: Decimal
	description: str | None = None

	class Config:
		orm_mode = True


class OperationModel(OperationBase):
	id: int


class OperationCreate(OperationBase):
	...
