import streamlit as st
import matplotlib.pyplot as plt
from fpdf import FPDF
import io

# Configuración inicial
st.set_page_config(page_title="Calculadora de Flete PRO", layout="centered")
st.title("📦 Calculadora de Flete (Triangulación vs Directo)")

# Inicializar historial
if "historial" not in st.session_state:
    st.session_state["historial"] = []

# --- Entradas generales ---
st.header("Datos de las Cajas")
col1, col2 = st.columns(2)
with col1:
    largo = st.number_input("Largo", min_value=0.0, value=44.0)
    ancho = st.number_input("Ancho", min_value=0.0, value=37.0)
    alto = st.number_input("Alto", min_value=0.0, value=44.0)
with col2:
    unidad_medida = st.selectbox("Unidad de Medida", ["cm", "m", "inches"], index=0)
    cantidad = st.number_input("Cantidad de cajas", min_value=1, step=1, value=2)

# Conversión a cm
if unidad_medida == "m":
    largo *= 100
    ancho *= 100
    alto *= 100
elif unidad_medida == "inches":
    largo *= 2.54
    ancho *= 2.54
    alto *= 2.54

# Cálculo de volumen
volumen_caja_cm3 = largo * ancho * alto
volumen_total_cm3 = volumen_caja_cm3 * cantidad
cbm_total = volumen_total_cm3 / 1_000_000
ft3_total = volumen_total_cm3 / 28_316.8466

# Mostrar datos calculados
st.subheader("📐 Volumen calculado")
st.info(f"CBM Total: {cbm_total:.4f} m³ | ft³ Total: {ft3_total:.4f}")

# --- Sección Triangulación ---
st.markdown("### ✈️ Ruta Triangulación (China → USA → VE)")
col3, col4 = st.columns(2)
with col3:
    ddp = st.number_input("Costo DDP (China → USA)", min_value=0.0, value=456.0)
with col4:
    tarifa_usa = st.number_input("Tarifa USA → Venezuela (USD por ft³)", min_value=0.0, value=34.0)

costo_usa = ft3_total * tarifa_usa
costo_triangulacion = ddp + costo_usa

st.success(f"**Costo USA → VE:** ${costo_usa:.2f}")
st.success(f"**Costo Total Triangulación:** ${costo_triangulacion:.2f}")

# --- Sección Directo ---
st.markdown("### 🚢 Ruta Directa (China → VE)")
tarifa_china = st.number_input("Tarifa China → VE (USD por CBM)", min_value=0.0, value=850.0)
costo_directo = cbm_total * tarifa_china

st.success(f"**Costo Total Directo:** ${costo_directo:.2f}")

# --- Comparación ---
st.markdown("---")
st.subheader("📊 Comparación de Rutas")
data = {"Triangulación": costo_triangulacion, "Directo": costo_directo}
st.write(data)

# Gráfico comparativo
fig, ax = plt.subplots()
ax.bar(data.keys(), data.values(), color=["#4CAF50", "#2196F3"])
ax.set_ylabel("Costo (USD)")
ax.set_title("Comparación de Costos")
st.pyplot(fig)

# --- Guardar en historial ---
if st.button("Guardar en historial"):
    st.session_state["historial"].append({
        "Dimensiones": f"{largo}x{ancho}x{alto} cm",
        "Cantidad": cantidad,
        "CBM Total": round(cbm_total, 4),
        "ft³ Total": round(ft3_total, 4),
        "Costo Triangulación": round(costo_triangulacion, 2),
        "Costo Directo": round(costo_directo, 2)
    })
    st.success("Guardado en historial")

# --- Mostrar historial ---
if st.session_state["historial"]:
    st.subheader("📜 Historial de Cálculos")
    for i, item in enumerate(st.session_state["historial"], start=1):
        st.write(f"**Cálculo {i}:** {item}")

# --- Exportar a PDF como descarga ---
def generar_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Reporte de Flete", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, f"Dimensiones: {largo}x{ancho}x{alto} cm", ln=True)
    pdf.cell(200, 10, f"Cantidad: {cantidad}", ln=True)
    pdf.cell(200, 10, f"CBM Total: {cbm_total:.4f}", ln=True)
    pdf.cell(200, 10, f"ft³ Total: {ft3_total:.4f}", ln=True)
    pdf.ln(10)
    pdf.cell(200, 10, f"Costo Triangulación: ${costo_triangulacion:.2f}", ln=True)
    pdf.cell(200, 10, f"Costo Directo: ${costo_directo:.2f}", ln=True)

    # Generar PDF como bytes usando dest='S'
    pdf_bytes = pdf.output(dest='S')
    return pdf_bytes

pdf_bytes = generar_pdf()
st.download_button(
    label="📥 Descargar Reporte en PDF",
    data=pdf_bytes,
    file_name="reporte_flete.pdf",
    mime="application/pdf"
)

# --- Botón Reiniciar ---
if st.button("🔄 Reiniciar"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()
