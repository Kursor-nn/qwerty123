from pydantic import BaseModel


class InputTextDto(BaseModel):
    text: str = None

    def __init__(self, text: str, **data):
        super().__init__(**data)
        self.text = text


class FilterResultDto(BaseModel):
    is_toxic: bool = True
    name: str = None
    llm_answer: str = None

    def __init__(self, is_toxic: bool, name: str, **data):
        super().__init__(**data)
        self.is_toxic = is_toxic
        self.name = name


class ValidationResultsDto(BaseModel):
    is_toxic: bool = True
    details: list[FilterResultDto] = list()
    llm_answer: str = None

    def __init__(self, is_toxic: bool, details: list[FilterResultDto], llm_answer: str = "", **data):
        super().__init__(**data)
        self.is_toxic = is_toxic
        self.details = details
        self.llm_answer = llm_answer
