# AI Workshop - Python Codebase

Complete codebase for the AI Workshop: "From AI User to AI Builder"

## Workshop Overview

This repository contains all the code examples and projects from the 2-hour AI development workshop. You'll learn to build AI-powered applications from scratch.

## Projects Included

### Hour 1: Hands-On Coding (3 Projects)

1. **Project 1: Basic Chatbot** - Your first LLM API call (10 lines)
2. **Project 2: Memory Chatbot** - Conversation with context
3. **Project 3: Function-Calling Bot** - AI that uses tools

### Bonus Projects (Your Roadmap)

4. **Project 4: RAG System** - Document Q&A with vector search
5. **Project 5: Multi-Agent System** - Collaborative AI agents

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- OpenAI API key (or Anthropic/Google API key)

### Installation

```bash
# Clone or download this repository
cd codebase

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Setup API Keys

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your API keys:
```
OPENAI_API_KEY=sk-your-key-here
```

3. Get API keys from:
   - OpenAI: https://platform.openai.com/api-keys
   - Anthropic: https://console.anthropic.com/
   - Google: https://makersuite.google.com/app/apikey

## Project Structure

```
codebase/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── .env.example                       # Example environment variables
├── project-1-basic-chatbot/          # Project 1
│   ├── README.md
│   ├── chatbot.py                    # Basic chatbot
│   └── variations/                   # Different personalities
├── project-2-memory-chatbot/         # Project 2
│   ├── README.md
│   ├── chatbot_memory.py            # Chatbot with conversation history
│   └── enhanced_memory.py           # Advanced version
├── project-3-function-calling/       # Project 3
│   ├── README.md
│   ├── weather_bot.py               # Function-calling example
│   └── multi_function_bot.py        # Multiple tools
├── project-4-rag-system/            # Project 4 (RAG)
│   ├── README.md
│   ├── simple_rag.py                # Basic RAG implementation
│   ├── rag_with_chromadb.py         # Using ChromaDB
│   └── rag_streamlit_app.py         # Web interface
├── project-5-multi-agent/           # Project 5 (Multi-Agent)
│   ├── README.md
│   ├── simple_agents.py             # Basic multi-agent
│   └── langgraph_example.py         # Using LangGraph
└── utils/                           # Shared utilities
    ├── config.py                    # Configuration loader
    ├── helpers.py                   # Helper functions
    └── cost_tracker.py              # Track API costs
```

## Running the Projects

### Project 1: Basic Chatbot
```bash
cd project-1-basic-chatbot
python chatbot.py
```

### Project 2: Memory Chatbot
```bash
cd project-2-memory-chatbot
python chatbot_memory.py
```

### Project 3: Function-Calling Bot
```bash
cd project-3-function-calling
python weather_bot.py
```

### Project 4: RAG System
```bash
cd project-4-rag-system
# Simple version
python simple_rag.py

# Web interface
streamlit run rag_streamlit_app.py
```

### Project 5: Multi-Agent System
```bash
cd project-5-multi-agent
python simple_agents.py
```

## Key Concepts Covered

### Tokens
- Text is broken into tokens
- Pricing is based on tokens
- English is more efficient than other languages

### Context Window
- Short-term memory for AI (128K tokens for GPT-4)
- Entire conversation sent with each request
- Oldest messages drop when full

### Temperature
- Controls randomness/creativity
- 0.0 = deterministic, 2.0 = very creative
- Use 0.2 for facts, 0.7 for chat, 1.2 for creative writing

### System Prompts
- Defines AI personality and behavior
- Controls tone, format, and rules
- Most powerful way to customize responses

## Cost Optimization

Monitor your API usage to avoid surprises:

```python
# Use cost tracker utility
from utils.cost_tracker import track_cost

cost = track_cost(model="gpt-3.5-turbo", input_tokens=100, output_tokens=50)
print(f"This request cost: ${cost:.4f}")
```

**Tips to save money:**
1. Use GPT-3.5-turbo instead of GPT-4 when possible (20x cheaper)
2. Keep prompts concise
3. Set `max_tokens` to limit response length
4. Cache common responses
5. Use streaming for better UX without extra cost

## Common Issues

### "ModuleNotFoundError: No module named 'openai'"
```bash
pip install -r requirements.txt
```

### "AuthenticationError: Invalid API key"
- Check your `.env` file has the correct key
- Ensure no extra spaces around the key
- Verify key is active on OpenAI dashboard

### "RateLimitError: Rate limit exceeded"
- You're making requests too fast
- Wait a minute and try again
- Implement exponential backoff (see utils/helpers.py)

### "Context length exceeded"
- Your conversation is too long
- Clear message history or implement truncation
- See `enhanced_memory.py` for context management

## Learning Resources

### Official Documentation
- OpenAI API: https://platform.openai.com/docs
- LangChain: https://python.langchain.com/docs/
- Anthropic: https://docs.anthropic.com

### Recommended Tutorials
- DeepLearning.AI: Free courses on LLM development
- OpenAI Cookbook: Practical examples
- LangChain Tutorials: Framework deep-dives

### Community
- Discord: LangChain community
- Reddit: r/LangChain, r/OpenAI
- Twitter: Follow @OpenAI, @LangChainAI

## Next Steps

After completing these projects:

1. **Week 1-2**: Build variations of Project 1-3
2. **Week 3-4**: Complete Project 4 (RAG System)
3. **Week 5-8**: Build Project 5 (Multi-Agent)
4. **Week 9-12**: Create your own full-stack AI app

## Contributing

Found a bug or want to improve the code? Contributions welcome!

## License

MIT License - Feel free to use this code for learning and building.

## Questions?

- Workshop Discord: [Link in participant handout]
- Twitter: @codewitharjit
- LinkedIn: Arjit Verma

---

**Happy Building! 🚀**

Built with ❤️ for AI Workshop - November 2025
