import faiss
import numpy as np
import json
import os

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class MemoryStore:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        self.dimension = 384

        self.index_path = "data/memory.index"
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
            print("🆕 Creating new memory store...")

            self.index = faiss.IndexFlatL2(self.dimension)
            self.texts = []

    # -------------------------
    # SAVE
    # -------------------------
    def _save(self):
        faiss.write_index(self.index, self.index_path)

        with open(self.texts_path, "w") as f:
            json.dump(self.texts, f, indent=2)

    # -------------------------
    # MEMORY RANKING
    # -------------------------
    def importance_score(self, text):
        text = text.lower()

        score = 0

        # durable user facts
        important_keywords = [
            "user owns",
            "user likes",
            "user works",
            "user lives",
            "user is",
            "user has"
        ]

        for keyword in important_keywords:
            if keyword in text:
                score += 10

        # temporary conversation
        weak_keywords = [
            "hello",
            "hi",
            "thanks",
            "agent:"
        ]

        for keyword in weak_keywords:
            if keyword in text:
                score -= 5

        return score

    # -------------------------
    # DUPLICATE CHECK
    # -------------------------
    def memory_exists(self, text, threshold=0.92):
        if len(self.texts) == 0:
            return False

        new_embedding = self.model.encode([text])

        existing_embeddings = self.model.encode(self.texts)

        similarities = cosine_similarity(
            new_embedding,
            existing_embeddings
        )[0]

        best_similarity = max(similarities)

        return best_similarity >= threshold

    # -------------------------
    # ADD MEMORY
    # -------------------------
    def add(self, text):
        text = text.strip()

        if len(text) < 5:
            return

        # deduplication
        if self.memory_exists(text):
            print(f"⚠️ Skipping duplicate memory: {text}")
            return

        score = self.importance_score(text)

        # skip low-value memories
        if score < -3:
            print(f"⚠️ Skipping low-value memory: {text}")
            return

        embedding = self.model.encode([text])

        self.index.add(
            np.array(embedding).astype("float32")
        )

        self.texts.append(text)

        self._save()

        print(f"✅ Memory stored: {text}")

    # -------------------------
    # SEARCH
    # -------------------------
    def search(self, query, k=6):
        if len(self.texts) == 0:
            return []

        query_embedding = self.model.encode([query])

        distances, indices = self.index.search(
            np.array(query_embedding).astype("float32"),
            k
        )

        results = []

        for idx, distance in zip(indices[0], distances[0]):
            if idx < len(self.texts):
                results.append(
                    (self.texts[idx], float(distance))
                )

        return results

    # -------------------------
    # RESET MEMORY
    # -------------------------
    def reset(self):
        self.index = faiss.IndexFlatL2(self.dimension)
        self.texts = []

        self._save()

        print("🧠 Memory reset complete")