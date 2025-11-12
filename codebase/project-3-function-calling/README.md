# Project 3: Function-Calling Bot

Build an AI that can actually DO things - not just chat!

## What You'll Learn

- What function calling is and why it matters
- How AI decides when to use tools
- Integrating external APIs
- Building multi-tool assistants
- Real-world AI applications

## The Problem

Chatbots can only... chat. They can't:
- Check the weather
- Search the web
- Run calculations
- Query databases
- Send emails
- Book appointments

**Function calling solves this!**

## What is Function Calling?

Function calling lets the AI decide WHEN to use tools and WHAT parameters to use.

### Flow:
```
User: "What's the weather in Delhi?"
    ↓
AI analyzes and decides: "I need to call get_weather function"
    ↓
AI returns: function_name="get_weather", args={"location": "Delhi"}
    ↓
You execute the function → result: "Sunny, 25°C"
    ↓
Send result back to AI
    ↓
AI uses result to respond: "The weather in Delhi is sunny with a temperature of 25°C!"
```

## Real-World Examples

This is how these work:
- **ChatGPT browsing** - Calls web search function
- **ChatGPT code interpreter** - Executes Python code
- **ChatGPT plugins** - Various tool integrations
- **GitHub Copilot** - Searches documentation
- **Customer support bots** - Check order status, book appointments

## Files

- `weather_bot.py` - Simple weather bot (one function)
- `multi_function_bot.py` - Bot with multiple tools
- `calculator_bot.py` - Math operations bot
- `web_search_bot.py` - Web search integration (requires API)

## Quick Start

```bash
cd project-3-function-calling
python weather_bot.py
```

## Code Walkthrough

### Step 1: Define Your Function

```python
def get_weather(location: str) -> str:
    """
    Get current weather for a location.
    In real app, call actual weather API here.
    """
    # Simulated response
    return f"Weather in {location}: Sunny, 25°C"
```

### Step 2: Describe Function to AI

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name, e.g., Delhi, Mumbai"
                    }
                },
                "required": ["location"]
            }
        }
    }
]
```

### Step 3: Make API Call with Tools

```python
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    tools=tools,
    tool_choice="auto"  # Let AI decide when to use tools
)
```

### Step 4: Check if AI Wants to Call Function

```python
if response.choices[0].message.tool_calls:
    # AI decided to call a function!
    tool_call = response.choices[0].message.tool_calls[0]
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments)

    # Execute the function
    if function_name == "get_weather":
        result = get_weather(function_args["location"])
```

### Step 5: Send Result Back to AI

```python
# Add function result to messages
messages.append({
    "role": "tool",
    "tool_call_id": tool_call.id,
    "name": function_name,
    "content": result
})

# Second API call - AI uses result to respond
final_response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages
)
```

## Sample Conversations

### Weather Bot
```
You: What's the weather like in Mumbai?
[AI calls get_weather("Mumbai")]
AI: The weather in Mumbai is sunny with a temperature of 25°C.

You: Thanks!
[No function call needed]
AI: You're welcome! Let me know if you need anything else.
```

### Calculator Bot
```
You: What's 847 * 923?
[AI calls calculator("847 * 923")]
AI: 847 × 923 = 781,781

You: And that divided by 100?
[AI calls calculator("781781 / 100")]
AI: 781,781 ÷ 100 = 7,817.81
```

## Multi-Function Example

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather for a location",
            "parameters": {...}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the internet",
            "parameters": {...}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Perform calculations",
            "parameters": {...}
        }
    }
]
```

AI will automatically choose the right tool!

## Real API Integrations

### Weather API (OpenWeatherMap)
```python
import requests

def get_weather(location: str) -> str:
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"

    response = requests.get(url)
    data = response.json()

    temp = data["main"]["temp"] - 273.15  # Convert to Celsius
    description = data["weather"][0]["description"]

    return f"Weather in {location}: {description}, {temp:.1f}°C"
```

### Web Search (SerpAPI)
```python
import requests

def search_web(query: str) -> str:
    api_key = os.getenv("SERPAPI_KEY")
    url = f"https://serpapi.com/search?q={query}&api_key={api_key}"

    response = requests.get(url)
    data = response.json()

    # Extract top results
    results = data.get("organic_results", [])[:3]
    return "\n".join([f"- {r['title']}: {r['snippet']}" for r in results])
```

## Best Practices

### 1. Clear Function Descriptions
```python
# Bad
"description": "Gets data"

# Good
"description": "Get current weather including temperature, conditions, and humidity for any city worldwide"
```

### 2. Validate Parameters
```python
def get_weather(location: str) -> str:
    if not location or not location.strip():
        return "Error: Location cannot be empty"

    # Call API...
```

### 3. Handle Errors
```python
try:
    result = get_weather(location)
except Exception as e:
    result = f"Error fetching weather: {str(e)}"
```

### 4. Return Structured Data
```python
# Instead of just text, return structured data
return json.dumps({
    "location": location,
    "temperature": 25,
    "condition": "Sunny",
    "humidity": 60,
    "timestamp": datetime.now().isoformat()
})
```

## Common Patterns

### Function Router
```python
def execute_function(function_name: str, arguments: dict) -> str:
    """Route function calls to appropriate handlers"""

    functions = {
        "get_weather": get_weather,
        "search_web": search_web,
        "calculate": calculate,
        "get_time": get_current_time
    }

    if function_name in functions:
        return functions[function_name](**arguments)
    else:
        return f"Error: Unknown function {function_name}"
```

### Async Function Calls
```python
import asyncio

async def async_function_call(function_name: str, args: dict):
    # For slow API calls, use async
    result = await some_async_api_call(**args)
    return result
```

## Use Cases

### Customer Support Bot
```python
tools = [
    {"function": {"name": "check_order_status"}},
    {"function": {"name": "process_refund"}},
    {"function": {"name": "book_appointment"}},
    {"function": {"name": "search_knowledge_base"}}
]
```

### Personal Assistant
```python
tools = [
    {"function": {"name": "check_calendar"}},
    {"function": {"name": "send_email"}},
    {"function": {"name": "set_reminder"}},
    {"function": {"name": "search_contacts"}}
]
```

### Code Assistant
```python
tools = [
    {"function": {"name": "search_documentation"}},
    {"function": {"name": "run_tests"}},
    {"function": {"name": "analyze_code"}},
    {"function": {"name": "suggest_improvements"}}
]
```

## Performance Tips

### 1. Minimize Function Calls
- AI makes 2 API calls per function (one to decide, one to respond)
- Cost = 2x normal chat
- Solution: Batch operations when possible

### 2. Cache Results
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_weather(location: str) -> str:
    # Results cached for repeated queries
    pass
```

### 3. Use Parallel Execution
```python
# If AI calls multiple functions, run them in parallel
results = await asyncio.gather(
    func1(**args1),
    func2(**args2)
)
```

## Common Issues

### AI doesn't call function
- Check function description is clear
- Verify parameters are well-defined
- Make sure user query matches function purpose

### Invalid function arguments
- Add validation in function description
- Include examples in description
- Handle errors gracefully

### Multiple tool calls
- AI might call same function multiple times
- Implement rate limiting
- Add caching

## Next Steps

After mastering function calling:
1. Build a personal assistant with 5+ tools
2. Integrate real APIs (weather, search, calendar)
3. Add database queries as functions
4. Move on to **Project 4** (RAG System)!

## Key Takeaways

- Function calling = AI as a decision-maker
- AI decides WHEN and HOW to use tools
- You execute functions, AI uses results
- This unlocks real-world applications
- Powers ChatGPT plugins, assistants, agents

---

**Time to complete:** 15 minutes
**Difficulty:** 🌶️🌶️🌶️ Intermediate+
**Previous:** project-2-memory-chatbot
**Next:** project-4-rag-system
