
# A charger en premier pour éviter les problèmes d'USER_AGENT réclamé par les dépendances
from dotenv import load_dotenv  # Pour charger les variables d'environnement depuis un fichier .env
import os # Fournit des outils pour accéder aux variables d'environnement et manipuler les fichiers système

# Charger les variables d'environnement (par ex. clé API OpenAI) depuis un fichier .env
load_dotenv()
USER_AGENT = os.getenv("USER_AGENT")


import bs4
from langchain import hub
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.prompts import ChatPromptTemplate
from langchain.prompts.chat import (
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter
from langchain_openai import ChatOpenAI
from langchain.load import dumps, loads
from langchain_core.pydantic_v1 import BaseModel, Field

from colorama import Fore
import warnings
warnings.filterwarnings("ignore")

load_dotenv()

llm = ChatOpenAI()

#### INDEXING ####
urls = [
    "http://blog.langchain.dev/deconstructing-rag",
    "https://blog.langchain.dev/enhancing-rag-based-applications-accuracy-by-constructing-and-leveraging-knowledge-graphs/",
    "https://blog.langchain.dev/graph-based-metadata-filtering-for-improving-vector-search-in-rag-applications/",
]

docs = [WebBaseLoader(url).load() for url in urls]
docs_list = [item for sublist in docs for item in sublist]

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=250, chunk_overlap=0
)
doc_splits = text_splitter.split_documents(docs_list)

vectorstore = Chroma.from_documents(
    documents=doc_splits,
    collection_name="rag-chroma",
    embedding=OpenAIEmbeddings(),
)
retriever = vectorstore.as_retriever()


#### Retrieval Grader : Retrieval Evaluator ####
class GradeDocuments(BaseModel):
    """Binary score for relevance check on retrieved documents."""

    binary_score: str = Field(description="Documents are relevant to the question, 'yes' or 'no'")

    def get_score(self) -> str:
        """Return the binary score as a string."""
        return self.binary_score


def get_score(self) -> str:
    """Return the binary score as a string."""
    return self.binary_score

# LLM with function call 
structured_llm_grader = llm.with_structured_output(GradeDocuments)

# Prompt 
system_template = """You are an evaluator determining the relevance of a retrieved {documents} to a user's query {question}.If the document contains keyword(s) or semantic meaning related to the question, mark it as relevant.Assign a binary score of 'yes' or 'no' to indicate the document's relevance to the question."""

system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
human_message_prompt = HumanMessagePromptTemplate.from_template(
    input_variables=["documents", "question"],
    template="{question}",
)
grader_prompt = ChatPromptTemplate.from_messages(
    [system_message_prompt, human_message_prompt]
)

### Question Re-writer - Knowledge Refinement ####
# Prompt 
prompt_template = """Given a user input {question}, your task is re-write or rephrase the question to optimize the query in order to imprive the content generation"""

system_prompt = SystemMessagePromptTemplate.from_template(prompt_template)
human_prompt = HumanMessagePromptTemplate.from_template(
    input_variables=["question"],
    template="{question}",
)
re_write_prompt = ChatPromptTemplate.from_messages(
    [system_prompt, human_prompt]
)

### Web Search Tool - Knowledge Searching ####
web_search_tool = TavilySearchResults(k=3) 

#### Generate Answer  ####
# Prompt
prompt = hub.pull("rlm/rag-prompt")

# Retrieve and assess
def assess_retrieved_docs(query):
    """Retrieve and assess the relevance of documents to a given query."""
    retrieval_grader = grader_prompt | structured_llm_grader | get_score
    docs = retriever.get_relevant_documents(query) 
    doc_txt = docs[0].page_content
    binary_score = retrieval_grader.invoke({"question": query, "documents": doc_txt})
    return binary_score, docs

# Rewrite and optimize 
def rewrite_query(query):
    """Rewrite and optimize a given user query for the model."""
    question_rewriter = re_write_prompt | llm | StrOutputParser()
    return question_rewriter.invoke({"question": query})

# Search the web
def search_web(query):
    """Search the web for complimentary information."""
    docs = web_search_tool.invoke({"query": query})
    print(docs)
    web_results = "\n".join([d["content"] for d in docs])
    return Document(page_content=web_results)

def generate_answer(docs, query):
    # Chain
    rag_chain = prompt | llm | StrOutputParser()
    # Run
    return rag_chain.invoke({"context": docs, "question": query})

def query(query):
    """Query the model with a question and assess the relevance of retrieved documents."""
    # question = "RAG"
    binary_score, docs = assess_retrieved_docs(query)
    print(f"Relevance score: {binary_score}")
    # Rewrite and optimize the query
    print(f"{Fore.YELLOW}Rewriting the query for content generation.{Fore.RESET}")
    optimized_query = rewrite_query(query)
    if binary_score == "no":
        print(f"{Fore.MAGENTA}Retrieved documents are irrelevant. Searching the web for additional information.{Fore.RESET}")
        docs = search_web(optimized_query)
    return generate_answer(docs, optimized_query)