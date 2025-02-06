import streamlit as st
import pandas as pd
import re
from io import BytesIO

# Configuración de la página de Streamlit
st.set_page_config(page_title="Extractor de Contactos", layout="wide")

# Título principal
st.title("📧 Extractor de Contactos (Emails, Teléfonos y Más)")

# Instrucciones en la barra lateral
with st.sidebar:
    st.header("🛠️ Instrucciones")
    st.markdown("""
    1️⃣ **Instala la extensión Google 100 Results**  
       - [Descargar aquí](https://chromewebstore.google.com/detail/google-100-results-now-yo/bcolekijhplpbjhepfpbighenphmkegl?hl=en)  
       - Esto ayuda a encontrar más datos en Google.

    2️⃣ **Busca en Google o LinkedIn usando estos formatos:**  
       ```bash
       site:linkedin.com/in ("@gmail.com" OR "@yahoo.com" OR "@hotmail.com") AND "país"
       ```

    3️⃣ **Copia y pega los resultados en el cuadro de texto**  

    4️⃣ **Presiona el botón para extraer los datos automáticamente.**  
    """)

# Expresiones regulares
EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
PHONE_REGEX = r'\+?\d{1,4}[-.\s]?\(?\d{2,5}\)?[-.\s]?\d{3,5}[-.\s]?\d{3,5}'

# Función para extraer datos
def extract_contacts(text):
    emails = re.findall(EMAIL_REGEX, text, re.IGNORECASE)
    phones = re.findall(PHONE_REGEX, text)
    emails = sorted(set(emails))  # Eliminar duplicados y ordenar
    phones = sorted(set(phones))

    contacts = []
    for email in emails:
        name = ""  # Se puede mejorar si hay más estructura en el texto
        domain = email.split("@")[-1]
        company = domain.split(".")[0]  # Suponer que la empresa es el dominio del correo
        position = ""  # Sin datos estructurados de LinkedIn, es difícil extraer esto
        
        contacts.append({"Nombre": name, "Empresa": company, "Puesto": position, "Email": email})

    # Añadir teléfonos como filas separadas
    for phone in phones:
        contacts.append({"Nombre": "", "Empresa": "", "Puesto": "", "Email": "", "Teléfono": phone})

    return pd.DataFrame(contacts)

# Función para convertir a Excel
def convert_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Contactos')
    output.seek(0)
    return output

# Función principal
def main():
    user_text = st.text_area("✍️ Pegue aquí el contenido copiado de los resultados de Google o LinkedIn:", height=250)

    if st.button("🔍 Extraer Contactos"):
        if not user_text.strip():
            st.warning("⚠️ Por favor ingrese texto para analizar.")
        else:
            try:
                contacts_df = extract_contacts(user_text)

                if not contacts_df.empty:
                    st.success(f"✅ Se encontraron {len(contacts_df)} contactos únicos.")

                    # Mostrar tabla con resultados
                    st.dataframe(contacts_df, use_container_width=True)

                    # Descargas en Excel y CSV
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
