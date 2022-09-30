import datetime
from fastapi import HTTPException, status, Depends
from jose import jwt, JWTError
from passlib.hash import bcrypt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.db.database import get_session
from app.models.auth import UserModel, Token, UserCreate
import config
from app.db import tables


class AuthService:
	@classmethod
	def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
		return bcrypt.verify(plain_password, hashed_password)

	@classmethod
	def hash_password(cls, password: str) -> str:
		return bcrypt.hash(password)

	@classmethod
	def validate_token(cls, token: str) -> UserModel:
		exception = HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Could not validate credentials",
			headers={
				"WWW-Authenticate": "Bearer"
			},
		)

		try:
			payload = jwt.decode(token, config.JWT_SECRET, algorithms=["HS256"])
		except JWTError:
			raise exception

		user_data = payload.get("user")

		try:
			user = UserModel.parse_obj(user_data)
		except ValidationError:
			raise exception

		return user

	@classmethod
	def create_token(cls, user: tables.User) -> Token:
		user_data = UserModel.from_orm(user)
		now = datetime.date.today()
		payload = {
			"iat": now,
			"nbf": now,
			'exp': now + datetime.timedelta(seconds=3600),
			"sub": str(user_data.id),
			"user": user_data.dict(),
		}
		token = jwt.encode(payload, config.JWT_SECRET, algorithm="HS256")

		return Token(access_token=token)

	def __init__(self, session: Session = Depends(get_session)):
		self.session = session

	def register(self, user_data: UserCreate) -> Token:
		user = tables.User(
			email=user_data.email,
			username=user_data.username,
			password=self.hash_password(user_data.password)
		)
		self.session.add(user)
		self.session.commit()

		return self.create_token(user)

	def authenticate(self, username: str, password: str) -> Token:
		user = self.session.query(tables.User).filter_by(username=username).first()
		exception = HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Could not validate credentials",
			headers={
				"WWW-Authenticate": "Bearer"
			},
		)
		if not user:
			raise exception
		if not self.verify_password(password, user.password):
			raise exception
		return self.create_token(user)
