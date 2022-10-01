import csv
from fastapi import Depends
from typing import Any

from .operations_services import OperationsService
from app.models.operations import OperationCreate


class ReportService:
	def __init__(self, operation_service: OperationsService = Depends()):
		self.operation_service = operation_service

	def import_csv(self, user_id: int, file: Any):
		reader = csv.DictReader(
			(line.decode() for line in file),
			fieldnames=[
				"date", "kind", "amount", "description"
			]
		)
		operations = []
		for row in reader:
			operation_data = OperationCreate.parse_obj(row)
			if operation_data.description == "":
				operation_data.description = None
			operations.append(operation_data)

		self.operation_service.create_many(user_id=user_id, operations_data=operations)

	def export_csv(self, user_id: int) -> Any:
		pass
