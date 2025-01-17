# Projet : CRAG - Corrective RAG

**CRAG** (Corrective RAG) améliore le pipeline traditionnel du Retrieval-Augmented Generation (RAG) en introduisant un évaluateur de pertinence. Cet outil évalue la relation entre les documents récupérés et la requête afin d'améliorer la précision des réponses générées.


## Objectif de l'application

L'application est une interface utilisateur simple permettant de poser des questions et d'obtenir des réponses grâce à un système de RAG (Retrieval-Augmented Generation). Ce système utilise LangChain et des modèles LLM pour rechercher des informations pertinentes, optimiser les requêtes et générer des réponses basées sur des documents indexés ou des résultats de recherche web.

---

## Données utilisées pour le RAG

- **Sources de données indexées** :  
  Les documents sont récupérés à partir des URL suivantes :  
  - [http://blog.langchain.dev/deconstructing-rag](http://blog.langchain.dev/deconstructing-rag)  
  - [https://blog.langchain.dev/enhancing-rag-based-applications-accuracy-by-constructing-and-leveraging-knowledge-graphs/](https://blog.langchain.dev/enhancing-rag-based-applications-accuracy-by-constructing-and-leveraging-knowledge-graphs/)  
  - [https://blog.langchain.dev/graph-based-metadata-filtering-for-improving-vector-search-in-rag-applications/](https://blog.langchain.dev/graph-based-metadata-filtering-for-improving-vector-search-in-rag-applications/)  

- **Indexation** :  
  Les documents récupérés sont découpés en fragments grâce au `RecursiveCharacterTextSplitter` et stockés dans une base vectorielle Chroma pour permettre une recherche efficace.

- **Recherche web** :  
  En cas de pertinence faible des documents indexés, une recherche en ligne est effectuée via l'outil `TavilySearchResults`.

---

## Fonctionnement de l'application

1. **Menu principal** :  
   L'utilisateur peut choisir entre poser une question ou quitter l'application.  

2. **Interaction utilisateur** :  
   - L'utilisateur saisit une question.  
   - L'application récupère les documents pertinents via la base vectorielle.  
   - Un évaluateur (retrieval grader) vérifie la pertinence des documents.  
   - Si les documents sont jugés non pertinents, une recherche web est lancée pour compléter les informations.  

3. **Optimisation des requêtes** :  
   Les questions de l'utilisateur sont reformulées pour améliorer leur clarté et leur adéquation avec les modèles LLM.  

4. **Génération des réponses** :  
   Les réponses sont générées en utilisant un modèle LLM avec un prompt spécialisé.

---

## Architecture de l'application

### **main.py**

- **start()**  
  - Affiche le menu principal.  
  - Propose deux choix :  
    - Poser une question (redirige vers `ask()`).  
    - Quitter l'application.  

- **ask()**  
  - Récupère la question de l'utilisateur.  
  - Appelle la fonction `query()` pour générer une réponse.  
  - Affiche la réponse ou revient au menu principal si l'utilisateur le souhaite.  

---

### **query.py**

#### Fonctions principales

- **assess_retrieved_docs(query)**  
  - Récupère les documents pertinents pour une question.  
  - Évalue leur pertinence via un grader basé sur un modèle LLM.  

- **rewrite_query(query)**  
  - Réécrit la requête pour en améliorer la qualité et la pertinence.  

- **search_web(query)**  
  - Effectue une recherche web en cas de documents indexés jugés non pertinents.  

- **generate_answer(docs, query)**  
  - Génère une réponse basée sur les documents récupérés et la requête reformulée.  

- **query(query)**  
  - Pipeline complet :  
    1. Évaluation des documents récupérés.  
    2. Optimisation de la question.  
    3. Recherche web si nécessaire.  
    4. Génération de la réponse finale.  

---

### **utils.py**

- **sliding_window(text, window_size)**  
  - Découpe un texte en fragments selon une fenêtre glissante de taille définie.  

- **convert_to_embeddings(chunks)**  
  - Génère des embeddings pour les fragments de texte à l'aide d'un modèle `SentenceTransformer`.  
  - Ajoute ces embeddings à une base vectorielle Chroma.  

- **format_docs(docs)**  
  - Formate les documents pour une présentation lisible.  
