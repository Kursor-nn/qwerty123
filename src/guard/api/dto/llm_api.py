from pydantic import BaseModel


class LlmAnswerDto(BaseModel):
    is_toxic: bool = True
    status: str = "success"
    text: str = None

    def __init__(self, is_toxic: bool, text: str, status: str = "success", **data):
        super().__init__(**data)
        self.status = status
        self.is_toxic = is_toxic
        self.text = text


class LlmRequestDto(BaseModel):
    text: str = None

    def __init__(self, text: str, **data):
        super().__init__(**data)
        self.text = text
