# app.py

import os
from flask import Flask, render_template, request, Response, stream_with_context
from dotenv import load_dotenv
from pymongo import MongoClient
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

load_dotenv()

app = Flask(__name__)

# --- Config ---
MONGO_URI = os.getenv("MONGODB_ATLAS_URI")
DB_NAME = os.getenv("MONGODB_DATABASE")
COLLECTION_NAME = os.getenv("MONGODB_COLLECTION")
VECTOR_INDEX_NAME = os.getenv("MONGODB_VECTOR_INDEX")
EMBEDDING_MODEL = os.getenv("GEMINI_EMBEDDING_MODEL")
LLM_MODEL = os.getenv("GEMINI_LLM_MODEL")

# --- Connessione MongoDB ---
client = MongoClient(MONGO_URI)
collection = client[DB_NAME][COLLECTION_NAME]

# --- Embeddings e Vector Store ---
embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)
vector_store = MongoDBAtlasVectorSearch(
    collection=collection,
    embedding=embeddings,
    index_name=VECTOR_INDEX_NAME
)

# --- LLM ---
llm = ChatGoogleGenerativeAI(model=LLM_MODEL, temperature=0.2, streaming=False)  # streaming False

# --- Prompt ---
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

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask_stream", methods=["POST"])
def ask_stream():
    data = request.json
    query = data.get("question", "").strip()
    if not query:
        return Response("Domanda vuota", status=400)

    try:
        # Recupera documenti più rilevanti
        docs_with_scores = vector_store.similarity_search_with_score(query, k=3)
        context_text = "\n\n".join([doc.page_content for doc, _ in docs_with_scores])

        # Invoca LLM
        answer_obj = llm.invoke(prompt.format(question=query, context=context_text))
        if hasattr(answer_obj, "text"):
            answer_text = answer_obj.text
        else:
            answer_text = str(answer_obj)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response(f"Errore LLM: {e}", status=500)

    def generate():
        # Invio chunk di risposta (50 caratteri ciascuno)
        for i in range(0, len(answer_text), 50):
            yield answer_text[i:i+50]

        # Separatore chiaro tra risposta e fonti
        yield "\n<END_OF_ANSWER>\n"

        # Invia fonti tutte insieme
        sources_text = "\n".join(
            [f"Fonte {i+1}: {doc.page_content[:200]} (Score: {score})"
             for i, (doc, score) in enumerate(docs_with_scores)]
        )
        yield f"<SOURCES>{sources_text}\n"

    return Response(stream_with_context(generate()), mimetype="text/plain")



if __name__ == "__main__":
    app.run(debug=True)
