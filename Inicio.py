import re
from nltk.stem import SnowballStemmer
import pandas as pd
from PIL import Image
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

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

# -------------------------------------------------------------
# 2. CABECERA E IMAGEN DEL CEREBRITO LECTOR
# -------------------------------------------------------------
st.title("🧠 BookMind: Asistente de Lectura & Citas")
st.caption(
    "Explora textos, capta ideas principales y encuentra el pasaje exacto que"
    " responde a tus dudas."
)

# Espacio para adjuntar la imagen del cerebrito leyendo
try:
  imagen_cerebro = Image.open("Bob_lector.png")
  st.image(
      imagen_cerebro,
      use_container_width=True,
      caption="Análisis semántico de pasajes con TF-IDF",
  )
except FileNotFoundError:
  st.info(
      "🖼️ *Coloca una imagen llamada 'cerebro_lector.png' en la carpeta de tu"
      " app para verla aquí.*"
  )

st.divider()

# -------------------------------------------------------------
# 3. LÓGICA DE PROCESAMIENTO TF-IDF
# -------------------------------------------------------------
default_docs = """Muchos años después, frente al pelotón de fusilamiento, el coronel Aureliano Buendía había de recordar aquella tarde remota en que su padre lo llevó a conocer el hielo.
Macondo era entonces una aldea de veinte casas de barro y cañabrava construidas a la orilla de un río de aguas diáfanas.
El mundo era tan reciente que muchas cosas carecían de nombre, y para mencionarlas había que señalarlas con el dedo.
José Arcadio Buendía pasaba las noches en su cuarto analizando los mapas de la navegación y calculando las posibilidades de la alquimia.
Úrsula Iguarán vendía los animalitos de caramelo para sostener la economía de la casa familiar.
Melquíades trajo los imanes gigantescos y los lingotes de oro para realizar los experimentos en el laboratorio."""

stemmer = SnowballStemmer("spanish")


def tokenize_and_stem(text):
  text = text.lower()
  text = re.sub(r"[^a-záéíóúüñ\s]", " ", text)
  tokens = [t for t in text.split() if len(t) > 1]
  return [stemmer.stem(t) for t in tokens]


# -------------------------------------------------------------
# 4. INTERFAZ DE USUARIO
# -------------------------------------------------------------
col1, col2 = st.columns([2, 1])

with col1:
  text_input = st.text_area(
      "📖 Pasajes o capítulos del libro (uno por línea):",
      default_docs,
      height=180,
  )

  if "question" not in st.session_state:
    st.session_state.question = "¿Quién llevó a conocer el hielo a Aureliano?"

  question = st.text_input(
      "❓ Escribe tu pregunta sobre el texto:", st.session_state.question
  )

with col2:
  st.markdown("### 💡 Consultas Rápidas")

  def aplicar_pregunta(q):
    st.session_state.question = q

  if st.button("🧊 ¿Quién conoció el hielo?", use_container_width=True):
    aplicar_pregunta("¿Quién llevó a conocer el hielo a Aureliano?")
    st.rerun()

  if st.button("🏡 ¿Cómo era Macondo?", use_container_width=True):
    aplicar_pregunta("¿Cómo era la aldea y las casas de Macondo?")
    st.rerun()

  if st.button("🍬 ¿Qué vendía Úrsula?", use_container_width=True):
    aplicar_pregunta("¿Qué cosas vendía Úrsula para la economía?")
    st.rerun()

  if st.button("🧲 ¿Qué trajo Melquíades?", use_container_width=True):
    aplicar_pregunta("¿Qué inventos e imanes trajo Melquíades?")
    st.rerun()

# -------------------------------------------------------------
# 5. RESULTADOS DEL ANÁLISIS
# -------------------------------------------------------------
if st.button("🔍 Rastrear Cita Relevante", type="primary"):
  documents = [d.strip() for d in text_input.split("\n") if d.strip()]

  if not documents:
    st.error("⚠️ Ingresa al menos un pasaje del libro.")
  elif not question.strip():
    st.error("⚠️ Escribe una pregunta.")
  else:
    vectorizer = TfidfVectorizer(tokenizer=tokenize_and_stem, min_df=1)

    X = vectorizer.fit_transform(documents)
    question_vec = vectorizer.transform([question])
    similarities = cosine_similarity(question_vec, X).flatten()

    best_idx = similarities.argmax()
    best_doc = documents[best_idx]
    best_score = similarities[best_idx]

    st.markdown("---")
    st.subheader("🎯 Cita / Idea Encontrada")

    if best_score > 0.05:
      st.success(f"📖 **Pasaje detectado:** \"{best_doc}\"")
      st.metric(
          label="Nivel de Coincidencia Semántica",
          value=f"{best_score * 100:.1f}%",
      )
    else:
      st.warning(
          "⚠️ **Baja coincidencia.** El pasaje más cercano fue: "
          f"\"{best_doc}\""
      )
      st.metric(
          label="Nivel de Coincidencia Semántica",
          value=f"{best_score * 100:.1f}%",
      )

    with st.expander(
        "📊 Visualizar Matriz de Similitud Term-Vector (TF-IDF)"
    ):
      df_tfidf = pd.DataFrame(
          X.toarray(),
          columns=vectorizer.get_feature_names_out(),
          index=[f"Pasaje {i+1}" for i in range(len(documents))],
      )
      st.dataframe(df_tfidf.round(3), use_container_width=True)
