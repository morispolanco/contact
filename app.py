import streamlit as st
import pandas as pd
import re
from io import BytesIO

# Configurar la página de Streamlit
st.set_page_config(page_title="Extractor de Emails", layout="centered")

# Función para extraer emails del texto
def extract_emails(text):
    email_pattern = r'\b[\w._%+-]+@[\w.-]+\.[a-zA-Z]{2,}\b'
    
    # Extrae todos los correos encontrados (sin duplicados)
    emails = re.findall(email_pattern, text, re.IGNORECASE)
    
    # Verificar si se encontraron correos
    if not emails:
        return pd.DataFrame(columns=["Email"])
    
    return pd.DataFrame({"Email": emails})

# Interfaz de usuario en Streamlit
st.title("Extractor de Emails")

# Entrada de texto del usuario
user_text = st.text_area("Ingrese el texto del cual desea extraer emails:")

if st.button("Extraer Emails"):
    # Extraer emails del texto ingresado
    emails_df = extract_emails(user_text)
    
    # Verificar si se extrajeron correos
    if not emails_df.empty:
        st.write("### Correos extraídos:")
        st.dataframe(emails_df)

        # Guardar los emails en un archivo Excel
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            emails_df.to_excel(writer, index=False, sheet_name='Emails')
        output.seek(0)

        # Botón para descargar el archivo
        st.download_button(
            label="Descargar como Excel",
            data=output,
            file_name="emails.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("No se encontraron correos electrónicos en el texto ingresado.")
