# rag_chain.py

import os
from dotenv import load_dotenv
from pymongo import MongoClient
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

load_dotenv()

# --- Configurazione Variabili ---
MONGO_URI = os.getenv("MONGODB_ATLAS_URI")
DB_NAME = os.getenv("MONGODB_DATABASE")
COLLECTION_NAME = os.getenv("MONGODB_COLLECTION")
VECTOR_INDEX_NAME = os.getenv("MONGODB_VECTOR_INDEX")
EMBEDDING_MODEL = os.getenv("GEMINI_EMBEDDING_MODEL")
LLM_MODEL = os.getenv("GEMINI_LLM_MODEL")

# --- 1. Inizializzazione ---
client = MongoClient(MONGO_URI)
collection = client[DB_NAME][COLLECTION_NAME]

embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)

vector_store = MongoDBAtlasVectorSearch(
    collection=collection,
    embedding=embeddings,
    index_name=VECTOR_INDEX_NAME
)

# LLM Gemini
llm = ChatGoogleGenerativeAI(model=LLM_MODEL, temperature=0.2)

# --- 2. Prompt e Parser ---
prompt = ChatPromptTemplate.from_template(
    """
Sei un assistente esperto che risponde basandosi solo sui documenti forniti nel contesto.
Se l'informazione non è presente nei documenti, rispondi chiaramente che non appare nei documenti.

Contesto:
{context}

Domanda: {question}

Risposta:
"""
)

parser = StrOutputParser()

# --- 3. Pipeline RAG ---
rag_chain = (
    {
        "context": lambda x: x["context"],  # testo puro
        "question": lambda x: x["question"]
    }
    | prompt
    | llm
    | parser
)

# --- 4. Funzione interattiva ---
def interactive_query(k: int = 3):
    """
    Ciclo interattivo per fare query RAG all'utente.
    Mostra prima i documenti (con score) e poi la risposta dell'LLM.
    """
    print("Benvenuto! Inserisci le tue domande. Scrivi 'fine' per uscire.\n")
    running = True

    while running:
        query = input("Inserisci la domanda: ").strip()
        if query.lower() == "fine":
            running = False
        else:
            # Recupero documenti con score reale
            docs_with_scores = vector_store.similarity_search_with_score(query, k=k)

            # Mostra i documenti
            print("\n📚 Documenti recuperati dal database:")
            for i, (doc, score) in enumerate(docs_with_scores, start=1):
                print(f"Documento {i}:")
                print(f" - Contenuto: {doc.page_content[:200]}...")
                print(f" - Score: {score}")
                print(f" - Metadati: {doc.metadata}\n")

            # Prepara contesto
            context_text = "\n\n".join([doc.page_content for doc, _ in docs_with_scores])

            # Genera la risposta
            response = rag_chain.invoke({"question": query, "context": context_text})

            print("🤖 Risposta di Gemini:")
            print(response)
            print("\n" + "-"*80 + "\n")

    print("Sessione terminata.")

# --- 5. Avvio ---
if __name__ == "__main__":
    interactive_query(k=3)  # Puoi cambiare k se vuoi più documenti
