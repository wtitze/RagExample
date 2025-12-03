import argparse
from dotenv import load_dotenv
import os

# Nuovo import Chroma
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate

load_dotenv()

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based ONLY on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

# Soglia minima di similarità MODIFICA SE NECESSARIO!
SIMILARITY_THRESHOLD = 0.5

def main():
    # CLI
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text

    # Carica DB
    embedding_function = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Ricerca similarità
    results = db.similarity_search_with_relevance_scores(query_text, k=3)

    # Debug: mostra tutti i chunk trovati
    if results:
        print("\n--- Risultati trovati ---")
        for doc, score in results:
            print(f"Score: {score:.3f} | {doc.page_content[:150]}...\n")
        print("------------------------\n")

    # Controllo soglia
    if len(results) == 0 or results[0][1] < SIMILARITY_THRESHOLD:
        print("Unable to find matching results.")
        return

    # Combina contesto
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

    # Costruisci prompt
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    # LLM Gemini
    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.2,
    )

    # Genera risposta
    response_text = model.predict(prompt)

    sources = [doc.metadata.get("source", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)


if __name__ == "__main__":
    main()
