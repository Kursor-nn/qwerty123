from pydantic import BaseModel


class AlertMessage(BaseModel):
    title: str = None
    message: str = None

    def __init__(self, title: str, message: str, **data):
        super().__init__(**data)
        self.title = title
        self.message = message
