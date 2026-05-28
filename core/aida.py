from random import choice
from unicodedata import category, normalize

from core.memory import MemoryManager
from core.personality import AIDA_PERSONALITY


# Cada chave representa uma intenção detectada na mensagem do usuário.
# AIDA escolhe uma frase aleatória dentro da lista para não responder sempre igual.
RESPONSE_OPTIONS = {
    "greeting": [
        "Oi. Estou aqui. Me conta o que você quer construir, resolver ou pensar agora.",
        "Oi, Gabriel. Cheguei junto. O que a gente vai mexer hoje?",
        "Olá. Pode mandar do seu jeito mesmo; eu acompanho e organizo com você.",
    ],
    "thanks": [
        "De nada. E se quiser, eu já posso transformar isso no próximo passo.",
        "Sempre. Fico aqui pra ir refinando com você, uma peça por vez.",
        "Tamo junto. Quando você trouxer a próxima parte, eu continuo dali.",
    ],
    "capabilities": [
        "Eu posso conversar com continuidade, guardar informações importantes, ajudar a organizar ideias, opinar com cuidado e transformar pedidos soltos em próximos passos.",
        "Hoje eu consigo te ajudar com conversa, memória seletiva, ideias de projeto, organização, estudo, planejamento e respostas mais humanas.",
        "Minhas melhores funções agora são: entender o contexto, lembrar pontos úteis, responder com empatia e ajudar a clarear decisões.",
    ],
    "identity": [
        "Eu sou a AIDA, uma IA criada para conversar de forma mais humana, lembrar o que importa e manter continuidade com você.",
        "Sou a AIDA. Meu foco não é só responder; é entender o contexto, perceber o tom da conversa e seguir com você sem parecer uma resposta engessada.",
        "Eu sou a AIDA, sua assistente de diálogo e apoio. Ainda sou simples, mas fui desenhada para evoluir com memória, personalidade e respostas naturais.",
    ],
    "continue_with_topic": [
        "A gente tinha parado em algo relacionado a: '{last_topic}'. Posso retomar por ali e transformar isso em próximos passos.",
        "Pelo que ficou salvo, o último ponto importante foi: '{last_topic}'. Quer que eu continue a partir dessa linha?",
        "Tenho esse ponto como referência recente: '{last_topic}'. Dá para seguir dele e organizar a próxima decisão.",
    ],
    "continue_without_topic": [
        "Eu ainda não tenho um ponto anterior muito claro salvo, mas posso continuar a partir do que você me disser agora.",
        "Não achei um assunto anterior forte o bastante para retomar. Me dá uma frase de contexto e eu pego o fio.",
        "Ainda não tenho uma memória recente útil sobre isso, mas posso montar o caminho com você a partir daqui.",
    ],
    "memory": [
        "Guardei isso como uma informação importante para usar nas próximas conversas.",
        "Anotado. Vou tratar isso como contexto relevante, não como uma frase solta.",
        "Beleza, isso entrou como memória útil. Vou usar quando fizer sentido, sem forçar.",
    ],
    "sad": [
        "{continuity}percebi que isso parece estar pesando um pouco. Vamos diminuir o tamanho do problema: qual é a parte que mais está te incomodando agora?",
        "{continuity}isso soa cansativo. Antes de tentar resolver tudo, vale separar o que é urgente do que só está fazendo barulho.",
        "{continuity}eu estou te acompanhando. Me conta o ponto principal e a gente organiza com calma, sem atropelar você.",
    ],
    "happy": [
        "{continuity}dá para sentir sua empolgação. Vamos aproveitar essa energia e transformar em um próximo passo concreto.",
        "{continuity}isso parece bom. Quando a ideia vem com esse gás, o melhor é registrar o caminho antes que ele se espalhe.",
        "{continuity}gostei desse ritmo. Agora vale escolher uma ação pequena que prove que isso funciona.",
    ],
    "angry": [
        "{continuity}eu entendo a irritação. Vamos separar o problema da frustração e achar onde exatamente está travando.",
        "{continuity}isso dá raiva mesmo quando não sai como esperado. A gente pode ir por partes até encontrar a causa.",
        "{continuity}vamos respirar e atacar o ponto certo. Me diz o que aconteceu antes disso travar.",
    ],
    "doubt": [
        "{continuity}vamos simplificar. Você não precisa resolver tudo de uma vez; dá para quebrar isso em partes pequenas.",
        "{continuity}a dúvida faz sentido. Primeiro a gente define o objetivo, depois escolhe o caminho mais simples.",
        "{continuity}vamos clarear isso. Me diga o resultado que você quer, e eu te ajudo a montar os passos.",
    ],
    "project": [
        "{continuity}isso tem cara de projeto em evolução. Eu começaria separando objetivo, público, funções principais e o próximo teste.",
        "{continuity}boa direção. Para esse projeto crescer sem virar bagunça, vale listar o que ele já faz, o que falta e o que é prioridade.",
        "{continuity}se a ideia é tirar do papel, eu faria uma versão pequena primeiro: uma função útil, uma conversa real e um ajuste depois do uso.",
    ],
    "aida_improvement": [
        "Boa. Para deixar a AIDA com mais opções de resposta, o caminho é criar intenções diferentes e várias frases por intenção, em vez de uma resposta fixa para tudo.",
        "Sim, dá para deixar a AIDA bem menos repetitiva. Eu ampliaria respostas por humor, saudação, dúvida, projeto, agradecimento, memória, ajuda e continuação.",
        "Faz sentido. A AIDA fica mais natural quando escolhe entre respostas variadas conforme o contexto, e não quando cai sempre no mesmo texto padrão.",
    ],
    "code": [
        "{continuity}se isso envolve código, me manda o erro, o arquivo ou o comportamento esperado. Eu consigo te ajudar a achar a causa.",
        "{continuity}vamos tratar isso como investigação: o que você tentou, o que aconteceu e qual resultado você esperava?",
        "{continuity}dá para resolver. Primeiro eu preciso entender onde está o problema: API, lógica, memória, voz ou resposta?",
    ],
    "planning": [
        "{continuity}vamos organizar. Eu dividiria em objetivo, prioridade, primeira ação e critério para saber se deu certo.",
        "{continuity}posso te ajudar a transformar isso em um plano curto, com passos que você consiga executar sem se perder.",
        "{continuity}a melhor saída aqui é tirar da cabeça e colocar em ordem: o que é essencial, o que pode esperar e o que destrava tudo.",
    ],
    "learning": [
        "{continuity}posso te ensinar por partes. Primeiro eu explico a ideia simples, depois mostro um exemplo e por fim a gente pratica.",
        "{continuity}vamos aprender isso sem pressa. Me diz se você quer uma explicação rápida, um passo a passo ou um exemplo prático.",
        "{continuity}dá para estudar isso de um jeito leve: conceito, exemplo, tentativa sua e correção comigo.",
    ],
    "fallback": [
        "{continuity}eu entendi o que você quis dizer. Posso te ajudar a transformar isso em uma ideia mais clara ou em um próximo passo.",
        "{continuity}minha leitura é que tem algo importante aí. Me dá um pouco mais de contexto e eu respondo com mais precisão.",
        "{continuity}faz sentido. Eu posso seguir por três caminhos: explicar melhor, organizar em passos ou opinar sobre a melhor direção.",
        "{continuity}vamos trabalhar isso. Se você me disser o objetivo final, eu ajudo a montar o caminho mais simples.",
    ],
}


class AIDA:
    def __init__(self):
        self.memory = MemoryManager()

    def normalize_text(self, message: str) -> str:
        # Remove acentos e deixa tudo minúsculo para facilitar comparações.
        # Assim "opção", "opcao" e "OPÇÃO" podem ser tratados do mesmo jeito.
        normalized = normalize("NFD", message.lower())
        return "".join(
            character for character in normalized
            if category(character) != "Mn"
        )

    def has_any(self, text: str, terms: list[str]) -> bool:
        # Verifica se algum termo conhecido aparece no texto normalizado.
        return any(term in text for term in terms)

    def pick_response(self, response_type: str, **values) -> str:
        # Escolhe uma resposta do banco e preenche campos como {continuity}.
        return choice(RESPONSE_OPTIONS[response_type]).format(**values)

    def is_greeting(self, text: str) -> bool:
        # Detecta cumprimentos curtos sem confundir palavras maiores.
        # Por isso "oi" é checado como palavra separada.
        words = set(text.split())
        greeting_words = {"oi", "ola", "opa", "salve"}
        greeting_phrases = ["bom dia", "boa tarde", "boa noite", "e ai"]

        return bool(words.intersection(greeting_words)) or self.has_any(text, greeting_phrases)

    def detect_emotion(self, message: str) -> str:
        # Detecção emocional simples por palavras-chave.
        # Depois pode evoluir para um modelo de IA mais preciso.
        text = self.normalize_text(message)

        sad_words = ["triste", "cansado", "desanimado", "ansioso", "preocupado", "mal", "sozinho"]
        happy_words = ["feliz", "animado", "empolgado", "contente", "felicidade"]
        angry_words = ["raiva", "irritado", "puto", "bravo", "estressado"]
        doubt_words = ["nao sei", "duvida", "confuso", "perdido", "como faco", "nao entendi"]

        if self.has_any(text, sad_words):
            return "tristeza/preocupação"
        if self.has_any(text, happy_words):
            return "felicidade/empolgação"
        if self.has_any(text, angry_words):
            return "irritação"
        if self.has_any(text, doubt_words):
            return "dúvida/confusão"

        return "neutro"

    def build_context(self, user_id: str) -> str:
        # Monta um texto com personalidade, memória e histórico recente.
        # Esse contexto pode ser usado futuramente por um LLM externo.
        user_memory = self.memory.get_user_memory(user_id)
        history = self.memory.get_history(user_id)

        # Limita o histórico para a conversa não ficar pesada demais.
        recent_history = history[-8:]

        context = "CONTEXTO DA AIDA\n"
        context += f"Nome: {AIDA_PERSONALITY['name']}\n"
        context += f"Estilo: {AIDA_PERSONALITY['style']}\n"
        context += f"Missão: {AIDA_PERSONALITY['mission']}\n\n"

        context += "MEMÓRIAS IMPORTANTES DO USUÁRIO:\n"
        for fact in user_memory.get("important_facts", []):
            context += f"- {fact}\n"

        context += "\nÚLTIMO ASSUNTO:\n"
        context += f"{user_memory.get('last_topic')}\n\n"

        context += "HISTÓRICO RECENTE:\n"
        for item in recent_history:
            context += f"{item['role']}: {item['message']}\n"

        return context

    def generate_opinion(self, message: str) -> str:
        # Respostas opinativas também têm variações para soar menos mecânico.
        text = self.normalize_text(message)

        if "ia" in text or "inteligencia artificial" in text:
            return choice([
                (
                    "Minha opinião? IA não deveria ser só uma ferramenta fria. "
                    "Ela fica muito mais poderosa quando entende contexto, intenção e o lado humano da conversa."
                ),
                (
                    "Eu acho que IA boa precisa ser útil antes de parecer impressionante. "
                    "Se ela entende contexto e ajuda de verdade, a tecnologia começa a fazer sentido."
                ),
                (
                    "Pra mim, IA tem mais valor quando amplia a clareza da pessoa, "
                    "não quando tenta substituir o jeito dela pensar."
                ),
            ])

        if "projeto" in text:
            return choice([
                (
                    "Minha opinião: projeto bom não nasce gigante. Nasce simples, funcional, "
                    "e vai evoluindo com base no uso real."
                ),
                (
                    "Eu gosto de projeto que começa pequeno, mas com uma direção clara. "
                    "O segredo é construir algo que já sirva para alguém desde cedo."
                ),
                (
                    "Pra mim, um projeto forte precisa de três coisas: motivo claro, uso real "
                    "e coragem para cortar o que não ajuda."
                ),
            ])

        if "negocio" in text or "empresa" in text:
            return choice([
                (
                    "Minha opinião: uma ideia só vira negócio quando resolve uma dor clara "
                    "e alguém aceita pagar por isso."
                ),
                (
                    "Eu vejo negócio como uma ponte entre dor real e solução simples. "
                    "Se essa ponte fica clara, a venda começa a ficar menos misteriosa."
                ),
                (
                    "Pra mim, empresa boa não começa pelo logo nem pela promessa. "
                    "Começa por entender exatamente quem ela ajuda e por quê."
                ),
            ])

        return choice([
            (
                "Minha opinião sincera: eu acho melhor olhar isso com calma, entender o contexto "
                "e decidir com base no que realmente te aproxima do objetivo."
            ),
            (
                "Eu olharia para isso perguntando: essa escolha te deixa mais perto do resultado "
                "ou só cria mais complexidade?"
            ),
            (
                "Do jeito que eu vejo, a melhor resposta depende do objetivo. "
                "Quando o objetivo fica claro, a decisão costuma ficar mais leve."
            ),
        ])

    def human_response_engine(self, user_id: str, message: str) -> str:
        """
        Motor simples de resposta humana.
        Depois você pode trocar essa parte por OpenAI, Ollama, Gemini ou outro LLM.
        """

        emotion = self.detect_emotion(message)
        user_memory = self.memory.get_user_memory(user_id)
        history = self.memory.get_history(user_id)

        text = self.normalize_text(message)

        # No chat(), a mensagem do usuário é salva antes da resposta.
        # Aqui removemos essa última mensagem para saber se já existia conversa antes.
        previous_history = history[:-1] if history and history[-1]["message"] == message else history

        if len(previous_history) > 0:
            continuity = "Pelo que a gente vinha conversando, "
        else:
            continuity = "Entendi, "

        # A ordem importa: intenções mais específicas vêm antes das genéricas.
        # Exemplo: melhorar respostas da AIDA deve vencer a intenção "opções".
        if self.has_any(text, ["lembre", "guarde", "memorize", "salve isso", "anote"]):
            response = self.pick_response("memory")

        elif self.has_any(text, ["quem e voce", "se apresente", "qual seu nome", "voce e quem"]):
            response = self.pick_response("identity")

        elif self.has_any(text, ["continuar", "onde paramos", "retomar", "ultimo assunto"]):
            last_topic = user_memory.get("last_topic")

            if last_topic:
                response = self.pick_response("continue_with_topic", last_topic=last_topic)
            else:
                response = self.pick_response("continue_without_topic")

        elif self.has_any(text, ["opiniao", "o que voce acha", "acha que", "na sua visao"]):
            response = self.generate_opinion(message)

        elif self.is_greeting(text):
            response = self.pick_response("greeting")

        elif self.has_any(text, ["obrigado", "obrigada", "valeu", "vlw", "agradeco"]):
            response = self.pick_response("thanks")

        elif "aida" in text and self.has_any(text, ["resposta", "respostas", "melhorar", "mais opcoes", "opcoes"]):
            response = self.pick_response("aida_improvement")

        elif self.has_any(text, ["o que voce faz", "como voce pode ajudar", "suas funcoes", "comandos", "opcoes"]):
            response = self.pick_response("capabilities")

        elif emotion == "tristeza/preocupação":
            response = self.pick_response("sad", continuity=continuity)

        elif emotion == "felicidade/empolgação":
            response = self.pick_response("happy", continuity=continuity)

        elif emotion == "irritação":
            response = self.pick_response("angry", continuity=continuity)

        elif emotion == "dúvida/confusão":
            response = self.pick_response("doubt", continuity=continuity)

        elif self.has_any(text, ["codigo", "programar", "programacao", "python", "erro", "bug", "api", "fastapi"]):
            response = self.pick_response("code", continuity=continuity)

        elif self.has_any(text, ["projeto", "ideia", "aplicativo", "sistema", "startup"]):
            response = self.pick_response("project", continuity=continuity)

        elif self.has_any(text, ["plano", "planejar", "organizar", "passo", "meta", "objetivo", "prioridade"]):
            response = self.pick_response("planning", continuity=continuity)

        elif self.has_any(text, ["estudar", "aprender", "curso", "aula", "explica", "me ensina"]):
            response = self.pick_response("learning", continuity=continuity)

        else:
            response = self.pick_response("fallback", continuity=continuity)

        return response

    def chat(self, user_id: str, message: str) -> dict:
        # Salva a fala do usuário antes de gerar resposta para manter histórico.
        self.memory.add_message(user_id, "user", message)

        # Só guarda na memória permanente quando a frase parece relevante.
        self.memory.remember_if_relevant(user_id, message)

        response = self.human_response_engine(user_id, message)

        # Salva também a resposta da AIDA para manter continuidade.
        self.memory.add_message(user_id, "aida", response)

        return {
            "assistant": "AIDA",
            "user_id": user_id,
            # "response" ajuda a rota de voz; "message" mantém compatibilidade.
            "response": response,
            "message": response,
            "emotion_detected": self.detect_emotion(message),
            "context_used": True
        }
