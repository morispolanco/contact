import streamlit as st
import pandas as pd
import re
from io import BytesIO

# Configurar la página de Streamlit
st.set_page_config(page_title="Extractor de Emails", layout="centered")

# Agregar instrucciones en la barra lateral
st.sidebar.title("Instrucciones")
st.sidebar.write("""
### **🛠️ Instrucciones para encontrar emails en LinkedIn**  

1️⃣ **Instala la extensión Google 100 Results**  
   - [Descargar aquí](https://chromewebstore.google.com/detail/google-100-results-now-yo/bcolekijhplpbjhepfpbighenphmkegl?hl=en)  
   - Esta extensión permite mostrar hasta 100 resultados en Google, facilitando la búsqueda de correos.  

2️⃣ **Cómo buscar emails y teléfonos en Google**  
   - Para encontrar correos electrónicos y teléfonos de profesionales en LinkedIn con emails de Gmail, Yahoo o Hotmail en un país específico, usa la siguiente búsqueda en Google:  
site:linkedin.com/in ("@gmail.com" OR "@yahoo.com" OR "@hotmail.com") AND "país"
- Esto mostrará perfiles de LinkedIn con correos electrónicos públicos de los dominios especificados.  

3️⃣ **Ejemplo de búsqueda para España:**  
site:linkedin.com/in ("@gmail.com" OR "@yahoo.com" OR "@hotmail.com") AND "país"

🔎 **Esto mostrará perfiles de LinkedIn en España que tienen correos electrónicos públicos de Gmail, Yahoo o Hotmail.**
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
