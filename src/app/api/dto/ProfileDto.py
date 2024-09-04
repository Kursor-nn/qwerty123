from typing import Any, Union

from pydantic import BaseModel
from typing_extensions import List


class FilterDto(BaseModel):
    id: str
    name: str
    enabled: str

    def __init__(self, id, name, enabled, **data: Any):
        super().__init__(**data)
        self.id = id
        self.name = name
        self.enabled = enabled


class NotificationDto(BaseModel):
    id: str
    name: str
    enabled: str
    receiver: str

    def __init__(self, id, name, enabled, receiver, **data: Any):
        super().__init__(**data)
        self.id = id
        self.name = name
        self.enabled = enabled
        self.receiver = receiver


class StatisticsConfDto(BaseModel):
    id: Union[str, None] = None
    name: Union[str, None] = None
    enabled: Union[str, None] = None

    def __init__(self, id, name, enabled, **data: Any):
        super().__init__(**data)
        self.id = id
        self.name = name
        self.enabled = enabled


class UserFeatureDto(BaseModel):
    feature_type_id: Union[str, None] = None
    name: Union[str, None] = None
    type: Union[str, None] = None
    enabled: bool = True

    def __init__(self, feature_type_id, name, type, enabled, **data: Any):
        super().__init__(**data)
        self.name = name
        self.feature_type_id = feature_type_id
        self.enabled = enabled
        self.type = type


class ProfileInfo(BaseModel):
    username: str = None
    features: List[UserFeatureDto] = list()

    def __init__(self, username: str, features: list = list(), **data):
        super().__init__(**data)
        self.username = username
        self.features = [UserFeatureDto(**a) for a in features]
