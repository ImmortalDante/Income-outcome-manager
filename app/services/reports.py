import csv
from io import StringIO

from fastapi import Depends
from typing import Any

from .operations_services import OperationsService
from app.models.operations import OperationCreate
from app.models.operations import OperationModel


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
		next(reader)  # пропускаем заголовок
		for row in reader:
			operation_data = OperationCreate.parse_obj(row)
			if operation_data.description == "":
				operation_data.description = None
			operations.append(operation_data)

		self.operation_service.create_many(user_id=user_id, operations_data=operations)

	def export_csv(self, user_id: int) -> Any:
		output = StringIO()
		writer = csv.DictWriter(output, fieldnames=["date", "kind", "amount", "description"], extrasaction="ignore")
		operations = self.operation_service.get_list(user_id)
		writer.writeheader()
		for operation in operations:
			operation_data = OperationModel.from_orm(operation)
			writer.writerow(operation_data.dict())

		output.seek(0)
		return output
