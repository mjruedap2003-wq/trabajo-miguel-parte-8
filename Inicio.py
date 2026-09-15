# -------------------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA Y ESTILOS CSS CORREGIDOS
# -------------------------------------------------------------
st.set_page_config(
    page_title="BookMind - Buscador Inteligente",
    page_icon="🧠",
    layout="wide",
)

# Estilos CSS con alto contraste para fondo oscuro
st.markdown(
    """
    <style>
    /* Fondo principal de la app */
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
    }
    
    /* Etiquetas/Textos encima de los campos de entrada */
    label, div[data-testid="stWidgetLabel"] p {
        color: #F8FAFC !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }

    /* Cajas de texto e inputs */
    textarea, input {
        background-color: #1E293B !important;
        color: #FFFFFF !important;
        border: 1px solid #475569 !important;
        border-radius: 10px !important;
    }

    /* Botones laterales (Consultas Rápidas) */
    .stButton>button {
        background-color: #1E293B !important;
        color: #38BDF8 !important; /* Azul claro brillante */
        border: 1px solid #38BDF8 !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        background-color: #38BDF8 !important;
        color: #0F172A !important;
        transform: translateY(-2px);
    }

    /* Botón Principal (Rastrear Cita Relevante) */
    div.stButton > button[kind="primary"] {
        background-color: #EF4444 !important;
        color: #FFFFFF !important;
        border: none !important;
    }

    /* Cuadro informativo de imagen no encontrada */
    div[data-testid="stAlert"] {
        background-color: #1E293B !important;
        color: #38BDF8 !important;
        border: 1px solid #334155 !important;
    }

    /* Desplegable de matriz TF-IDF */
    div[data-testid="stExpander"] {
        background-color: #1E293B !important;
        border-radius: 10px;
        border: 1px solid #334155;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
