import faiss
import numpy as np
import os
import json
from sentence_transformers import SentenceTransformer

class MemoryStore:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.dimension = 384

        self.index_path = "data/faiss.index"
        self.texts_path = "data/memory.json"

        self.index = None
        self.texts = []

        self._load_or_initialize()

    # -------------------------
    # INIT / LOAD
    # -------------------------
    def _load_or_initialize(self):
        os.makedirs("data", exist_ok=True)

        if os.path.exists(self.index_path) and os.path.exists(self.texts_path):
            print("🔁 Loading memory from disk...")
            self.index = faiss.read_index(self.index_path)

            with open(self.texts_path, "r") as f:
                self.texts = json.load(f)
        else:
            print("Creating new memory store...")
            self.index = faiss.IndexFlatL2(self.dimension)
            self.texts = []

    # -------------------------
    # SAVE
    # -------------------------
    def _save(self):
        faiss.write_index(self.index, self.index_path)

        with open(self.texts_path, "w") as f:
            json.dump(self.texts, f)

    # -------------------------
    # ADD MEMORY
    # -------------------------
    def add(self, text):
        embedding = self.model.encode([text])
        self.index.add(np.array(embedding).astype("float32"))
        self.texts.append(text)

        self._save()  # persist immediately

    # -------------------------
    # SEARCH MEMORY
    # -------------------------
    def search(self, query, k=3):
        if len(self.texts) == 0:
            return []

        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(
            np.array(query_embedding).astype("float32"), k
        )

        results = []

        for i, idx in enumerate(indices[0]):
            if idx < len(self.texts):
                score = distances[0][i]
                results.append((self.texts[idx], score))

        return results