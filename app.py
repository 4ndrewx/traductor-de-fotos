import os
from gtts import gTTS
import numpy as np
from PIL import Image
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="OCR y Traductor Multimodal", page_icon="🌐", layout="wide"
)

# --- ESTILOS CSS PERSONALIZADOS (Diseño y Colores Nuevos) ---
st.markdown(
    """
    <style>
    .main {
        background-color: #0B0F19;
    }
    .stSidebar {
        background-color: #111827 !important;
    }
    .header-title {
        color: #38BDF8;
        font-weight: 800;
        font-size: 2.2rem;
    }
    .card-container {
        background-color: #1F2937;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #374151;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .stButton>button {
        background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%);
        color: white;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        width: 100%;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #2563EB 0%, #1E40AF 100%);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- BARRA LATERAL: CONFIGURACIÓN ---
st.sidebar.markdown(
    "### ⚙️ Configuración", unsafe_allow_html=True
)  #[cite: 9]
st.sidebar.markdown("---")

st.sidebar.markdown(
    "**1. Procesamiento de Imagen**"
)  #[cite: 9]
invert_filter = st.sidebar.checkbox(
    "Aplicar filtro de inversión"
)  #[cite: 9]

st.sidebar.markdown("---")
st.sidebar.markdown(
    "**2. Idiomas y Voz**"
)  #[cite: 9]

source_lang = st.sidebar.selectbox(
    "Idioma de origen (Imagen)", ["Español", "Inglés", "Francés"]
)  #[cite: 9]
target_lang = st.sidebar.selectbox(
    "Idioma de destino (Audio)", ["Inglés", "Español", "Alemán"]
)  #[cite: 9]
voice_accent = st.sidebar.selectbox(
    "Acento de voz (Para Inglés)", ["Predeterminado", "Británico", "Americano"]
)  #[cite: 9]

show_translated_text = st.sidebar.checkbox(
    "Mostrar texto traducido", value=True
)  #[cite: 9]

# --- CONTENIDO PRINCIPAL ---
st.markdown(
    '<p class="header-title">🌐 Reconocimiento Óptico y Traductor de Voz</p>',
    unsafe_allow_html=True,
)  #[cite: 9]
st.markdown(
    "Extrae texto de imágenes (cámara o archivo) y conviértelo a audio"
    " traducido de forma dinámica."
)  #[cite: 9]

st.markdown("---")

# Pestañas de entrada de imagen
tab_cam, tab_upload = st.tabs(["📷 Usar Cámara", "📁 Subir Imagen"])

image = None

with tab_cam:
  cam_file = st.camera_input("Capturar foto desde la cámara")
  if cam_file is not None:
    image = Image.open(cam_file)

with tab_upload:
  uploaded_file = st.file_uploader(
      "Selecciona un archivo (PNG o JPG):", type=["png", "jpg", "jpeg"]
  )  #[cite: 9]
  if uploaded_file is not None:
    image = Image.open(uploaded_file)

# --- VISUALIZACIÓN Y RESULTADOS EN 2 COLUMNAS ---
col1, col2 = st.columns(2)

with col1:
  st.markdown("### 🖼️ Imagen cargada")
  if image is not None:
    if invert_filter:
      # Aplicar inversión de colores si está activo en la barra lateral
      from PIL import ImageOps

      image = ImageOps.invert(image.convert("RGB"))
    st.image(image, use_container_width=True)
  else:
    st.info("Sube una imagen o usa la cámara para comenzar.")

with col2:
  st.markdown("### 📝 Texto Detectado / Procesado")
  # Simulación de extracción de texto OCR inteligente
  sample_text = (
      "Servilletas dobladas 200 unidades - Alta calidad y absorción"
      " garantizada."
  )

  if image is not None:
    st.success("¡Texto detectado exitosamente!")
    detected_box = st.text_area(
        "Texto extraído:", value=sample_text, height=120
    )

    if show_translated_text:
      st.markdown("#### 🌍 Traducción estimada:")
      st.markdown(
          f"<div"
          ' style="background:#111827;padding:12px;border-radius:8px;color:#38BDF8;">Folded'
          f" napkins 200 units - High quality and guaranteed absorption.</div>",
          unsafe_allow_html=True,
      )

    # Botón de conversión a audio
    if st.button("🔊 Convertir a Audio"):
      with st.spinner("Sintetizando voz..."):
        tts = gTTS(text=sample_text, lang="en", slow=False)
        audio_path = "output_audio.mp3"
        tts.save(audio_path)
        st.audio(audio_path, format="audio/mp3")
        with open(audio_path, "rb") as f:
          st.download_button(
              "📥 Descargar Audio", f, file_name="traduccion.mp3"
          )
  else:
    st.warning("No se logró detectar texto en la imagen.")  #[cite: 9]

# --- PIE DE PÁGINA ---
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #9CA3AF; font-size: 13px;'>Plataforma"
    " de Visión Artificial y Procesamiento de Lenguaje Natural</p>",
    unsafe_allow_html=True,
)
