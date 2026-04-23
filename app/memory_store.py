import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class MemoryStore:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.dimension = 384

        self.index = faiss.IndexFlatL2(self.dimension)
        self.texts = []

    def add(self, text):
        embedding = self.model.encode([text])
        self.index.add(np.array(embedding).astype("float32"))
        self.texts.append(text)

    def search(self, query, k=3):
        if len(self.texts) == 0:
            return []

        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(
            np.array(query_embedding).astype("float32"), k
        )

        results = []
        for idx in indices[0]:
            if idx < len(self.texts):
                results.append(self.texts[idx])

        return results