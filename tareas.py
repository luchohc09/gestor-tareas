import streamlit as st
import yaml
from yaml.loader import SafeLoader
from streamlit_extras.switch_page_button import switch_page

# =======================
# 1. Cargar usuarios
# =======================
with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

USUARIOS = config["credentials"]["usernames"]

# Inicializar estado de sesión
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.usuario = None

# =======================
# 2. Mostrar LOGIN
# =======================
st.set_page_config(page_title="Login", page_icon="🔒", layout="centered")

st.title("🔒 Login")

usuario = st.text_input("Usuario")
password = st.text_input("Contraseña", type="password")

if st.button("Ingresar"):
    if usuario in USUARIOS and password == USUARIOS[usuario]["password"]:
        st.session_state.logged_in = True
        st.session_state.usuario = usuario
        st.success(f"Bienvenido {usuario} 👋")

        # 🔽 Aquí va el cambio: redirige al gestor de tareas (login.py)
        switch_page("Login")
    else:
        st.error("❌ Usuario o contraseña incorrectos")

