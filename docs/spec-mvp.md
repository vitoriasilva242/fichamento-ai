# Spec do MVP

## Objetivo

Validar o núcleo do produto: **uma gravação de aula entra, um fichamento útil para estudar sai.**

## Escopo do MVP

### Dentro
- Upload de um arquivo de áudio (mp3, m4a, wav)
- Transcrição em português
- Geração do fichamento a partir da transcrição
- Visualização do fichamento na tela
- Exportação em Markdown

### Fora (por enquanto)
- Login e contas de usuário
- Gravação direto pelo app
- Upload de materiais da disciplina (RAG), previsto para a v2
- Histórico de aulas e organização por disciplina
- App mobile

## Estrutura do fichamento

| Seção | Conteúdo |
|---|---|
| Identificação | Disciplina, tema, data |
| Resumo | 1 a 2 parágrafos sobre a aula |
| Tópicos | Lista dos assuntos na ordem em que apareceram |
| Conceitos-chave | Termo + definição + como o professor explicou |
| Exemplos | Exemplos e casos citados em aula |
| Ênfases | Trechos em que o professor indicou importância ("isso cai na prova") |
| Referências | Separadas entre *dito em aula* e *complemento externo* (com link) |
| Questões | Questões no estilo de prova, com gabarito comentado |
| Trechos incertos | Partes em que a transcrição ficou confusa, sinalizadas |

## Critérios de sucesso

- O fichamento de uma aula real é útil para estudar sem precisar reouvir o áudio.
- Nenhuma referência inventada: toda fonte externa tem link verificável.
- O processamento de uma aula de ~2h leva poucos minutos.

## Próximos passos

1. Gravar uma aula e transcrever manualmente (Whisper).
2. Iterar o prompt de geração com 2 a 3 transcrições reais.
3. Definir a stack (ver [arquitetura](arquitetura.md)).
4. Implementar o fluxo ponta a ponta.
