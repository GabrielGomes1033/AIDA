from datetime import datetime
from core.utils import load_json, save_json


MEMORY_FILE = "data/memory.json"
CONVERSATION_FILE = "data/conversations.json"


class MemoryManager:
    def __init__(self):
        # Carrega os arquivos JSON uma vez quando a AIDA inicia.
        # Se os arquivos não existirem, load_json cria estruturas vazias.
        self.memory = load_json(MEMORY_FILE)
        self.conversations = load_json(CONVERSATION_FILE)

    def get_user_memory(self, user_id: str) -> dict:
        # Retorna a memória permanente de um usuário.
        # Quando é um usuário novo, entrega um formato padrão completo.
        return self.memory.get(user_id, {
            "profile": {},
            "preferences": {},
            "important_facts": [],
            "emotional_context": [],
            "projects": [],
            "last_topic": None
        })

    def save_user_memory(self, user_id: str, memory_data: dict):
        # Atualiza a memória em RAM e grava no arquivo JSON.
        self.memory[user_id] = memory_data
        save_json(MEMORY_FILE, self.memory)

    def get_history(self, user_id: str) -> list:
        # Histórico é a conversa recente, diferente da memória permanente.
        return self.conversations.get(user_id, [])

    def add_message(self, user_id: str, role: str, message: str):
        # Adiciona uma fala no histórico com papel, texto e horário.
        # role pode ser "user" ou "aida".
        history = self.get_history(user_id)

        history.append({
            "role": role,
            "message": message,
            "time": datetime.now().isoformat()
        })

        # mantém só as últimas 40 mensagens para não ficar pesado
        self.conversations[user_id] = history[-40:]
        save_json(CONVERSATION_FILE, self.conversations)

    def selective_memory_check(self, user_message: str) -> bool:
        """
        Decide se vale guardar algo na memória.
        AIDA não salva tudo. Só coisas úteis.
        """

        triggers = [
            "meu nome é",
            "eu gosto de",
            "eu não gosto de",
            "lembre que",
            "guarde isso",
            "meu projeto",
            "estou criando",
            "minha ideia",
            "meu objetivo",
            "quero ser",
            "trabalho com",
            "estudo",
            "prefiro",
            "não quero",
            "da próxima vez"
        ]

        text = user_message.lower()

        return any(trigger in text for trigger in triggers)

    def extract_memory(self, user_message: str) -> str:
        """
        Versão simples: salva a frase importante inteira.
        Depois você pode trocar isso por IA/LLM para extrair melhor.
        """
        return user_message.strip()

    def remember_if_relevant(self, user_id: str, user_message: str):
        # Só tenta salvar quando a mensagem bate com os gatilhos úteis.
        if not self.selective_memory_check(user_message):
            return

        user_memory = self.get_user_memory(user_id)
        fact = self.extract_memory(user_message)

        # Evita repetir a mesma memória várias vezes.
        if fact not in user_memory["important_facts"]:
            user_memory["important_facts"].append(fact)

        # last_topic ajuda a AIDA retomar o assunto depois.
        user_memory["last_topic"] = fact

        self.save_user_memory(user_id, user_memory)
