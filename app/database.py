from sqlmodel import SQLModel, Session, create_engine
from .config import settings

_engine = None

def get_engine():
    global _engine
    if _engine is None:
        DATABASE_URL = settings.database_url or (
            f"postgresql://"
            f"{settings.database_username}:{settings.database_password}"
            f"@{settings.database_hostname}:{settings.database_port}"
            f"/{settings.database_name}"
        )
        _engine = create_engine(DATABASE_URL)
    return _engine


def create_db_and_tables():
    SQLModel.metadata.create_all(get_engine())


def get_db():
    with Session(get_engine()) as session:
        yield session