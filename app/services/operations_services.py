from fastapi import Depends
from sqlalchemy import extract
from sqlalchemy.orm import Session

from app.db import database, tables
from .model_enum import OperationKind
from app.models.operations import OperationCreate, OperationUpdate


class OperationsService:
	def __init__(self, session: Session = Depends(database.get_session)):
		self.session = session

	def _get(self, user_id: int, operation_id: int) -> tables.Operation:
		operation = self.session.query(tables.Operation).filter_by(id=operation_id, user_id=user_id).first()
		return operation

	def get_list(
			self,
			user_id: int,
			kind: OperationKind | None = None,
			month: int | None = None,
	) -> list[tables.Operation]:
		query = self.session.query(tables.Operation)
		if kind and not month:
			query = query.filter_by(kind=kind)
		elif kind and month:
			query = query.filter(
				tables.Operation.user_id == user_id,
				tables.Operation.kind == kind,
				extract("month", tables.Operation.date) == month
			)
		elif month and not kind:
			query = query.filter(
				tables.Operation.user_id == user_id,
				extract("month", tables.Operation.date) == month
			)
		operations = query.all()
		return operations

	def get_month_statistic(self, user_id: int, month: int):
		operations = self.get_list(user_id=user_id, month=month)
		income = [operation.amount for operation in operations if operation.kind == "income"]
		outcome = [operation.amount for operation in operations if operation.kind == "outcome"]
		result = sum(income) - sum(outcome)
		return result

	def get_operation(self, user_id: int, operation_id: int) -> tables.Operation:
		return self._get(user_id, operation_id)

	def create_many(self, user_id: int, operations_data: list[OperationCreate]) -> list[tables.Operation]:
		operations = [tables.Operation(**operation_data.dict(), user_id=user_id) for operation_data in operations_data]
		self.session.add_all(operations)
		self.session.commit()
		return operations

	def create(self, user_id: int, operation_data: OperationCreate) -> tables.Operation:
		operation = tables.Operation(**operation_data.dict(), user_id=user_id)
		self.session.add(operation)
		self.session.commit()
		return operation

	def update(self, user_id: int, operation_id: int, operation_data: OperationUpdate) -> tables.Operation:
		operation = self._get(user_id, operation_id)
		for field, value in operation_data:
			setattr(operation, field, value)
		self.session.commit()
		return operation

	def delete(self, user_id: int, operation_id: int):
		operation = self._get(user_id, operation_id)
		self.session.delete(operation)
		self.session.commit()
