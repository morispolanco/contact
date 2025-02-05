import streamlit as st
import pandas as pd
import re
from io import BytesIO

# Configurar la página de Streamlit
st.set_page_config(page_title="Extractor de Emails", layout="centered")

# Agregar instrucciones en la barra lateral
st.sidebar.title("Instrucciones")
st.sidebar.write("""
Especifica el dominio de LinkedIn: Usa site:linkedin.com para limitar la búsqueda a LinkedIn.

Incluye palabras clave relacionadas con el profesional: Por ejemplo, "CEO", "ingeniero", "diseñador", etc.

Agrega los dominios de correo electrónico: Usa @gmail.com, @yahoo.com, o @hotmail.com para filtrar correos específicos.

Especifica el país: Usa intitle:[país] o intext:[país] para limitar la búsqueda a un país en particular.

Busca números de teléfono: Usa términos como "teléfono", "contacto", o "número" para encontrar información de contacto.

Combina los operadores: Usa comillas (" ") para frases exactas y el signo OR para incluir múltiples opciones.

Ejemplo de búsqueda:
Si quieres encontrar correos y teléfonos de ingenieros en LinkedIn que tengan cuentas de Gmail, Yahoo o Hotmail en México, puedes escribir lo siguiente en Google:

site:linkedin.com intitle:"ingeniero" ("@gmail.com" OR "@yahoo.com" OR "@hotmail.com") intext:"México" ("teléfono" OR "contacto")
""")

# Función para extraer emails del texto
def extract_emails(text):
 email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
 
 # Extraer y eliminar duplicados
 emails = list(set(re.findall(email_pattern, text, re.IGNORECASE)))
 
 # Crear DataFrame con los emails extraídos
 return pd.DataFrame({"Email": emails}) if emails else pd.DataFrame(columns=["Email"])

# Interfaz de usuario en Streamlit
st.title("📧 Extractor de Emails")

# Entrada de texto del usuario
user_text = st.text_area("Ingrese el texto del cual desea extraer emails:")

if st.button("🔍 Extraer Emails"):
 if not user_text.strip():
     st.warning("⚠️ Por favor ingrese texto para analizar.")
 else:
     # Extraer emails del texto ingresado
     emails_df = extract_emails(user_text)
     
     if not emails_df.empty:
         st.success(f"✅ Se encontraron {len(emails_df)} correos electrónicos únicos.")
         st.dataframe(emails_df)

         # Guardar los emails en un archivo Excel
         output = BytesIO()
         with pd.ExcelWriter(output, engine='openpyxl') as writer:
             emails_df.to_excel(writer, index=False, sheet_name='Emails')
         output.seek(0)

         # Botón para descargar el archivo
         st.download_button(
             label="⬇️ Descargar como Excel",
             data=output,
             file_name="emails_extraidos.xlsx",
             mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
         )
     else:
         st.warning("❌ No se encontraron correos electrónicos en el texto ingresado.")
