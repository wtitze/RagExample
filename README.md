# RagExample

**Chatbot RAG (Retrieval-Augmented Generation) con MongoDB come database vettoriale**

## Scopo del progetto

Questo progetto mostra come costruire un sistema RAG completo basato su:

- **MongoDB Atlas** come database vettoriale per indicizzare e recuperare documenti;
- **Google Generative AI (modelli Gemini)** per la generazione delle risposte;
- **LangChain** per la gestione del retriever e della catena di generazione;
- **Python / Flask** per l’interfaccia web.

Il progetto permette di interrogare documenti tramite domande in linguaggio naturale e ottenere risposte basate sui documenti recuperati.

---

## Stato del progetto

- La **parte a terminale** (`rag_chain.py`) funziona correttamente: inserendo domande, il sistema restituisce la risposta RAG e le fonti dei documenti.
- La **parte webapp** (`app.py` + `templates/index.html`) è ancora in fase di sviluppo e **non funziona completamente**: lo streaming della risposta e la visualizzazione delle fonti non sono operativi.

---

## Struttura del progetto

```
RagExample/
├─ app.py                # Server Flask e webapp
├─ rag_chain.py          # Logica RAG da terminale
├─ index_documents.py    # Script per creare l'indice vettoriale su MongoDB
├─ data/books/           # Documenti da indicizzare
├─ templates/
│   └─ index.html        # Interfaccia web (in sviluppo)
├─ .env                  # Variabili ambiente: MongoDB, Gemini
├─ requirements.txt      # Dipendenze Python
└─ README.md             # Questo file
```

---

## Setup e prerequisiti

- Python 3.12+  
- Account MongoDB Atlas con cluster e credenziali valide  
- API Key Google Generative AI attiva  
- Virtual environment consigliato  

Installazione:

```bash
git clone https://github.com/wtitze/RagExample.git
cd RagExample
python -m venv .venv
source .venv/bin/activate        # Linux/Mac
# .venv\Scripts\activate         # Windows
pip install -r requirements.txt
```

Creare il file `.env` con le variabili necessarie:

```
MONGODB_ATLAS_URI="mongodb+srv://<USER>:<PASSWORD>@<CLUSTER>.mongodb.net/?retryWrites=true&w=majority"
MONGODB_DATABASE=<nome_database>
MONGODB_COLLECTION=<nome_collezione>
MONGODB_VECTOR_INDEX=<nome_index>
GEMINI_EMBEDDING_MODEL=<modello_embedding>
GEMINI_LLM_MODEL=<modello_llm>
```

---

## Creazione dell’indice vettoriale

0. Creare un indice (vuoto) per la ricerca vettoriale sul proprio database MongoDB (sarà poi ripemito con gli embeddings)
1. Inserire i documenti (PDF) in `data/books/`.
2. Eseguire lo script per creare l’indice vettoriale su MongoDB (inserisce gli embeddings nell'indice):

```bash
python index_documents.py
```

3. Dopo questo passaggio, il database vettoriale è pronto per essere interrogato.

---

## Uso

### Terminale

Eseguire `rag_chain.py`:

```bash
python rag_chain.py
```

- Inserire domande al terminale.  
- Il sistema recupera i documenti più rilevanti dal database vettoriale e genera la risposta.  
- Le fonti vengono stampate subito dopo la risposta.

### Webapp

- La webapp (`app.py` + `templates/index.html`) è **ancora in sviluppo**.  
- Può essere avviata con:

```bash
python app.py
```

- Aprire il browser su `http://localhost:5000`.  
- Attualmente lo streaming della risposta e la visualizzazione delle fonti non sono completamente funzionanti.

---

## Note

- La funzionalità completa è disponibile solo a terminale.  
- MongoDB viene utilizzato come database vettoriale per supportare retrieval e similarity search.  
- Il progetto è un prototipo, utile come base per futuri sviluppi e sperimentazioni RAG.

---

## Licenza

Open-source, uso libero a fini didattici o di prototipazione.
