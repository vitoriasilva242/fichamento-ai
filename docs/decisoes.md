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
- **Status:** decidido (2026-10-21)
- **Decisão:** Whisper rodando localmente no Mac (mlx-whisper, otimizado para Apple Silicon). Fallback: API gratuita da Groq (whisper-large-v3).
- **Por quê:** custo zero, sem limite de uso e o áudio não sai do computador.

## D005 · Stack da aplicação
- **Status:** decidido (2026-10-21)
- **Decisão:** Python + Streamlit, rodando localmente.
- **Por quê:** zero custo de hospedagem, uma linguagem só e interface pronta para upload e visualização. Migrar para web (FastAPI + front) só se o app for aberto a outras pessoas.

## D006 · Restrição de custo zero
- **Status:** decidido (2026-10-21)
- **Decisão:** o MVP não pode ter custo de implementação ou operação.
- **Consequências:** transcrição local; LLM via plano gratuito; app roda localmente; RAG com embeddings locais.

## D007 · Modelo para gerar o fichamento
- **Status:** decidido (2026-10-21)
- **Decisão:** Gemini Flash pelo plano gratuito da API do Google, atrás de uma interface própria (`gerar_fichamento(transcricao)`) para poder trocar de provedor depois. Alternativa offline: modelo local via Ollama.
- **Fase de validação do prompt:** feita manualmente no Claude (chat), sem custo extra.
- **Atenção:** no plano gratuito do Gemini, o Google pode usar os dados enviados para melhorar os produtos. Não enviar gravações com dados sensíveis. A API do Claude é paga; fica como opção futura.
