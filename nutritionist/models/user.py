from pydantic import BaseModel, Field

class User(BaseModel):
    telegram_id: int
    name: str 
    sex: str 
    age: str 
    height_cm: str 
    weight_kg: str 
    has_diabetes: str 
    goal: str 
