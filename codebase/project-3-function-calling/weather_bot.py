"""
Project 3: Function-Calling Weather Bot
AI that can check the weather using function calling!

This demonstrates how ChatGPT browses web, runs code, etc.
"""

from openai import OpenAI
import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.config import Config
from utils.helpers import print_colored

# Initialize OpenAI client
client = Config.get_openai_client()

print_colored("=" * 70, "cyan")
print_colored("FUNCTION-CALLING WEATHER BOT - Project 3", "green")
print_colored("=" * 70, "cyan")
print("Ask me about the weather in any city!")
print("Type 'quit' to exit\n")


# Define the weather function
def get_weather(location: str) -> str:
    """
    Get current weather for a location.
    In a real app, you'd call an actual weather API here.
    For demo, we return simulated data.
    """
    # Simulated weather data
    weather_data = {
        "delhi": "Sunny, 28°C, Humidity: 45%",
        "mumbai": "Partly cloudy, 32°C, Humidity: 70%",
        "bangalore": "Rainy, 22°C, Humidity: 85%",
        "chennai": "Hot and sunny, 35°C, Humidity: 60%",
        "kolkata": "Humid, 30°C, Humidity: 75%",
        "hyderabad": "Clear skies, 29°C, Humidity: 50%",
    }

    location_lower = location.lower()

    # Check if we have data for this location
    for city in weather_data:
        if city in location_lower:
            return f"Weather in {location}: {weather_data[city]}"

    # Default response for unknown cities
    return f"Weather in {location}: Sunny, 25°C (Simulated data)"


# Define function schema for the AI
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a specific location/city. Returns temperature, conditions, and humidity.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city name, e.g., Delhi, Mumbai, New York, London",
                    }
                },
                "required": ["location"],
            },
        },
    }
]

# Message history
messages = [
    {
        "role": "system",
        "content": "You are a helpful weather assistant. When users ask about weather, "
        "use the get_weather function to get accurate information. "
        "Present the weather information in a friendly, conversational way.",
    }
]

# Main conversation loop
while True:
    # Get user input
    user_input = input("You: ")

    # Exit condition
    if user_input.lower() in ["quit", "exit", "bye"]:
        print_colored("\nWeather Bot: Goodbye! Stay weather-aware!", "green")
        break

    if not user_input.strip():
        continue

    # Add user message to history
    messages.append({"role": "user", "content": user_input})

    try:
        # First API call - AI decides if it needs to use the weather function
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", messages=messages, tools=tools, tool_choice="auto"
        )

        response_message = response.choices[0].message

        # Check if AI wants to call a function
        if response_message.tool_calls:
            print_colored("[AI is checking the weather...]", "yellow")

            # Extract function call details
            tool_call = response_message.tool_calls[0]
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            print_colored(
                f"[Calling {function_name} with location: {function_args.get('location')}]",
                "yellow",
            )

            # Execute the function
            if function_name == "get_weather":
                function_response = get_weather(function_args["location"])
            else:
                function_response = f"Error: Unknown function {function_name}"

            # Add function call and result to messages
            messages.append(response_message)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": function_response,
                }
            )

            # Second API call - AI uses function result to formulate response
            second_response = client.chat.completions.create(
                model="gpt-3.5-turbo", messages=messages
            )

            final_message = second_response.choices[0].message.content
            print_colored(f"\nWeather Bot: {final_message}\n", "green")

            # Add final response to history
            messages.append({"role": "assistant", "content": final_message})

        else:
            # No function call needed - just a normal response
            print_colored(f"\nWeather Bot: {response_message.content}\n", "green")
            messages.append({"role": "assistant", "content": response_message.content})

    except Exception as e:
        print_colored(f"\nError: {e}", "red")
        # Remove the user message if there was an error
        if messages and messages[-1]["role"] == "user":
            messages.pop()

print_colored("\n" + "=" * 70, "cyan")
print_colored(
    "💡 This is how ChatGPT browses web, runs code, and uses plugins!", "yellow"
)
print_colored("=" * 70, "cyan")
