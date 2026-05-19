class AgentBrain:
    def __init__(self, memory_store):
        self.memory_store = memory_store

    # -------------------------
    # MEMORY RETRIEVAL
    # -------------------------
    def retrieve_memory(self, query):
        raw_memory = self.memory_store.search(query, k=8)

        filtered_memory = []

        for text, memory_type, distance in raw_memory:

            # reflections are more valuable
            threshold = 1.8 if memory_type == "reflection" else 1.5

            if distance < threshold:
                filtered_memory.append(text)

        # fallback if filtering removes everything
        if len(filtered_memory) == 0:
            filtered_memory = [
                text for text, _, _ in raw_memory[:3]
            ]

        return filtered_memory

    # -------------------------
    # PROMPT CONSTRUCTION
    # -------------------------
    def build_prompt(self, query, memory, history):
        memory_text = "\n".join(memory)

        history_text = "\n".join(history[-4:])

        return f"""
You are a helpful AI assistant.

Use the user's long-term memory
and conversation history to answer accurately.

Long-term memory:
{memory_text}

Conversation history:
{history_text}

User question:
{query}

Rules:
- Use memory when relevant
- Be concise
- Do not invent facts
- If memory contains the answer, prioritize it

Answer:
"""