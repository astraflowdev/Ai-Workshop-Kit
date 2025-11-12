"""
Variation: Hindi Bot
A chatbot that responds in Hindi!
"""

from openai import OpenAI
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from utils.config import Config

client = Config.get_openai_client()

print("🇮🇳 " + "=" * 60)
print("HINDI BOT - हिंदी में बात करें!")
print("=" * 60 + " 🇮🇳\n")

user_message = input("आप: ")

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    temperature=0.7,
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant. Always respond in Hindi. "
            "Use clear, simple Hindi that anyone can understand. "
            "Be polite and respectful.",
        },
        {"role": "user", "content": user_message},
    ],
)

print("\n🇮🇳 AI:", response.choices[0].message.content)
print("\n💡 Note: Hindi uses more tokens, so it costs ~3x more than English!")
