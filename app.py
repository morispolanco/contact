import streamlit as st
import pandas as pd
import re
from io import BytesIO

# Configurar la página de Streamlit
st.set_page_config(page_title="Extractor de Emails", layout="centered")

# Función para extraer emails del texto
def extract_emails(text):
    # Definir la expresión regular para emails
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    
    # Encontrar coincidencias de emails en el texto
    emails = re.findall(email_pattern, text, re.IGNORECASE)  # Añadir re.IGNORECASE para ignorar mayúsculas/minúsculas
    
    # Combinar los resultados en un DataFrame
    data = {
        'Email': emails
    }
    return pd.DataFrame(data)

# Interfaz de usuario
st.title("Extractor de Emails")
user_text = st.text_area("Ingrese el texto del cual desea extraer emails:")
if st.button("Extraer Emails"):
    # Extraer emails del texto
    emails_df = extract_emails(user_text)
    
    # Mostrar los emails y permitir exportar a Excel
    st.write(emails_df)
    output = BytesIO()
    emails_df.to_excel(output, index=False, engine='openpyxl', sheet_name='Emails')
    st.download_button(
        label="Descargar como Excel",
        data=output.getvalue(),
        file_name='emails.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
