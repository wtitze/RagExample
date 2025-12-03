import argparse
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based ONLY on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def main():
    # CLI argument input
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()

    query_text = args.query_text

    # Load vector DB
    embedding_function = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004"
    )

    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embedding_function,
    )

    # Perform similarity search
    results = db.similarity_search_with_relevance_scores(query_text, k=3)

    if len(results) == 0 or results[0][1] < 0.7:
        print("Unable to find matching results.")
        return

    # Combine context text
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

    # Build prompt
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    # Use Gemini 1.5 Flash as the LLM
    model = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.2,
    )

    # Generate output
    response_text = model.predict(prompt)

    sources = [doc.metadata.get("source", None) for doc, _score in results]

    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)


if __name__ == "__main__":
    main()
