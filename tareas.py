import streamlit as st
import yaml
from yaml.loader import SafeLoader

# =======================
# 1. Cargar usuarios
# =======================
with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

USUARIOS = config["credentials"]["usernames"]

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.usuario = None

st.set_page_config(page_title="Login", page_icon="🔒", layout="centered")

st.title("🔒 Login")

usuario = st.text_input("Usuario")
password = st.text_input("Contraseña", type="password")

if st.button("Ingresar"):
    if usuario in USUARIOS and password == USUARIOS[usuario]["password"]:
        st.session_state.logged_in = True
        st.session_state.usuario = usuario
        st.success(f"Bienvenido {usuario} 👋")

        # Guardamos la "página activa"
        st.session_state.page = "gestor"
        st.experimental_rerun()
    else:
        st.error("❌ Usuario o contraseña incorrectos")

# Si ya está logueado → redirigir
if st.session_state.get("page") == "gestor":
    st.switch_page("pages/login.py")
