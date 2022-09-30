import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
	__tablename__ = "users"

	id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
	username = sqlalchemy.Column(sqlalchemy.Text, unique=True)
	email = sqlalchemy.Column(sqlalchemy.Text, unique=True)
	password = sqlalchemy.Column(sqlalchemy.Text)


class Operation(Base):
	__tablename__ = "operations"

	id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
	user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
	date = sqlalchemy.Column(sqlalchemy.Date)
	kind = sqlalchemy.Column(sqlalchemy.String)
	amount = sqlalchemy.Column(sqlalchemy.NUMERIC(10, 2))
	description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
