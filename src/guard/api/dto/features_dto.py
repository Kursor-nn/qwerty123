from typing import Union

from pydantic import BaseModel


class FeatureToggleDto(BaseModel):
    feature_type_id: str = None
    value: bool = None
    chat_name: str = None

    def __init__(self, feature_type_id: str, value: bool, chat_name: bool, **data):
        super().__init__(**data)
        self.feature_type_id = feature_type_id
        self.value = value
        self.chat_name = chat_name


class FeatureConfigDto(BaseModel):
    chat_name: Union[None, str] = None
    config: str = None

    def __init__(self, chat_name: str = None, config: str = None, **data):
        super().__init__(**data)
        self.chat_name = chat_name
        self.config = config


class OperationStatusResponseDto(BaseModel):
    status: bool = True
    details: str = ""

    def __init__(self, status: bool = True, details: str = "", **data):
        super().__init__(**data)
        self.status = status
        self.details = details
