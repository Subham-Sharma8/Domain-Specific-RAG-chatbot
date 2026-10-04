from pathlib import Path
from typing import Dict, List
import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


class FAISSVectorStore:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
                 store_dir: str = "vector_store/saved_index"):
        self.model_name = model_name
        self.store_dir = Path(store_dir)
        self.store_dir.mkdir(parents=True, exist_ok=True)
        self.index_path = self.store_dir / "index.faiss"
        self.metadata_path = self.store_dir / "metadata.pkl"
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.metadata: List[Dict] = []
        self.load()

    def build(self, chunks: List[Dict]) -> int:
        if not chunks:
            raise ValueError("No text chunks were produced.")

        texts = [c["text"] for c in chunks]
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False,
            convert_to_numpy=True,
        ).astype("float32")

        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(embeddings)
        self.metadata = chunks
        self.save()
        return len(chunks)

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        if self.index is None or not self.metadata:
            raise RuntimeError("Vector store is empty. Process documents first.")

        query_embedding = self.model.encode(
            [query],
            normalize_embeddings=True,
            show_progress_bar=False,
            convert_to_numpy=True,
        ).astype("float32")

        k = min(top_k, len(self.metadata))
        scores, indices = self.index.search(query_embedding, k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0:
                continue
            item = dict(self.metadata[int(idx)])
            item["score"] = float(score)
            results.append(item)
        return results

    def save(self) -> None:
        if self.index is not None:
            faiss.write_index(self.index, str(self.index_path))
            with open(self.metadata_path, "wb") as f:
                pickle.dump(self.metadata, f)

    def load(self) -> None:
        if self.index_path.exists() and self.metadata_path.exists():
            self.index = faiss.read_index(str(self.index_path))
            with open(self.metadata_path, "rb") as f:
                self.metadata = pickle.load(f)

    def clear(self) -> None:
        self.index = None
        self.metadata = []
        for path in (self.index_path, self.metadata_path):
            if path.exists():
                path.unlink()
