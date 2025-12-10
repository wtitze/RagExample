# RagExample

**Chatbot RAG (Retrieval-Augmented Generation) con MongoDB come database vettoriale**

## Scopo del progetto

Questo progetto è un esempio didattico / prototipo che mostra come costruire un sistema RAG completo, basato su:

- **MongoDB Atlas** come database vettoriale per indicizzare e recuperare documenti;
- **Google Generative AI (modelli Gemini)** per la generazione delle risposte;
- **LangChain** per la gestione del retriever e della catena di generazione;
- **Python / Flask** per l’interfaccia web.

Il progetto consente di interrogare documenti tramite domande in linguaggio naturale e ottenere risposte generate dal modello, basate sui documenti recuperati.

---

## Stato del progetto

- La **parte a terminale** (`rag_chain.py`) funziona correttamente: è possibile inserire domande, ottenere la risposta RAG e visualizzare le fonti dei documenti.
- La **parte webapp** (`app.py` + `index.html`) è ancora in fase di codifica e **non funziona completamente**: lo streaming della risposta e la visualizzazione delle fonti non sono ancora operative.

---

## Struttura del progetto

```
RagExample/
├─ app.py                # Server Flask e webapp
├─ rag_chain.py          # Logica RAG per l’esecuzione da terminale
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

Esempio installazione:

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

## Uso

### Terminale

Eseguire lo script `rag_chain.py`:

```bash
python rag_chain.py
```

- Inserire domande a terminale.  
- Il sistema recupera i documenti più rilevanti dal database vettoriale e genera la risposta con Gemini.  
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
- Il progetto è un prototipo, utile come base per futuri sviluppi e per sperimentare RAG con LLM.

---

## Licenza

Open-source, uso libero a fini didattici o di prototipazione.
