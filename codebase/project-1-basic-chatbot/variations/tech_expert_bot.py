"""
Variation: Tech Expert Bot
A chatbot that gives detailed technical explanations with code examples!
"""

from openai import OpenAI
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from utils.config import Config

client = Config.get_openai_client()

print("💻 " + "=" * 60)
print("TECH EXPERT BOT - Detailed technical answers")
print("=" * 60 + " 💻\n")

user_message = input("You: ")

response = client.chat.completions.create(
    model="gpt-4",  # Using GPT-4 for better technical accuracy
    temperature=0.3,  # Lower temperature for more accurate, focused responses
    messages=[
        {
            "role": "system",
            "content": "You are a senior software engineer and technical expert. "
            "Provide detailed, accurate technical explanations. Include code examples "
            "when relevant. Use proper terminology and best practices. "
            "Format code in markdown with proper syntax highlighting.",
        },
        {"role": "user", "content": user_message},
    ],
)

print("\n💻 Tech Expert:", response.choices[0].message.content)
print("\n💡 Note: This uses GPT-4 for better accuracy (but costs more!)")
