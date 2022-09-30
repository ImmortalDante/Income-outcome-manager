from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db import database, tables
from .model_enum import OperationKind
from app.models.operations import OperationCreate, OperationUpdate


class OperationsService:
	def __init__(self, session: Session = Depends(database.get_session)):
		self.session = session

	def _get(self, operation_id: int) -> tables.Operation:
		operation = self.session.query(tables.Operation).get(operation_id)
		return operation

	def get_list(self, kind: OperationKind | None = None) -> List[tables.Operation]:
		query = self.session.query(tables.Operation)
		if kind:
			query = query.filter_by(kind=kind)
		operations = query.all()
		return operations

	def get_operation(self, operation_id: int) -> tables.Operation:
		return self._get(operation_id)

	def create(self, operation_data: OperationCreate) -> tables.Operation:
		operation = tables.Operation(**operation_data.dict())
		self.session.add(operation)
		self.session.commit()
		return operation

	def update(self, operation_id: int, operation_data: OperationUpdate) -> tables.Operation:
		operation = self._get(operation_id)
		for field, value in operation_data:
			setattr(operation, field, value)
		self.session.commit()
		return operation

	def delete(self, operation_id: int):
		operation = self._get(operation_id)
		self.session.delete(operation)
		self.session.commit()
