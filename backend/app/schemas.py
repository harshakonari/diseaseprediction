from pydantic import BaseModel

class UserInput(BaseModel):
    age: int
    height: float
    weight: float
    fever: str
    chest_pain: str
    sugar: str
    bp: str