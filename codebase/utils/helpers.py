"""
Helper functions for AI Workshop projects.
Common utilities used across different projects.
"""

import time
import functools
from typing import Callable, Any


def retry_with_exponential_backoff(
    func: Callable,
    initial_delay: float = 1,
    exponential_base: float = 2,
    max_retries: int = 5,
    errors: tuple = (Exception,),
):
    """
    Retry a function with exponential backoff.
    Useful for handling rate limits and temporary failures.

    Args:
        func: Function to retry
        initial_delay: Initial delay in seconds
        exponential_base: Multiplier for delay
        max_retries: Maximum number of retry attempts
        errors: Tuple of exceptions to catch

    Returns:
        Decorated function with retry logic
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        delay = initial_delay
        last_exception = None

        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except errors as e:
                last_exception = e
                if attempt == max_retries - 1:
                    raise last_exception

                print(f"Attempt {attempt + 1} failed: {e}")
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= exponential_base

        raise last_exception

    return wrapper


def truncate_messages(messages: list, max_messages: int = 20) -> list:
    """
    Truncate message history to prevent context overflow.
    Keeps system message and most recent messages.

    Args:
        messages: List of message dictionaries
        max_messages: Maximum number of messages to keep

    Returns:
        Truncated message list
    """
    if len(messages) <= max_messages:
        return messages

    # Always keep system message (first message)
    system_messages = [msg for msg in messages if msg["role"] == "system"]
    other_messages = [msg for msg in messages if msg["role"] != "system"]

    # Keep most recent messages
    recent_messages = other_messages[-(max_messages - len(system_messages)) :]

    return system_messages + recent_messages


def count_tokens(text: str, model: str = "gpt-3.5-turbo") -> int:
    """
    Estimate token count for a given text.
    Uses tiktoken for accurate counting.

    Args:
        text: Input text
        model: Model name for tokenizer

    Returns:
        Estimated token count
    """
    try:
        import tiktoken

        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except ImportError:
        # Fallback: rough estimation (1 token ≈ 4 characters)
        return len(text) // 4
    except Exception:
        # If model not found, use cl100k_base (GPT-4 encoding)
        import tiktoken

        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))


def format_cost(cost: float) -> str:
    """
    Format cost in a human-readable way.

    Args:
        cost: Cost in dollars

    Returns:
        Formatted cost string
    """
    if cost < 0.01:
        return f"${cost:.4f} (< 1 cent)"
    elif cost < 1:
        return f"${cost:.2f} ({int(cost * 100)} cents)"
    else:
        return f"${cost:.2f}"


def print_colored(text: str, color: str = "green"):
    """
    Print colored text to terminal.

    Args:
        text: Text to print
        color: Color name (green, red, yellow, blue, cyan)
    """
    colors = {
        "green": "\033[92m",
        "red": "\033[91m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "cyan": "\033[96m",
        "reset": "\033[0m",
    }

    color_code = colors.get(color, colors["reset"])
    print(f"{color_code}{text}{colors['reset']}")


def create_system_prompt(
    personality: str = "helpful",
    tone: str = "professional",
    format: str = "markdown",
    additional_instructions: str = "",
) -> str:
    """
    Create a system prompt with common patterns.

    Args:
        personality: AI personality (helpful, creative, concise, etc.)
        tone: Communication tone (professional, casual, friendly)
        format: Output format (markdown, json, plain)
        additional_instructions: Extra instructions

    Returns:
        Formatted system prompt
    """
    personalities = {
        "helpful": "You are a helpful and knowledgeable assistant.",
        "creative": "You are a creative assistant who thinks outside the box.",
        "concise": "You are a concise assistant who gives brief, to-the-point answers.",
        "technical": "You are a technical expert who provides detailed, accurate information.",
        "friendly": "You are a friendly and approachable assistant.",
    }

    tones = {
        "professional": "Maintain a professional tone.",
        "casual": "Use a casual, conversational tone.",
        "friendly": "Be warm and friendly.",
        "formal": "Use formal language.",
    }

    formats = {
        "markdown": "Format your responses in clean markdown.",
        "json": "Always respond with valid JSON.",
        "plain": "Use plain text without special formatting.",
        "code": "Include code examples when relevant.",
    }

    prompt_parts = [
        personalities.get(personality, personalities["helpful"]),
        tones.get(tone, tones["professional"]),
        formats.get(format, formats["markdown"]),
    ]

    if additional_instructions:
        prompt_parts.append(additional_instructions)

    return " ".join(prompt_parts)


def streaming_print(text_generator, prefix: str = "AI: "):
    """
    Print streaming text with a prefix.

    Args:
        text_generator: Generator that yields text chunks
        prefix: Prefix to print before text
    """
    print(prefix, end="", flush=True)
    full_text = ""

    for chunk in text_generator:
        print(chunk, end="", flush=True)
        full_text += chunk

    print()  # New line at the end
    return full_text


# Example usage
if __name__ == "__main__":
    # Test token counting
    sample_text = "Hello, how are you? I'm learning about AI!"
    tokens = count_tokens(sample_text)
    print(f"Text: '{sample_text}'")
    print(f"Estimated tokens: {tokens}")

    # Test colored printing
    print_colored("Success!", "green")
    print_colored("Warning!", "yellow")
    print_colored("Error!", "red")

    # Test system prompt creation
    prompt = create_system_prompt(
        personality="technical",
        tone="professional",
        format="markdown",
        additional_instructions="Focus on Python programming.",
    )
    print(f"\nGenerated system prompt:\n{prompt}")

    # Test message truncation
    messages = [
        {"role": "system", "content": "You are helpful"},
        *[{"role": "user", "content": f"Message {i}"} for i in range(25)],
    ]
    truncated = truncate_messages(messages, max_messages=10)
    print(f"\nOriginal messages: {len(messages)}")
    print(f"Truncated messages: {len(truncated)}")
