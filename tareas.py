import streamlit as st
import yaml
from yaml.loader import SafeLoader
from streamlit_extras.switch_page_button import switch_page

# --- Configuración inicial ---
st.set_page_config(page_title="Login", page_icon="🔒")
st.title("Login")

# --- Cargar usuarios ---
with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

USUARIOS = config["credentials"]["usernames"]

# --- Inicializar sesión ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.usuario = None

# =======================
#  LOGIN
# =======================
if not st.session_state.logged_in:
    usuario = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        if usuario in USUARIOS and password == USUARIOS[usuario]["password"]:
            st.session_state.logged_in = True
            st.session_state.usuario = usuario
            st.success(f"Bienvenido {usuario} 👋")
            switch_page("login")  # 👈 Ir a login.py (gestor)
        else:
            st.error("❌ Usuario o contraseña incorrectos")
else:
    # Si ya estaba logueado, ir directo al gestor
    switch_page("login")
