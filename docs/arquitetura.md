# Arquitetura

## Visão geral

```
Login / cadastro (Supabase Auth)
     │  usuário autenticado
     ▼
Áudio da aula
     │
     ▼
[1] Transcrição (speech-to-text)
     │  texto bruto
     ▼
[2] Geração do fichamento (Claude API)
     │  JSON estruturado
     ▼
[3] Interface (visualizar / exportar Markdown)
```

## Componentes

### 0. Acesso
- Cadastro e login com e-mail e senha pelo Supabase Auth, com código de convite no cadastro.
- Ver [autenticacao.md](autenticacao.md).

### 1. Transcrição
- **Opção inicial:** Whisper (open source; roda local ou via API).
- Alternativas a avaliar: Deepgram, AssemblyAI.
- Critérios: qualidade em português, custo por hora de áudio, suporte a áudio longo, timestamps.

### 2. Geração do fichamento
- Chamada à API do Claude com a transcrição completa no contexto.
- Saída em **JSON estruturado** seguindo as seções definidas no [spec](spec-mvp.md).
- Prompt versionado no repositório (`prompts/`), para iterar e comparar versões.
- Referências externas: habilitar a ferramenta de web search da API, exigindo link para cada fonte.

### 3. Interface
- MVP: página web simples com upload de arquivo e renderização do fichamento.
- Stack a definir (ver [decisões](decisoes.md)).

## v2: materiais da disciplina (RAG)
- Upload de slides, ementa e PDFs da bibliografia.
- O fichamento cita trechos reais desses materiais, em vez de depender só do conhecimento do modelo.

## Riscos
- **Referências inventadas:** mitigado com web search + RAG + separação explícita entre "dito em aula" e "complemento externo".
- **Transcrição ruim** (ruído, vários falantes): sinalizar trechos incertos em vez de completar.
- **Custo:** medir tokens e custo por aula desde o início.
