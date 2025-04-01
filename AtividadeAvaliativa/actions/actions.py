from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import logging

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ActionFornecerSuporte(Action):

    def name(self) -> str:
        return "action_fornecer_suporte"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:

        problema = tracker.get_slot('problema')

        if problema is None:
            return self.handle_unrecognized_problem(dispatcher)

        try:
            response = self.get_support_response(problema)
            dispatcher.utter_message(text=response)
        except Exception as e:
            logger.error(f"Erro ao processar a ação 'action_fornecer_suporte': {e}")
            dispatcher.utter_message(text="Ocorreu um erro ao tentar processar sua solicitação. Por favor, tente novamente mais tarde.")

        return []

    def get_support_response(self, problema: str) -> str:
        """Retorna a resposta apropriada com base no problema relatado."""
        responses = {
            "não consigo acessar minha conta": "Aqui estão algumas soluções para o seu problema: [link para a solução].",
            "o aplicativo não funciona": "Tente reiniciar o aplicativo ou verificar sua conexão com a internet.",
            "quero mudar meu plano": "Você pode mudar seu plano através do aplicativo ou site. Aqui está o link: [link para mudar plano].",
            "estou tendo problemas com o pagamento": "Verifique se os dados do seu cartão estão corretos e se há saldo disponível.",
            "não consigo ouvir música": "Verifique se o volume do seu dispositivo está ativado e se você está conectado à internet.",
            "o aplicativo não carrega": "Tente limpar o cache do aplicativo ou reinstalá-lo.",
            "minha conta foi bloqueada": "Para desbloquear sua conta, siga este link: [link para desbloquear].",
            "não consigo redefinir minha senha": "Você pode redefinir sua senha através deste link: [link para redefinir senha].",
            "quero cancelar minha assinatura": "Você pode cancelar sua assinatura diretamente no aplicativo ou através do nosso site. Aqui está o link: [link para cancelar assinatura].",
            "não recebo notificações": "Verifique se as notificações estão ativadas nas configurações do seu dispositivo.",
            "quero feedback sobre minha música": "Adoramos receber feedback! Você pode enviar suas sugestões através deste link: [link para feedback].",
        }

        return responses.get(problema, self.handle_unrecognized_problem(dispatcher))

    def handle_unrecognized_problem(self, dispatcher: CollectingDispatcher) -> str:
        """Lida com problemas não reconhecidos."""
        dispatcher.utter_message(text="Desculpe, não consegui entender seu problema. Poderia me dar mais detalhes ou reformular sua pergunta?")
        return []
