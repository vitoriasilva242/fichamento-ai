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
- **Status:** decidido (2026-10-21, revisado)
- **Decisão:** API gratuita da Groq (whisper-large-v3-turbo). O áudio é comprimido e dividido em partes antes do envio, por causa do limite de tamanho de arquivo do plano gratuito.
- **Alternativa:** enviar o áudio direto ao Gemini, que transcreve e gera o fichamento numa chamada só.
- **Por quê:** o app roda na nuvem e não deve depender do computador da usuária; servidores gratuitos são fracos demais para rodar o Whisper.

## D005 · Stack e hospedagem
- **Status:** decidido (2026-10-21, revisado)
- **Decisão:** Python + Streamlit, hospedado no Streamlit Community Cloud (gratuito), com deploy automático a partir deste repositório no GitHub.
- **Por quê:** custo zero, uma linguagem só, abre no navegador do computador e do celular, e permite gravar áudio direto pelo navegador.
- **Alternativa:** Hugging Face Spaces (também gratuito).
- **Cuidado:** as chaves de API ficam nos *secrets* do Streamlit, nunca no código. O app exige login, para outras pessoas não consumirem a cota gratuita (ver D009).

## D006 · Restrição de custo zero
- **Status:** decidido (2026-10-21)
- **Decisão:** o MVP não pode ter custo de implementação ou operação.
- **Consequências:** só serviços com plano gratuito; nada roda no computador da usuária.

## D007 · Modelo para gerar o fichamento
- **Status:** decidido (2026-10-21)
- **Decisão:** Gemini Flash pelo plano gratuito da API do Google, atrás de uma interface própria (`gerar_fichamento(transcricao)`) para poder trocar de provedor depois.
- **Fase de validação do prompt:** feita manualmente no Claude (chat), sem custo extra.
- **Atenção:** no plano gratuito do Gemini, o Google pode usar os dados enviados para melhorar os produtos. A API do Claude é paga; fica como opção futura.

## D008 · Armazenamento
- **Status:** decidido (2026-10-21)
- **Decisão:** no MVP, sem banco de dados: o fichamento é exibido e baixado em Markdown. Histórico de aulas fica para depois (ex.: Supabase, plano gratuito).
- **Exceção (2026-10-22):** as contas de usuário já ficam no Supabase Auth (D009); os fichamentos continuam sem banco.

## D009 · Login com contas de usuário
- **Status:** decidido (2026-10-22)
- **Contexto:** a primeira versão tinha só uma senha única (`APP_PASSWORD` nos *secrets*). Não havia tela de cadastro, e o app quebrava na entrada quando o segredo não estava configurado, impedindo o acesso.
- **Decisão:** cadastro e login com e-mail e senha pelo **Supabase Auth** (plano gratuito). O cadastro exige um código de convite (`CODIGO_CONVITE`), para manter a proteção da cota gratuita das APIs. Detalhes em [autenticacao.md](autenticacao.md).
- **Por quê:** o Streamlit Community Cloud não guarda arquivos entre reinícios, então os usuários precisam de um banco externo; o Supabase é gratuito, faz *hash* das senhas e já resolve confirmação de e-mail e limite de tentativas. Mantém a restrição de custo zero (D006).
- **Alternativas descartadas:** `streamlit-authenticator` com YAML no repositório (cadastros se perdem no reinício e as senhas ficariam no Git); login com Google via `st.login` (exige configurar OAuth no Google Cloud; pode vir depois).
- **Consequências:** a sessão não sobrevive a recarregar a página; o app ainda não tem tela de "esqueci a senha" (feito pelo painel do Supabase).
