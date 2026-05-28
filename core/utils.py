import json
from pathlib import Path


def load_json(path: str) -> dict:
    # Converte string em Path para facilitar operações de arquivo e pasta.
    file = Path(path)

    # Se o arquivo ainda não existe, cria a pasta e começa com JSON vazio.
    if not file.exists():
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text("{}", encoding="utf-8")

    try:
        # Lê JSON usando UTF-8 para preservar acentos em português.
        return json.loads(file.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        # Se o arquivo estiver corrompido ou vazio, evita quebrar a aplicação.
        return {}


def save_json(path: str, data: dict) -> None:
    # Garante que a pasta existe antes de tentar gravar o arquivo.
    file = Path(path)
    file.parent.mkdir(parents=True, exist_ok=True)

    # ensure_ascii=False mantém textos com acento legíveis no arquivo.
    file.write_text(
        json.dumps(data, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )
