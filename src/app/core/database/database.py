from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

database_connection_string = config("CONNECTION_URI")
engine = create_engine(database_connection_string)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


async def init_db():
    Base.metadata.create_all(bind=engine)


def conn():
    SQLModel.metadata.create_all(engine)


def get_session():
    return SessionLocal()
