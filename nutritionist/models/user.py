from pydantic import BaseModel

class User(BaseModel):
    telegram_id: int
    name: str
    sex: str
    age: int
    height_cm: int
    weight_kg: int
    has_diabetes: str
    goal: str
    
    
    
    
    