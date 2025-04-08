# Extraction d'Informations Médicales depuis un PDF
Ce projet est conçu pour extraire automatiquement des informations médicales spécifiques à partir de rapports PDF en utilisant un modèle d'IA Ollama. L'application utilise Streamlit comme interface utilisateur et enregistre les résultats dans un fichier Excel téléchargeable.

# Fonctionnalités
- Extraction de données brutes à partir de comptes rendus d'hospitalisation au format PDF.
- Traitement et nettoyage des données en utilisant Ollama.
- Téléchargement des résultats sous format Excel.
- Barre de progression pour suivre l'avancement de l'extraction.

# Installation
Prérequis
- **Python** : Assurez-vous que Python 3.11 ou une version compatible est installé sur votre système.
- **Ollama** : Nécessaire pour la gestion des modèles de génération de texte (LLM) comme llama3.2.

## Important - Choix du modèle
L’utilisation d’un modèle plus performant (ex. : meditron 7B ou un modèle spécialisé dans le domaine médical avec davantage de paramètres) permet d’obtenir des résultats nettement meilleurs.

Avec un modèle plus grand, nous avons atteint jusqu’à 79 % de termes correctement identifiés. Ce chiffre inclut toutefois des cas où des mots non pertinents ont également été extraits — les bons termes étaient présents, mais souvent accompagnés de contenu superflu. Cela dit, l’usage de modèles plus puissants allonge considérablement le temps de traitement et n’élimine pas totalement les phénomènes d’hallucination, en particulier sur les termes complexes ou ambigus.

- Pour des raisons de rapidité d'exécution, nous avons utilisé le modèle llama3.2-1b, plus léger mais aussi moins précis. Ce choix était fait dans une logique de proof of concept et ne reflète donc pas les performances réelles qu’on pourrait obtenir avec un modèle plus robuste.

# Étapes d'Installation

## Étape 1. Cloner le dépôt :

```bash
git clone https://github.com/rxdhwxne1/apothicare.git
cd apothicare
```

## Étape 2. Créer un environnement virtuel (optionnel mais recommandé) :

```bash
python -m venv env
source env/bin/activate  # Pour macOS/Linux
.\env\Scripts\activate   # Pour Windows
```

## Étape 3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Étape 4. Installer et configurer Ollama :

Le projet utilise Ollama pour gérer le modèle de langage Llama 3.2.

Téléchargez et installez Ollama depuis ollama.com.

### Exécutez le modèle Llama 3.2 en local :

```bash
ollama run llama3.2:1b
```

## Étape 5. Lancer l'application Streamlit :

```bash
streamlit run apothicare.py
```

## Utilisation

**Importer un fichier PDF** : Téléchargez un compte rendu d’hospitalisation au format PDF via l’interface Streamlit. **Étant donné que ces documents sont strictement confidentiels, des exemples fictifs sont fournis avec le projet, mais peuvent être remplacés par de véritables comptes rendus si nécessaire.**

**Extraire les informations** : Cliquez sur le bouton d'extraction pour démarrer le traitement.

**Télécharger les résultats** : Une fois l'extraction terminée, téléchargez le fichier Excel généré contenant les données extraites.

## Structure du code

apothicare.py : Script principal pour exécuter l'application Streamlit.

requirements.txt : Liste des dépendances requises pour le projet.

## Dépendances

streamlit : Pour l'interface web interactive.

ollama : Pour le traitement du texte médical avec les modèles de langage.

## Contribution

Namaoui Radhwane

Baptiste Prevot

Thomas Van Der Perre
