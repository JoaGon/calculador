import streamlit as st

# --- Título ---
st.title("Calculadora de Flete por Volumen 📦")

# --- Entradas ---
st.header("Datos de la Caja")

largo = st.number_input("Largo", min_value=0.0, format="%.2f")
ancho = st.number_input("Ancho", min_value=0.0, format="%.2f")
alto = st.number_input("Alto", min_value=0.0, format="%.2f")
unidad_medida = st.selectbox("Unidad de Medida", ["cm", "m", "inches"])
cantidad = st.number_input("Cantidad de cajas", min_value=1, step=1)

# --- Selección de unidad de conversión ---
st.header("Conversión y costo")
tipo_resultado = st.radio("¿En qué medida quieres el resultado?", ["CBM (m³)", "ft³"])
tarifa = st.number_input(f"Tarifa por {tipo_resultado}", min_value=0.0, format="%.2f")

# --- Conversión a cm ---
if unidad_medida == "m":
    largo *= 100
    ancho *= 100
    alto *= 100
elif unidad_medida == "inches":
    largo *= 2.54
    ancho *= 2.54
    alto *= 2.54

# --- Cálculo ---
volumen_total_cm3 = (largo * ancho * alto) * cantidad
volumen_caja_cm3 = largo * ancho * alto

if tipo_resultado == "CBM (m³)":
    volumen_caja = volumen_caja_cm3 / 1_000_000
    volumen_total = volumen_total_cm3 / 1_000_000
else:
    volumen_caja = volumen_caja_cm3 / 28_316.8466
    volumen_total = volumen_total_cm3 / 28_316.8466

# --- Costo total ---
costo_total = volumen_total * tarifa

# --- Resultados ---
st.subheader("Resultados")
st.write(f"Volumen por caja: **{volumen_caja:.4f} {tipo_resultado}**")
st.write(f"Volumen total ({cantidad} cajas): **{volumen_total:.4f} {tipo_resultado}**")
st.write(f"Costo total del flete: **${costo_total:,.2f} USD**")

# --- Botón para reiniciar ---
if st.button("Reiniciar"):
    st.experimental_rerun()
