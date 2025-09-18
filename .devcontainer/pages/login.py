import streamlit as st
import yaml
from yaml.loader import SafeLoader
from streamlit_extras.switch_page_button import switch_page

# --- Cargar usuarios ---
with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

USUARIOS = config["credentials"]["usernames"]

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.usuario = None

# --- Si ya está logueado, mostrar bienvenida y opción de logout ---
if st.session_state.logged_in:
    st.success(f"Ya estás logueado como **{st.session_state.usuario}** ✅")
    if st.button("Cerrar sesión"):
        st.session_state.logged_in = False
        st.session_state.usuario = None
        st.rerun()
    if st.button("Ir al Gestor de Tareas"):
        switch_page("tareas")

else:
    # --- CSS personalizado ---
    st.markdown("""
        <style>
        .login-box {
            background: #1e2027;
            padding: 30px;
            border-radius: 12px;
            text-align: center;
            width: 350px;
            margin: auto;
            margin-top: 100px;
            box-shadow: 0 0 15px rgba(0,0,0,0.5);
        }
        .login-title {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 15px;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown('<div class="login-title">Indicadores Logística</div>', unsafe_allow_html=True)

    usuario = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        if usuario in USUARIOS and password == USUARIOS[usuario]["password"]:
            st.session_state.logged_in = True
            st.session_state.usuario = usuario
            st.success("Bienvenido!")
            switch_page("tareas")
        else:
            st.error("❌ Usuario o contraseña incorrectos")

    st.markdown('</div>', unsafe_allow_html=True)
