from langchain.tools import BaseTool
from repositories.user import UserRepository
from repositories.weight_history import WeightHistoryRepository
from pydantic import PrivateAttr


class WeightUpdateTool(BaseTool):
    name: str = "weight_update"
    description: str = (
        "Use esta ferramenta para registrar o peso de um usuário. "
        "Entrada: telegram_id do usuário e weight_kg."
    )

    _user_repo: UserRepository = PrivateAttr()
    _weight_history_repo: WeightHistoryRepository = PrivateAttr()

    def __init__(self):
        super().__init__()
        self._user_repo = UserRepository()
        self._weight_history_repo = WeightHistoryRepository()

    def _run(self, telegram_id: str, weight_kg: str) -> str:
        try:
            user = self._user_repo.get_user_by_telegram_id(telegram_id)
            if not user:
                return f"Usuário com telegram_id {telegram_id} não encontrado. Por favor, registre-se primeiro."
            
            self._weight_history_repo.add_weight_history(telegram_id, weight_kg)
            return f"Peso de {weight_kg} kg registrado com sucesso para o usuário {user.name}."
        except Exception as e:
            return f"Erro ao registrar o peso: {str(e)}"

    async def _arun(self, telegram_id: str, weight_kg: float) -> str:
        raise NotImplementedError("Execução assíncrona não suportada para atualizar o peso.")
