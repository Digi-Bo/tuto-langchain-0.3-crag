# utils.py
# Ce fichier contient des fonctions utiles pour le traitement et l'indexation de documents.
# Il inclut le découpage de textes en fragments, la génération d'embeddings pour ces fragments
# et leur stockage dans une base vectorielle pour une recherche efficace.

# Importation des bibliothèques nécessaires
import nltk  # Outil pour le traitement du langage naturel
from nltk.tokenize import sent_tokenize  # Découpe un texte en phrases
from langchain_community.vectorstores import Chroma  # Base vectorielle pour stocker les embeddings
from langchain.docstore.document import Document  # Structure pour représenter les fragments de texte
from sentence_transformers import SentenceTransformer  # Génération d'embeddings à partir de texte
from langchain.embeddings import HuggingFaceEmbeddings  # Embeddings via des modèles Hugging Face
import json  # Manipulation des données au format JSON

# Téléchargement du tokenizer nécessaire pour NLTK
nltk.download('punkt')  # Assure que le tokenizer 'punkt' est disponible pour découper les phrases

def sliding_window(text, window_size=3):
    """
    Découpe un texte en fragments (ou chunks) en utilisant une fenêtre glissante.
    Chaque fragment contient un certain nombre de phrases.

    Args:
    text (str): Texte d'entrée à découper.
    window_size (int): Nombre de phrases par fragment.

    Returns:
    list of str: Liste des fragments de texte.
    """
    sentences = sent_tokenize(text)  # Découpe le texte en phrases
    # Génère des fragments en combinant `window_size` phrases avec une fenêtre glissante
    return [' '.join(sentences[i:i+window_size]) for i in range(len(sentences) - window_size + 1)]


# Exemple d'utilisation
text = "This is the first sentence. Here comes the second sentence. And here is the third one. Finally, the fourth sentence."
chunks = sliding_window(text, window_size=3)  # Découpe le texte en fragments de 3 phrases
for chunk in chunks:
    print(chunk)  # Affiche chaque fragment
    print("-----")
    # Ici, chaque fragment peut être converti en embedding et stocké dans une base vectorielle


def convert_to_embeddings(chunks):
    """
    Génère des embeddings pour une liste de fragments de texte et les stocke dans une base vectorielle.

    Args:
    chunks (list of str): Liste de fragments de texte.

    Returns:
    Chroma: Base vectorielle contenant les fragments et leurs embeddings.
    """
    # Chargement d'un modèle pré-entraîné pour générer des embeddings
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Génération des embeddings pour chaque fragment
    embeddings = model.encode(chunks)

    # Initialisation de la base vectorielle Chroma avec des embeddings Hugging Face
    embedding_function = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    vector_store = Chroma(
        embedding_function=embedding_function,  # Fonction pour générer les embeddings
        collection_name="text_chunks"  # Nom de la collection dans la base vectorielle
    )

    # Création de documents avec leur contenu et leurs embeddings
    documents = [Document(
        page_content=chunk,  # Texte original du fragment
        metadata={"embedding": json.dumps(embedding.tolist())})  # Embedding converti en JSON
        for chunk, embedding in zip(chunks, embeddings)]

    # Ajout des documents à la base vectorielle
    vector_store.add_documents(documents)

    print("Les embeddings ont été enregistrés avec succès dans la collection ChromaDB.")
    return vector_store  # Retourne la base vectorielle pour une utilisation ultérieure


def format_docs(docs):
    """
    Formate une liste de documents en une seule chaîne de texte lisible.

    Args:
    docs (list of Document): Liste de documents.

    Returns:
    str: Texte formaté combinant tous les contenus des documents.
    """
    return "\n\n".join([d.page_content for d in docs])  # Combine le contenu des documents avec des sauts de ligne
