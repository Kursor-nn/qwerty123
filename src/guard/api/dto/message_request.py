from pydantic import BaseModel


class ValidationMessage(BaseModel):
    text: str = None
    type: str = None
    user: str = None

    def __init__(self, text: str, type: str, user: str, **data):
        super().__init__(**data)
        self.text = text
        self.type = type


class ValidationResultMessage(BaseModel):
    is_toxic: bool = True
    filter: str = None

    def __init__(self, is_toxic: bool, filter: str, **data):
        super().__init__(**data)
        self.is_toxic = is_toxic
        self.filter = filter
