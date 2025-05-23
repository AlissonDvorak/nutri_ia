from typing import Optional, List
from tinydb import Query
from models import MealEntry
from repositories.base_repository import BaseRepository
from datetime import datetime
import json


class MealEntryRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.meal_entry_table = self.get_table('meal_entries')
        
    def create_meal_entry(
        self,
        user_id: int,
        meal_description: str,
        image_path: Optional[str] = None,
        calories: Optional[str] = None,
        carbs: Optional[str] = None,
        protein: Optional[str] = None,
        fat: Optional[str] = None
    ) -> MealEntry:
        meal_entry = MealEntry(
            user_id=user_id,
            meal_description=meal_description,
            image_path=image_path,
            calories=calories,
            carbs=carbs,
            protein=protein,
            fat=fat,
        )
        self.meal_entry_table.insert(json.loads(meal_entry.model_dump_json()))
        return meal_entry
    
    def get_meal_entries_by_user_and_date(
        self,
        user_id: int,
        date: datetime
    ) -> List[MealEntry]:
        start_date = datetime.combine(date.date(), datetime.min.time())
        end_date = datetime.combine(date.date(), datetime.max.time())
        
        MealEntryQuery = Query()
        results = self.meal_entry_table.search(
            (MealEntryQuery.user_id == user_id) &
            (MealEntryQuery.created_at >= start_date) &
            (MealEntryQuery.created_at <= end_date)
        )
        return [MealEntry(**result) for result in results]
    
    def update_meal_entry(
        self,
        meal_entry_id: int,
        **kwargs
    ) -> None:
        MealEntryQuery = Query()
        self.meal_entry_table.update(kwargs, MealEntryQuery.id == meal_entry_id)
        
    def delete_meal_entry(self, meal_entry_id: int) -> None:
        MealEntryQuery = Query()
        self.meal_entry_table.remove(MealEntryQuery.id == meal_entry_id)
        
        
    def get_meal_entry_by_id(self, meal_entry_id: int) -> Optional[MealEntry]:
        MealEntryQuery = Query()
        result = self.meal_entry_table.search(MealEntryQuery.user_id == meal_entry_id)
        return result
        
    def get_all_meal_entries(self) -> List[MealEntry]:
        return [MealEntry(**entry) for entry in self.meal_entry_table.all()]