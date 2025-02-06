import streamlit as st
import pandas as pd
import re
from io import BytesIO

# Configurar la página de Streamlit
st.set_page_config(page_title="Extractor de Emails", layout="wide")

# Título principal
st.title("📧 Extractor de Emails")

# Instrucciones en la barra lateral
with st.sidebar:
    st.header("🛠️ Instrucciones")
    st.markdown("""
    1️⃣ **Instala la extensión Google 100 Results**  
       - [Descargar aquí](https://chromewebstore.google.com/detail/google-100-results-now-yo/bcolekijhplpbjhepfpbighenphmkegl?hl=en)  
       - Esta extensión permite mostrar hasta 100 resultados en Google, facilitando la búsqueda de correos.  

    2️⃣ **Busca en Google lo que te interese.**  
       - Usa palabras clave relacionadas con la profesión o industria que buscas.  

    3️⃣ **Cómo encontrar correos electrónicos y teléfonos en LinkedIn**  
       - Usa la siguiente búsqueda en Google para encontrar profesionales con correos públicos de Gmail, Yahoo o Hotmail en un país específico:  
       ```bash
       site:linkedin.com/in ("@gmail.com" OR "@yahoo.com" OR "@hotmail.com") AND "país"
       ```
    4️⃣ **Ejemplo de búsqueda para España:**  
       ```bash
       site:linkedin.com/in ("@gmail.com" OR "@yahoo.com" OR "@hotmail.com") AND "España"
       ```  
       🔎 Esto mostrará perfiles de LinkedIn en España que tienen correos electrónicos públicos de Gmail, Yahoo o Hotmail.

    5️⃣ **Selecciona todo el contenido de la primera página de resultados y pégalo en el cuadro de texto.**

    Luego, presiona el botón para extraer los correos electrónicos automáticamente.
    """)

# Función para extraer emails del texto
def extract_emails(text):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return list(set(re.findall(email_pattern, text, re.IGNORECASE)))

# Función principal para procesar la entrada del usuario
def main():
    # Entrada de texto del usuario
    user_text = st.text_area("✍️ Pegue aquí el contenido copiado de los resultados de Google:", height=200)

    if st.button("🔍 Extraer Emails"):
        if not user_text.strip():
            st.warning("⚠️ Por favor ingrese texto para analizar.")
        else:
            try:
                # Extraer emails del texto ingresado
                emails = extract_emails(user_text)

                if emails:
                    emails_df = pd.DataFrame({"Email": emails})
                    st.success(f"✅ Se encontraron {len(emails)} correos electrónicos únicos.")

                    # Mostrar todos los resultados sin truncamiento
                    st.dataframe(emails_df, use_container_width=True, height=min(400, len(emails) * 35))

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
            except Exception as e:
                st.error(f"⚠️ Ocurrió un error al procesar el texto: {str(e)}")

if __name__ == "__main__":
    main()
