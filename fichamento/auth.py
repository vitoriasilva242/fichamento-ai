"""Cadastro e login de usuários com o Supabase Auth (plano gratuito).

O Supabase guarda os usuários e as senhas (com hash) num banco externo,
porque o Streamlit Community Cloud não mantém arquivos entre reinícios.
Este módulo não depende do Streamlit, para poder ser testado sozinho.
"""

from dataclasses import dataclass

from supabase import Client, create_client

TAMANHO_MINIMO_SENHA = 8


@dataclass
class Resultado:
    ok: bool
    mensagem: str
    email: str | None = None


def criar_cliente(url: str, chave_anon: str) -> Client:
    return create_client(url, chave_anon)


def _traduzir_erro(erro: Exception) -> str:
    texto = str(erro).lower()
    if "invalid login credentials" in texto:
        return "E-mail ou senha incorretos."
    if "email not confirmed" in texto:
        return "Confirme seu e-mail pelo link que enviamos antes de entrar."
    if "already registered" in texto or "already exists" in texto:
        return "Este e-mail já está cadastrado. Use a aba Entrar."
    if "rate limit" in texto:
        return "Muitas tentativas seguidas. Espere alguns minutos e tente de novo."
    if "password" in texto and ("weak" in texto or "at least" in texto):
        return "Senha fraca. Use pelo menos 8 caracteres, misturando letras e números."
    if "invalid" in texto and "email" in texto:
        return "E-mail inválido."
    return f"Não foi possível concluir: {erro}"


def cadastrar(cliente: Client, email: str, senha: str) -> Resultado:
    email = email.strip().lower()
    if not email or "@" not in email:
        return Resultado(False, "Informe um e-mail válido.")
    if len(senha) < TAMANHO_MINIMO_SENHA:
        return Resultado(False, f"A senha precisa ter pelo menos {TAMANHO_MINIMO_SENHA} caracteres.")
    try:
        resposta = cliente.auth.sign_up({"email": email, "password": senha})
    except Exception as erro:
        return Resultado(False, _traduzir_erro(erro))

    # Com "Confirm email" ligado no Supabase, não vem sessão até a confirmação.
    if resposta.session is None:
        return Resultado(True, "Conta criada! Abra o link que enviamos para o seu e-mail e depois entre.")
    return Resultado(True, "Conta criada!", email=email)


def entrar(cliente: Client, email: str, senha: str) -> Resultado:
    email = email.strip().lower()
    if not email or not senha:
        return Resultado(False, "Preencha e-mail e senha.")
    try:
        resposta = cliente.auth.sign_in_with_password({"email": email, "password": senha})
    except Exception as erro:
        return Resultado(False, _traduzir_erro(erro))
    return Resultado(True, "Bem-vinda(o)!", email=resposta.user.email)


def sair(cliente: Client) -> None:
    try:
        cliente.auth.sign_out()
    except Exception:
        pass
