from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.models.auth import UserCreate, Token, UserModel
from app.services.auth_service import AuthService, get_current_user

router = APIRouter()


@router.post("/sign-up", response_model=Token)
def sign_up(user_data: UserCreate, service: AuthService = Depends()):
	return service.register(user_data)


@router.post("/sign-in", response_model=Token)
def sign_in(
		form_data: OAuth2PasswordRequestForm = Depends(),
		service: AuthService = Depends(),
):
	return service.authenticate(form_data.username, form_data.password,)


@router.get("/user", response_model=UserModel)
def get_user(user: UserModel = Depends(get_current_user)):
	"""Получение текущего пользователя"""
	return user
