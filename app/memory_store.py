import faiss
import numpy as np
import json
import os

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class MemoryStore:
    def __init__(self):
        self.model = None

        self.dimension = 384

        self.index_path = "data/memory.index"
        self.texts_path = "data/memory.json"

        self.index = None
        self.texts = []

        self.memory_weights = {
            "identity": 10,
            "goal": 9,
            "preference": 7,
            "fact": 6,
            "reflection": 5,
            "conversation": 1
        }

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
    # MODEL
    # -------------------------
    def get_model(self):
        if self.model is None:
            print("Loading embedding model...")
            self.model = SentenceTransformer(
                "all-MiniLM-L6-v2",
                local_files_only=True
            )

        return self.model

    # -------------------------
    # MEMORY RANKING
    # -------------------------
    def importance_score(self, text, memory_type):
        text = text.lower()

        score = self.memory_weights.get(memory_type, 1)

        important_keywords = [
            "user owns",
            "user likes",
            "user works",
            "user lives",
            "user prefers",
            "user goal",
            "user is"
        ]

        for keyword in important_keywords:
            if keyword in text:
                score += 5

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

        new_embedding = self.get_model().encode([text])

        existing_embeddings = self.get_model().encode(
            [m["text"] for m in self.texts]
        )

        similarities = cosine_similarity(
            new_embedding,
            existing_embeddings
        )[0]

        best_similarity = max(similarities)

        return best_similarity >= threshold

    # -------------------------
    # ADD MEMORY
    # -------------------------
    def add(self, text, memory_type="fact"):
        text = text.strip()

        if len(text) < 5:
            return

        if self.memory_exists(text):
            print(f"⚠️ Skipping duplicate memory: {text}")
            return

        score = self.importance_score(text, memory_type)

        if score < -3:
            print(f"⚠️ Skipping low-value memory: {text}")
            return

        embedding = self.get_model().encode([text])

        self.index.add(
            np.array(embedding).astype("float32")
        )

        self.texts.append({
            "text": text,
            "type": memory_type,
            "score": score
        })

        self._save()

        print(f"✅ Memory stored [{memory_type}]: {text}")

        # -------------------------
    # SEARCH
    # -------------------------
    def search(self, query, k=10):
        if len(self.texts) == 0:
            return []

        query_embedding = self.get_model().encode([query])

        distances, indices = self.index.search(
            np.array(query_embedding).astype("float32"),
            k
        )

        results = []

        for idx, distance in zip(indices[0], distances[0]):

            if idx >= len(self.texts):
                continue

            if idx == -1:
                continue

            if distance > 1e20:
                continue

            memory = self.texts[idx]

            final_score = (
                memory["score"]
                - float(distance)
            )

            results.append({
                "text": memory["text"],
                "type": memory["type"],
                "distance": float(distance),
                "score": memory["score"],
                "final_score": final_score
            })

        results.sort(
            key=lambda x: x["final_score"],
            reverse=True
        )

        return results

    # -------------------------
    # RESET
    # -------------------------
    def reset(self):
        self.index = faiss.IndexFlatL2(self.dimension)
        self.texts = []

        self._save()

        print("🧠 Memory reset complete")