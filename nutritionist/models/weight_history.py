from pydantic import BaseModel
from datetime import datetime, timezone
from typing import Optional

class WeightHistory(BaseModel):
    user_id: int
    date: datetime = datetime.now(timezone.utc)
    weight_kg: Optional[str]