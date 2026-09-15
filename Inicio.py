import re
from nltk.stem import SnowballStemmer
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

# Configuración de la aplicación
st.set_page_config(
    page_title="BookFinder - Buscador Inteligente en Libros",
    page_icon="📚",
    layout="wide",
)

st.title("📚 BookFinder: Asistente de Lectura y Citas")
st.caption(
    "Ingresa pasajes o capítulos de un libro y realiza preguntas para ubicar"
    " la idea exacta mediante análisis TF-IDF."
)

# Ejemplos por defecto basados en literatura
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


# Estructura principal
col1, col2 = st.columns([2, 1])

with col1:
  text_input = st.text_area(
      "📖 Pasajes del libro (un pasaje o fragmento por línea):",
      default_docs,
      height=200,
  )

  # Manejo del estado para preguntas
  if "question" not in st.session_state:
    st.session_state.question = "¿Quién llevó a conocer el hielo a Aureliano?"

  question = st.text_input(
      "❓ Escribe tu pregunta sobre la historia:", st.session_state.question
  )

with col2:
  st.markdown("### 💡 Consultas sugeridas:")

  def aplicar_pregunta(q):
    st.session_state.question = q

  if st.button("¿Quién conoció el hielo?", use_container_width=True):
    aplicar_pregunta("¿Quién llevó a conocer el hielo a Aureliano?")
    st.rerun()

  if st.button("¿Cómo era el pueblo de Macondo?", use_container_width=True):
    aplicar_pregunta("¿Cómo era la aldea y las casas de Macondo?")
    st.rerun()

  if st.button("¿Qué vendía Úrsula?", use_container_width=True):
    aplicar_pregunta("¿Qué cosas vendía Úrsula para la economía?")
    st.rerun()

  if st.button("¿Qué experimentos hacía Melquíades?", use_container_width=True):
    aplicar_pregunta("¿Qué inventos e imanes trajo Melquíades?")
    st.rerun()

# Procesamiento del análisis
if st.button("🔍 Buscar Pasaje Relevante", type="primary"):
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

    st.divider()
    st.subheader("🎯 Cita/Pasaje Encontrado")
    st.markdown(f"**Tu pregunta:** *\"{question}\"*")

    if best_score > 0.05:
      st.success(f"📖 **Pasaje del libro:** \"{best_doc}\"")
      st.info(f"📊 Nivel de coincidencia textual: **{best_score * 100:.1f}%**")
    else:
      st.warning(
          "⚠️ **No se encontró un pasaje con suficiente certeza.** "
          f"El más cercano fue: \"{best_doc}\""
      )
      st.info(f"📊 Nivel de coincidencia: **{best_score * 100:.1f}%**")

    # Inspección de términos relevantes
    with st.expander("📊 Inspeccionar relevancia de términos (Matriz TF-IDF)"):
      df_tfidf = pd.DataFrame(
          X.toarray(),
          columns=vectorizer.get_feature_names_out(),
          index=[f"Pasaje {i+1}" for i in range(len(documents))],
      )
      st.dataframe(df_tfidf.round(3), use_container_width=True)
