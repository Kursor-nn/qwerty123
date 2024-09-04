from pydantic import BaseModel


class FeatureToggleDto(BaseModel):
    feature_type_id: str = None
    value: bool = None

    def __init__(self, feature_type_id: str, value: bool, **data):
        super().__init__(**data)
        self.feature_type_id = feature_type_id
        self.value = value
