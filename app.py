import streamlit as st
import pandas as pd
from api_client import obtener_clima_api

st.set_page_config(page_title="Clima API", layout="wide")

st.title("Consulta del Clima")
st.write("Aplicación sencilla en Streamlit que consume la API pública de Open-Meteo.")

ciudades = {
    "Tegucigalpa": (14.0818, -87.2068),
    "San Pedro Sula": (15.5042, -88.0250),
    "Villanueva": (15.3167, -88.0000),
    "La Ceiba": (15.7835, -86.7930),
    "Choluteca": (13.3000, -87.1833)
}

# Menú lateral
st.sidebar.title("Menú")
st.sidebar.write("Seleccione una ciudad para consultar el clima.")

ciudad = st.sidebar.selectbox(
    "Ciudad",
    list(ciudades.keys())
)

latitud, longitud = ciudades[ciudad]

if st.sidebar.button("Consultar clima"):

    datos = obtener_clima_api(latitud, longitud)

    if datos:
        actual = datos["current"]

        st.success(f"Clima actual de {ciudad}")

        col1, col2, col3 = st.columns(3)

        col1.metric("Temperatura", f"{actual['temperature_2m']} °C")
        col2.metric("Humedad", f"{actual['relative_humidity_2m']} %")
        col3.metric("Viento", f"{actual['wind_speed_10m']} km/h")

        st.subheader("Pronóstico por hora")

        df = pd.DataFrame({
            "Hora": datos["hourly"]["time"][:24],
            "Temperatura (°C)": datos["hourly"]["temperature_2m"][:24],
            "Humedad (%)": datos["hourly"]["relative_humidity_2m"][:24],
            "Viento (km/h)": datos["hourly"]["wind_speed_10m"][:24]
        })

        st.dataframe(df, use_container_width=True)

        st.subheader("Gráfico de temperatura")

        st.line_chart(df.set_index("Hora")["Temperatura (°C)"])

    else:
        st.error("No se pudo obtener información del clima.")
