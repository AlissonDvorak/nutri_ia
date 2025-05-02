from langchain.tools import BaseTool
from typing import Any, Dict, Optional
from repositories.user import UserRepository
from repositories.meal_entry import MealEntryRepository
from pydantic import PrivateAttr


class MealEntryTool(BaseTool):
    name: str = "meal_entry_tool"
    description: str = (
        "Ferramenta para toda vez que o usuário quiser que você registre uma refeição que ele fez no dia. "
        "Se você não tiver todos os dados para registrar uma refeição, pergunte ao usuário até que tenha todas as informações necessárias. "
        "Use esta ferramenta para registrar uma refeição de um usuário. "
        "Entrada: meal_description, calories, carbs, proteins, fats. "
        "Você deve se basear nas informações que o usuário passou para gerar as informações de calories, carbs, proteins, fats."
    )

    _user_repository: UserRepository = PrivateAttr()
    _meal_entry_repository: MealEntryRepository = PrivateAttr()

    def __init__(self):
        super().__init__()
        self._user_repository = UserRepository()
        self._meal_entry_repository = MealEntryRepository()

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
            user = self._user_repository.get_user_by_telegram_id(telegram_id)
            if not user:
                return "Usuário não encontrado. Por favor, registre-se primeiro."

            self._meal_entry_repository.create_meal_entry(
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
