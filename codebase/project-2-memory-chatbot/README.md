# Project 2: Chatbot with Memory

Build a chatbot that actually remembers your conversation!

## What You'll Learn

- How to maintain conversation history
- Message array management
- Context window usage
- Continuous chat loops
- How ChatGPT actually works under the hood

## The Problem with Project 1

Project 1 has a major limitation:
- Every message is standalone
- No memory of previous messages
- Can't have real conversations

**Example:**
```
You: My name is Arjit
AI: Nice to meet you!

You: What's my name?
AI: I don't know your name.  ❌
```

## The Solution: Conversation History

Send the entire conversation with each request!

```
Messages Array:
[
  {"role": "system", "content": "You are helpful"},
  {"role": "user", "content": "My name is Arjit"},
  {"role": "assistant", "content": "Nice to meet you!"},
  {"role": "user", "content": "What's my name?"},  ← New message
]

AI sees full context and responds: "Your name is Arjit!" ✓
```

## Files

- `chatbot_memory.py` - Basic chatbot with memory
- `enhanced_memory.py` - Advanced version with features

## Quick Start

```bash
cd project-2-memory-chatbot
python chatbot_memory.py
```

Type `quit` to exit the conversation.

## Code Walkthrough

### Key Changes from Project 1

**1. Message History Array**
```python
messages = [
    {"role": "system", "content": "You are a helpful assistant"}
]
```

**2. Continuous Loop**
```python
while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break
```

**3. Append User Message**
```python
messages.append({
    "role": "user",
    "content": user_input
})
```

**4. Send Full History**
```python
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages  # ← Entire conversation!
)
```

**5. Append AI Response**
```python
messages.append({
    "role": "assistant",
    "content": ai_message
})
```

## Sample Conversation

```
You: My name is Arjit and I'm learning AI
AI: That's great, Arjit! AI is a fascinating field. What specifically
    are you interested in learning about?

You: What's my name again?
AI: Your name is Arjit!

You: What am I learning?
AI: You mentioned you're learning AI!

You: Spell my name backwards
AI: tijrA
```

See how it remembers everything? That's the power of context!

## Experiments to Try

### 1. Test Memory Limits

Have a very long conversation and see when it starts "forgetting" (when context window fills up at 128K tokens).

### 2. Modify System Prompt

```python
messages = [
    {
        "role": "system",
        "content": "You are a therapist. Listen carefully and ask follow-up questions."
    }
]
```

### 3. Add Message Counter

```python
print(f"[Messages in history: {len(messages)}]")
```

### 4. Show Token Count

```python
from utils.helpers import count_tokens

total_tokens = sum(count_tokens(msg["content"]) for msg in messages)
print(f"Total tokens used: {total_tokens}")
```

## Enhanced Features

The `enhanced_memory.py` file includes:

- **Context management** - Truncate old messages when too long
- **Message counter** - See how many messages in history
- **Token tracking** - Monitor context usage
- **Colored output** - Better UX
- **Save/load conversations** - Continue later

## Common Patterns

### Truncating Context

```python
def truncate_messages(messages, max_messages=20):
    if len(messages) <= max_messages:
        return messages

    # Keep system message + recent messages
    system_msg = [m for m in messages if m["role"] == "system"]
    recent = [m for m in messages if m["role"] != "system"][-19:]

    return system_msg + recent
```

### Saving Conversations

```python
import json

# Save
with open("conversation.json", "w") as f:
    json.dump(messages, f, indent=2)

# Load
with open("conversation.json", "r") as f:
    messages = json.load(f)
```

## Real-World Applications

This pattern is used in:
- ChatGPT interface
- Claude conversations
- Gemini chat
- Customer support bots
- Personal assistants
- Therapy chatbots

## Performance Tips

### Context Window Management

```python
# Check if context is getting full
if len(messages) > 50:
    messages = truncate_messages(messages, max_messages=30)
```

### Cost Optimization

Longer conversations = more tokens = higher cost!

```python
# Monitor costs
from utils.cost_tracker import CostTracker

tracker = CostTracker()
input_tokens = sum(count_tokens(m["content"]) for m in messages)
output_tokens = count_tokens(ai_message)

tracker.log_request("gpt-3.5-turbo", input_tokens, output_tokens, "project-2")
```

## Common Issues

### "Context length exceeded"
- Your conversation is too long
- Solution: Truncate old messages
- Or use a model with larger context (GPT-4 Turbo has 128K)

### Bot seems to forget things
- Context might be truncated
- Check if messages are being properly appended
- Verify system message is preserved

### Conversation loops
- Make sure quit condition works: `if user_input.lower() == "quit"`
- Add error handling for empty inputs

## Architecture Diagram

```
User Input
    ↓
Append to messages[]
    ↓
Send messages[] to API
    ↓
Receive Response
    ↓
Append AI response to messages[]
    ↓
Display to User
    ↓
Loop Back (while True)
```

## Next Steps

Once you master this:
1. Try building a specialized chatbot (tutor, therapist, coding assistant)
2. Implement context truncation
3. Add conversation saving/loading
4. Move on to **Project 3** to add tool integration!

## Key Takeaways

- Memory = Sending full conversation array
- Each API call sees entire history
- Context window is limited (but large!)
- This is how ALL modern chatbots work
- Managing context is crucial for cost and performance

---

**Time to complete:** 15 minutes
**Difficulty:** 🌶️🌶️ Intermediate
**Previous:** project-1-basic-chatbot
**Next:** project-3-function-calling
