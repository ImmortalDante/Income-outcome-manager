from typing import List
from fastapi import APIRouter
from fastapi import Depends

from app.models.operations import OperationModel, OperationCreate
from app.services import operations_services, model_enum


router = APIRouter()


@router.get("", response_model=List[OperationModel])
def get_operation_by_kind(
        kind: model_enum.OperationKind | None = None,
        service: operations_services.OperationsService = Depends()
):
    return service.get_list(kind=kind)


@router.post("", response_model=OperationModel)
def add_operation(
        operation_data: OperationCreate,
        service: operations_services.OperationsService = Depends()
):
    return service.create(operation_data)
