# Chatbot RAG con Gemini e Gecko Embeddings

Questo progetto è un esempio di **retrieval-augmented generation (RAG)** usando i modelli **Gemini 2.5** e gli embedding **Gecko** di Google Generative AI, integrato in Python con **LangChain** e una semplice interfaccia web tramite **Flask**.

---

## 📂 Struttura del progetto

```
project/
├─ app.py               # Chatbot Flask
├─ create_database.py   # Script per creare il database Chroma dai PDF
├─ query_data.py        # Script per interrogare il database via CLI
├─ data/books/          # Cartella con i PDF da indicizzare
├─ chroma/              # Database vettoriale generato
├─ templates/           # Template HTML per Flask
│   └─ index.html
├─ .env                 # Chiavi API (GOOGLE_API_KEY)
```

---

## ⚡ Requisiti

* Python 3.12+
* pacchetti Python:

```bash
pip install flask langchain langchain-chroma langchain-google-genai chromadb python-dotenv
```

* **API Key** Google Generative AI, salvata in `.env`:

```
GOOGLE_API_KEY="la_tua_chiave_api"
```

---

## 🏗️ Creare il database vettoriale

1. Metti i PDF da indicizzare in `data/books/`.
2. Esegui:

```bash
python create_database.py
```

Questo creerà il database Chroma in `chroma/`, pronto per le query.

---

## 🔍 Interrogare il database da CLI

Esempio:

```bash
python query_data.py "Cos'è AI Engineering?"
```

Lo script:

* Cerca i chunk più simili alla query
* Genera il contesto
* Chiede al modello Gemini 2.5 Flash di rispondere basandosi solo sul contesto
* Mostra risposta e fonti

---

## 🌐 Chatbot web con Flask

1. Esegui il server Flask:

```bash
python app.py
```

2. Apri il browser su:

```
http://localhost:5000
```

3. Scrivi una domanda e ricevi la risposta generata dal tuo modello RAG.

---

## 📌 Note importanti

* I modelli supportati dal tuo account possono cambiare. Controlla i modelli disponibili con:

```python
from google.generativeai import client
client.configure(api_key="LA_TUA_API_KEY")
print(client.list_models())
```

* Per le embedding, assicurati di usare un modello che supporti `embedText`.
* Soglia di similarità nei tuoi script: **0.5** consigliata per query in italiano.

---

## 🔗 Risorse utili

* [LangChain](https://github.com/hwchase17/langchain)
* [LangChain Chroma](https://pypi.org/project/langchain-chroma/)
* [Google Generative AI](https://developers.generativeai.google)
* [Gemini Models Documentation](https://developers.generativeai.google/models)

---

## 📜 Licenza

Progetto open source per scopi educativi e
