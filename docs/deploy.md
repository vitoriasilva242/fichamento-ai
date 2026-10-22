# Como colocar o site no ar (Streamlit Community Cloud)

1. Acesse https://share.streamlit.io e entre com a conta do GitHub.
2. Clique em **Create app** → **Deploy a public app from GitHub** (o *app* fica atrás de login, mesmo com o nome "public").
3. Preencha:
   - **Repository:** `vitoriasilva242/fichamento-ai`
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - **App URL:** escolha um endereço, ex.: `fichamento-ai`
4. Configure o login no Supabase seguindo [autenticacao.md](autenticacao.md#configuração-uma-vez).
5. Em **Advanced settings → Secrets**, cole (com os seus valores):
   ```toml
   SUPABASE_URL = "https://xxxxxxxx.supabase.co"
   SUPABASE_ANON_KEY = "eyJ..."
   CODIGO_CONVITE = "um-codigo-seu"   # exigido para criar conta
   GROQ_API_KEY = "gsk_..."
   GEMINI_API_KEY = "..."
   ```
6. Clique em **Deploy**. Na primeira vez leva alguns minutos (instala o ffmpeg e as bibliotecas).

Depois disso, todo `git push` na `main` atualiza o site sozinho.

### App já publicado? Atualizar os secrets
No app aberto, clique em **Manage app** (canto inferior direito) → **⋮** → **Settings** → **Secrets**, cole o bloco acima e salve. O app reinicia sozinho. A linha antiga `APP_PASSWORD` pode ser apagada.

Na primeira vez, abra a aba **Criar conta**, use o `CODIGO_CONVITE` e cadastre seu e-mail.

## Rodar localmente (opcional)

```bash
pip install -r requirements.txt   # e ffmpeg instalado na máquina
cp .streamlit/secrets.toml.example .streamlit/secrets.toml   # preencha as chaves
streamlit run app.py
```

## Limites a conhecer
- Recarregar a página pede login de novo.
- O plano gratuito do Supabase pausa projetos sem uso por 7 dias; é só reativar no painel.
- Upload de até 200 MB por arquivo (padrão do Streamlit).
- O app "dorme" depois de um tempo sem uso; é só abrir o link e esperar acordar.
- Os planos gratuitos da Groq e do Gemini têm limites diários. Se der erro de cota, espere e tente de novo.
