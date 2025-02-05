import streamlit as st
import pandas as pd
import requests
import json
import io

def extract_contact_info(text, api_key):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "openai/o1",
        "messages": [
            {"role": "user", "content": f"Extract only names and phone numbers from the following text and present it in JSON format: {text}"}
        ]
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        result = response.json()
        content = result.get("choices", [{}])[0].get("message", {}).get("content", "{}")
        try:
            contact_data = json.loads(content)
            return contact_data
        except json.JSONDecodeError:
            return []
    else:
        st.error("Error fetching data from OpenRouter API")
        return []

st.title("Extracción de Información de Contacto")

api_key = st.secrets["OPENROUTER_API_KEY"]

text_input = st.text_area("Introduce el texto para extraer la información de contacto:")

if st.button("Extraer Contactos"):
    if text_input:
        contact_list = extract_contact_info(text_input, api_key)
        if contact_list:
            df = pd.DataFrame(contact_list, columns=["name", "phone"])
            st.write("### Información de Contacto Extraída")
            st.dataframe(df)
            
            # Descargar CSV
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            csv_buffer.seek(0)
            st.download_button(
                label="Descargar CSV",
                data=csv_buffer.getvalue(),
                file_name="contact_info.csv",
                mime="text/csv"
            )
        else:
            st.warning("No se encontró información de contacto en el texto proporcionado.")
    else:
        st.warning("Por favor, introduce un texto antes de extraer los contactos.")
