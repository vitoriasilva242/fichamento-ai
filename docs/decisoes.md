# Registro de decisões

Formato: cada decisão registra o contexto, o que foi decidido e o porquê. Decisões em aberto ficam marcadas como **pendentes**.

---

## D001 · Nome do projeto
- **Status:** decidido (2026-10-21)
- **Decisão:** `fichamento-ai`
- **Por quê:** "fichamento" é o termo acadêmico para resumo com referências, que é o diferencial do produto.

## D002 · Transcrição separada do LLM
- **Status:** decidido (2026-10-21)
- **Decisão:** usar um serviço dedicado de speech-to-text e enviar só o texto ao Claude.
- **Por quê:** serviços de STT são especializados em áudio longo e em português; o Claude fica responsável pela organização e pelo conteúdo.

## D003 · Validar o prompt antes de automatizar
- **Status:** decidido (2026-10-21)
- **Decisão:** iterar o prompt manualmente com 2 a 3 transcrições reais antes de escrever o app.
- **Por quê:** a qualidade do fichamento é o produto; o resto é infraestrutura.

## D004 · Serviço de transcrição
- **Status:** pendente
- **Opções:** Whisper (local/API), Deepgram, AssemblyAI.

## D005 · Stack da aplicação
- **Status:** pendente
- **Opções a considerar:** backend em Python (FastAPI) + front simples; ou framework full-stack.
