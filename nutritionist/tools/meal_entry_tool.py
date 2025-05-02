from langchain.tools import BaseTool
from typing import Any, Dict, Optional
from repositories.user import  UserRepository
from repositories.meal_entry import MealEntryRepository


class MealEntryTool(BaseTool):
    name: str = "meal_entry_tool"
    description: str = (
            "Ferramenta para toda vez que o usuario quiser que você registre uma refeição que ele fez no dia"
            "se você nao tiver todos os dados para registrar uma refeição, pergunte a ao usuario até que tenha todas as informações necessarias"
            "Use esta ferramenta para registrar uma refeição de um usuário. "
            "Entrada: como meal_description, calories, carbs, proteins, fats."
            "Você deve se basear nas informações que o usuario passou para gerar as informações de calories, carbs, proteins, fats"
        )

    
    def __init__(self):
        super().__init__()
        self.user_repository = UserRepository()
        self.meal_entry_repository = MealEntryRepository()
        
        
    def _run(
        self, 
        telegram_id: int,
        meal_description: str,
        image_path: Optional[str] = None,
        calories: Optional[str] = None,
        carbs: Optional[str] = None,
        proteins: Optional[str] = None,
        fats: Optional[str] = None,
        ) -> str:
        try: 
            user = self.user_repository.get_user_by_telegram_id(telegram_id)
            if not user:
                return "Usuário não encontrado. Por favor, registre-se primeiro."
            
            self.meal_entry_repository.create_meal_entry(
                telegram_id=telegram_id,
                meal_description=meal_description,
                image_path=image_path,
                calories=calories,
                carbs=carbs,
                proteins=proteins,
                fats=fats
            ) 
            return f"Refeição registrada com sucesso para o usuário {user.name}."
        except Exception as e:
            return f"Erro ao registrar a refeição: {str(e)}"
        
        
    async def _arun(self, telegram_id: str, meal_data: Dict[str, Any]) -> str:
        raise NotImplementedError("Execução assíncrona não suportada.")
        