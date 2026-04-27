class UserProfile:
    def __init__(self):
        self.profile = {}

    def update(self, info: dict):
        for key, value in info.items():
            self.profile[key] = value

    def get_context(self):
        if not self.profile:
            return "No user profile yet."

        lines = []
        for key, value in self.profile.items():
            lines.append(f"{key}: {value}")

        return "\n".join(lines)