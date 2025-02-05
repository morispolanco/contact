import streamlit as st
import pandas as pd
import requests
import json
import io

def extraer_info_contacto(texto, api_key):
    url = "https://openrouter.ai/api/v1/chat/completions"
    encabezados = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    datos = {
        "model": "amazon/nova-lite-v1",
        "messages": [
            {"role": "user", "content": f"Extrae solo nombres y números de tel. del siguiente texto y preséntalos en formato JSON: {texto}"}
        ]
    }
    
    respuesta = requests.post(url, headers=encabezados, data=json.dumps(datos))
    
    if respuesta.status_code == 200:
        resultado = respuesta.json()
        contenido = resultado.get("choices", [{}])[0].get("message", {}).get("content", "{}")
        try:
            datos_contacto = json.loads(contenido)
            return datos_contacto
        except json.JSONDecodeError:
            return []
    else:
        st.error("Error al obtener datos de la API de OpenRouter")
        return []

st.title("Extracción de Información de Contacto")

api_key = st.secrets["OPENROUTER_API_KEY"]

texto_entrada = st.text_area("Introduce el texto para extraer la información de contacto:")

if st.button("Extraer Contactos"):
    if texto_entrada:
        lista_contactos = extraer_info_contacto(texto_entrada, api_key)
        if lista_contactos:
            df = pd.DataFrame(lista_contactos, columns=["nombre", "tel."])
            st.write("### Información de Contacto Extraída")
            st.dataframe(df)
            
            # Descargar CSV
            buffer_csv = io.StringIO()
            df.to_csv(buffer_csv, index=False)
            buffer_csv.seek(0)
            st.download_button(
                label="Descargar CSV",
                data=buffer_csv.getvalue(),
                file_name="informacion_contacto.csv",
                mime="text/csv"
            )
        else:
            st.warning("No se encontró información de contacto en el texto proporcionado.")
    else:
        st.warning("Por favor, introduce un texto antes de extraer los contactos.")
