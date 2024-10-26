import os
import logging
from typing import Dict, List, Optional
import ollama
import PyPDF2
import pandas as pd
import streamlit as st
from io import BytesIO
from info_fields import info_fields
from streamlit import session_state as ss


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
OLLAMA_MODEL = "llama3.2"
OUTPUT_FILENAME = "extraction_infos_pdf.xlsx"

class MedicalInfoExtractor:
    def __init__(self):
        # Load fields from a separate configuration
        self.info_fields = self._load_medical_fields()
        
    @staticmethod
    def _load_medical_fields() -> List[str]:
        """Load the list of medical fields to extract."""
        return info_fields

    @staticmethod
    def extract_text_from_pdf(file) -> Optional[str]:
        """Extract text from a PDF file."""
        try:
            reader = PyPDF2.PdfReader(file)
            text = []
            for page in reader.pages:
                text.append(page.extract_text())
            return "\n".join(text)
        except Exception as e:
            logger.error(f"Error extracting PDF text: {str(e)}")
            return None

    def extract_info_with_ollama(self, text: str, field: str) -> str:
        """Extract specific information using Ollama model."""
        try:
            prompt = f"""            
            Voici un rapport médical hospitalier détaillé contenant des informations démographiques, biologiques, et des antécédents médicaux : \n{text}\n

            Extrait uniquement la valeur brute pour le champ ci-dessous. Répond uniquement avec la donnée sans ajouter de texte supplémentaire ou de phrase explicative. Si la donnée n'est pas trouvée, indique "Non renseigné".

            Champ demandé : '{field}'
            """
            
            response = ollama.generate(
                model=OLLAMA_MODEL,
                prompt=prompt,
                options={
                    "temperature": 0.1,  # Lower temperature for more focused responses
                    "top_p": 0.9
                }
            )
            return response.get("response", "").strip()
        except Exception as e:
            logger.error(f"Error in Ollama extraction for field {field}: {str(e)}")
            return ""

    def process_pdf(self, pdf_file) -> Optional[pd.DataFrame]:
        """Process PDF and extract all required information."""
        pdf_text = self.extract_text_from_pdf(pdf_file)
        if not pdf_text:
            return None

        data = {}
        total_fields = len(self.info_fields)
        
        progress_bar = st.progress(0)
        status_text = st.empty()

        for index, field in enumerate(self.info_fields, 1):
            try:
                status_text.text(f"Extraction du champ {index}/{total_fields}: {field}")
                data[field] = self.extract_info_with_ollama(pdf_text, field)
                progress_bar.progress(index / total_fields)
            except Exception as e:
                logger.error(f"Error processing field {field}: {str(e)}")
                data[field] = ""

        status_text.empty()
        progress_bar.empty()
        
        return pd.DataFrame([data])

    
def main():
    st.set_page_config(
        page_title="Apothicare - Extraction d'informations médicales depuis PDF",
        page_icon="./assets/logo.png",
        layout="wide"
    )


    page_bg_img = '''
                <style>
                .stApp {
                    background-image: url("data:image/png;base64,%s");
                    background-size: cover;
                    background-repeat: no-repeat;
                    background-position: center 50px;                
                    }
                </style>
                '''
    import base64
    with open("./assets/background.png", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

    # Appliquer le CSS personnalisé
    st.markdown(page_bg_img % encoded_string, unsafe_allow_html=True)

    st.title("Extraction d'informations médicales depuis PDF")
    st.header("Instructions")
    st.markdown("""
    1. Importer un fichier PDF contenant des informations médicales
    2. Cliquez sur le bouton d'extraction
    3. Téléchargez le fichier Excel généré
    """)

    extractor = MedicalInfoExtractor()
    
    pdf_file = st.file_uploader(
        "Téléchargez un fichier PDF",
        type=["pdf"],
        help="Sélectionnez un fichier PDF contenant le rapport médical",
        key="pdf"
    )

    col1, col2, col3 = st.columns(3) # Colonnes pour la mise en page

    if pdf_file:
        with col2:
            base64_pdf = base64.b64encode(pdf_file.read()).decode('utf-8')
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="700px" style="border:none;"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)
            
        
        with col1:
            if st.button("Extraire les informations", type="primary"):
                try:
                    with st.spinner("Extraction en cours..."):
                        df = extractor.process_pdf(pdf_file)
                        
                    if df is not None:
                        # Save to BytesIO instead of file
                        buffer = BytesIO()
                        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                            df.to_excel(writer, index=False)
                        
                        buffer.seek(0)  # Reset buffer position to the beginning
                        
                        st.success("✅ Extraction terminée avec succès!")
                        
                        # Offer download button
                        st.download_button(
                            label="📥 Télécharger le fichier Excel",
                            data=buffer,
                            file_name=OUTPUT_FILENAME,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                        
                        # Show preview
                        with st.expander("Aperçu des données extraites"):
                            st.dataframe(df, height=200)
                            #ajouter un peu de place dans le container

                    else:
                        st.error("❌ Erreur lors de l'extraction du PDF")
                
                except Exception as e:
                    st.error(f"❌ Une erreur est survenue: {str(e)}")
                    logger.exception("Error in main process")

if __name__ == "__main__":
    main()
