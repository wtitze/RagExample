from flask import Flask, request, render_template
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.prompts.chat import ChatPromptTemplate
from dotenv import load_dotenv
import os

# Carica chiave API
load_dotenv()
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

app = Flask(__name__)

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based ONLY on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

# Inizializza DB Chroma
embedding_function = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

# Inizializza LLM Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2,
)

@app.route("/", methods=["GET", "POST"])
def index():
    response_text = ""
    if request.method == "POST":
        query_text = request.form["query"]

        # Similarity search
        results = db.similarity_search_with_relevance_scores(query_text, k=3)
        if results and results[0][1] >= 0.5:
            context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in results])
            prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
            prompt = prompt_template.format(context=context_text, question=query_text)

            response_text = llm.predict(prompt)
        else:
            response_text = "Mi dispiace, non ho trovato informazioni rilevanti."

    return render_template("index.html", response=response_text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
