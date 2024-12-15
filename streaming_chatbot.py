from anthropic import AsyncAnthropic
from dotenv import load_dotenv

class StreamingChatbot:
    def __init__(self):
        self.green = "\033[92m"
        self.reset = "\033[0m"
        self.history = []

        load_dotenv()
        self.client = AsyncAnthropic()


    async def speak(self, user_msg):
        # Add next user question to chat history
        self.history.append({"role": "user", "content": user_msg})

        # Print streaming response
        print(self.green + "Claude: " + self.reset, end="")
        async with self.client.messages.stream(
            max_tokens=1024,
            messages=self.history,
            model="claude-3-haiku-20240307"
        ) as stream:
            async for text in stream.text_stream:
                print(text, end="", flush=True)
        print("")

        # Store complete response in history
        final_msg = await stream.get_final_message()
        self.history.append({"role": "assistant", "content": final_msg.content[0].text})