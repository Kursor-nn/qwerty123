from pydantic import BaseModel


class LlmAnswerDto(BaseModel):
    status: str = "success"
    text: str = None

    def __init__(self, text: str, status: str = "success", **data):
        super().__init__(**data)
        self.status = status
        self.text = text


class LlmRequestDto(BaseModel):
    text: str = None
    user: str = None
    filters: list[str] = list()

    def __init__(self, text: str, user: str, filters: list[str] = [], **data):
        super().__init__(**data)
        self.text = text
        self.user = user
        self.filters = filters
