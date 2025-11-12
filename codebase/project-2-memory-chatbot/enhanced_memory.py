"""
Project 2: Enhanced Memory Chatbot
Advanced version with context management, token tracking, and colored output.
"""

from openai import OpenAI
import sys
import os
import json
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.config import Config
from utils.helpers import truncate_messages, count_tokens, print_colored
from utils.cost_tracker import CostTracker

# Initialize
client = Config.get_openai_client()
tracker = CostTracker()

print_colored("=" * 70, "cyan")
print_colored("ENHANCED MEMORY CHATBOT - Project 2", "green")
print_colored("=" * 70, "cyan")
print("Features: Context management, token tracking, conversation saving")
print("Commands: 'quit' to exit, 'save' to save conversation, 'stats' for info\n")

# Message history
messages = [
    {
        "role": "system",
        "content": "You are a helpful and knowledgeable assistant. "
        "Be friendly and concise in your responses.",
    }
]

# Track conversation metadata
conversation_start = datetime.now()
total_cost = 0.0


def save_conversation(filename=None):
    """Save conversation to JSON file"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"conversation_{timestamp}.json"

    data = {
        "timestamp": conversation_start.isoformat(),
        "messages": messages,
        "total_cost": total_cost,
    }

    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

    print_colored(f"\n✓ Conversation saved to {filename}", "green")


def show_stats():
    """Display conversation statistics"""
    total_tokens = sum(count_tokens(m["content"]) for m in messages)
    duration = (datetime.now() - conversation_start).total_seconds()

    print_colored("\n" + "=" * 70, "cyan")
    print_colored("CONVERSATION STATISTICS", "green")
    print_colored("=" * 70, "cyan")
    print(f"Messages: {len(messages)} (System: 1, User/AI: {len(messages)-1})")
    print(f"Total Tokens: ~{total_tokens:,}")
    print(f"Total Cost: ${total_cost:.4f}")
    print(f"Duration: {int(duration)} seconds")
    print_colored("=" * 70, "cyan")


# Main conversation loop
while True:
    try:
        # Get user input
        user_input = input("You: ")

        # Handle commands
        if user_input.lower() in ["quit", "exit", "bye"]:
            print_colored("\nAI: Goodbye! It was nice chatting with you!", "green")
            show_stats()

            # Ask to save
            save_choice = input("\nSave this conversation? (y/n): ")
            if save_choice.lower() == "y":
                save_conversation()
            break

        if user_input.lower() == "save":
            save_conversation()
            continue

        if user_input.lower() == "stats":
            show_stats()
            continue

        # Skip empty inputs
        if not user_input.strip():
            continue

        # Add user message to history
        messages.append({"role": "user", "content": user_input})

        # Context management: Truncate if too long
        if len(messages) > 50:
            print_colored("[Context getting long, truncating old messages...]", "yellow")
            messages = truncate_messages(messages, max_messages=30)

        # Count input tokens for cost tracking
        input_tokens = sum(count_tokens(m["content"]) for m in messages)

        # Get response
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", temperature=0.7, messages=messages
        )

        # Extract AI response
        ai_message = response.choices[0].message.content
        output_tokens = count_tokens(ai_message)

        # Track cost
        cost = tracker.log_request(
            model="gpt-3.5-turbo",
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            project="project-2",
        )
        total_cost += cost

        # Print response
        print_colored(f"AI: {ai_message}\n", "green")

        # Add AI response to history
        messages.append({"role": "assistant", "content": ai_message})

        # Show mini stats
        print_colored(
            f"[Messages: {len(messages)} | Tokens: ~{input_tokens + output_tokens:,} | "
            f"Cost: ${cost:.4f} | Total: ${total_cost:.4f}]",
            "cyan",
        )
        print()

    except KeyboardInterrupt:
        print_colored("\n\nInterrupted! Exiting...", "yellow")
        show_stats()
        break

    except Exception as e:
        print_colored(f"\nError: {e}", "red")
        # Remove the user message we just added since we got an error
        if messages and messages[-1]["role"] == "user":
            messages.pop()

print_colored("\n" + "=" * 70, "cyan")
print_colored("Thank you for using Enhanced Memory Chatbot!", "green")
print_colored("=" * 70, "cyan")
