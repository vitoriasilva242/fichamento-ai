# Como colocar o site no ar (Streamlit Community Cloud)

1. Acesse https://share.streamlit.io e entre com a conta do GitHub.
2. Clique em **Create app** → **Deploy a public app from GitHub** (o *app* fica atrás de senha, mesmo com o nome "public").
3. Preencha:
   - **Repository:** `vitoriasilva242/fichamento-ai`
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - **App URL:** escolha um endereço, ex.: `fichamento-ai`
4. Em **Advanced settings → Secrets**, cole (com os seus valores):
   ```toml
   APP_PASSWORD = "uma-senha-sua"
   GROQ_API_KEY = "gsk_..."
   GEMINI_API_KEY = "..."
   ```
5. Clique em **Deploy**. Na primeira vez leva alguns minutos (instala o ffmpeg e as bibliotecas).

Depois disso, todo `git push` na `main` atualiza o site sozinho.

## Rodar localmente (opcional)

```bash
pip install -r requirements.txt   # e ffmpeg instalado na máquina
cp .streamlit/secrets.toml.example .streamlit/secrets.toml   # preencha as chaves
streamlit run app.py
```

## Limites a conhecer
- Upload de até 200 MB por arquivo (padrão do Streamlit).
- O app "dorme" depois de um tempo sem uso; é só abrir o link e esperar acordar.
- Os planos gratuitos da Groq e do Gemini têm limites diários. Se der erro de cota, espere e tente de novo.
