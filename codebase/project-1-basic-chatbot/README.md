# Project 1: Basic Chatbot

Your first AI-powered application! This project teaches you the fundamentals of calling LLM APIs.

## What You'll Learn

- How to make API calls to OpenAI
- How system prompts work
- How to control creativity with temperature
- Basic prompt engineering

## Files

- `chatbot.py` - Main chatbot (10 lines of code!)
- `variations/` - Different personality examples

## Quick Start

```bash
# Make sure you're in the project directory
cd project-1-basic-chatbot

# Run the basic chatbot
python chatbot.py
```

## Code Walkthrough

### The Complete Code (10 Lines!)

```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key-here")

user_message = input("You: ")

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    temperature=0.7,
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": user_message}
    ]
)

print("AI:", response.choices[0].message.content)
```

### Breaking It Down

**Line 1-2:** Import and initialize
```python
from openai import OpenAI
client = OpenAI(api_key="your-api-key-here")
```

**Line 4:** Get user input
```python
user_message = input("You: ")
```

**Lines 6-13:** Make the API call
- `model`: Which AI brain to use (3.5 is fast & cheap, 4 is smart & expensive)
- `temperature`: Creativity level (0.0 = boring, 2.0 = wild)
- `messages`: Array with system prompt and user message

**Line 15:** Print the response
```python
print("AI:", response.choices[0].message.content)
```

## Experiments to Try

### 1. Change the Personality

Replace the system prompt:

```python
# Pirate Bot
{"role": "system", "content": "You are a pirate captain. Always talk like a pirate!"}

# 5-Year-Old
{"role": "system", "content": "You are a 5-year-old child. Use simple words and big imagination!"}

# Tech Expert
{"role": "system", "content": "You are a technical expert who gives detailed, accurate answers."}

# Sarcastic Friend
{"role": "system", "content": "You are a sarcastic but friendly assistant."}
```

### 2. Adjust Temperature

```python
temperature=0.2  # Very predictable, good for facts
temperature=0.7  # Balanced (default)
temperature=1.2  # Creative, good for brainstorming
temperature=1.8  # Wild, experimental
```

### 3. Change Models

```python
model="gpt-3.5-turbo"  # Fast & cheap ($0.0005/1K tokens)
model="gpt-4"           # Smart but expensive ($0.03/1K tokens)
model="gpt-4-turbo"     # Balanced ($0.01/1K tokens)
```

### 4. Add Max Tokens Limit

```python
max_tokens=50  # Short responses only
max_tokens=500 # Medium length
```

## Common Issues

### "AuthenticationError"
- Check your API key in `.env` file
- Make sure there are no extra spaces
- Verify key is active on OpenAI dashboard

### "RateLimitError"
- You're sending requests too fast
- Add `time.sleep(1)` between requests
- Upgrade your OpenAI plan if needed

### Response is cut off
- Increase `max_tokens` parameter
- Or remove it entirely for unlimited length

## Sample Conversations

### Default Assistant
```
You: Explain AI in one sentence
AI: Artificial Intelligence is the simulation of human intelligence
     processes by machines, enabling them to learn, reason, and make decisions.
```

### Pirate Bot
```
You: Explain AI in one sentence
AI: Arrr, AI be like teachin' a parrot to think like a human,
     but with fancy machines instead of feathers, matey!
```

### 5-Year-Old
```
You: Explain AI in one sentence
AI: AI is like a super smart robot that can learn and think
     just like you do when you play games!
```

## Next Steps

Once you're comfortable with this:
1. Try all the personality variations
2. Experiment with different temperatures
3. Test different models
4. Move on to **Project 2** to add memory!

## Key Takeaways

- LLMs are just APIs (text in → text out)
- System prompts control personality
- Temperature controls creativity
- It's simpler than you thought!

---

**Time to complete:** 10 minutes
**Difficulty:** 🌶️ Beginner
**Next project:** project-2-memory-chatbot
