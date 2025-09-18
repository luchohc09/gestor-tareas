import streamlit as st
import json
import os
import yaml
from yaml.loader import SafeLoader

with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

USUARIOS = config["credentials"]["usernames"]

# =======================
# 2. Estado de sesión
# =======================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.usuario = None

# =======================
# 3. Ventana de Login
# =======================
if not st.session_state.logged_in:
    st.markdown('<div class="login-box">', unsafe_allow_html=True)

    usuario = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        if usuario in USUARIOS and password == USUARIOS[usuario]["password"]:
            st.session_state.logged_in = True
            st.session_state.usuario = usuario
            st.rerun()
        else:
            st.error("❌ Usuario o contraseña incorrectos")

    st.markdown('</div>', unsafe_allow_html=True)

# =======================
# 4. Mostrar solo si está logueado
# =======================
else:
    st.sidebar.success(f"Bienvenido {USUARIOS[st.session_state.usuario]['name']}")
    if st.sidebar.button("Cerrar sesión"):
        st.session_state.logged_in = False
        st.rerun()

    # 🚀 🚀 🚀 Aquí recién va tu gestor de tareas
    st.title("📌 Gestor de Tareas")


# --- Si logueado, mostrar gestor de tareas ---
if st.session_state.logged_in:
    st.title("📌 Gestor de Tareas")

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


if "tareas" not in st.session_state:
    st.session_state.tareas = cargar_datos()

if "editando" not in st.session_state:
    st.session_state.editando = None


for carpeta in ["Facturas", "Edi"]:
    if carpeta in st.session_state.tareas and isinstance(st.session_state.tareas[carpeta], list):
        st.session_state.tareas[carpeta] = {"General": st.session_state.tareas[carpeta]}
guardar_datos()

st.title("📌 Gestor de Tareas")

# Formulario inicial
with st.form("nueva_tarea"):
    categoria = st.text_input("📂 Nombre de la Carpeta")
    subtarea = st.text_input("📝 Nombre de la tarea ")
    submitted = st.form_submit_button("➕ Agregar")

    if submitted and categoria:
        if categoria not in st.session_state.tareas:
            if categoria in ["Facturas", "Edi"]:
                st.session_state.tareas[categoria] = {}
            else:
                st.session_state.tareas[categoria] = []

        if subtarea:
            if categoria in ["Facturas", "Edi"]:
                if "General" not in st.session_state.tareas[categoria]:
                    st.session_state.tareas[categoria]["General"] = []
                st.session_state.tareas[categoria]["General"].append(
                    {"nombre": subtarea, "estado": "Pendiente"}
                )
            else:
                st.session_state.tareas[categoria].append(
                    {"nombre": subtarea, "estado": "Pendiente"}
                )

        guardar_datos()
        st.success(f"Agregado en carpeta '{categoria}'")
        st.rerun()

# categorías 
for categoria, contenido in list(st.session_state.tareas.items()):
    with st.expander(f"📂 {categoria}", expanded=True):

        # Edi y Facturas
        if categoria in ["Facturas", "Edi"]:
            with st.form(f"add_subcat_{categoria}"):
                subcarpeta = st.text_input(f"➕ Nueva subcarpeta en {categoria}")
                submitted_sub = st.form_submit_button("Crear subcarpeta")
                if submitted_sub and subcarpeta:
                    if subcarpeta not in st.session_state.tareas[categoria]:
                        st.session_state.tareas[categoria][subcarpeta] = []
                        guardar_datos()
                        st.rerun()

            for subcarpeta, subtareas in list(st.session_state.tareas[categoria].items()):
                with st.expander(f"📁 {subcarpeta}", expanded=False):
                    filtro = st.radio(
                        f"🔲 Filtrar en {subcarpeta}:",
                        ["Todas", "Pendiente", "Finalizado"],
                        horizontal=True,
                        key=f"filtro_{categoria}_{subcarpeta}"
                    )

                    filtro_texto = st.text_input(
                        "🔍 Buscar tarea por nombre o número:",
                        key=f"filtro_texto_{categoria}_{subcarpeta}"
                    ).strip().lower()

                    with st.form(f"add_task_{categoria}_{subcarpeta}"):
                        nueva_tarea = st.text_input("📝 Nueva tarea", key=f"task_{categoria}_{subcarpeta}")
                        submitted_task = st.form_submit_button("➕ Agregar tarea")
                        if submitted_task and nueva_tarea:
                            subtareas.append({"nombre": nueva_tarea, "estado": "Pendiente"})
                            guardar_datos()
                            st.rerun()

                    for i, tarea in enumerate(subtareas):
                        if filtro != "Todas" and tarea["estado"] != filtro:
                            continue
                        if filtro_texto and filtro_texto not in tarea["nombre"].lower():
                            continue

                        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                        with col1:
                            if st.session_state.editando == (categoria, subcarpeta, i):
                                nuevo_nombre = st.text_input(
                                    "Editar:",
                                    value=tarea["nombre"],
                                    key=f"edit_{categoria}_{subcarpeta}_{i}"
                                )
                                if st.button("💾 Guardar", key=f"save_{categoria}_{subcarpeta}_{i}"):
                                    tarea["nombre"] = nuevo_nombre
                                    st.session_state.editando = None
                                    guardar_datos()
                                    st.rerun()
                            else:
                                st.write(f"📝 {tarea['nombre']} - **{tarea['estado']}**")

                        with col2:
                            if st.button("🟢 Finalizar", key=f"fin_{categoria}_{subcarpeta}_{i}"):
                                tarea["estado"] = "Finalizado"
                                guardar_datos()
                                st.rerun()

                        with col3:
                            if st.button("✏️", key=f"mod_{categoria}_{subcarpeta}_{i}"):
                                st.session_state.editando = (categoria, subcarpeta, i)
                                st.rerun()

                        with col4:
                            if st.button("❌", key=f"del_{categoria}_{subcarpeta}_{i}"):
                                st.session_state.tareas[categoria][subcarpeta].pop(i)
                                guardar_datos()
                                st.rerun()

        else:
            filtro = st.radio(
                f"🔲 Filtrar en {categoria}:",
                ["Todas", "Pendiente", "Finalizado"],
                horizontal=True,
                key=f"filtro_{categoria}"
            )

            filtro_texto = st.text_input(
                "🔍 Buscar tarea por nombre o número:",
                key=f"filtro_texto_{categoria}"
            ).strip().lower()

            for i, tarea in enumerate(contenido):
                if filtro != "Todas" and tarea["estado"] != filtro:
                    continue
                if filtro_texto and filtro_texto not in tarea["nombre"].lower():
                    continue

                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                with col1:
                    if st.session_state.editando == (categoria, i):
                        nuevo_nombre = st.text_input(
                            "Editar:",
                            value=tarea["nombre"],
                            key=f"edit_{categoria}_{i}"
                        )
                        if st.button("💾 Guardar", key=f"save_{categoria}_{i}"):
                            tarea["nombre"] = nuevo_nombre
                            st.session_state.editando = None
                            guardar_datos()
                            st.rerun()
                    else:
                        st.write(f"📝 {tarea['nombre']} - **{tarea['estado']}**")

                with col2:
                    if st.button("🟢 Finalizar", key=f"fin_{categoria}_{i}"):
                        tarea["estado"] = "Finalizado"
                        guardar_datos()
                        st.rerun()

                with col3:
                    if st.button("✏️", key=f"mod_{categoria}_{i}"):
                        st.session_state.editando = (categoria, i)
                        st.rerun()

                with col4:
                    if st.button("❌", key=f"del_{categoria}_{i}"):
                        st.session_state.tareas[categoria].pop(i)
                        guardar_datos()
                        st.rerun()



