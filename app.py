import hmac
from datetime import date

import streamlit as st

from fichamento.gerador import MODELO_PADRAO, gerar_fichamento
from fichamento.transcricao import transcrever

st.set_page_config(page_title="fichamento-ai", page_icon="📝", layout="centered")


# --- Acesso com senha (protege a cota gratuita das APIs) ---------------------
def senha_correta() -> bool:
    if st.session_state.get("autenticado"):
        return True
    st.title("📝 fichamento-ai")
    senha = st.text_input("Senha", type="password")
    if senha:
        if hmac.compare_digest(senha, st.secrets["APP_PASSWORD"]):
            st.session_state.autenticado = True
            st.rerun()
        st.error("Senha incorreta.")
    return False


if not senha_correta():
    st.stop()


# --- Interface ---------------------------------------------------------------
st.title("📝 fichamento-ai")
st.caption("Envie ou grave o áudio da aula e receba um fichamento para estudar.")

aba_upload, aba_gravar = st.tabs(["Enviar arquivo", "Gravar agora"])
with aba_upload:
    arquivo = st.file_uploader(
        "Áudio da aula", type=["mp3", "m4a", "wav", "ogg", "webm", "aac", "mp4"]
    )
with aba_gravar:
    gravacao = st.audio_input("Gravar aula")

audio = arquivo or gravacao

col1, col2 = st.columns(2)
disciplina = col1.text_input("Disciplina", placeholder="Ex.: Cálculo I")
tema = col2.text_input("Tema da aula (opcional)")
tipo_prova = st.selectbox(
    "Formato da prova",
    ["Não sei / variado", "Discursiva", "Múltipla escolha", "Exercícios de cálculo", "Código"],
)

if st.button("Gerar fichamento", type="primary", disabled=audio is None):
    try:
        barra = st.progress(0.0, text="Transcrevendo o áudio...")
        transcricao = transcrever(
            audio.getvalue(),
            getattr(audio, "name", "gravacao.wav"),
            api_key=st.secrets["GROQ_API_KEY"],
            ao_progredir=lambda i, n: barra.progress(
                i / n, text=f"Transcrevendo parte {i} de {n}..."
            ),
        )
        barra.empty()

        with st.spinner("Montando o fichamento..."):
            fichamento = gerar_fichamento(
                transcricao,
                api_key=st.secrets["GEMINI_API_KEY"],
                disciplina=disciplina,
                tema=tema,
                tipo_prova="" if tipo_prova.startswith("Não sei") else tipo_prova,
                modelo=st.secrets.get("GEMINI_MODEL", MODELO_PADRAO),
            )
        st.session_state.resultado = {"transcricao": transcricao, "fichamento": fichamento}
    except Exception as erro:  # mostra o erro em vez de quebrar a página
        st.error(f"Algo deu errado: {erro}")

# --- Resultado ---------------------------------------------------------------
if resultado := st.session_state.get("resultado"):
    st.divider()
    st.markdown(resultado["fichamento"])

    base = f"fichamento_{(disciplina or 'aula').lower().replace(' ', '-')}_{date.today()}"
    c1, c2 = st.columns(2)
    c1.download_button(
        "⬇️ Baixar fichamento (.md)", resultado["fichamento"], f"{base}.md", "text/markdown"
    )
    c2.download_button(
        "⬇️ Baixar transcrição (.txt)", resultado["transcricao"], f"{base}_transcricao.txt"
    )
    with st.expander("Ver transcrição completa"):
        st.text(resultado["transcricao"])
