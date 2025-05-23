from typing import Optional, List
from tinydb import Query
from models import DietPlan
from repositories.base_repository import BaseRepository
import json

class DietPlanRepository(BaseRepository):
    
    def __init__(self):
        super().__init__()
        self.diet_plan_table = self.get_table('diet_plans')  
    
    
    def create_diet_plan(self, telegram_id: int, plan_details: str) -> DietPlan:
        new_diet_plan = DietPlan(user_id=telegram_id, details=plan_details)
        self.diet_plan_table.insert(json.loads(new_diet_plan.model_dump_json()))
        return new_diet_plan
        
        
    def get_diet_plan_by_id(self, diet_plan_id: int) -> Optional[DietPlan]:
        DietPlanQuery = Query()
        result = self.diet_plan_table.get(DietPlanQuery.id == diet_plan_id)
        return DietPlan(**result) if result else None
    
    def get_latest_diet_plan_for_user(self, telegram_id: int) -> Optional[DietPlan]:
        DietPlanQuery = Query()
        plans = self.diet_plan_table.search(DietPlanQuery.user_id == telegram_id)
        if not plans:
            return None
        latest_plan = sorted(plans, key=lambda plan: plan['created_at'], reverse=True)[0]
        return DietPlan(**latest_plan)
    
    def update_diet_plan (
        self,
        diet_id: int,
        plan_details: str,
    ) -> Optional[DietPlan]:
       DietPlanQuery = Query()
       self.diet_plan_table.update({"plan_details": plan_details}, DietPlanQuery.id == diet_id)
       updated_plan = self.get_diet_plan_by_id(diet_id)
       return DietPlan(**updated_plan)
   
    def delete_diet_plan(self, diet_plan_id: int) -> None:
        DietPlanQuery = Query()
        self.diet_plan_table.remove(DietPlanQuery.id == diet_plan_id)
       
    def get_all_diet_plans(self) -> List[DietPlan]:
        all_plans = self.diet_plan_table.all()
        return [DietPlan(**plan) for plan in all_plans]