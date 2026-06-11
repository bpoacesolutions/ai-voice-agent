class AgentBrain:

    def __init__(self, memory_store):
        self.memory_store = memory_store

    # -------------------------
    # MEMORY RETRIEVAL
    # -------------------------
    def retrieve_memory(self, query):

        raw_memory = self.memory_store.search(
            query,
            k=10
        )

        identity_memories = []
        goal_memories = []
        preference_memories = []
        fact_memories = []
        reflection_memories = []

        print("\n--- Memory Retrieval ---")

        for memory in raw_memory:

            text = memory["text"]
            memory_type = memory["type"]
            distance = memory["distance"]
            final_score = memory["final_score"]

            print(
                f"[{memory_type}] "
                f"score={final_score:.2f} "
                f"distance={distance:.2f} "
                f"{text}"
            )

            # discard weak memories
            if final_score < 0:
                continue

            if memory_type == "identity":
                identity_memories.append(text)

            elif memory_type == "goal":
                goal_memories.append(text)

            elif memory_type == "preference":
                preference_memories.append(text)

            elif memory_type == "fact":
                fact_memories.append(text)

            elif memory_type == "reflection":
                reflection_memories.append(text)

        print("------------------------\n")

        return {
            "identity": identity_memories[:3],
            "goal": goal_memories[:3],
            "preference": preference_memories[:3],
            "fact": fact_memories[:5],
            "reflection": reflection_memories[:3]
        }

    # -------------------------
    # REFLECTION VALIDATION
    # -------------------------
    def validate_reflection(self, reflection):

        reflection = reflection.lower()

        banned_patterns = [
            "work-life balance",
            "likely",
            "probably",
            "maybe",
            "possibly"
        ]

        for pattern in banned_patterns:
            if pattern in reflection:
                return False

        if len(reflection) > 120:
            return False

        return True

    # -------------------------
    # PROMPT BUILDER
    # -------------------------
    def build_prompt(self, query, memory, history):

        history_text = "\n".join(history[-4:])

        identity_text = "\n".join(
            memory.get("identity", [])
        )

        goal_text = "\n".join(
            memory.get("goal", [])
        )

        preference_text = "\n".join(
            memory.get("preference", [])
        )

        fact_text = "\n".join(
            memory.get("fact", [])
        )

        reflection_text = "\n".join(
            memory.get("reflection", [])
        )

        return f"""
You are a helpful AI assistant.

Use memory only when relevant.

IDENTITY:
{identity_text}

GOALS:
{goal_text}

PREFERENCES:
{preference_text}

FACTS:
{fact_text}

REFLECTIONS:
{reflection_text}

RECENT CONVERSATION:
{history_text}

User:
{query}

Assistant:
"""