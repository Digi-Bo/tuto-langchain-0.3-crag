Ce projet est adapté d'un exemple de cette formation : [Udemy : Master RAG](https://www.udemy.com/course/llm-retrieval-augmented-generation-masterclass/)
Il met à jour le projet pour la version 0.3 de langchain et fournit une version francophone détaillée adaptée aux débutants.
---

# Projet : CRAG - Corrective RAG

---


Le CRAG améliore le pipeline traditionnel de Retrieval-Augmented Generation (RAG) en introduisant un évaluateur de pertinence. Cet outil évalue la relation entre les documents récupérés et la requête afin d'améliorer la précision des réponses générées.

---

## Fonctionnalités principales :

- **OpenAI** : [OpenAI](https://python.langchain.com/docs/integrations/platforms/openai) fournit une interface Python pour interagir avec l'API OpenAI et générer des réponses basées sur les modèles GPT.
- **python-dotenv** : [python-dotenv](https://pypi.org/project/python-dotenv/) permet de charger des variables d'environnement depuis un fichier `.env` pour sécuriser les clés API.
- **ChromaDB** : [ChromaDB](https://python.langchain.com/v0.2/docs/integrations/vectorstores/chroma/) est une base de données vectorielle open-source pour stocker l'embedding en local.
- **Tavily Search API** : [Tavily](https://app.tavily.com/documentation/apis) est un moteur de recherche conçu pour les modèles de langage (LLM), fournissant des résultats précis et en temps réel.

---

## Prérequis

1. **Python**  
   Assurez-vous d'avoir Python 3.12 ou une version ultérieure installée.  
   - Téléchargez Python depuis [python.org](https://www.python.org/downloads/).

2. **Créer un environnement virtuel**  
   Exécutez la commande suivante dans votre terminal pour créer un environnement virtuel :
   ```bash
   python3 -m venv env
   ```

3. **Activer l'environnement virtuel**  
   Activez l'environnement virtuel avec la commande suivante :
   ```bash
   source env/bin/activate
   ```

---

## Installation des dépendances

1. Installez les bibliothèques nécessaires :  
   ```bash
   pip install -r requirements.txt
   pip install langchain chromadb sentence-transformers
   ```

---

## Configuration

1. **Obtenir une clé API OpenAI**  
   Créez un compte ou connectez-vous sur [OpenAI](https://platform.openai.com/account/api-keys) pour récupérer votre clé API.  
   Exemple de contenu pour le fichier `.env` :  
   ```
   OPENAI_API_KEY=sk-XXXXXX...XXXXXX
   ```

   Ajoutez également cette clé à votre environnement système si nécessaire :
   ```bash
   export OPENAI_API_KEY='sk-XXXXXX...XXXXXX'
   ```

2. **Configurer l'API Tavily**  
   Consultez la documentation officielle pour activer et configurer l'API Tavily :  
   [Tavily API Documentation](https://app.tavily.com/documentation/apis).

---

## Lancer le script

1. Une fois tout configuré, exécutez le programme en activant votre environnement virtuel :  
   ```bash
   python3 main.py
   ```

---

## Ressources supplémentaires

- [Documentation LangChain](https://js.langchain.com/docs/introduction/)
- [Documentation OpenAI](https://platform.openai.com/docs/)
- [Documentation ChromaDB](https://python.langchain.com/v0.2/docs/integrations/vectorstores/chroma/)
