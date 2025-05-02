from typing import Any, Dict, Type
from pydantic import BaseModel
from langchain.tools import BaseTool
from repositories.user import UserRepository
from models import User


class UserRegistrationTool(BaseModel):
    name: str = "user_registration"
    description: str = (
    "Use esta ferramenta para registrar um novo usuário ou atualizar as informações de um usuário existente. "
    "Esta ferramenta requer os seguintes dados do usuário: "
    "name (nome), sex (sexo), age (idade como uma string), height_cm (altura em centímetros como uma string), weight_kg (peso em quilogramas como uma string), "
    "has_diabetes (se tem diabetes: sim/não) e goal (objetivo: perder peso, ganhar peso, ganhar massa muscular). "
    "Se algum dado estiver faltando, você deve primeiro coletar essas informações do usuário antes de usar esta ferramenta."
    )
    args_schema: Type[BaseModel] = User
    
    def __init__(self):
        super().__init__()
        self.user_repo = UserRepository()
        
    def _run(self,
        telegram_id: int,
        name: str,
        sex: str,
        age: int,
        height_cm: int,
        weight_kg: int,
        has_diabetes: bool,
        goal: str
    ) -> str:
        if not name:
            raise AttributeError("Os atributos inseridos na Tool UserRegistrationTool não podem ser vazios.")
        
        try:
            user_data = {
                "telegram_id": telegram_id,
                "name": name,
                "sex": sex,
                "age": age,
                "height_cm": height_cm,
                "weight_kg": weight_kg,
                "has_diabetes": has_diabetes,
                "goal": goal,
            }
            user = self.user_repo.get_user_by_telegram_id(telegram_id)
            if user:
                updated_user = self.user_repo.update_user(**user_data)
                return f"Usuário atualizado com sucesso para o usuário: {updated_user.name}"
            
            new_user = self.user_repo.create_user(**user_data)
            return f"Usuário registrado com sucesso: {new_user.name}"
        except Exception as e:
            return f"Erro ao registrar o usuário: {str(e)}"
        
            
    async def _arun(self, **kwargs: Any) -> str:
        raise NotImplementedError("Execucao assíncrona não suportada.")