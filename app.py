import streamlit as st
import pandas as pd
import re
from io import BytesIO

# Configurar la página de Streamlit
st.set_page_config(page_title="Extractor de Emails", layout="centered")

# Función para extraer emails del texto
def extract_emails(text):
    # Expresión regular mejorada para capturar todos los emails posibles
    email_pattern = r'\b[\w._%+-]+@[\w.-]+\.[a-zA-Z]{2,}\b'
    
    # Encontrar coincidencias únicas de emails en el texto
    emails = list(set(re.findall(email_pattern, text, re.IGNORECASE)))
    
    # Convertir a DataFrame
    return pd.DataFrame({'Email': emails})

# Interfaz de usuario en Streamlit
st.title("Extractor de Emails")

# Entrada de texto del usuario
user_text = st.text_area("Ingrese el texto del cual desea extraer emails:")

if st.button("Extraer Emails"):
    # Extraer emails del texto
    emails_df = extract_emails(user_text)
    
    # Mostrar los emails extraídos
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
            file_name='emails.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    else:
        st.warning("No se encontraron correos electrónicos en el texto ingresado.")
