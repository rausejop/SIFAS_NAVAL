import streamlit as st
import pandas as pd
import json
import xml.etree.ElementTree as ET
import io
import random
from datetime import datetime
from loguru import logger

# --- 0. Configuración de Logging ---
logger.add("debug.log", rotation="500 MB", level="DEBUG")
logger.info("Aplicación iniciada correctamente.")

# --- 1. Configuración de la Página (Estándar CONFIANZA23) ---
st.set_page_config(
    page_title="Validador SIFAS Naval | CONFIANZA23",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. Estilo CSS Corporativo ---
st.markdown("""
<style>
    /* Fondo principal */
    .main { background-color: #0e1117; }
    
    /* Paneles de métricas */
    .stMetric { 
        background-color: #1f2937; 
        padding: 20px; 
        border-radius: 12px; 
        border: 1px solid #374151; 
        color: #f9fafb !important; 
    }
    .stMetric * { color: #f9fafb !important; }
    
    /* Bordes redondeados para tablas de datos */
    .stDataFrame { border-radius: 12px; overflow: hidden; }
    
    /* Gradientes de color corporativos para cabeceras */
    h1, h2, h3 { 
        background: linear-gradient(90deg, #3b82f6, #8b5cf6); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
    }
</style>
""", unsafe_allow_html=True)

# --- 3. Diseño de la Barra Lateral ---
with st.sidebar:
    # Logo de la empresa
    try:
        st.image("skills/Logo_CONFIANZA23.png", use_container_width=True)
    except:
        st.warning("⚠️ Logo no encontrado en 'skills/Logo_CONFIANZA23.png'")

    st.title("⚙️ Controles de Generación")
    
    # Entradas de Usuario
    num_buques = st.slider("Número de Buques", min_value=1, max_value=100, value=10)
    inicio = st.number_input("ID de Inicio", value=1000)
    fin = st.number_input("ID de Fin", value=2000)
    
    # Botón de Generar
    generate_btn = st.button("🚀 Generar Datos", use_container_width=True)
    
    st.divider()
    
    # Sección Sobre nosotros
    st.markdown("""
    ### 👨‍💻 Sobre esta herramienta
    Herramienta de validación para el sistema **SIFAS Naval**. Permite generar conjuntos de datos sintéticos basados en plantillas oficiales.
    
    Desarrollado por **CONFIANZA23 Inteligencia y Seguridad, S.L.**
    """)
    
    st.info("💡 **Consejo:** Ajusta los IDs para evitar colisiones en la base de datos de validación.")

# --- 4. Diseño del Panel Principal ---
st.title("🚢 Generador de Validación SIFAS Naval")
st.subheader("Generación de registros de buques en base a plantilla técnica")

st.divider()

# --- 5. Lógica de Generación de Datos ---
def load_template():
    logger.info("Intentando cargar plantilla Format.txt")
    try:
        with open("Format.txt", "r", encoding="utf-8") as f:
            data = json.load(f)
            logger.debug("Format.txt cargado con éxito.")
            return data[0] if isinstance(data, list) and len(data) > 0 else data
    except Exception as e:
        logger.error(f"Error crítico al cargar Format.txt: {e}")
        st.error(f"Error al cargar Format.txt: {e}")
        return None

template = load_template()

if "generated_data" not in st.session_state:
    st.session_state.generated_data = None

if generate_btn and template:
    logger.info(f"Iniciando generación de {num_buques} buques.")
    ships = []
    # Definición de rangos realistas (Zona Mediterráneo Central/Oriental)
    lat_min, lat_max = 35.0, 39.0
    lon_min, lon_max = 20.0, 26.0

    for i in range(num_buques):
        try:
            new_ship = template.copy()
            
            # 1. Identificadores (basados en entradas del usuario)
            ship_id = random.randint(int(inicio), int(fin))
            new_ship["SHIP_ID"] = str(ship_id)
            new_ship["MMSI"] = str(random.randint(200000000, 700000000))
            new_ship["IMO"] = str(random.randint(1000000, 9999999))
            
            # 2. Dinámica de Navegación (Rangos reales)
            new_ship["LAT"] = "{:.6f}".format(random.uniform(lat_min, lat_max))
            new_ship["LON"] = "{:.6f}".format(random.uniform(lon_min, lon_max))
            new_ship["SPEED"] = str(random.randint(0, 25))
            new_ship["HEADING"] = str(random.randint(0, 359))
            new_ship["COURSE"] = str(random.randint(0, 359))
            new_ship["ROT"] = str(random.randint(-127, 127))
            new_ship["DRAUGHT"] = str(random.randint(5, 150))
            
            # 3. Estado y Metadatos
            new_ship["STATUS"] = random.choice(["0", "1", "5", "8", "3"])
            new_ship["DSRC"] = random.choice(["TER", "SAT"])
            new_ship["TIMESTAMP"] = datetime.utcnow().isoformat() + "Z"
            
            # 4. Nombres y Banderas (Por variedad)
            new_ship["SHIPNAME"] = random.choice(["OCEAN GUARDIAN", "AQUARIUS", "SEA STAR", "NEPTUNE", "POSEIDON", "MARITIME BOSS"])
            new_ship["FLAG"] = random.choice(["MH", "PA", "LR", "GR", "ES", "MT"])
            
            ships.append(new_ship)
        except Exception as e:
            logger.warning(f"Error generando buque índice {i}: {e}")
    
    st.session_state.generated_data = pd.DataFrame(ships)
    logger.success(f"Generación completada: {len(ships)} buques registrados.")
    st.success(f"✅ Se han generado {num_buques} registros realistas en zona marítima.")

# --- 6. Visualización y Exportación ---
if st.session_state.generated_data is not None:
    df = st.session_state.generated_data
    
    # Métricas
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Buques", len(df))
    col2.metric("Rango IDs", f"{inicio} - {fin}")
    col3.metric("Hora Local", datetime.now().strftime("%H:%M:%S"))
    
    st.divider()
    
    # Tabla de Datos
    st.dataframe(df, use_container_width=True)
    
    st.divider()
    
    # Sección de Exportación
    st.write("### 📥 Exportar Resultados")
    
    # 1. Exportar CSV
    csv = df.to_csv(index=False).encode('utf-8')

    # 2. Exportar Markdown (MD)
    try:
        md = df.to_markdown(index=False).encode('utf-8')
    except ImportError:
        # Fallback si tabulate no está instalado
        md = df.to_csv(index=False, sep="|").encode('utf-8')

    # 3. Exportar XML
    xml_df = df.copy()
    xml_df.columns = [str(c).replace(' ', '_') for c in xml_df.columns]
    xml = xml_df.to_xml(index=False).encode('utf-8')

    # 4. Exportar JSON
    json_data = df.to_json(orient='records', indent=4).encode('utf-8')
    
    # 5. Exportar TXT (Formato personalizado)
    txt_content = df.to_string(index=False).encode('utf-8')

    # Botones Alineados
    exp_col1, exp_col2, exp_col3, exp_col4, exp_col5 = st.columns(5)
    
    file_base = "reporte_val_naval"
    
    exp_col1.download_button("Exportar CSV", data=csv, file_name=f"{file_base}.csv", mime="text/csv", use_container_width=True)
    exp_col2.download_button("Exportar MD", data=md, file_name=f"{file_base}.md", mime="text/markdown", use_container_width=True)
    exp_col3.download_button("Exportar XML", data=xml, file_name=f"{file_base}.xml", mime="application/xml", use_container_width=True)
    exp_col4.download_button("Exportar JSON", data=json_data, file_name=f"{file_base}.json", mime="application/json", use_container_width=True)
    exp_col5.download_button("Exportar TXT", data=txt_content, file_name=f"{file_base}.txt", mime="text/plain", use_container_width=True)

else:
    st.info("🚀 Pulsa el botón 'Generar Datos' en la barra lateral para comenzar.")
    # Imagen decorativa de alta calidad
    st.image("https://images.unsplash.com/photo-1520641321593-9c8646067eb2?q=80&w=2000&auto=format&fit=crop", use_container_width=True)
