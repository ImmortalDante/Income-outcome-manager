from typing import List
from fastapi import APIRouter, Depends, Response, status

from app.models.auth import UserModel
from app.models.operations import OperationModel, OperationCreate, OperationUpdate
from app.services import operations_services, model_enum
from app.services.auth_service import get_current_user

router = APIRouter()


@router.get("", response_model=List[OperationModel])
def get_operation_by_kind(
        kind: model_enum.OperationKind | None = None,
        user: UserModel = Depends(get_current_user),
        service: operations_services.OperationsService = Depends()
):
    return service.get_list(user_id=user.id, kind=kind)


@router.get("/{operation_id}", response_model=OperationModel)
def get_operation_by_id(
        operation_id: int,
        user: UserModel = Depends(get_current_user),
        service: operations_services.OperationsService = Depends()
):
    return service.get_operation(user_id=user.id, operation_id=operation_id)


@router.put("/{operation_id}", response_model=OperationModel)
def update_operation(
        operation_id: int,
        operation_data: OperationUpdate,
        user: UserModel = Depends(get_current_user),
        service: operations_services.OperationsService = Depends(),
):
    return service.update(user_id=user.id, operation_id=operation_id, operation_data=operation_data)


@router.delete("/{operation_id}")
def delete_operation(
        operation_id: int,
        user: UserModel = Depends(get_current_user),
        service: operations_services.OperationsService = Depends()):
    service.delete(user_id=user.id, operation_id=operation_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("", response_model=OperationModel)
def add_operation(
        operation_data: OperationCreate,
        user: UserModel = Depends(get_current_user),
        service: operations_services.OperationsService = Depends()
):
    return service.create(user_id=user.id, operation_data=operation_data)
