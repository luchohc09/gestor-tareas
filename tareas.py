import streamlit as st
import yaml
from yaml.loader import SafeLoader
import json
import os

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
            st.success("Bienvenido!")
            st.rerun()
        else:
            st.error("❌ Usuario o contraseña incorrectos")

# =======================
# 3. Mostrar GESTOR solo si hay login
# =======================
else:
    st.sidebar.success(f"Bienvenido {st.session_state.usuario}")
    if st.sidebar.button("Cerrar sesión"):
        st.session_state.logged_in = False
        st.session_state.usuario = None
        st.rerun()

    st.set_page_config(page_title="Gestor De Tareas", layout="wide")

    DATA_FILE = "tareas.json"

    def cargar_datos():
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def guardar_datos():
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(st.session_state.tareas, f, ensure_ascii=False, indent=4)

    # 👉 Aquí pega todo tu gestor de tareas original
