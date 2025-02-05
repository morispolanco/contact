import streamlit as st
import pandas as pd
import re
from io import BytesIO

# Configurar la página de Streamlit
st.set_page_config(page_title="Extractor de Emails", layout="centered")

# Título principal
st.title("📧 Extractor de Emails")

# Agregar instrucciones arriba del cuadro de texto
st.markdown("""
### 🛠️ Instrucciones para encontrar emails en LinkedIn

1️⃣ **Instala la extensión Google 100 Results**  
   - [Descargar aquí](https://chromewebstore.google.com/detail/google-100-results-now-yo/bcolekijhplpbjhepfpbighenphmkegl?hl=en)  
   - Esta extensión permite mostrar hasta 100 resultados en Google, facilitando la búsqueda de correos.  

2️⃣ **Busca en Google lo que te interese.**  
   - Usa palabras clave relacionadas con la profesión o industria que buscas.  

3️⃣ **Cómo encontrar correos electrónicos y teléfonos en LinkedIn**  
   - Usa la siguiente búsqueda en Google para encontrar profesionales con correos públicos de Gmail, Yahoo o Hotmail en un país específico:  
   ```bash
   site:linkedin.com/in ("@gmail.com" OR "@yahoo.com" OR "@hotmail.com") AND "país"
Esto mostrará perfiles de LinkedIn con correos electrónicos visibles en sus perfiles.
4️⃣ Ejemplo de búsqueda para España:

site:linkedin.com/in ("@gmail.com" OR "@yahoo.com" OR "@hotmail.com") AND "España"
🔎 Esto mostrará perfiles de LinkedIn en España que tienen correos electrónicos públicos de Gmail, Yahoo o Hotmail.

5️⃣ Selecciona todo el contenido de la primera página de resultados y pégalo en el cuadro de abajo.

Luego, presiona el botón para extraer los correos electrónicos automáticamente.
""")

#  Función para extraer emails del texto
def extract_emails(text): email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Z|a-z]{2,}\b'

# Extraer y eliminar duplicados
emails = list(set(re.findall(email_pattern, text, re.IGNORECASE)))

# Crear DataFrame con los emails extraídos
return pd.DataFrame({"Email": emails}) if emails else pd.DataFrame(columns=["Email"])
Entrada de texto del usuario
user_text = st.text_area("✍️ Pegue aquí el contenido copiado de los resultados de Google:")

if st.button("🔍 Extraer Emails"): if not user_text.strip(): st.warning("⚠️ Por favor ingrese texto para analizar.") else: # Extraer emails del texto ingresado emails_df = extract_emails(user_text)

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
