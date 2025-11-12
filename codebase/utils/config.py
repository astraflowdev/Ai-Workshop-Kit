"""
Configuration loader for AI Workshop projects.
Loads environment variables and provides default settings.
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for API keys and settings"""

    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")

    # Model Settings
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1000"))

    # Cost Tracking
    TRACK_COSTS = os.getenv("TRACK_COSTS", "true").lower() == "true"
    COST_ALERT_THRESHOLD = float(os.getenv("COST_ALERT_THRESHOLD", "10.00"))

    # LangSmith (Optional)
    LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
    LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
    LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "ai-workshop")

    @classmethod
    def validate(cls):
        """Validate that required API keys are present"""
        if not cls.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY not found in environment variables. "
                "Please create a .env file with your API key."
            )
        return True

    @classmethod
    def get_openai_client(cls):
        """Get configured OpenAI client"""
        from openai import OpenAI
        cls.validate()
        return OpenAI(api_key=cls.OPENAI_API_KEY)

    @classmethod
    def get_anthropic_client(cls):
        """Get configured Anthropic client"""
        from anthropic import Anthropic
        if not cls.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY not found")
        return Anthropic(api_key=cls.ANTHROPIC_API_KEY)

    @classmethod
    def print_config(cls):
        """Print current configuration (without exposing keys)"""
        print("=" * 50)
        print("Current Configuration:")
        print("=" * 50)
        print(f"Model: {cls.MODEL_NAME}")
        print(f"Temperature: {cls.TEMPERATURE}")
        print(f"Max Tokens: {cls.MAX_TOKENS}")
        print(f"Cost Tracking: {cls.TRACK_COSTS}")
        print(f"OpenAI Key: {'✓ Set' if cls.OPENAI_API_KEY else '✗ Not Set'}")
        print(f"Anthropic Key: {'✓ Set' if cls.ANTHROPIC_API_KEY else '✗ Not Set'}")
        print("=" * 50)


# Example usage
if __name__ == "__main__":
    Config.print_config()

    # Test OpenAI connection
    try:
        client = Config.get_openai_client()
        print("\n✓ Successfully connected to OpenAI API")
    except Exception as e:
        print(f"\n✗ Error connecting to OpenAI: {e}")
