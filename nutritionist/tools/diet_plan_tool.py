from langchain.tools import BaseTool
from typing import Optional
from repositories.user import UserRepository
from repositories.diet_plan import DietPlanRepository


class DietPlanTool(BaseTool):
    name: str = "diet_plan"
    description: str = (
        "Use esta ferramenta para criar um plano de dieta de um usuário. "
        "Entrada: telegram_id do usuário e, e plan_details para criar um novo plano ou buscar um plano já existente."
        "A regra para essa Tool é quando o usuario gostar do plano montado por você ai você está autorizado a usar essa tool para salvar o plano"
    )
    
    def __init__(self):
        super().__init__()
        self.user_repo = UserRepository()
        self.diet_plan_repo = DietPlanRepository()
        
        
    def _run(self, telegram_id: int, plan_details: Optional[str] = None) -> str:
        try:
            user = self.user_repo.get_user_by_telegram_id(telegram_id)
            if not user:
                return "Usuário não encontrado. Por favor, registre-se primeiro."
            
            if plan_details:
                self.diet_plan_repo.create_diet_plan(user.telegram_id, plan_details)
                return f"Novo plano de dieta criado para o usuário {user.name}"

            latest_plan = self.diet_plan_repo.get_latest_diet_plan_for_user(user.telegram_id)
            if latest_plan:
                return f"Último plano de dieta para o usuário {user.name}: {latest_plan.details}"
            else:
                return "Nenhum plano de dieta encontrado para este usuário."
        except Exception as e:
            return f"Erro ao processar a solicitação do plano de dieta: {str(e)}"
        
             
    async def _arun(self, telegram_id: int, plan_details: Optional[str] = None) -> str:
        raise NotImplementedError("Execucao assíncrona não suportada.")