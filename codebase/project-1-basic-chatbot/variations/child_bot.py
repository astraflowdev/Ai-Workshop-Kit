"""
Variation: 5-Year-Old Bot
A chatbot that explains things like a 5-year-old child!
"""

from openai import OpenAI
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from utils.config import Config

client = Config.get_openai_client()

print("👶 " + "=" * 60)
print("5-YEAR-OLD BOT - Simple and fun explanations!")
print("=" * 60 + " 👶\n")

user_message = input("You: ")

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    temperature=0.8,
    messages=[
        {
            "role": "system",
            "content": "You are a 5-year-old child. Use very simple words that a "
            "kindergartener would understand. Be excited and use your imagination! "
            "Compare things to toys, games, and things kids love.",
        },
        {"role": "user", "content": user_message},
    ],
)

print("\n👶 Kid AI:", response.choices[0].message.content)
