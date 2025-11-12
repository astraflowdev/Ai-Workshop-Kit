"""
Project 2: Chatbot with Memory
A chatbot that remembers your conversation!

This is how ChatGPT, Claude, and all modern chatbots work.
"""

from openai import OpenAI
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.config import Config

# Initialize OpenAI client
client = Config.get_openai_client()

print("=" * 60)
print("MEMORY CHATBOT - Project 2")
print("=" * 60)
print("I'll remember our entire conversation!")
print("Type 'quit' to exit\n")

# Message history - this is the memory!
messages = [
    {"role": "system", "content": "You are a helpful and friendly assistant."}
]

# Continuous conversation loop
while True:
    # Get user input
    user_input = input("You: ")

    # Exit condition
    if user_input.lower() in ["quit", "exit", "bye"]:
        print("\nAI: Goodbye! It was nice chatting with you!")
        break

    # Skip empty inputs
    if not user_input.strip():
        continue

    # Add user message to history
    messages.append({"role": "user", "content": user_input})

    try:
        # Get response (with full history!)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", messages=messages  # Full conversation sent
        )

        # Extract AI response
        ai_message = response.choices[0].message.content
        print(f"AI: {ai_message}\n")

        # Add AI response to history (important!)
        messages.append({"role": "assistant", "content": ai_message})

    except Exception as e:
        print(f"Error: {e}")
        # Remove the user message we just added since we got an error
        messages.pop()

print("\n" + "=" * 60)
print(f"Total messages in this conversation: {len(messages)}")
print("=" * 60)
