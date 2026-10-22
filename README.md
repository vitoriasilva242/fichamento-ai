# fichamento-ai

Transforma o áudio de uma aula em um **fichamento de estudo**: anotações estruturadas, com referências verificáveis e material pronto para revisar para a prova.

## O problema

Durante a aula, é difícil prestar atenção e anotar ao mesmo tempo. Depois, as anotações ficam incompletas, sem conexão com a bibliografia e pouco úteis na hora de estudar.

## A proposta

1. O usuário cria uma conta (com código de convite), entra e envia a gravação da aula.
2. O áudio é transcrito.
3. Um modelo de linguagem (Claude) organiza a transcrição em um fichamento com:
   - tópicos da aula e resumo
   - conceitos-chave com definições
   - exemplos dados pelo professor
   - pontos que o professor enfatizou
   - referências (materiais da disciplina e fontes externas com link)
   - questões no estilo de prova, com gabarito comentado

## Status

🚧 MVP em construção: Streamlit + Groq (Whisper) + Gemini, hospedado no Streamlit Community Cloud, com login e cadastro de usuários pelo Supabase Auth.

## Documentação

- [Spec do MVP](docs/spec-mvp.md)
- [Arquitetura](docs/arquitetura.md)
- [Registro de decisões](docs/decisoes.md)
- [Login e cadastro de usuários](docs/autenticacao.md)
- [Como colocar no ar](docs/deploy.md)

## Autora

Vitória Silva · [@vitoriasilva242](https://github.com/vitoriasilva242)
