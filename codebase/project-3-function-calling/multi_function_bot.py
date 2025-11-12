"""
Project 3: Multi-Function Bot
AI assistant with multiple tools (weather, calculator, time)

Demonstrates how AI chooses the right tool for each task.
"""

from openai import OpenAI
import json
import sys
import os
from datetime import datetime
import math

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.config import Config
from utils.helpers import print_colored

client = Config.get_openai_client()

print_colored("=" * 70, "cyan")
print_colored("MULTI-FUNCTION BOT - Project 3 Advanced", "green")
print_colored("=" * 70, "cyan")
print("I can help with: weather, calculations, and time!")
print("Try asking: 'What's the weather in Delhi?'")
print("          'Calculate 847 * 923'")
print("          'What time is it?'\n")


# Function 1: Weather
def get_weather(location: str) -> str:
    """Get current weather for a location"""
    weather_data = {
        "delhi": "Sunny, 28°C",
        "mumbai": "Partly cloudy, 32°C",
        "bangalore": "Rainy, 22°C",
        "chennai": "Hot, 35°C",
    }

    for city in weather_data:
        if city in location.lower():
            return f"{weather_data[city]}"

    return "Sunny, 25°C (Simulated)"


# Function 2: Calculator
def calculate(expression: str) -> str:
    """Safely evaluate mathematical expressions"""
    try:
        # Remove any dangerous operations
        allowed_chars = "0123456789+-*/(). "
        if not all(c in allowed_chars for c in expression):
            return "Error: Invalid characters in expression"

        # Evaluate safely
        result = eval(expression, {"__builtins__": {}}, {"math": math})
        return str(result)

    except Exception as e:
        return f"Error: {str(e)}"


# Function 3: Get Time
def get_current_time(timezone: str = "UTC") -> str:
    """Get current time"""
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


# Function 4: Search (simulated)
def search_information(query: str) -> str:
    """Simulated web search"""
    return f"Search results for '{query}': [Simulated web search - in real app, use SerpAPI or similar]"


# Define all tools for the AI
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name (e.g., Delhi, Mumbai)",
                    }
                },
                "required": ["location"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Perform mathematical calculations. Supports +, -, *, /, parentheses, and math functions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to evaluate (e.g., '847 * 923', '(100 + 50) / 2')",
                    }
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get the current date and time",
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "Timezone (default: UTC)",
                    }
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_information",
            "description": "Search for information on the internet",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query",
                    }
                },
                "required": ["query"],
            },
        },
    },
]

# Function router
function_map = {
    "get_weather": get_weather,
    "calculate": calculate,
    "get_current_time": get_current_time,
    "search_information": search_information,
}

# Message history
messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant with access to various tools. "
        "Use the appropriate tool to help answer user questions. "
        "Be friendly and explain what you're doing.",
    }
]

# Main loop
while True:
    user_input = input("You: ")

    if user_input.lower() in ["quit", "exit", "bye"]:
        print_colored("\nBot: Goodbye!", "green")
        break

    if not user_input.strip():
        continue

    messages.append({"role": "user", "content": user_input})

    try:
        # First API call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", messages=messages, tools=tools, tool_choice="auto"
        )

        response_message = response.choices[0].message

        # Check for function calls
        if response_message.tool_calls:
            # AI wants to use tools!
            messages.append(response_message)

            # Process each tool call (AI might call multiple tools)
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                print_colored(
                    f"[Using tool: {function_name} with args: {function_args}]", "yellow"
                )

                # Execute the function
                if function_name in function_map:
                    function_response = function_map[function_name](**function_args)
                else:
                    function_response = f"Error: Unknown function {function_name}"

                # Add function result to messages
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                        "content": function_response,
                    }
                )

            # Second API call with function results
            second_response = client.chat.completions.create(
                model="gpt-3.5-turbo", messages=messages
            )

            final_message = second_response.choices[0].message.content
            print_colored(f"\nBot: {final_message}\n", "green")
            messages.append({"role": "assistant", "content": final_message})

        else:
            # No function needed
            print_colored(f"\nBot: {response_message.content}\n", "green")
            messages.append({"role": "assistant", "content": response_message.content})

    except Exception as e:
        print_colored(f"\nError: {e}", "red")
        if messages and messages[-1]["role"] == "user":
            messages.pop()

print_colored("\n" + "=" * 70, "cyan")
print_colored("This is the foundation of AI agents and assistants!", "yellow")
print_colored("=" * 70, "cyan")
