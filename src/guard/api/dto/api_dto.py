from pydantic import BaseModel


class InputTextDto(BaseModel):
    text: str = None
    filter_type: str = None
    request_filters: list[str] = list()
    answer_filters: list[str] = list()

    def __init__(self, text: str, request_filters: list[str] = list, answer_filters: list[str] = list, **data):
        super().__init__(**data)
        self.text = text
        self.request_filters = request_filters
        self.answer_filters = answer_filters


class FilterResultDto(BaseModel):
    is_toxic: bool = True
    details: dict = None

    def __init__(self, is_toxic: bool, details: dict = {}, **data):
        super().__init__(**data)
        self.is_toxic = is_toxic
        self.details = details


class ValidationResultsDto(BaseModel):
    is_toxic: bool = True
    llm_answer: str = None
    question: str = None
    input_validation: list[FilterResultDto] = list()
    answer_validation: list[FilterResultDto] = list()

    def __init__(self, is_toxic: bool, question: str="", llm_answer: str = "", input_validation: list[FilterResultDto] = list(), answer_validation: list[FilterResultDto] = list(), **data):
        super().__init__(**data)
        self.is_toxic = is_toxic
        self.question = question
        self.llm_answer = llm_answer
        self.answer_validation = answer_validation
        self.input_validation = input_validation

