"""
Variation: Pirate Bot
A chatbot that talks like a pirate captain!
"""

from openai import OpenAI
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from utils.config import Config

client = Config.get_openai_client()

print("🏴‍☠️ " + "=" * 60)
print("PIRATE BOT - Arrr matey!")
print("=" * 60 + " 🏴‍☠️\n")

user_message = input("You: ")

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    temperature=0.9,  # Higher for more creative/fun responses
    messages=[
        {
            "role": "system",
            "content": "You are a pirate captain. Always talk like a pirate! "
            "Use pirate slang like 'arrr', 'matey', 'shiver me timbers', etc. "
            "Be enthusiastic and colorful in your language!",
        },
        {"role": "user", "content": user_message},
    ],
)

print("\n🏴‍☠️ Captain AI:", response.choices[0].message.content)
