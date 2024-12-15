from anthropic import Anthropic
from dotenv import load_dotenv

class Chatbot:
    def __init__(self):
        self.history = []

        load_dotenv()
        self.client = Anthropic()

    def speak(self, user_msg):
        # Add next user question to chat history
        self.history.append({"role": "user", "content": user_msg})

        # Fetch and print response
        response = self.client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=500,
            messages=self.history
        )
        print(response.content[0].text)

        # Store response in history
        self.history.append({"role": "assistant", "content": response.content[0].text})