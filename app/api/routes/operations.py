from typing import List
from fastapi import APIRouter, Depends, Response, status

from app.models.operations import OperationModel, OperationCreate, OperationUpdate
from app.services import operations_services, model_enum


router = APIRouter()


@router.get("", response_model=List[OperationModel])
def get_operation_by_kind(
        kind: model_enum.OperationKind | None = None,
        service: operations_services.OperationsService = Depends()
):
    return service.get_list(kind=kind)


@router.get("/{operation_id}", response_model=OperationModel)
def get_operation_by_id(operation_id: int, service: operations_services.OperationsService = Depends()):
    return service.get_operation(operation_id=operation_id)


@router.put("/{operation_id}", response_model=OperationModel)
def update_operation(
        operation_id: int,
        operation_data: OperationUpdate,
        service: operations_services.OperationsService = Depends(),
):
    return service.update(operation_id, operation_data)


@router.delete("/{operation_id}")
def delete_operation(operation_id, service: operations_services.OperationsService = Depends()):
    service.delete(operation_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("", response_model=OperationModel)
def add_operation(
        operation_data: OperationCreate,
        service: operations_services.OperationsService = Depends()
):
    return service.create(operation_data)
