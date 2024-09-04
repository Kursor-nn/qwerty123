from sqlmodel import Session

from core.database.database import get_session
from core.models.model import User


def get_user_by_login(login: str, session: Session = get_session()) -> User:
    return session.query(User).where(User.login == login).one_or_none()


def get_user_email(email: str, session: Session) -> User:
    return session.query(User).where(User.email == email).one_or_none()


def __add_user(login: str, email: str, user_type: str, password: str, session: Session):
    user = User(login=login, email=email, role=user_type, password=password)
    session.add(user)
    session.commit()


def add_admin(login: str, email: str, password: str, session: Session):
    __add_user(login=login, email=email, user_type="admin", password=password, session=session)


def add_client(login: str, email: str, password: str, session: Session):
    __add_user(login=login, email=email, user_type="client", password=password, session=session)
