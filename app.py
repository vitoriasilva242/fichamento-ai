import hmac
from datetime import date

import streamlit as st

from fichamento import auth
from fichamento.gerador import MODELO_PADRAO, gerar_fichamento
from fichamento.transcricao import transcrever

st.set_page_config(page_title="fichamento-ai", page_icon="📝", layout="centered")


# --- Login e cadastro (Supabase Auth) ---------------------------------------
# O acesso protege a cota gratuita das APIs. O cadastro pede um código de
# convite (CODIGO_CONVITE nos secrets), para só quem você convidar criar conta.
def cliente_supabase():
    if "supabase" not in st.session_state:
        try:
            st.session_state.supabase = auth.criar_cliente(
                st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_ANON_KEY"]
            )
        except KeyError:
            st.error(
                "Login não configurado: adicione SUPABASE_URL e SUPABASE_ANON_KEY "
                "em Manage app → Settings → Secrets (veja docs/deploy.md)."
            )
            st.stop()
    return st.session_state.supabase


def tela_de_acesso() -> None:
    st.title("📝 fichamento-ai")
    cliente = cliente_supabase()
    aba_entrar, aba_cadastrar = st.tabs(["Entrar", "Criar conta"])

    with aba_entrar:
        with st.form("entrar"):
            email = st.text_input("E-mail")
            senha = st.text_input("Senha", type="password")
            if st.form_submit_button("Entrar", type="primary"):
                r = auth.entrar(cliente, email, senha)
                if r.ok:
                    st.session_state.usuario = r.email
                    st.rerun()
                st.error(r.mensagem)
        st.caption("Esqueceu a senha? Peça à administradora para redefinir no Supabase.")

    with aba_cadastrar:
        convite_exigido = st.secrets.get("CODIGO_CONVITE", "")
        with st.form("cadastrar"):
            email = st.text_input("E-mail")
            senha = st.text_input(
                "Senha", type="password", help=f"Mínimo de {auth.TAMANHO_MINIMO_SENHA} caracteres."
            )
            confirmacao = st.text_input("Repita a senha", type="password")
            convite = st.text_input("Código de convite", type="password") if convite_exigido else ""
            if st.form_submit_button("Criar conta", type="primary"):
                if convite_exigido and not hmac.compare_digest(convite, convite_exigido):
                    st.error("Código de convite inválido.")
                elif senha != confirmacao:
                    st.error("As senhas não conferem.")
                else:
                    r = auth.cadastrar(cliente, email, senha)
                    if r.ok and r.email:
                        st.session_state.usuario = r.email
                        st.rerun()
                    (st.success if r.ok else st.error)(r.mensagem)


if not st.session_state.get("usuario"):
    tela_de_acesso()
    st.stop()

with st.sidebar:
    st.write(f"Conectada(o) como **{st.session_state.usuario}**")
    if st.button("Sair"):
        auth.sair(cliente_supabase())
        for chave in ("usuario", "supabase", "resultado"):
            st.session_state.pop(chave, None)
        st.rerun()


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
