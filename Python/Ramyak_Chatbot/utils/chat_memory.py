# utils/chat_memory.py
# Stores recent conversation for context

class ChatMemory:
    def __init__(self, max_memory=5):
        self.max_memory = max_memory
        self.messages = []

    def add_message(self, role, content):
        if len(self.messages) >= self.max_memory:
            self.messages.pop(0)
        self.messages.append(f"{role}: {content}")

    def get_context(self):
        return "\n".join(self.messages) + "\nAI:"
