from pydantic import BaseModel


class Book(BaseModel):
    id: int  # Adding an ID field
    name: str
    description: str = None
    is_active: bool | None =None