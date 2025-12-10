# Istruzioni per agenti di coding (Copilot / AI)

Breve guida per diventare produttivi in questo repository RAG (retrieval-augmented generation).

- **Big picture**: il progetto costruisce una pipeline RAG che indicizza PDF in vettori e risponde tramite un LLM.
  - Due opzioni di storage dei vettori coesistono: `Chroma` (locale, directory `chroma/`) e MongoDB Atlas (vector search).
  - Embeddings: `GoogleGenerativeAIEmbeddings` (modello di embedding tipico: `models/text-embedding-004` o variabile `GEMINI_EMBEDDING_MODEL`).
  - LLM: `ChatGoogleGenerativeAI` (es. `gemini-2.5-flash`).

- **Flusso dati**:
  1. Caricare PDF da `data/books/` (o da `DOCUMENTS_PATH` se si usa `index_documents.py`).
  2. Suddividere il testo in chunk (diversi script usano chunk size differenti: vedi sotto).
  3. Generare embedding e salvare in `chroma/` (locale) o in MongoDB Atlas (collezione configurata).
  4. In fase di query: ottenere k risultati di similarity, combinare il testo in `context`, inserire nel prompt template (`PROMPT_TEMPLATE`) e chiamare l'LLM.

- **File chiave & cosa fanno (comandi d'uso)**
  - `create_database.py`: crea il DB Chroma locale dai PDF in `data/books/`.
    - Comando: `python create_database.py`
  - `web_chatbot.py`: Flask web UI che usa `Chroma` locale e `ChatGoogleGenerativeAI`.
    - Comando: `python web_chatbot.py` -> visita `http://localhost:5000`.
  - `query_data.py`: interrogazione CLI che carica `chroma/` e invoca `gemini-2.5-flash`.
    - Comando: `python query_data.py "La tua domanda"`.
  - `index_documents.py`: versione che crea un vector store su MongoDB Atlas usando `langchain_mongodb`.
    - Comando: `python index_documents.py` (richiede variabili MongoDB in `.env`).
  - `create_mongo_rag.py`: script alternativo che estrae PDF e inserisce chunk + embedding direttamente in MongoDB.
  - `get_gemini_models.py`: lista i modelli disponibili con la API key corrente.

- **Variabili d'ambiente importanti** (file `.env` alla radice):
  - `GOOGLE_API_KEY` : API key Generative AI (usata da `get_gemini_models.py` e dallo SDK Google).
  - `GEMINI_EMBEDDING_MODEL` : nome del modello embedding (es. `models/text-embedding-004`).
  - `MONGODB_ATLAS_URI`, `MONGODB_DATABASE`, `MONGODB_COLLECTION`, `MONGODB_VECTOR_INDEX` : usate da `index_documents.py`.
  - Nota: `create_mongo_rag.py` usa `URI` come nome env per la stringa Mongo; questo è incoerente con `index_documents.py` — verifica o uniforma prima di eseguire.
  - `DOCUMENTS_PATH` : opzionale, percorso dei PDF per `index_documents.py`.

- **Convenzioni del progetto da rispettare**
  - Prompt template condiviso: `PROMPT_TEMPLATE` presente in `web_chatbot.py` e `query_data.py`. Quando costruisci prompt, usa lo stesso formato: contesto seguito dalla domanda.
  - Similarity threshold: `query_data.py` usa `SIMILARITY_THRESHOLD = 0.5` — non ridurla senza testare.
  - Chunking: diversi script usano parametri diversi:
    - `create_database.py`: chunk_size=300, overlap=100
    - `index_documents.py`: chunk_size=1000, overlap=200
    - `create_mongo_rag.py`: CHUNK_SIZE=500 (parole-based)
  - Metadata: i documenti salvati in MongoDB possono usare campi `metadata.source` o `metadata.source_file` a seconda dello script. Non assumere un singolo schema senza verificare lo script di lettura.

- **Dipendenze e setup rapido**
  - Installazione pacchetti: `pip install -r requirements.txt` (poi verifica pacchetti commentati in `requirements.txt`).
  - Popolare `.env` con le chiavi necessarie prima di eseguire gli script.

- **Verifiche e debug rapidi**
  - Controlla modelli disponibili: `python get_gemini_models.py`.
  - Ricreare Chroma: cancellare `chroma/` e lanciare `python create_database.py`.
  - Eseguire l'indicizzazione su MongoDB: `python index_documents.py` (assicurarsi che `MONGODB_ATLAS_URI` sia impostato).
  - Se ottieni errori di import dai loader, installa `langchain-community` e `langchain-text-splitters` (sono elencati in `requirements.txt`).

- **Piccoli accorgimenti per l'agente**
  - Non cambiare automaticamente nomi di env vars o schema della collection senza prima eseguire uno script di smoke-test: ci sono due back-end (Chroma vs MongoDB).
  - Quando modifichi chunking o soglie, aggiungi un breve script di confronto per misurare differenze sulla stessa query (smoke tests).
  - Mantieni il prompt template invariato a meno che non venga richiesto esplicitamente dall'autore del repo.

Se vuoi, posso adattare questo file per includere esempi di patch/template di test automatico o uniformare le variabili `.env` (es. sostituire `URI` con `MONGODB_ATLAS_URI`). Fammi sapere quali sezioni vuoi espandere.
