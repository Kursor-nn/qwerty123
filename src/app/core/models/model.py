from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Text

from core.database.database import Base, engine


class User(Base):
    __tablename__ = "susers"
    id = Column(Integer, primary_key=True, nullable=False)
    login = Column(String, unique=True, nullable=False)
    email = Column(String)
    role = Column(String, nullable=False)
    password = Column(String, nullable=False)

    def __init__(self, login, email, role, password: str):
        super().__init__()
        self.login = login
        self.email = email
        self.role = role
        self.password = password


class NotificationConfig(Base):
    __tablename__ = "notification_config"
    id = Column(Integer, primary_key=True, nullable=False)
    userId = Column(Integer, ForeignKey("susers.id"))
    enabled = Column(Boolean, nullable=False)
    configuration = Column(Text, nullable=False)

    def __init__(self, user_id, configuration):
        super().__init__()
        self.user_id = user_id
        self.configuration = configuration


if __name__ == "__main__":
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
