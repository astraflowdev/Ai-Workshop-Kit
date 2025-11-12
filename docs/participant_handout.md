# AI Workshop Participant Handout
## From AI User to AI Builder: Your Development Journey

**Workshop Date:** November 2025
**Instructor:** Arjit | Full Stack AI Consultant
**Contact:** @codewitharjit | 183k+ Followers

---

## Table of Contents

1. [Workshop Overview](#workshop-overview)
2. [Core Concepts](#core-concepts)
3. [Project Code Examples](#project-code-examples)
4. [Your 5-Project Roadmap](#your-5-project-roadmap)
5. [Career Opportunities](#career-opportunities)
6. [Resources & Learning Path](#resources--learning-path)
7. [Community & Support](#community--support)
8. [Quick Reference](#quick-reference)

---

## Workshop Overview

### What You Learned Today

✅ **Technical Skills:**
- How to make LLM API calls (OpenAI/Anthropic)
- Building chatbots with personality and memory
- Understanding RAG architecture
- Integrating AI into applications
- Function calling and tool integration

✅ **Career Clarity:**
- Real job opportunities in AI
- Salary expectations (₹8-60 LPA range)
- 5-project roadmap to job-ready
- Communities and resources to continue learning

---

## Core Concepts

### 1. Tokens - The Currency of AI

**What are tokens?**
- Everything gets broken into tokens (words or parts of words)
- Text → Tokens (numbers) → Processing → Tokens → Text

**Key Facts:**
- "Hello world" = 2 tokens
- "नमस्ते दुनिया" = 6 tokens (Hindi is less efficient)
- English < Hindi < Code < Special characters

**Pricing (GPT-4):**
- Input: $0.03 per 1,000 tokens
- Output: $0.06 per 1,000 tokens

**Test Your Text:**
- Tool: https://platform.openai.com/tokenizer
- Tip: Shorter prompts = Lower costs

---

### 2. Context Window - Short-Term Memory

**What is it?**
- The "memory" available to the AI during a conversation
- Like WhatsApp Status: After capacity is full, oldest content gets dropped

**Size Reference:**
- GPT-4: 128K tokens
- ≈ 96,000 words
- ≈ Entire Harry Potter book
- ≈ 200 pages of text

**Why It Matters:**
- AI "forgets" when context fills up
- Not a bug - it's by design
- Solution: RAG (Retrieval Augmented Generation) for large documents

---

### 3. Temperature - Creativity Dial

**Scale: 0.0 to 2.0**

```
0.0 ────── 0.5 ────── 1.0 ────── 1.5 ────── 2.0
│          │          │          │          │
Cold       Cool      Normal      Hot      Burning
Boring     Safe    Balanced   Creative    Chaotic
```

**When to Use:**
- **0.0-0.3**: Factual Q&A, data extraction, classification
- **0.5-0.7**: General chatbots, customer support
- **0.8-1.2**: Creative writing, brainstorming
- **1.5-2.0**: Experimental art, poetry (use carefully!)

**Example:**
```python
# Boring but accurate
temperature=0.2

# Balanced (most common)
temperature=0.7

# Creative and wild
temperature=1.5
```

---

### 4. System Prompts - Personality Setting

**What they do:**
- Define WHO the AI is
- Control HOW it behaves
- Set tone, format, rules, personality

**Example Transformations:**

```python
# Default Assistant
{"role": "system", "content": "You are a helpful assistant."}
# Result: Professional, formal, educational

# Personality Bot
{"role": "system", "content": "You are Shah Rukh Khan. Talk with signature style, spreading arms wide gestures."}
# Result: Entertaining, Bollywood style, charismatic

# Specialized Bot
{"role": "system", "content": "You are a pirate captain. Always talk like a pirate!"}
# Result: "Arrr matey! Let me tell ye about AI..."
```

**Pro Tips:**
- Control tone: formal/casual/funny
- Control format: JSON/markdown/code
- Set rules: "Don't mention competitors", "Stay on topic"
- Define personality: helpful/sarcastic/professional

---

## Project Code Examples

### Project 1: Basic Chatbot

**What it does:** Simple CLI chatbot that takes input and gives AI response

**Code:**
```python
# chatbot.py
from openai import OpenAI

# Initialize the client with your API key
client = OpenAI(api_key="your-api-key-here")

# Get user input
user_message = input("You: ")

# Make the API call
response = client.chat.completions.create(
    model="gpt-3.5-turbo",        # Which AI to use
    temperature=0.7,               # Creativity level
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},  # Personality
        {"role": "user", "content": user_message}                      # User's question
    ]
)

# Print the response
print("AI:", response.choices[0].message.content)
```

**Run it:**
```bash
python chatbot.py
```

**Experiment Ideas:**
- Change system prompt to make it talk like a pirate
- Adjust temperature (try 0.2, then 1.5)
- Try different models (gpt-4, gpt-3.5-turbo)

---

### Project 2: Chatbot with Memory

**What it does:** Chatbot that remembers conversation history

**Code:**
```python
# chatbot_memory.py
from openai import OpenAI

client = OpenAI(api_key="your-api-key-here")

# Message history - this is the memory!
messages = [
    {"role": "system", "content": "You are a helpful assistant"}
]

# Continuous conversation loop
while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break

    # Add user message to history
    messages.append({
        "role": "user",
        "content": user_input
    })

    # Get response (with full history!)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages  # Full conversation sent
    )

    # Extract AI response
    ai_message = response.choices[0].message.content
    print(f"AI: {ai_message}")

    # Add AI response to history (important!)
    messages.append({
        "role": "assistant",
        "content": ai_message
    })
```

**Run it:**
```bash
python chatbot_memory.py
```

**Test the Memory:**
```
You: My name is Arjit
AI: Nice to meet you, Arjit!

You: What's my name?
AI: Your name is Arjit!

You: Spell it backwards
AI: tijrA
```

**Key Difference from Project 1:**
- `messages = []` array stores all messages
- `while True` loop for continuous conversation
- `.append()` to add each message to history
- Send entire `messages` array with each API call

---

### Project 3: Function-Calling Bot

**What it does:** AI that can use tools (check weather, calculate, search web)

**Concept: Function Calling**
- AI decides WHEN to call a function
- You provide function definitions
- AI returns which function to call with what parameters
- You execute the function and return results
- AI uses results to answer user

**Simple Weather Example:**

```python
# weather_bot.py
from openai import OpenAI
import json

client = OpenAI(api_key="your-api-key-here")

# Define available functions
def get_weather(location):
    """Simulated weather function"""
    # In real app, call weather API here
    return f"Weather in {location}: Sunny, 25°C"

# Function definitions for AI
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
                        "description": "City name"
                    }
                },
                "required": ["location"]
            }
        }
    }
]

messages = [
    {"role": "system", "content": "You are a helpful assistant with access to weather data."}
]

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break

    messages.append({"role": "user", "content": user_input})

    # First API call - AI decides if it needs to use tools
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    response_message = response.choices[0].message

    # Check if AI wants to call a function
    if response_message.tool_calls:
        # AI decided to call a function
        tool_call = response_message.tool_calls[0]
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)

        # Execute the function
        if function_name == "get_weather":
            function_response = get_weather(function_args["location"])

        # Send function result back to AI
        messages.append(response_message)
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "name": function_name,
            "content": function_response
        })

        # Second API call - AI uses function result to answer
        second_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        final_message = second_response.choices[0].message.content
        print(f"AI: {final_message}")
        messages.append({"role": "assistant", "content": final_message})
    else:
        # No function call needed, just respond
        print(f"AI: {response_message.content}")
        messages.append({"role": "assistant", "content": response_message.content})
```

**Test it:**
```
You: What's the weather in Delhi?
AI: The weather in Delhi is sunny with a temperature of 25°C.

You: Thanks!
AI: You're welcome! Let me know if you need anything else.
```

**How it Works:**
1. User asks about weather
2. AI sees available functions and decides to call `get_weather`
3. You execute the function and return result
4. AI uses result to formulate natural response

**Real-World Applications:**
- Customer support bots (check order status, book appointments)
- Research assistants (search databases, fetch documents)
- Code assistants (run tests, check documentation)
- Personal assistants (check calendar, send emails)

---

## Your 5-Project Roadmap

### Overview: From Today to Job-Ready

```
TODAY → 2 WEEKS → 4 WEEKS → 8 WEEKS → 12 WEEKS → JOB READY
  ↓        ↓         ↓         ↓          ↓
Projects Projects  Project   Project    Project
1,2,3      4         5         +         ++
(Done!)  (RAG)  (Multi-Agent) (Full Stack) (Portfolio)
```

---

### Project 4: RAG System (Document Q&A)
**Timeline:** Complete in 2 weeks
**Difficulty:** 🌶️🌶️🌶️ Intermediate+

**What is RAG?**
- Retrieval Augmented Generation
- Lets AI answer questions about YOUR documents
- Solution to context window limitation

**How it Works:**
```
Your Documents
    ↓
1. Chunk & Embed (convert to vectors)
    ↓
2. Store in Vector DB (Pinecone/ChromaDB)
    ↓
3. User asks question
    ↓
4. Search similar chunks (semantic search)
    ↓
5. Send relevant chunks + question to LLM
    ↓
6. Get accurate answer
```

**What You'll Build:**
- Upload PDF/documents
- Ask questions about the content
- Get accurate, sourced answers
- Web interface with Streamlit

**Tech Stack:**
- **LLM**: OpenAI GPT-4 or Anthropic Claude
- **Embeddings**: OpenAI ada-002
- **Vector DB**: Pinecone (free tier) or ChromaDB (local)
- **Frontend**: Streamlit
- **PDF Processing**: PyPDF2 or LangChain

**Core Concepts:**
- Embeddings (text → vectors)
- Similarity search (cosine similarity)
- Chunking strategies
- Vector databases

**Example Use Cases:**
- Legal document Q&A
- Company knowledge base
- Research paper analysis
- Customer support documentation

**Learning Resources:**
- LangChain Documentation
- Pinecone Tutorials
- "RAG from Scratch" by LangChain

---

### Project 5: Multi-Agent System
**Timeline:** Complete by week 8
**Difficulty:** 🌶️🌶️🌶️🌶️ Advanced

**What are Multi-Agent Systems?**
- Multiple AI agents working together
- Each agent has specialized role
- Coordinate to solve complex tasks

**Example: Content Creation Team**
```
User Request: "Create a blog post about AI"
    ↓
Researcher Agent → Researches topic, finds data
    ↓
Writer Agent → Writes draft using research
    ↓
Editor Agent → Reviews and improves
    ↓
SEO Agent → Optimizes for search engines
    ↓
Final Blog Post
```

**What You'll Build:**
- Multi-agent research assistant
- Agents for different tasks (search, analyze, summarize)
- Coordination logic
- Web interface

**Tech Stack:**
- **Framework**: LangGraph or AutoGen
- **LLM**: GPT-4 or Claude
- **Tools**: Web search, calculator, code execution
- **Frontend**: Streamlit or Gradio

**Core Concepts:**
- Agent orchestration
- Tool integration
- State management
- Error handling

**Example Use Cases:**
- Automated research reports
- Complex data analysis
- Code review systems
- Customer support triage

**Learning Resources:**
- LangGraph Documentation
- AutoGen Examples
- Multi-agent research papers

---

### Project 6: Full Stack AI Application
**Timeline:** Weeks 8-12
**Difficulty:** 🌶️🌶️🌶️🌶️🌶️ Advanced+

**What You'll Build:**
- Production-ready AI SaaS application
- User authentication
- Database integration
- Payment processing (optional)
- Deployment to cloud

**Example Ideas:**
1. **AI Writing Assistant**
   - User accounts
   - Document management
   - Multiple AI tools (summarize, rewrite, expand)
   - Usage tracking

2. **Smart Customer Support**
   - Ticket management
   - AI-powered responses
   - Knowledge base integration
   - Analytics dashboard

3. **Personal Research Assistant**
   - Upload documents
   - RAG-based Q&A
   - Summarization
   - Note-taking

**Tech Stack:**
- **Backend**: FastAPI or Flask
- **Frontend**: React or Next.js
- **Database**: PostgreSQL + Supabase
- **Auth**: Clerk or Auth0
- **AI**: OpenAI + LangChain
- **Deployment**: Vercel + Railway

**Core Concepts:**
- REST API design
- Database schema design
- Authentication & authorization
- Rate limiting
- Cost optimization
- Error handling & monitoring

**Learning Path:**
1. Backend API with FastAPI
2. Database design & integration
3. Frontend with React
4. User authentication
5. AI integration
6. Testing & deployment

---

### Beyond Project 6: Portfolio Projects

**Build These to Stand Out:**

1. **Industry-Specific Tool**
   - Healthcare: Medical report analyzer
   - Legal: Contract review assistant
   - Education: Personalized tutor
   - Finance: Financial report summarizer

2. **Open Source Contribution**
   - Contribute to LangChain
   - Build LangChain tools
   - Create tutorials
   - Write documentation

3. **Unique Use Case**
   - AI for regional languages (Hindi, Tamil, etc.)
   - Accessibility tools
   - Local business solutions

---

## Career Opportunities

### Job Roles in AI Development

#### 1. AI Engineer
**Salary Range:** ₹12-35 LPA
**Experience:** 0-3 years

**What You'll Do:**
- Integrate LLM APIs into products
- Build chatbots and AI assistants
- Implement RAG systems
- Optimize AI performance

**Skills Required:**
- Python programming
- LLM API integration (OpenAI, Anthropic)
- Prompt engineering
- Basic understanding of embeddings
- FastAPI or Flask

**Companies Hiring:**
- Startups building AI products
- SaaS companies adding AI features
- Consulting firms

---

#### 2. Full Stack AI Developer
**Salary Range:** ₹15-40 LPA
**Experience:** 1-4 years

**What You'll Do:**
- Build end-to-end AI applications
- Frontend + Backend + AI integration
- User experience design for AI features
- Deployment and monitoring

**Skills Required:**
- Full stack development (React, Node.js/Python)
- LLM integration
- Database design
- Cloud deployment (AWS, GCP, Azure)
- DevOps basics

**Companies Hiring:**
- AI-first startups
- Product companies
- Tech consulting

---

#### 3. AI Product Engineer
**Salary Range:** ₹18-50 LPA
**Experience:** 2-5 years

**What You'll Do:**
- Design AI product features
- Build prototypes
- Optimize for performance and cost
- Work with product managers

**Skills Required:**
- Strong product sense
- AI/ML knowledge
- Full stack skills
- Cost optimization
- User research

**Companies Hiring:**
- Funded AI startups
- FAANG companies
- Unicorns (Razorpay, Cred, Zomato)

---

### Salary Breakdown by Experience

#### Fresher (0-1 year)
**Range:** ₹8-25 LPA

**What Makes You Valuable:**
- 5+ AI projects in portfolio
- Good understanding of RAG and agents
- Full stack skills
- Good communication

**Realistic Expectations:**
- Service-based: ₹8-12 LPA
- Product startups: ₹12-18 LPA
- Well-funded startups: ₹18-25 LPA

---

#### Mid-Level (2-4 years)
**Range:** ₹15-35 LPA

**What Makes You Valuable:**
- Production AI apps experience
- Cost optimization skills
- System design knowledge
- Team collaboration

**Realistic Expectations:**
- Good product companies: ₹15-22 LPA
- AI-first startups: ₹22-28 LPA
- Unicorns/FAANG: ₹28-35 LPA

---

#### Senior (5+ years)
**Range:** ₹35-60+ LPA

**What Makes You Valuable:**
- Led AI projects end-to-end
- Architectural decisions
- Team leadership
- Domain expertise

**Realistic Expectations:**
- Senior Engineer: ₹35-45 LPA
- Lead/Staff Engineer: ₹45-60 LPA
- Principal Engineer: ₹60+ LPA + Equity

---

### Real Job Openings (November 2025)

**Backend Engineer (AI Features) - Zomato**
- Location: Bangalore
- Salary: ₹18-28 LPA
- Skills: Python, LLM APIs, FastAPI

**Full Stack Engineer (LLM Integration) - Razorpay**
- Location: Bangalore
- Salary: ₹15-25 LPA
- Skills: React, Python, OpenAI API

**Product Engineer (AI/ML) - Cred**
- Location: Bangalore
- Salary: ₹20-35 LPA
- Skills: Full Stack, AI Integration, Product Sense

**AI Integration Engineer - Swiggy**
- Location: Bangalore
- Salary: ₹16-30 LPA
- Skills: Python, LangChain, RAG

**Backend Engineer (AI) - Paytm**
- Location: Noida
- Salary: ₹14-24 LPA
- Skills: Python, AI APIs, Microservices

**Founding Engineer (AI Products) - Zepto**
- Location: Mumbai
- Salary: ₹12-20 LPA + Equity
- Skills: Full Stack, AI, Fast execution

**Where to Find Jobs:**
- AngelList (startups)
- LinkedIn (all companies)
- Naukri.com (established companies)
- Instahyre (curated opportunities)
- YC Jobs (Y Combinator startups)

---

## Resources & Learning Path

### Essential Documentation

#### LLM Providers
1. **OpenAI**
   - Docs: https://platform.openai.com/docs
   - API Reference: https://platform.openai.com/docs/api-reference
   - Cookbook: https://cookbook.openai.com/

2. **Anthropic (Claude)**
   - Docs: https://docs.anthropic.com
   - Prompt Library: https://docs.anthropic.com/claude/prompt-library

3. **Google (Gemini)**
   - Docs: https://ai.google.dev/docs
   - Quickstart: https://ai.google.dev/tutorials/python_quickstart

#### Frameworks & Tools
1. **LangChain**
   - Docs: https://python.langchain.com/docs/
   - Tutorials: https://python.langchain.com/docs/tutorials/
   - Use Cases: RAG, Agents, Chains

2. **LangGraph**
   - Docs: https://langchain-ai.github.io/langgraph/
   - Multi-agent systems
   - State management

3. **LlamaIndex**
   - Docs: https://docs.llamaindex.ai/
   - RAG-focused framework
   - Data connectors

#### Vector Databases
1. **Pinecone**
   - Docs: https://docs.pinecone.io/
   - Free tier: 1 index, 100K vectors

2. **ChromaDB**
   - Docs: https://docs.trychroma.com/
   - Local-first, free
   - Easy to get started

3. **Weaviate**
   - Docs: https://weaviate.io/developers/weaviate
   - Open source
   - Self-hosted or cloud

---

### YouTube Channels

1. **For Beginners:**
   - **Tech with Tim** - AI tutorials
   - **Coding with Lewis** - LangChain tutorials
   - **AI Jason** - Practical AI projects

2. **Intermediate:**
   - **LangChain Official** - Framework tutorials
   - **Data Independent** - AI engineering
   - **Sam Witteveen** - Advanced LangChain

3. **Advanced:**
   - **Sentdex** - AI from scratch
   - **1littlecoder** - Production AI
   - **AI Engineering** - System design

---

### Courses & Tutorials

#### Free Courses
1. **DeepLearning.AI**
   - "ChatGPT Prompt Engineering for Developers"
   - "Building Systems with ChatGPT API"
   - "LangChain for LLM Application Development"
   - Link: https://www.deeplearning.ai/short-courses/

2. **OpenAI Cookbook**
   - Practical examples
   - Best practices
   - Production tips
   - Link: https://cookbook.openai.com/

3. **Microsoft Learn**
   - "Develop AI solutions with Azure OpenAI"
   - Free and comprehensive

#### Paid Courses (Worth It)
1. **Udemy - "LangChain: Develop LLM powered applications"**
   - Comprehensive LangChain course
   - ~₹500 on sale

2. **ZTM - "Complete AI & Machine Learning Bootcamp"**
   - Beginner to advanced
   - Includes projects

---

### Books

1. **"AI Engineering" by Chip Huyen**
   - Production AI systems
   - Best practices
   - System design

2. **"Building LLM Apps" by Valentina Alto**
   - Practical guide
   - Real-world examples
   - Available on Amazon

3. **"Prompt Engineering Guide"**
   - Free online book
   - Link: https://www.promptingguide.ai/

---

### Blogs & Newsletters

1. **Personal Blogs:**
   - Chip Huyen's Blog (huyenchip.com)
   - Eugene Yan (eugeneyan.com)
   - Lil'Log by Lilian Weng (lilianweng.github.io)

2. **Company Blogs:**
   - OpenAI Blog (openai.com/blog)
   - Anthropic Blog (anthropic.com/news)
   - LangChain Blog (blog.langchain.dev)

3. **Newsletters:**
   - The Rundown AI (daily AI news)
   - TLDR AI (tech-focused)
   - AI Tidbits (weekly digest)

---

### Practice Platforms

1. **Build in Public:**
   - Twitter/X: Share your progress
   - LinkedIn: Post project updates
   - Dev.to: Write tutorials

2. **Code Practice:**
   - Build 100 micro-projects
   - Contribute to open source
   - Take part in hackathons

3. **Kaggle:**
   - AI competitions
   - Datasets for practice
   - Community discussions

---

## Community & Support

### Online Communities

#### Discord Servers
1. **LangChain Discord**
   - Official community
   - Ask questions
   - Share projects
   - Link: https://discord.gg/langchain

2. **OpenAI Developer Community**
   - API help
   - Best practices
   - Networking

3. **AI Engineers**
   - General AI development
   - Career advice
   - Project feedback

#### Reddit Communities
1. **r/MachineLearning**
   - Latest research
   - Technical discussions

2. **r/LangChain**
   - Framework help
   - Project showcases

3. **r/OpenAI**
   - API discussions
   - Use cases

#### Twitter/X
**Follow These Accounts:**
- @OpenAI - Official updates
- @LangChainAI - LangChain news
- @sama (Sam Altman) - AI industry insights
- @karpathy (Andrej Karpathy) - AI education
- @GregKamradt - LangChain tutorials
- @hwchase17 (Harrison Chase) - LangChain creator

---

### Local Communities

#### Meetups (India)
- AI/ML Bangalore Meetup
- Delhi AI Developers
- Mumbai Machine Learning
- Pune Data Science Group

#### College Clubs
- Join/start an AI club
- Organize workshops
- Build together
- Share knowledge

---

### Getting Help

#### When Stuck on Code:
1. **Read error message carefully**
2. **Search on Google** (add "site:stackoverflow.com")
3. **Ask in Discord/Reddit**
4. **Check official docs**
5. **Use ChatGPT to debug** (yes, really!)

#### When Stuck on Career:
1. **DM people on LinkedIn** (ask specific questions)
2. **Join office hours** (many free on Twitter)
3. **Attend meetups** (network in person)
4. **Share your work** (get feedback)

---

## Quick Reference

### Common API Patterns

#### Basic Completion
```python
from openai import OpenAI
client = OpenAI(api_key="your-key")

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are helpful"},
        {"role": "user", "content": "Hello!"}
    ]
)

print(response.choices[0].message.content)
```

#### Streaming Response
```python
stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Tell me a story"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

#### With Temperature Control
```python
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    temperature=0.2,  # More focused
    messages=[...]
)
```

#### With Max Tokens
```python
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    max_tokens=100,  # Limit response length
    messages=[...]
)
```

---

### Prompt Engineering Tips

#### Be Specific
❌ Bad: "Write about AI"
✅ Good: "Write a 200-word explanation of how transformers work, for beginners"

#### Give Examples (Few-Shot)
```python
messages = [
    {"role": "system", "content": "Extract names from text"},
    {"role": "user", "content": "Text: John went to Paris\nName:"},
    {"role": "assistant", "content": "John"},
    {"role": "user", "content": "Text: Mary loves coding\nName:"},
    {"role": "assistant", "content": "Mary"},
    {"role": "user", "content": "Text: Bob and Alice are friends\nName:"}
]
```

#### Use Delimiters
```python
prompt = """
Extract the key points from the following text:
###
{text}
###
Format as bullet points.
"""
```

#### Specify Format
```python
prompt = """
Analyze this review and return JSON:
{
  "sentiment": "positive/negative/neutral",
  "score": 0-10,
  "key_points": ["point1", "point2"]
}
"""
```

---

### Cost Optimization Tips

1. **Use Right Model**
   - GPT-3.5 for simple tasks (20x cheaper)
   - GPT-4 only when needed

2. **Optimize Prompts**
   - Shorter = cheaper
   - Remove unnecessary context

3. **Implement Caching**
   - Cache common responses
   - Use semantic cache

4. **Set Max Tokens**
   - Limit response length
   - Avoid runaway costs

5. **Monitor Usage**
   - Track costs daily
   - Set up budget alerts

---

### Common Error Solutions

#### "Rate limit exceeded"
- You're making requests too fast
- Solution: Add delay between requests
- Use exponential backoff

```python
import time
from openai import RateLimitError

try:
    response = client.chat.completions.create(...)
except RateLimitError:
    time.sleep(60)  # Wait 1 minute
    response = client.chat.completions.create(...)
```

#### "Invalid API key"
- Check key is correct
- Check key has required permissions
- Regenerate if needed

#### "Context length exceeded"
- Your input is too long
- Solution: Truncate input or use smaller context

```python
def truncate_context(messages, max_tokens=4000):
    # Keep system message and recent messages only
    return [messages[0]] + messages[-10:]
```

#### "Model not found"
- Check model name spelling
- Check you have access to that model
- Use available models list:

```python
models = client.models.list()
for model in models.data:
    print(model.id)
```

---

### Environment Setup Checklist

#### Python Environment
```bash
# Create virtual environment
python -m venv ai-env

# Activate (Mac/Linux)
source ai-env/bin/activate

# Activate (Windows)
ai-env\Scripts\activate

# Install packages
pip install openai langchain pinecone-client chromadb streamlit
```

#### Environment Variables
```bash
# .env file
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
PINECONE_API_KEY=...
```

```python
# Load in Python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
```

---

## Your Action Plan

### This Week (Days 1-7)
- [ ] Set up development environment
- [ ] Get API keys (OpenAI/Anthropic)
- [ ] Review workshop code
- [ ] Modify Project 1 with different personalities
- [ ] Build 3 variations of Project 2
- [ ] Join Discord communities
- [ ] Follow AI accounts on Twitter/LinkedIn

### Week 2-3
- [ ] Start Project 4 (RAG System)
- [ ] Read LangChain documentation
- [ ] Watch RAG tutorials
- [ ] Build simple document Q&A
- [ ] Add vector database
- [ ] Deploy to Streamlit Cloud

### Week 4-6
- [ ] Complete Project 4
- [ ] Start Project 5 (Multi-Agent)
- [ ] Learn LangGraph basics
- [ ] Build 2-agent system
- [ ] Expand to 3+ agents
- [ ] Share progress on LinkedIn

### Week 7-10
- [ ] Complete Project 5
- [ ] Plan Project 6 (Full Stack App)
- [ ] Learn FastAPI basics
- [ ] Set up React frontend
- [ ] Integrate all learnings
- [ ] Build MVP

### Week 11-12
- [ ] Polish Project 6
- [ ] Write documentation
- [ ] Create demo video
- [ ] Update portfolio
- [ ] Apply to 10 jobs
- [ ] Prepare for interviews

---

## Final Thoughts

### You Have Everything You Need

Today you learned:
- ✅ How to call LLM APIs
- ✅ How to build AI applications
- ✅ How to add memory and tools
- ✅ What to build next
- ✅ Where the opportunities are

### The Path Forward

```
Today → Practice → Build → Share → Get Hired
  ↓        ↓         ↓       ↓         ↓
  1hr      2wks     2mos    Daily    3mos
```

### Remember

1. **AI development is accessible** - You don't need a PhD
2. **Start building immediately** - Don't wait for perfect knowledge
3. **Share your journey** - Document and post online
4. **Join communities** - You can't do this alone
5. **Stay consistent** - 1 hour daily > 7 hours once a week

### Keep in Touch

- **Twitter/X:** @codewitharjit
- **LinkedIn:** Arjit Verma
- **Instagram:** 183k+ followers
- **Workshop Discord:** [Link shared in group]

---

## Cheat Sheet

### Essential Commands
```bash
# Install packages
pip install openai langchain chromadb streamlit

# Run Python file
python app.py

# Run Streamlit app
streamlit run app.py

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### Model Names
- **GPT-3.5 Turbo**: `gpt-3.5-turbo` (fast, cheap)
- **GPT-4**: `gpt-4` (smart, expensive)
- **GPT-4 Turbo**: `gpt-4-turbo` (balanced)
- **Claude 3 Opus**: `claude-3-opus-20240229` (best)
- **Claude 3 Sonnet**: `claude-3-sonnet-20240229` (balanced)

### Quick Patterns
```python
# Simple call
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello"}]
)

# With system prompt
messages=[
    {"role": "system", "content": "You are..."},
    {"role": "user", "content": "..."}
]

# With history
messages.append({"role": "user", "content": user_input})
messages.append({"role": "assistant", "content": ai_response})
```

---

**Generated at:** AI Workshop - November 2025
**Last Updated:** Workshop Day
**Questions?** Reach out on social media or Discord!

**Now go build something amazing! 🚀**
