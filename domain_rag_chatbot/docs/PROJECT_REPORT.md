# Project Report
## Domain-Specific RAG Chatbot for PDF Question Answering

### 1. Introduction
The project implements a document-grounded chatbot that allows users to upload PDF documents and ask questions in natural language. The system retrieves relevant passages and uses them as context for answer generation.

### 2. Problem Statement
Large documents are difficult to search manually. A user may need to read many pages to find one answer. The proposed system reduces this effort by providing natural-language question answering over uploaded documents.

### 3. Objectives
- Extract text from PDF documents.
- Preserve document and page metadata.
- Split documents into manageable overlapping chunks.
- Convert chunks into embeddings.
- Store embeddings in FAISS.
- Retrieve relevant passages for each question.
- Generate answers using retrieved context.
- Display document and page sources.
- Refuse to invent answers when information is unavailable.
- Provide a usable Streamlit interface.

### 4. Scope
The baseline application supports text-based PDFs and multiple uploaded documents. OCR for scanned PDFs, authentication and advanced conversation memory are optional extensions.

### 5. Technology Stack
| Component | Technology |
|---|---|
| Language | Python |
| UI | Streamlit |
| PDF extraction | pypdf |
| Chunking | LangChain text splitters |
| Embeddings | Sentence Transformers all-MiniLM-L6-v2 |
| Vector database | FAISS |
| LLM | Groq |
| Environment variables | python-dotenv |
| Testing | pytest |
| Version control | Git/GitHub |

### 6. Architecture
The architecture is:

PDF Upload → PDF Extraction → Chunking → Embeddings → FAISS Vector Store → Query Embedding → Similarity Retrieval → Grounded Prompt → LLM → Answer + Sources

See `assets/architecture.svg`.

### 7. Modules
#### Document Upload
Accepts one or multiple PDF files, validates the extension and limits each file to 15 MB.

#### Text Extraction
Reads each PDF page with pypdf and preserves the filename and page number.

#### Chunking
Uses recursive character splitting with a 900-character chunk size and 120-character overlap.

#### Embedding and Vector Store
Uses the pretrained `all-MiniLM-L6-v2` embedding model and FAISS inner-product similarity with normalized embeddings.

#### Retrieval
Retrieves the top five most similar chunks.

#### Answer Generation
The prompt explicitly instructs the LLM to answer only from supplied context and to use the required fallback when information is unavailable.

#### User Interface
Streamlit provides upload controls, processing controls, chat history, source display and status information.

### 8. Security and Responsible AI
API keys are kept in `.env` and ignored by Git. Uploaded document instructions cannot change the system's grounding rules. Users are warned to verify high-stakes information.

### 9. Testing
Testing includes component tests and a 15-question evaluation sheet covering correct retrieval, answer grounding and unavailable information.

### 10. Limitations
- Scanned PDFs need OCR.
- Retrieval quality depends on embedding and chunking choices.
- Generated answers should be verified against source documents.
- The baseline application is intended for a student project and not as a replacement for professional document-management controls.

### 11. Future Enhancements
- OCR for scanned documents.
- Document collection filters.
- Conversation memory.
- Authentication and access control.
- Feedback buttons.
- FastAPI backend.
- Docker deployment.
- Automated retrieval/groundedness evaluation.

### 12. Conclusion
The project demonstrates the complete beginner-friendly RAG workflow specified in the project guidance: document ingestion, page-aware extraction, chunking, embeddings, FAISS retrieval, grounded LLM generation, source display and Streamlit deployment.
