"""
Project 1: Basic Chatbot
Your first AI-powered application!

This is the "Hello World" of AI development - 10 lines of code that talk to GPT.
"""

from openai import OpenAI
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.config import Config

# Initialize OpenAI client
client = Config.get_openai_client()

print("=" * 60)
print("BASIC CHATBOT - Project 1")
print("=" * 60)
print("Ask me anything! (Type your question and press Enter)\n")

# Get user input
user_message = input("You: ")

# Make the API call
response = client.chat.completions.create(
    model="gpt-3.5-turbo",  # Which AI to use
    temperature=0.7,  # Creativity level (0.0-2.0)
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant",
        },  # Personality
        {"role": "user", "content": user_message},  # User's question
    ],
)

# Print the response
print("AI:", response.choices[0].message.content)

print("\n" + "=" * 60)
print("That's it! You just talked to GPT with 10 lines of code!")
print("=" * 60)
