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

# =======================
# 2. Mostrar LOGIN si no está logueado
# =======================
if not st.session_state.logged_in:
    st.title("🔒 Login")

    usuario = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        if usuario in USUARIOS and password == USUARIOS[usuario]["password"]:
            st.session_state.logged_in = True
            st.session_state.usuario = usuario
            st.success(f"Bienvenido {usuario} 👋")

            # ✅ Redirigir al gestor de tareas en pages/login.py
            st.switch_page("pages/login.py")
        else:
            st.error("❌ Usuario o contraseña incorrectos")

# =======================
# 3. Si ya está logueado, redirigir directo al gestor
# =======================
else:
    st.switch_page("pages/login.py")
