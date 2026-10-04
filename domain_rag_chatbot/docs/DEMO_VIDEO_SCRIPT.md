# Demonstration Video Script

## 0:00–0:30 — Introduction
"Hello, this is my Domain-Specific RAG Chatbot for PDF Question Answering. The system lets a user upload documents and ask questions in natural language."

## 0:30–1:00 — Explain workflow
Show the architecture diagram and explain:
PDF → extraction → chunking → embeddings → FAISS → retrieval → LLM → answer and sources.

## 1:00–1:45 — Upload documents
Open the Streamlit application. Upload `company_policy.pdf` and `employee_handbook.pdf`. Click Process Documents.

## 1:45–2:30 — Correct question
Ask:
"What is the standard leave entitlement?"
Show the answer and the source document/page.

## 2:30–3:00 — Second document
Ask:
"How is attendance recorded?"
Show that the handbook source is displayed.

## 3:00–3:30 — Unavailable question
Ask:
"Who is the current company CEO?"
Show the required fallback:
"I could not find this information in the uploaded documents."

## 3:30–4:00 — Explain implementation
Briefly show `document_loader.py`, `vector_store.py`, `rag_pipeline.py`, `prompt.py` and `app.py`.

## 4:00–4:30 — GitHub and conclusion
Show the GitHub repository and README. Explain that `.env` is excluded and the project contains the required source code, sample documents, testing sheet and documentation.
