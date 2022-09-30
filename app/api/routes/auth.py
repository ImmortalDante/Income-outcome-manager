from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.models.auth import UserCreate, Token


router = APIRouter()


@router.post("/sign-up", response_model=Token)
def sign_up(user_data: UserCreate):
	pass


@router.post("/sign-in", response_model=Token)
def sign_in(form_data: OAuth2PasswordRequestForm = Depends()):
	pass
