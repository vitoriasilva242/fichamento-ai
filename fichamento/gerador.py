"""Geração do fichamento a partir da transcrição.

Toda a lógica do provedor de LLM fica aqui, atrás de gerar_fichamento(),
para que trocar o Gemini por outro modelo (ex.: Claude) mexa só neste arquivo.
"""

from pathlib import Path

from google import genai
from google.genai import types

PASTA_PROMPTS = Path(__file__).resolve().parent.parent / "prompts"
PROMPT_PADRAO = "fichamento_v1.md"
MODELO_PADRAO = "gemini-flash-latest"


def carregar_prompt(nome: str = PROMPT_PADRAO) -> str:
    return (PASTA_PROMPTS / nome).read_text(encoding="utf-8")


def gerar_fichamento(
    transcricao: str,
    api_key: str,
    disciplina: str = "",
    tema: str = "",
    tipo_prova: str = "",
    modelo: str = MODELO_PADRAO,
) -> str:
    """Devolve o fichamento em Markdown."""
    contexto = (
        f"Disciplina: {disciplina or 'não informada'}\n"
        f"Tema da aula: {tema or 'não informado'}\n"
        f"Formato da prova: {tipo_prova or 'não informado'}\n"
    )
    mensagem = f"{contexto}\n<transcricao>\n{transcricao}\n</transcricao>"

    cliente = genai.Client(api_key=api_key)
    resposta = cliente.models.generate_content(
        model=modelo,
        contents=mensagem,
        config=types.GenerateContentConfig(
            system_instruction=carregar_prompt(),
            temperature=0.3,
        ),
    )
    return resposta.text
