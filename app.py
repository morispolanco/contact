import streamlit as st
import requests
import pandas as pd
import json
import re

def extract_names_and_phones(text):
    api_key = st.secrets["OPENROUTER_API_KEY"]
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    prompt = f"""
    Extract names and phone numbers from the following text:
    {text}
    Return the result as a JSON list with keys 'name' and 'phone'. If no phone number is found, use 'N/A'.
    """
    
    data = {
        "model": "deepseek/deepseek-r1:free",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        response_data = response.json()
        try:
            extracted_data = json.loads(response_data["choices"][0]["message"]["content"])
            return extracted_data
        except (KeyError, IndexError, json.JSONDecodeError):
            return []
    else:
        st.error(f"Error: {response.status_code} - {response.text}")
        return []

st.title("Extracción de Nombres y Teléfonos")

texto_usuario = st.text_area("Ingrese el texto del cual desea extraer nombres y teléfonos:")

if st.button("Extraer Datos"):
    if texto_usuario:
        resultados = extract_names_and_phones(texto_usuario)
        if resultados:
            df = pd.DataFrame(resultados)
            st.write("### Datos Extraídos")
            st.dataframe(df)
            
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Descargar CSV",
                data=csv,
                file_name="nombres_telefonos.csv",
                mime="text/csv"
            )
        else:
            st.warning("No se encontraron nombres ni números de teléfono en el texto proporcionado.")
    else:
        st.warning("Por favor, ingrese un texto antes de extraer los datos.")
