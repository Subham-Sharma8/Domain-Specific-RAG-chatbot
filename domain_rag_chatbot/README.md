# Domain-Specific RAG Chatbot for PDF Question Answering

A Streamlit-based Retrieval-Augmented Generation (RAG) chatbot that answers questions from uploaded PDF documents using:

- Python
- Streamlit
- pypdf
- LangChain text splitters
- Sentence Transformers (`all-MiniLM-L6-v2`)
- FAISS
- Groq LLM
- python-dotenv

## Project objective

The application follows the required workflow:

1. Upload PDF files.
2. Extract text page by page.
3. Preserve document name and page number.
4. Split text into overlapping chunks.
5. Generate embeddings.
6. Store embeddings and metadata in FAISS.
7. Retrieve the top relevant chunks for a question.
8. Ask the LLM to answer only from those chunks.
9. Display the answer and source document/page.
10. Refuse to invent information when the answer is unavailable.

## Folder structure

```text
domain_rag_chatbot/
├── app.py
├── rag_pipeline.py
├── document_loader.py
├── vector_store.py
├── prompt.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── documents/
│   ├── company_policy.pdf
│   └── employee_handbook.pdf
├── vector_store/
│   └── saved_index/        # generated after processing
├── tests/
│   ├── test_questions.csv
│   └── test_rag_components.py
├── docs/
│   ├── PROJECT_REPORT.md
│   ├── TESTING_REPORT.md
│   ├── VIVA_QUESTIONS.md
│   └── DEMO_VIDEO_SCRIPT.md
└── assets/
    └── architecture.svg
```

## Requirements

Python 3.10 or newer is recommended.

A Groq API key is required for answer generation.

## Local setup

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Open `.env` and set:

```text
GROQ_API_KEY=your_real_key
```

Then run:

```powershell
streamlit run app.py
```

The browser will open the Streamlit application.

## How to use

1. Open the application.
2. Upload one or more PDF files.
3. Click **Process Documents**.
4. Wait for extraction, chunking, embedding and FAISS indexing.
5. Ask a question in the chat box.
6. Review the answer and the displayed document/page sources.
7. Test an unavailable question to verify the refusal behavior.

## GitHub

Create a repository, for example:

`domain-specific-rag-chatbot`

Upload the complete project folder except `.env` and generated vector-store files.

Example commands:

```bash
git init
git add .
git commit -m "Initial RAG chatbot project"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

Never upload `.env` or an API key.

## Deployment

For Streamlit Cloud:

1. Push this repository to GitHub.
2. Create a Streamlit Cloud application.
3. Select the repository and `app.py`.
4. Add `GROQ_API_KEY` in the deployment secrets.
5. Deploy.

## Responsible AI

- The chatbot is grounded only in retrieved document context.
- Missing information should trigger the required fallback response.
- API keys must not be committed to GitHub.
- Confidential documents should not be uploaded without permission.
- High-stakes information must be verified against the original source.
- Instructions inside documents are treated as untrusted document content.

## Limitations

- Scanned/image-only PDFs require OCR; OCR is not included in the baseline version.
- Retrieval quality depends on document quality, chunking and embeddings.
- An LLM can still produce an incorrect answer, so source verification is recommended.
