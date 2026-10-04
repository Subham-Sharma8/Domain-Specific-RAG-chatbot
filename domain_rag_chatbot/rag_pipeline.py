import os
import re
from pathlib import Path
from typing import List, Dict

from langchain_text_splitters import RecursiveCharacterTextSplitter
from groq import Groq

from document_loader import extract_pdf_pages
from vector_store import FAISSVectorStore
from prompt import build_prompt


class RAGPipeline:
    def __init__(self):
        self.embedding_model_name = os.getenv(
            "EMBEDDING_MODEL",
            "sentence-transformers/all-MiniLM-L6-v2"
        )
        self.llm_name = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
        self.chunk_size = int(os.getenv("CHUNK_SIZE", "900"))
        self.chunk_overlap = int(os.getenv("CHUNK_OVERLAP", "120"))
        self.top_k = int(os.getenv("TOP_K", "5"))
        self.min_similarity = float(os.getenv("MIN_SIMILARITY", "0.25"))

        self.vector_store = FAISSVectorStore(
            model_name=self.embedding_model_name,
            store_dir="vector_store/saved_index",
        )
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""],
        )

    def process_uploaded_files(self, uploaded_files) -> Dict:
        all_pages = []
        for uploaded_file in uploaded_files:
            all_pages.extend(
                extract_pdf_pages(uploaded_file, uploaded_file.name)
            )

        chunks: List[Dict] = []
        for page in all_pages:
            page_chunks = self.splitter.split_text(page["text"])
            for chunk_id, text in enumerate(page_chunks, start=1):
                clean = text.strip()
                if not clean:
                    continue
                chunks.append({
                    "document": page["document"],
                    "page": page["page"],
                    "chunk_id": chunk_id,
                    "text": clean,
                })

        self.vector_store.build(chunks)

        return {
            "documents": len(set(p["document"] for p in all_pages)),
            "pages": len(all_pages),
            "chunks": len(chunks),
        }

    def status(self) -> Dict:
        return {
            "ready": self.vector_store.index is not None and bool(self.vector_store.metadata),
            "chunks": len(self.vector_store.metadata),
        }

    def _answer_with_groq(self, prompt: str) -> str:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not configured. Add it to the .env file."
            )

        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model=self.llm_name,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Follow the grounding rules in the user prompt exactly. "
                        "Do not answer from outside knowledge."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0,
            max_tokens=700,
        )
        return response.choices[0].message.content.strip()

    def ask(self, question: str) -> Dict:
        retrieved = self.vector_store.search(question, top_k=self.top_k)

        if not retrieved or retrieved[0]["score"] < self.min_similarity:
            return {
                "answer": "I could not find this information in the uploaded documents.",
                "sources": retrieved,
            }

        # Keep the answer grounded in the strongest retrieved passages.
        prompt = build_prompt(question, retrieved)
        answer = self._answer_with_groq(prompt)

        # Extra guard: if the model returns an empty response, use the required fallback.
        if not answer:
            answer = "I could not find this information in the uploaded documents."

        return {
            "answer": answer,
            "sources": retrieved,
        }
