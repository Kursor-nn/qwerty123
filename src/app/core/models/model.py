from sqlalchemy import Column, String, Integer, Boolean, Text, ForeignKey

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


class UserFeaturesConfig(Base):
    __tablename__ = "user_features"
    id = Column(Integer, primary_key=True, nullable=False)
    enabled = Column(Boolean, nullable=False)
    user_id = Column(Integer, ForeignKey("susers.id"))
    feature_type_id = Column(Integer, ForeignKey("features.id"))

    def __init__(self, user_id, enabled, feature_type_id):
        super().__init__()
        self.user_id = user_id
        self.enabled = enabled
        self.feature_type_id = feature_type_id


class FeaturesConfig(Base):
    __tablename__ = "features"
    id = Column(Integer, primary_key=True, nullable=False)
    enabled = Column(Boolean, nullable=False)
    name = Column(Text, nullable=False)
    type = Column(Text, nullable=False)

    def __init__(self, user_id, enabled, name, type):
        super().__init__()
        self.user_id = user_id
        self.enabled = enabled
        self.name = name
        self.type = type


if __name__ == "__main__":
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
