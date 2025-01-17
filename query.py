# query.py
# Ce fichier contient les fonctions nécessaires pour gérer les questions posées par l'utilisateur.
# Il récupère des documents pertinents, les évalue, reformule les questions si nécessaire,
# et génère des réponses à l'aide de modèles de langage (LLM) et d'un pipeline RAG.



# A charger en premier pour éviter les problèmes d'USER_AGENT réclamé par les dépendances
from dotenv import load_dotenv  # Pour charger les variables d'environnement depuis un fichier .env
import os # Fournit des outils pour accéder aux variables d'environnement et manipuler les fichiers système

# Charger les variables d'environnement (par ex. clé API OpenAI) depuis un fichier .env
load_dotenv()
USER_AGENT = os.getenv("USER_AGENT")


# Importation des bibliothèques nécessaires
import warnings  # Pour ignorer les avertissements inutiles
from langsmith import Client  #pour importer des modèlesz de prompts
from langchain_community.tools.tavily_search import TavilySearchResults  # Outil de recherche web
from langchain.text_splitter import RecursiveCharacterTextSplitter  # Découpage de texte
from langchain.schema import Document  # Structure pour représenter les documents
from langchain.prompts import ChatPromptTemplate  # Modèle de prompt pour le chat
from langchain.prompts.chat import HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain_community.document_loaders import WebBaseLoader  # Chargement des documents depuis des URL
from langchain_community.vectorstores import Chroma  # Base vectorielle pour la recherche
from langchain_core.output_parsers import StrOutputParser  # Parsing des réponses LLM
from langchain_openai import ChatOpenAI, OpenAIEmbeddings  # Intégration OpenAI pour LLM et embeddings
from langchain_core.pydantic_v1 import BaseModel, Field  # Gestion des modèles avec Pydantic
from colorama import Fore  # Stylisation du texte dans le terminal

# Chargement des variables d'environnement
load_dotenv()
USER_AGENT = os.getenv("USER_AGENT")  # Récupère la variable USER_AGENT définie dans .env

# Ignorer les avertissements inutiles
warnings.filterwarnings("ignore")

# Initialisation du modèle de langage
llm = ChatOpenAI()

#### INDEXATION DES DOCUMENTS ####
# Définition des URLs contenant les articles à indexer
urls = [
    "http://blog.langchain.dev/deconstructing-rag",
    "https://blog.langchain.dev/enhancing-rag-based-applications-accuracy-by-constructing-and-leveraging-knowledge-graphs/",
    "https://blog.langchain.dev/graph-based-metadata-filtering-for-improving-vector-search-in-rag-applications/",
]

# Chargement des documents à partir des URLs
docs = [WebBaseLoader(url).load() for url in urls]  # Charge les documents depuis les URLs
docs_list = [item for sublist in docs for item in sublist]  # Aplatissement des listes imbriquées

# Découpage des documents en fragments pour une meilleure indexation
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=250, chunk_overlap=0  # Chaque fragment contient 250 tokens sans chevauchement
)
doc_splits = text_splitter.split_documents(docs_list)  # Découpe les documents en fragments

# Création de la base vectorielle Chroma pour stocker les fragments avec leurs embeddings
vectorstore = Chroma.from_documents(
    documents=doc_splits,
    collection_name="rag-chroma",
    embedding=OpenAIEmbeddings(),  # Utilisation des embeddings OpenAI
)
retriever = vectorstore.as_retriever()  # Initialisation d'un retriever pour la recherche

#### ÉVALUATION DES DOCUMENTS ####
class GradeDocuments(BaseModel):
    """
    Modèle pour attribuer un score binaire à un document selon sa pertinence ('yes' ou 'no').
    """
    binary_score: str = Field(description="Documents are relevant to the question, 'yes' or 'no'")

    def get_score(self) -> str:
        """Renvoie le score binaire sous forme de chaîne."""
        return self.binary_score

# Préparation d'un modèle de langage structuré pour évaluer la pertinence
structured_llm_grader = llm.with_structured_output(GradeDocuments)

# Prompt pour évaluer la pertinence des documents
system_template = """You are an evaluator determining the relevance of a retrieved {documents} to a user's query {question}.
If the document contains keyword(s) or semantic meaning related to the question, mark it as relevant.
Assign a binary score of 'yes' or 'no' to indicate the document's relevance to the question."""
system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
human_message_prompt = HumanMessagePromptTemplate.from_template(
    input_variables=["documents", "question"],
    template="{question}",
)
grader_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

#### REFORMULATION DES QUESTIONS ####
# Prompt pour reformuler les questions utilisateur
prompt_template = """Given a user input {question}, your task is to re-write or rephrase the question to optimize the query for improved content generation."""
system_prompt = SystemMessagePromptTemplate.from_template(prompt_template)
human_prompt = HumanMessagePromptTemplate.from_template(
    input_variables=["question"],
    template="{question}",
)
re_write_prompt = ChatPromptTemplate.from_messages([system_prompt, human_prompt])

#### OUTIL DE RECHERCHE WEB ####
web_search_tool = TavilySearchResults(k=3)  # Limite à 3 résultats de recherche pertinents

#### PIPELINE DE GÉNÉRATION DE RÉPONSES ####
# Chargement d'un prompt spécifique pour le RAG
client = Client()
prompt = client.pull_prompt("rlm/rag-prompt")

def assess_retrieved_docs(query):
    """
    Évalue la pertinence des documents récupérés pour une question donnée.
    """
    retrieval_grader = grader_prompt | structured_llm_grader | GradeDocuments.get_score
    docs = retriever.invoke(query) # Recherche des documents pertinents

    doc_txt = docs[0].page_content  # Récupère le contenu du premier document
    binary_score = retrieval_grader.invoke({"question": query, "documents": doc_txt})
    return binary_score, docs

def rewrite_query(query):
    """
    Reformule une requête utilisateur pour l'optimiser.
    """
    question_rewriter = re_write_prompt | llm | StrOutputParser()
    return question_rewriter.invoke({"question": query})

def search_web(query):
    """
    Effectue une recherche web pour compléter les informations.
    """
    docs = web_search_tool.invoke({"query": query})
    web_results = "\n".join([d["content"] for d in docs])
    return Document(page_content=web_results)

def generate_answer(docs, query):
    """
    Génère une réponse basée sur les documents récupérés et la requête utilisateur.
    """
    rag_chain = prompt | llm | StrOutputParser()
    return rag_chain.invoke({"context": docs, "question": query})

def query(query):
    """
    Pipeline complet pour traiter une question utilisateur :
    1. Récupération et évaluation des documents.
    2. Reformulation de la requête si nécessaire.
    3. Recherche web pour compléter les informations.
    4. Génération d'une réponse finale.
    """
    binary_score, docs = assess_retrieved_docs(query)
    print(f"Relevance score: {binary_score}")
    print(f"{Fore.YELLOW}Rewriting the query for content generation.{Fore.RESET}")
    optimized_query = rewrite_query(query)
    if binary_score == "no":
        print(f"{Fore.MAGENTA}Retrieved documents are irrelevant. Searching the web for additional information.{Fore.RESET}")
        docs = search_web(optimized_query)
    return generate_answer(docs, optimized_query)
