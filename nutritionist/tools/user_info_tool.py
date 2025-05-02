from langchain.tools import BaseTool
from repositories.user import UserRepository


class UserInfoTool(BaseTool):
    name: str = "user_info"
    description: str = (
        "Use esta ferramenta para buscar informações de um usuário existente. "
        "Ela requer o telegram_id do usuário como entrada para recuperar os dados."
    )
    
    def __init__(self):
        super().__init__()
        self.user_repo = UserRepository()
        
    
    def _run(self, telegram_id: int) -> str:
        try:
            user = self.user_repo.get_user_by_telegram_id(telegram_id)
            if not user:
                return "Usuário nao encontrado."
            else:
                user_info = (
                    f"Nome: {user.name},\n"
                    f"Sexo: {user.sex},\n"
                    f"Idade: {user.age},\n"
                    f"Altura: {user.height_cm} cm,\n"
                    f"Peso: {user.weight_kg} kg,\n"
                    f"Diabetes: {'Sim' if user.has_diabetes else 'Não'},\n"
                    f"Objetivo: {user.goal},\n"
                    )
                return user_info    
        except Exception as e:
            return f"Ocorreu um erro ao buscar o usuário: {e}"
        
       
    async def _arun(self, telegram_id: int) -> str:
        raise NotImplementedError("Execucao assíncrona não suportada.")