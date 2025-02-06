import streamlit as st
import pandas as pd
import re
import requests
import json
from io import BytesIO

# Cargar API Key desde los secretos de Streamlit
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]

# Configurar la página de Streamlit
st.set_page_config(page_title="Extractor de Contactos con IA", layout="wide")

# Título de la aplicación
st.title("📧 Extractor de Contactos con IA")

# Instrucciones en la barra lateral
with st.sidebar:
    st.header("🛠️ Instrucciones")
    st.markdown("""
    1️⃣ **Busca en Google o LinkedIn los contactos**  
    2️⃣ **Copia y pega los datos en el cuadro de texto**  
    3️⃣ **Presiona el botón para extraer emails, teléfonos y mejorar la información con IA**  
    """)

# Expresiones regulares para detección
EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
PHONE_REGEX = r'\+?\d{1,4}[-.\s]?\(?\d{2,5}\)?[-.\s]?\d{3,5}[-.\s]?\d{3,5}'

# Función para consultar OpenRouter y obtener nombre, empresa y puesto
def get_info_from_ai(email):
    domain = email.split("@")[-1]
    prompt = f"""
    Given the email domain '{domain}', provide:
    1. A likely company name
    2. A common job title associated with this domain
    3. A probable name structure (e.g., John Doe)
    """

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENROUTER_API_KEY}"
    }

    payload = {
        "model": "deepseek/deepseek-r1-distill-llama-70b:free",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        result = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        info = result.split("\n")[:3]  # Extraer nombre, empresa y puesto sugeridos
        return info if len(info) == 3 else ["Desconocido", "Desconocido", "Desconocido"]
    else:
        return ["Desconocido", "Desconocido", "Desconocido"]

# Función para extraer datos del texto
def extract_contacts(text):
    emails = sorted(set(re.findall(EMAIL_REGEX, text, re.IGNORECASE)))
    phones = sorted(set(re.findall(PHONE_REGEX, text)))

    contacts = []
    for email in emails:
        name, company, position = get_info_from_ai(email)
        contacts.append({"Nombre": name, "Empresa": company, "Puesto": position, "Email": email, "Teléfono": ""})

    for phone in phones:
        contacts.append({"Nombre": "", "Empresa": "", "Puesto": "", "Email": "", "Teléfono": phone})

    return pd.DataFrame(contacts)

# Función para exportar los datos en Excel
def convert_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Contactos')
    output.seek(0)
    return output

# Interfaz principal
def main():
    user_text = st.text_area("✍️ Pega aquí los datos extraídos de LinkedIn o Google:", height=250)

    if st.button("🔍 Extraer Contactos con IA"):
        if not user_text.strip():
            st.warning("⚠️ Por favor ingrese texto para analizar.")
        else:
            try:
                contacts_df = extract_contacts(user_text)

                if not contacts_df.empty:
                    st.success(f"✅ Se encontraron {len(contacts_df)} contactos únicos.")

                    # Mostrar tabla con los datos extraídos
                    st.dataframe(contacts_df, use_container_width=True)

                    # Generar archivos de descarga
                    excel_file = convert_to_excel(contacts_df)
                    csv_file = contacts_df.to_csv(index=False).encode("utf-8")

                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            label="⬇️ Descargar como Excel",
                            data=excel_file,
                            file_name="contactos_extraidos.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                    with col2:
                        st.download_button(
                            label="⬇️ Descargar como CSV",
                            data=csv_file,
                            file_name="contactos_extraidos.csv",
                            mime="text/csv"
                        )
                else:
                    st.warning("❌ No se encontraron contactos en el texto ingresado.")
            except Exception as e:
                st.error(f"⚠️ Ocurrió un error: {str(e)}")

if __name__ == "__main__":
    main()
