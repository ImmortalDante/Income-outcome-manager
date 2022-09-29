from typing import List
from fastapi import APIRouter
from app.models.operations import OperationModel
from fastapi import Depends
from app.db.database import get_session
from app.db.tables import Operation
from sqlalchemy.orm import Session


router = APIRouter()


@router.get("/", response_model=List[OperationModel])
def get_operations(session: Session = Depends(get_session)):
    operations = (session.query(Operation).all())
    return operations
