# Viva Questions and Answers

### 1. What is RAG?
Retrieval-Augmented Generation combines information retrieval with language generation. Relevant document passages are retrieved first and then supplied to the language model as context.

### 2. Why split documents into chunks?
Large documents are split so that smaller, semantically relevant passages can be retrieved efficiently and supplied to the model without sending the entire document.

### 3. What is an embedding?
An embedding is a numerical vector representation of text that captures semantic relationships so similar text can be compared mathematically.

### 4. What does FAISS store?
FAISS stores vectors and supports efficient similarity search. This project separately stores metadata such as document name and page number alongside the vectors.

### 5. How does cosine similarity help retrieval?
Cosine similarity measures the angle-based similarity between normalized vectors. Because this project normalizes embeddings and uses inner-product search, the score corresponds to cosine similarity.

### 6. Why can a RAG chatbot still produce an incorrect answer?
Retrieval can return irrelevant or incomplete chunks, and an LLM can generate unsupported text. Strong prompts, retrieval thresholds, source display and testing reduce this risk but do not eliminate it.

### 7. How do you test retrieval?
Ask questions with known source pages and compare the retrieved document/page against the expected source. The project includes a 15-question evaluation sheet.

### 8. What happens when the answer is not present?
The application returns: "I could not find this information in the uploaded documents."

### 9. Why is page metadata important?
It allows users to trace an answer back to the original PDF page.

### 10. Why use overlap in chunking?
Overlap helps preserve context when an important sentence or concept crosses a chunk boundary.

### 11. Why use all-MiniLM-L6-v2?
It is a compact pretrained sentence-embedding model suitable for a beginner-friendly semantic search system.

### 12. Why use FAISS?
FAISS provides a practical local vector similarity search implementation and is explicitly suggested in the project guidance.

### 13. Why use temperature 0?
A low/zero temperature reduces unnecessary variation in generated answers and is appropriate for grounded document QA.

### 14. Why are API keys kept in .env?
Keeping keys outside source code reduces the chance of accidentally exposing secrets in GitHub.

### 15. What is the main limitation?
The baseline version works with text-based PDFs. Scanned PDFs require an OCR extension.
