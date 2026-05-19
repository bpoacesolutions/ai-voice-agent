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
                loaded_texts = json.load(f)

            # ---- migration safety ----
            self.texts = []

            for item in loaded_texts:
                # old format: plain string
                if isinstance(item, str):
                    self.texts.append({
                        "text": item,
                        "type": "fact"
                    })

                # new format: dict
                elif isinstance(item, dict):
                    self.texts.append(item)

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
    def importance_score(self, text, memory_type="fact"):
        text = text.lower()

        score = 0

        # ---- reflection memories are valuable ----
        if memory_type == "reflection":
            score += 15

        # durable user facts
        important_keywords = [
            "user owns",
            "user likes",
            "user works",
            "user lives",
            "user is",
            "user has",
            "user enjoys",
            "user prefers"
        ]

        for keyword in important_keywords:
            if keyword in text:
                score += 10

        # weak / noisy conversation
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

        # ---- deduplication ----
        if self.memory_exists(text):
            print(f"⚠️ Skipping duplicate memory: {text}")
            return

        score = self.importance_score(
            text,
            memory_type
        )

        # ---- skip low-value memory ----
        if score < -3:
            print(f"⚠️ Skipping low-value memory: {text}")
            return

        embedding = self.get_model().encode([text])

        self.index.add(
            np.array(embedding).astype("float32")
        )

        self.texts.append({
            "text": text,
            "type": memory_type
        })

        self._save()

        print(f"✅ Memory stored [{memory_type}]: {text}")

    # -------------------------
    # SEARCH
    # -------------------------
    def search(self, query, k=6):
        if len(self.texts) == 0:
            return []

        query_embedding = self.get_model().encode([query])

        distances, indices = self.index.search(
            np.array(query_embedding).astype("float32"),
            k
        )

        results = []

        for idx, distance in zip(indices[0], distances[0]):
            if idx < len(self.texts):
                results.append(
                    (
                        self.texts[idx]["text"],
                        self.texts[idx]["type"],
                        float(distance)
                    )
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

    # -------------------------
    # MODEL LOADER
    # -------------------------
    def get_model(self):
        if self.model is None:
            print("Loading embedding model...")
            self.model = SentenceTransformer(
                "all-MiniLM-L6-v2"
            )

        return self.model