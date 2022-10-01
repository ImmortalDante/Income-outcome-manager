from pydantic import BaseModel, ValidationError, validator


class UserBase(BaseModel):
	email: str
	username: str

	@validator("email")
	def correct_email(cls, email: str) -> str:
		if "@" not in email.lower():
			raise ValidationError("Incorrect email value")
		return email

	class Config:
		orm_mode = True


class UserCreate(UserBase):
	password: str

	@validator("password")
	def min_length(cls, password: str) -> str:
		if len(password) < 5:
			raise ValidationError("Password should contain at least 5 characters")
		return password


class UserModel(UserBase):
	id: int


class Token(BaseModel):
	access_token: str
	token_type: str = "bearer"
