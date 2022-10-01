from pydantic import BaseModel, validator, ValidationError
from datetime import date
from decimal import Decimal
from app.services.model_enum import OperationKind


class OperationBase(BaseModel):
	date: date
	kind: OperationKind
	amount: Decimal
	description: str | None = None

	@validator("amount")
	def validate_amount(cls, amount: Decimal) -> Decimal:
		if amount <= 0:
			raise ValidationError("Amount value can not be less or equal 0")
		return amount

	class Config:
		orm_mode = True


class OperationModel(OperationBase):
	id: int


class OperationUpdate(OperationBase):
	pass


class OperationCreate(OperationBase):
	pass
