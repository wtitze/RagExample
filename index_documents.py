# index_documents.py (Versione Aggiornata)

import os
from dotenv import load_dotenv
from pymongo import MongoClient
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_google_genai import GoogleGenerativeAIEmbeddings
# Usiamo DirectoryLoader per caricare tutti i file nella cartella
# 1. DirectoryLoader e PyPDFLoader devono provenire da langchain_community
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader

# 2. RecursiveCharacterTextSplitter deve provenire da langchain_text_splitters
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

# --- Configurazione Variabili ---
MONGO_URI = os.getenv("MONGODB_ATLAS_URI")
DB_NAME = os.getenv("MONGODB_DATABASE")
COLLECTION_NAME = os.getenv("MONGODB_COLLECTION")
VECTOR_INDEX_NAME = os.getenv("MONGODB_VECTOR_INDEX")
EMBEDDING_MODEL = os.getenv("GEMINI_EMBEDDING_MODEL")
# NUOVA VARIABILE
DOCUMENTS_PATH = os.getenv("DOCUMENTS_PATH") 

# --- Connessione a MongoDB ---
client = MongoClient(MONGO_URI)
collection = client[DB_NAME][COLLECTION_NAME]

# Inizializza il modello di embedding di Gemini
embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)

def create_vector_store_and_index():
    print("Connessione a MongoDB riuscita. Inizio caricamento documenti...")
    
    # 1. Caricamento e Suddivisione dei Documenti
    
    # Usa DirectoryLoader per scansionare tutti i PDF nella directory specificata
    print(f"Scansione dei PDF nella directory: {DOCUMENTS_PATH}")
    loader = DirectoryLoader(
        path=DOCUMENTS_PATH,
        glob="**/*.pdf", # Cerca tutti i file .pdf in tutte le sottocartelle
        loader_cls=PyPDFLoader, # Usa PyPDFLoader per leggere i file
        silent_errors=True # Continua anche se trova file non leggibili
    )
    
    # Carica tutti i documenti
    documents = loader.load()
    if not documents:
        print("❌ ERRORE: Nessun documento PDF trovato. Controlla il percorso o i file.")
        return

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200, 
        length_function=len
    )
    
    # Suddividi i documenti caricati in chunks
    docs_chunks = text_splitter.split_documents(documents)
    print(f"Creati {len(docs_chunks)} chunks da {len(documents)} documenti per l'indicizzazione.")

    # 2. Creazione del Vector Store (Inserimento in MongoDB)
    print("Inizio creazione e caricamento degli embedding su MongoDB Atlas...")
    
    # Questa operazione crea i vettori e li inserisce nella collezione
    vector_store = MongoDBAtlasVectorSearch.from_documents(
        documents=docs_chunks,
        embedding=embeddings,
        collection=collection,
        index_name=VECTOR_INDEX_NAME
    )

    print("✅ Documenti e Vector Embeddings caricati su MongoDB Atlas con successo!")
    return vector_store

if __name__ == "__main__":
    create_vector_store_and_index()