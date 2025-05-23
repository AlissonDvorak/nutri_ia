import os
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from dotenv import load_dotenv
from chat.memory import SqliteMemory
from tools.food_analyser_tool import FoodImageAnalyserTool
from tools.user_info_tool import UserInfoTool
from tools.user_registration_tool import UserRegistrationTool
from tools.diet_plan_tool import DietPlanTool
from tools.weight_update_tool import WeightUpdateTool
from tools.meal_entry_tool import MealEntryTool
from tools.report_tool import ReportTool


load_dotenv()



SYSTEM_PROMPT = '''
        Backstory:
        Esse agente é uma referência global no campo da nutrição, apelidado de “Nutri I.A”. 
        Consultado por celebridades, atletas e profissionais de saúde, ele desenvolve planos alimentares personalizados, equilibrando saúde, desempenho e sustentabilidade. 
        Com vasto conhecimento em bioquímica e dietas globais (como a mediterrânea, cetogênica e ayurvédica), é defensor do consumo consciente e da preservação ambiental. 
        Agora, ele expande sua expertise para o mundo digital, oferecendo orientação de alta qualidade pelo Telegram para ajudar pessoas a montarem suas próprias dietas e responder dúvidas sobre alimentação.

        Expected Result:
        O agente deve ter um visual que una sua autoridade com a acessibilidade de um consultor digital. 
        Seu entorno deve mostrar opiniões de nutrição: informações de nutrientes, alimentos de diversas culturas e elementos químicos, criando um ambiente que pareça um “laboratório” virtual de alimentação.
        '''
        
        
class NutritionistAgent:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.llm = ChatOpenAI(
            model_name='gpt-4o-mini',
            temperature=0.1,
            openai_api_key=os.getenv("OPENAI_API_KEY"),
        )
        
        self.memory = SqliteMemory(
            session_id=self.session_id,
        ).history
        
        self.tools = [
            FoodImageAnalyserTool(),
            UserInfoTool(),
            UserRegistrationTool(),
            DietPlanTool(),
            WeightUpdateTool(),
            MealEntryTool(),
            ReportTool()
        ]
        
        self.agent = initialize_agent(
            llm=self.llm,
            tools=self.tools,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            memory=self.memory,
            agent_kwargs={
                "system_message": SYSTEM_PROMPT,
            },
            )
        
    def run(self, input_text: str):
        try:
            response = self.agent.invoke(input_text)
            return response.get("output")
        except Exception as e:
            print(f"An error occurred: {e}")
            return "Desculpe, não consegui processar sua solicitação no momento. Tente novamente mais tarde."
       
