from typing import Optional, List
from tinydb import Query
from models import WeightHistory
from repositories.base_repository import BaseRepository


class WeightHistoryRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.weight_history_table = self.get_table('weight_history')
        
    def add_weight_entry(self, user_id: int, weight_kg: str) -> WeightHistory:
        weight_entry = WeightHistory(user_id=user_id, weight_kg=weight_kg)
        self.weight_history_table.insert(weight_entry.model_dump())
        return weight_entry
    
    def get_weight_history(self, user_id: int) -> List[WeightHistory]:
        WeightHistoryQuery = Query()
        results = self.weight_history_table.search(WeightHistoryQuery.user_id == user_id)
        sorted_results = sorted(results, key=lambda result: result['date'])
        return sorted_results
    
    def get_weight_entry_by_id(self, weight_entry_id: int) -> Optional[WeightHistory]:
        WeightHistoryQuery = Query()
        result = self.weight_history_table.get(WeightHistoryQuery.id == weight_entry_id)
        return WeightHistory(**result) if result else None
    
    def delete_weight_entry(self, weight_entry_id: int) -> None:
        WeightHistoryQuery = Query()
        self.weight_history_table.remove(WeightHistoryQuery.id == weight_entry_id)
        
    def get_all_weight_entries(self) -> List[WeightHistory]:
        all_entries = self.weight_history_table.all()
        return [WeightHistory(**entry) for entry in all_entries]