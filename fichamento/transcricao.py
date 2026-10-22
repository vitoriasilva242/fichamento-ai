"""Transcrição de áudio com a API gratuita da Groq (Whisper).

O plano gratuito limita o tamanho de cada arquivo enviado, então o áudio é
convertido para mono/16 kHz/32 kbps e dividido em partes de 10 minutos
(~2,4 MB cada) antes do envio.
"""

import subprocess
import tempfile
from pathlib import Path

from groq import Groq

MODELO_WHISPER = "whisper-large-v3-turbo"
DURACAO_PARTE_S = 600  # 10 minutos


def dividir_audio(caminho_entrada: Path, pasta_saida: Path) -> list[Path]:
    """Comprime o áudio e divide em partes. Requer ffmpeg instalado."""
    padrao = pasta_saida / "parte_%03d.mp3"
    subprocess.run(
        [
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-i", str(caminho_entrada),
            "-vn", "-ac", "1", "-ar", "16000", "-b:a", "32k",
            "-f", "segment", "-segment_time", str(DURACAO_PARTE_S),
            str(padrao),
        ],
        check=True,
    )
    return sorted(pasta_saida.glob("parte_*.mp3"))


def transcrever(audio: bytes, nome_arquivo: str, api_key: str, ao_progredir=None) -> str:
    """Transcreve o áudio inteiro e devolve o texto concatenado.

    ao_progredir(i, total) é chamado após cada parte, para a barra de progresso.
    """
    cliente = Groq(api_key=api_key)
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        entrada = tmp / ("entrada" + Path(nome_arquivo).suffix)
        entrada.write_bytes(audio)
        partes = dividir_audio(entrada, tmp)

        textos = []
        for i, parte in enumerate(partes, start=1):
            with open(parte, "rb") as f:
                resposta = cliente.audio.transcriptions.create(
                    file=(parte.name, f.read()),
                    model=MODELO_WHISPER,
                    language="pt",
                    response_format="text",
                )
            textos.append(resposta if isinstance(resposta, str) else resposta.text)
            if ao_progredir:
                ao_progredir(i, len(partes))

    return "\n\n".join(t.strip() for t in textos)
