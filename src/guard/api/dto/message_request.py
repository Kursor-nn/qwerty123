from pydantic import BaseModel


class ValidationMessage(BaseModel):
    text: str = None
    user: str = None
    filters: list[str] = list()

    def __init__(self, text: str, user: str, filters: list[str] = [], **data):
        super().__init__(**data)
        self.text = text
        self.user = user
        self.filters = filters


class ValidationResultMessage(BaseModel):
    is_toxic: bool = True
    message: str = None
    details: dict = {}
    filter: str = None

    def __init__(self, is_toxic: bool, message: str = "", details: dict = {}, filter: str = "", **data):
        super().__init__(**data)
        self.is_toxic = is_toxic
        self.message = message
        self.details = details
