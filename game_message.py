class MessageHolder:
    def __init__(self):
        self.game_messages = []

    def append(self, message):
        self.game_messages.append(message)

    def flush(self):
        messages = list(self.game_messages)
        self.game_messages = []
        return messages
