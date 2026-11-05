import os
import easyocr
import numpy as np
from PIL import Image
import streamlit as st
from gtts import gTTS

# Configuración de la página
st.set_page_config(
    page_title="OCR y Traductor en Tiempo Real", page_icon="📷", layout="wide"
)

# --- ESTILOS CSS ---
st.markdown(
    """
    <style>
    .main { background-color: #0B0F19; }
    .stSidebar { background-color: #111827 !important; }
    .header-title { color: #38BDF8; font-weight: 800; font-size: 2rem; }
    .stButton>button {
        background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%);
        color: white; font-weight: bold; border-radius: 8px; border: none;
        padding: 10px 20px; width: 100%;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# Cargar el lector de EasyOCR en caché para optimizar velocidad
@st.cache_resource
def load_ocr_reader():
  # Soporta español e inglés por defecto
  return easyocr.Reader(["es", "en"], gpu=False)


with st.spinner("Inicializando motor OCR..."):
  reader = load_ocr_reader()

# --- BARRA LATERAL: CONFIGURACIÓN ---
st.sidebar.markdown("### ⚙️ Configuración")
st.sidebar.markdown("---")
invert_filter = st.sidebar.checkbox("Aplicar filtro de inversión de color")
source_lang = st.sidebar.selectbox("Idioma de origen (OCR)", ["Español / Inglés"])
target_lang = st.sidebar.selectbox("Idioma de destino (Audio)", ["Español", "Inglés"])
show_audio = st.sidebar.checkbox("Habilitar síntesis de voz", value=True)

# --- CONTENIDO PRINCIPAL ---
st.markdown(
    '<p class="header-title">📷 Lector Óptico Inteligente (OCR en Vivo)</p>',
    unsafe_allow_html=True,
)
st.markdown(
    "Toma una foto con tu cámara o sube una imagen; el sistema detectará y"
    " extraerá automáticamente el texto real que contenga."
)
st.markdown("---")

# Opciones de entrada (Cámara vs Subir Archivo)
tab_cam, tab_upload = st.tabs(["📷 Usar Cámara", "📁 Subir Imagen"])
image = None

with tab_cam:
  cam_file = st.camera_input("Capturar foto en tiempo real")
  if cam_file is not None:
    image = Image.open(cam_file)

with tab_upload:
  uploaded_file = st.file_uploader(
      "Selecciona una imagen (PNG o JPG):", type=["png", "jpg", "jpeg"]
  )
  if uploaded_file is not None:
    image = Image.open(uploaded_file)

# --- VISUALIZACIÓN EN 2 COLUMNAS ---
col1, col2 = st.columns(2)

with col1:
  st.markdown("### 🖼️ Imagen Procesada")
  if image is not None:
    if invert_filter:
      from PIL import ImageOps

      image = ImageOps.invert(image.convert("RGB"))
    st.image(image, use_container_width=True)
  else:
    st.info(
        "Esperando imagen... Usa la pestaña de cámara o sube un archivo para"
        " iniciar."
    )

with col2:
  st.markdown("### 📝 Texto Detectado por OCR")

  if image is not None:
    with st.spinner("Leyendo texto de la imagen..."):
      # Convertir imagen PIL a arreglo numpy para EasyOCR
      img_array = np.array(image)
      results = reader.readtext(img_array)

      # Extraer y concatenar todo el texto encontrado
      extracted_text = " ".join([res[1] for res in results])

    if extracted_text.strip() != "":
      st.success("¡Texto extraído con éxito de la fotografía!")
      user_text = st.text_area(
          "Texto reconocido (Puedes editarlo si es necesario):",
          value=extracted_text,
          height=130,
      )

      # Conversión a Audio si está habilitado
      if show_audio:
        st.markdown("#### 🔊 Reproducción de Voz")
        if st.button("Generar Audio del Texto"):
          with st.spinner("Sintetizando audio..."):
            lang_code = "es" if target_lang == "Español" else "en"
            tts = gTTS(text=user_text, lang=lang_code, slow=False)
            audio_path = "detected_audio.mp3"
            tts.save(audio_path)

            st.audio(audio_path, format="audio/mp3")
            with open(audio_path, "rb") as f:
              st.download_button(
                  "📥 Descargar Audio (.mp3)", f, file_name="texto_capturado.mp3"
              )
    else:
      st.warning(
          "No se detectó texto legible en esta fotografía. Intenta tomar otra"
          " con mejor iluminación o enfoque."
      )
  else:
    st.warning("Ninguna imagen cargada todavía.")

# --- PIE DE PÁGINA ---
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #9CA3AF; font-size: 13px;'>Sistema de"
    " Reconocimiento Óptico conectado en tiempo real</p>",
    unsafe_allow_html=True,
)
