# Login e cadastro de usuários

O app usa o **Supabase Auth** (plano gratuito) para cadastro e login com e-mail e senha.

## Por que não uma senha única?

A primeira versão tinha só um campo "Senha", comparado com `APP_PASSWORD` nos *secrets*. Isso causou um problema real: não havia onde se cadastrar, ninguém sabia qual senha usar e, se `APP_PASSWORD` não estivesse nos *secrets*, o app quebrava na tela de entrada. Ver [D009](decisoes.md#d009--login-com-contas-de-usuário).

## Por que um serviço externo?

O Streamlit Community Cloud **não guarda arquivos** entre reinícios: um `usuarios.json` ou SQLite local seria apagado quando o app "dorme". O Supabase guarda os usuários num Postgres gerenciado, faz o *hash* das senhas e cuida de confirmação de e-mail e limite de tentativas.

## Como funciona

```
Tela de acesso ── aba "Entrar" ──────► supabase.auth.sign_in_with_password
              └── aba "Criar conta" ─► confere CODIGO_CONVITE ─► supabase.auth.sign_up
                                              │
                                   sessão ok? ▼
                            st.session_state.usuario = e-mail ─► app liberado
```

- Código: [`fichamento/auth.py`](../fichamento/auth.py) (sem dependência do Streamlit) e a seção "Login e cadastro" do [`app.py`](../app.py).
- **Código de convite:** se `CODIGO_CONVITE` estiver nos *secrets*, o cadastro exige esse código. Assim só quem você convidar consegue criar conta e consumir a cota gratuita da Groq e do Gemini. Apague a linha para liberar o cadastro.
- **Senha:** mínimo de 8 caracteres (checado no app e também configurável no Supabase).
- **Sair:** botão na barra lateral; limpa a sessão do Streamlit e encerra a sessão no Supabase.
- A sessão vale enquanto a aba do navegador estiver aberta. Recarregar a página pede login de novo (o Streamlit não guarda cookies de sessão).

## Configuração (uma vez)

1. Crie uma conta em https://supabase.com e um projeto novo (plano **Free**).
2. Em **Project Settings → API**, copie:
   - **Project URL** → `SUPABASE_URL`
   - chave **anon public** → `SUPABASE_ANON_KEY`
   > Nunca use a chave `service_role` no app: ela ignora todas as regras de segurança.
3. Em **Authentication → Sign In / Providers → Email**:
   - Deixe **Enable Email provider** ligado.
   - **Confirm email:** ligado = a pessoa precisa clicar num link antes de entrar (mais seguro); desligado = entra logo após o cadastro (mais simples). O plano gratuito envia poucos e-mails por hora, então para uso pessoal desligar é razoável, já que o código de convite já controla quem entra.
4. Em **Authentication → URL Configuration**, coloque `https://fichamento-ai.streamlit.app` em **Site URL** (é para onde o link de confirmação leva).
5. Cole as chaves nos *secrets* do Streamlit (ver [deploy.md](deploy.md)).

## Administração

- **Ver usuários / apagar conta:** Supabase → **Authentication → Users**.
- **Esqueceu a senha:** em **Authentication → Users**, abra o usuário e use **Send password recovery** ou apague e peça para cadastrar de novo. (O app ainda não tem tela de redefinição de senha.)
- **Trocar o código de convite:** edite `CODIGO_CONVITE` nos *secrets*; contas já criadas continuam valendo.

## Próximos passos possíveis
- Tela "Esqueci a senha" dentro do app.
- Login com Google (Supabase → Providers → Google).
- Histórico de fichamentos por usuário numa tabela do Supabase com *Row Level Security* (ver [D008](decisoes.md#d008--armazenamento)).
