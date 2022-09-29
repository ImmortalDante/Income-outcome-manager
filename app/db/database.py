from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


database_url = "sqlite:///./database.sqlite3"

engine = create_engine(
	database_url,
	connect_args={"check_same_thread": False}
)

Session = sessionmaker(
	engine,
	autocommit=False,
	autoflush=False,
)


def get_session() -> Session:
	session = Session()
	try:
		yield session
	finally:
		session.close()
