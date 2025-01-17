# Application RAG avec LangChain
## Objectif de l'application
- Fournir une interface utilisateur permettant de poser des questions.
- Utiliser un pipeline RAG pour récupérer et évaluer des documents pertinents.
- Générer des réponses enrichies à partir de documents indexés ou d'une recherche web.

## Données utilisées pour le RAG
- **Sources indexées**
  - Articles de blog LangChain.
  - Documents découpés et stockés dans une base vectorielle Chroma.
- **Recherche web**
  - Utilisation de `TavilySearchResults` pour des informations complémentaires.

## Pipeline
1. L'utilisateur pose une question.
2. Les documents sont récupérés et évalués pour leur pertinence.
3. Si les documents sont jugés non pertinents, une recherche web est déclenchée.
4. La question est reformulée pour optimiser la génération de contenu.
5. Une réponse est générée et affichée.

## Architecture
### Main.py
- **start**
  - Affiche le menu principal.
  - Propose deux choix :
    - `ask()`
    - Quitter l'application.
- **ask**
  - Récupère la question de l'utilisateur.
  - Appelle `query` pour générer une réponse.
  - Retourne au menu principal ou quitte l'application.

### Query.py
- **assess_retrieved_docs**
  - Évalue la pertinence des documents récupérés avec un grader LLM.
- **rewrite_query**
  - Reformule la requête pour améliorer la qualité de la réponse.
- **search_web**
  - Effectue une recherche en ligne via Tavily Search.
- **generate_answer**
  - Génère une réponse basée sur les documents récupérés et la question reformulée.
- **query**
  - Pipeline complet pour récupérer, évaluer, optimiser et répondre.

### Utils.py
- **sliding_window**
  - Découpe un texte en fragments selon une fenêtre glissante.
- **convert_to_embeddings**
  - Crée des embeddings pour chaque fragment et les stocke dans Chroma.
- **format_docs**
  - Formate les documents pour une meilleure lisibilité.

## Technologies utilisées
- **LangChain**
  - Gestion des workflows RAG.
- **Chroma**
  - Base de données vectorielle pour les documents.
- **TavilySearchResults**
  - Recherche en ligne pour compléter les réponses.
- **OpenAI**
  - Modèle LLM pour la génération de contenu et l'évaluation de documents.
- **SentenceTransformer**
  - Génération d'embeddings pour les fragments de texte.
- **NLTK**
  - Découpage des textes en phrases avec `sent_tokenize`.
