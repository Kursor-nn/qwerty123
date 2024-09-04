from typing import Union

from pydantic import BaseModel


class UserFeatureData(BaseModel):
    feature_type_id: Union[str, None] = None
    name: Union[str, None] = None
    type: Union[str, None] = None
    enabled: bool = True

    def __init__(self, feature_type_id, name, type, enabled):
        super().__init__()
        self.feature_type_id = feature_type_id
        self.name = name
        self.type = type
        self.enabled = enabled
