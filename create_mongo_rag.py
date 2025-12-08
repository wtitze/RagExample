# create_mongo_rag.py

import os
import fitz  # PyMuPDF
from pymongo import MongoClient
from langchain.embeddings.openai import OpenAIEmbeddings
from tqdm import tqdm

# -----------------------------
# CONFIGURAZIONE
# -----------------------------
MONGODB_URI = os.getenv("URI")
DB_NAME = "rag_db"
COLLECTION_NAME = "documents"
PDF_FOLDER = "./data/books"  # cartella dove metti i PDF
CHUNK_SIZE = 500  # numero approssimativo di parole per chunk

# -----------------------------
# CONNESSIONE A MONGODB
# -----------------------------
client = MongoClient(MONGODB_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# -----------------------------
# FUNZIONI
# -----------------------------
def extract_text_from_pdf(pdf_path):
    """Estrae il testo da ogni pagina di un PDF e restituisce chunk di testo"""
    doc = fitz.open(pdf_path)
    text_chunks = []

    for page in doc:
        text = page.get_text()
        # chunking semplice: dividiamo il testo in CHUNK_SIZE parole
        words = text.split()
        for i in range(0, len(words), CHUNK_SIZE):
            chunk = " ".join(words[i:i+CHUNK_SIZE])
            if chunk.strip():
                text_chunks.append(chunk)
    return text_chunks

def generate_embeddings(chunks, embeddings_model):
    """Genera embedding per una lista di chunk di testo"""
    embeddings = []
    for chunk in tqdm(chunks, desc="Generando embedding"):
        emb = embeddings_model.embed_text(chunk)
        embeddings.append(emb)
    return embeddings

# -----------------------------
# SCRIPT PRINCIPALE
# -----------------------------
def main():
    embeddings_model = OpenAIEmbeddings()  # usa il modello di OpenAI o altro embedding
    
    pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.lower().endswith(".pdf")]
    
    all_docs = []

    for pdf_file in pdf_files:
        pdf_path = os.path.join(PDF_FOLDER, pdf_file)
        print(f"\nProcessing {pdf_file}...")
        chunks = extract_text_from_pdf(pdf_path)
        chunk_embeddings = generate_embeddings(chunks, embeddings_model)

        for chunk, embedding in zip(chunks, chunk_embeddings):
            doc = {
                "text": chunk,
                "embedding": embedding,
                "metadata": {"source_file": pdf_file}
            }
            all_docs.append(doc)

    if all_docs:
        collection.insert_many(all_docs)
        print(f"\nInseriti {len(all_docs)} chunk in MongoDB.")

    # Creazione indice vettoriale (solo se MongoDB supporta vector search)
    try:
        if len(all_docs) > 0:
            dim = len(all_docs[0]["embedding"])
            collection.create_index(
                [("embedding", "vector")],
                name="embedding_vector_index",
                vectorParams={"dimensions": dim, "similarityMetric": "cosine"}
            )
            print("Indice vettoriale creato su 'embedding'.")
    except Exception as e:
        print("Attenzione: non è stato possibile creare l'indice vettoriale. Dettagli:", e)

if __name__ == "__main__":
    main()
