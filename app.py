import streamlit as st
import pandas as pd
import re
import requests
from io import BytesIO

# Configurar la página de Streamlit
st.set_page_config(page_title="Extractor de Contactos", layout="centered")

# Función para extraer datos de contacto del texto
def extract_contacts(text):
    # Definir expresiones regulares
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
    name_pattern = r'\b[A-Z][a-z]+\s[A-Z][a-z]+\b'
    
    # Encontrar coincidencias en el texto
    emails = re.findall(email_pattern, text)
    phones = re.findall(phone_pattern, text)
    names = re.findall(name_pattern, text)
    
    # Combinar los resultados en un DataFrame
    # Asumimos que el orden es el mismo para nombres, emails y teléfonos
    # Esto podría no ser cierto en todos los casos, ajusta según sea necesario
    data = {
        'Nombre': names,
        'Email': emails,
        'Teléfono': phones
    }
    return pd.DataFrame(data)

# Interfaz de usuario
st.title("Extractor de Datos de Contacto")
user_text = st.text_area("Ingrese el texto del cual desea extraer contactos:")
if st.button("Extraer Contactos"):
    # Extraer contactos del texto
    contacts_df = extract_contacts(user_text)
    
    # Mostrar los contactos y permitir exportar a Excel
    st.write(contacts_df)
    output = BytesIO()
    contacts_df.to_excel(output, index=False, engine='openpyxl', sheet_name='Contactos')
    st.download_button(
        label="Descargar como Excel",
        data=output.getvalue(),
        file_name='contactos.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
