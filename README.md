# Extraction d'Informations Médicales depuis un PDF
Ce projet est conçu pour extraire automatiquement des informations médicales spécifiques à partir de rapports PDF en utilisant un modèle d'IA Ollama. L'application utilise Streamlit comme interface utilisateur et enregistre les résultats dans un fichier Excel téléchargeable.

# Fonctionnalités
- Extraction de données brutes de rapports hospitaliers en PDF.
- Traitement et nettoyage des données en utilisant Ollama.
- Téléchargement des résultats sous format Excel.
- Barre de progression pour suivre l'avancement de l'extraction.

# Installation
Prérequis
Assurez-vous que Python 3.11 ou une version compatible est installé sur votre système.

# Étapes d'Installation
1. Clonez le dépôt :
git clone https://github.com/rxdhwxne1/apothicare.git
cd apothicare

2. Créez un environnement virtuel (pas obligatoire):
python -m venv env
source env/bin/activate  # Pour macOS/Linux
.\env\Scripts\activate   # Pour Windows

3. Installez les dépendances :
pip install -r requirements.txt

4. Installez et configurez Ollama :

Ollama est utilisé pour gérer les modèles de génération de texte (LLM) comme llama2. Assurez-vous que ollama est installé :

Téléchargez et installez Ollama depuis [Ollama.com](https://ollama.com/).
Configurez votre clé API dans l'environnement pour accéder à Ollama (voir la documentation d'Ollama pour générer une clé d'API).

# Utilisation
1. Lancer l'application Streamlit :
streamlit run apothicare.py

2. Importer un fichier PDF :
Une fois l'application lancée, vous pouvez importer un fichier PDF contenant un rapport médical via l'interface.

3. Extraire les informations :
Cliquez sur le bouton d'extraction pour démarrer le processus. Une fois l'extraction terminée, un bouton de téléchargement vous permettra de télécharger le fichier Excel généré avec les données extraites.