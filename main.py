from anthropic import Anthropic
from dotenv import load_dotenv
from chatbot import Chatbot
from streaming_chatbot import StreamingChatbot
from vision import summarize_paper
import asyncio
import os


# EXERCISE 0
# ----------
# How to interact with Claude
def exercise_zero(client):
    print("Exercise 0:\n-----------")
    first_msg = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": "Hi there! Please tell me a joke"}
        ]
    )
    print(first_msg.content[0].text)
# ----------


# EXERCISE 1
# ----------
def translate(client, word, language):
    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=100,
        messages=[
            {"role": "user", "content": f"Translate the word {word} into {language}. Respond with only the translated word."}
        ]
    )
    print(f"The {language} word for \"{word}\" is:", response.content[0].text)

def exercise_one(client):
    print("Exercise 1:\n-----------")
    translate(client, "hello", "Spanish")
    translate(client, "chicken", "Italian")
# ----------


# EXERCISE 2
# ----------
# Interact with chatbot
def exercise_two():
    print("Exercise 2:\n-----------")

    claude = Chatbot()
    user_active = True
    while (user_active):
        query = input("Enter your message here (or type 'quit' to quit): ")
        if (query == "quit"):
            user_active = False
        else:
            claude.speak(query)
# ----------


# EXERCISE 3
# ----------
def generate_questions(client, topic, num_questions):
    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1000,
        system=f"You are an expert in {topic} and always responde with a numbered list.",
        stop_sequences=[f"{num_questions + 1}"],
        messages=[
            {"role": "user", "content": f"Give me {num_questions} thought-provoking questions about {topic}."}
        ]
    )
    print(response.content[0].text)

def exercise_four_params(client):
    print("Exercise 4:\n-----------")
    generate_questions(client, "software engineering", 3)
    print("\n\n")
    generate_questions(client, "national defense", 4)
    print("\n\n")
    generate_questions(client, "unmanned aerial vehicles", 6)
# ----------


# STREAMING
def streaming(client):
    stream = client.messages.create(
        messages=[
            {
                "role": "user",
                "content": "How do large language models work?",
            }
        ],
        model="claude-3-haiku-20240307",
        max_tokens=1000,
        temperature=0,
        stream=True
    )

    for event in stream:
        if event.type == "content_block_delta":
            print(event.delta.text, flush=True, end="")


# EXERCISE 5
# ----------
async def exercise_five():
    cyan = "\033[96m"
    reset = "\033[0m"
    claude = StreamingChatbot()

    print("Welcome to the Claude ChatBot!\nType 'quit' to exit the chat.")
    while True:
        query = input(cyan + "You: " + reset)
        if query == "quit":
            print("\n\nThanks for chatting!")
            break
        await claude.speak(query)
# ----------


if __name__ == "__main__":
    load_dotenv()
    client = Anthropic()

    #exercise_zero(client)
    #exercise_one(client)
    #exercise_two()
    #exercise_four_params(client)
    #streaming(client)
    #asyncio.run(exercise_five())
    summarize_paper()