from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db import database, tables
from .model_enum import OperationKind
from app.models.operations import OperationCreate


class OperationsService:
	def __init__(self, session: Session = Depends(database.get_session)):
		self.session = session

	def get_list(self, kind: OperationKind | None = None) -> List[tables.Operation]:
		query = self.session.query(tables.Operation)
		if kind:
			query = query.filter_by(kind=kind)
		operations = query.all()
		return operations

	def create(self, operation_data: OperationCreate) -> tables.Operation:
		operation = tables.Operation(**operation_data.dict())
		self.session.add(operation)
		self.session.commit()
		return operation
