import streamlit as st
import spacy
import pandas as pd
from io import BytesIO

# Cargar el modelo de SpaCy
nlp = spacy.load("en_core_web_sm")

# Función para exportar resultados a CSV
def export_to_csv(entities, pos_tags, noun_chunks):
    # Crear un DataFrame para cada sección
    df_entities = pd.DataFrame(entities, columns=["Texto", "Etiqueta", "Descripción"])
    df_pos_tags = pd.DataFrame(pos_tags, columns=["Texto", "Parte del discurso (POS)", "Descripción"])
    df_noun_chunks = pd.DataFrame(noun_chunks, columns=["Frase nominal"])

    # Escribir cada DataFrame a un solo archivo CSV con secciones
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_entities.to_excel(writer, sheet_name="Entidades nombradas", index=False)
        df_pos_tags.to_excel(writer, sheet_name="POS", index=False)
        df_noun_chunks.to_excel(writer, sheet_name="Frases nominales", index=False)
    
    output.seek(0)
    return output

# Título de la aplicación
st.title("Extractor de Información con SpaCy")

# Campo de entrada de texto
text_input = st.text_area("Introduce el texto para analizar:", height=200)

# Botón para procesar el texto
if st.button("Extraer información"):
    if text_input:
        # Procesar el texto con SpaCy
        doc = nlp(text_input)

        # Extracción de entidades nombradas
        st.subheader("Entidades nombradas")
        entities = []
        if doc.ents:
            for ent in doc.ents:
                entity_info = (ent.text, ent.label_, spacy.explain(ent.label_))
                entities.append(entity_info)
                st.write(f"**{ent.text}** ({ent.label_}) - {spacy.explain(ent.label_)}")
        else:
            st.write("No se encontraron entidades nombradas.")

        # Extracción de las partes del discurso (POS)
        st.subheader("Partes del discurso")
        pos_tags = []
        for token in doc:
            pos_info = (token.text, token.pos_, spacy.explain(token.pos_))
            pos_tags.append(pos_info)
            st.write(f"**{token.text}** - {token.pos_} ({spacy.explain(token.pos_)})")

        # Extracción de frases nominales
        st.subheader("Frases nominales")
        noun_chunks = []
        for chunk in doc.noun_chunks:
            noun_chunks.append((chunk.text,))
            st.write(f"- {chunk.text}")

        # Exportar resultados a CSV
        st.subheader("Exportar resultados")
        output = export_to_csv(entities, pos_tags, noun_chunks)
        st.download_button(
            label="Descargar resultados como CSV",
            data=output,
            file_name="resultados_spacy.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("Por favor, introduce un texto para analizar.")
