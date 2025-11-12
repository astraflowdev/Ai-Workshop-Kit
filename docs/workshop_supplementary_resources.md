# AI Workshop - Supplementary Resources
## Supporting Materials, Examples, and Templates

---

## REAL AI-NATIVE APP EXAMPLES (For Slide 7)

### 1. LTX Studio
- **URL:** https://ltx.studio
- **What it does:** AI-powered video creation platform that turns text stories into complete videos
- **Tech Stack:**
  - Frontend: React/Next.js
  - AI: GPT-4 for script generation, Stable Diffusion for images, AI video models
  - Backend: Python, FastAPI
- **User Flow:** Write story → AI generates storyboard → AI creates visuals → AI adds narration → Complete video
- **Why it's impressive:** Full video production pipeline automated with AI
- **Founded:** 2023
- **Funding:** Seed stage

### 2. Julius AI
- **URL:** https://julius.ai
- **What it does:** AI data analyst - upload CSV/Excel, ask questions in plain English, get visualizations
- **Tech Stack:**
  - GPT-4 + Code Interpreter
  - Python for data analysis (pandas, matplotlib)
  - React frontend
- **User Flow:** Upload data → Ask "What are sales trends?" → AI writes Python code → Executes it → Returns charts
- **Why it's impressive:** Makes data analysis accessible to non-technical users
- **Use case:** Business analysts, researchers, students

### 3. Notion AI
- **URL:** https://notion.so/product/ai
- **What it does:** Writing assistant integrated into Notion workspace
- **Tech Stack:**
  - Custom-tuned LLMs (likely GPT-4 based)
  - RAG for workspace context
  - Proprietary integration layer
- **Features:**
  - Highlight text → AI improves/expands/summarizes
  - Generate content from scratch
  - Answer questions about your workspace
- **Why it's impressive:** Seamless integration, context-aware

### 4. Perplexity AI
- **URL:** https://perplexity.ai
- **What it does:** AI-powered search engine with citations
- **Tech Stack:**
  - LLMs (GPT-4, Claude, own models)
  - Web scraping + indexing
  - Citation system
  - Real-time search
- **User Flow:** Ask question → AI searches web → Synthesizes answer → Provides sources
- **Why it's impressive:** Combines LLM intelligence with current information
- **Business model:** Freemium (Pro version $20/month)

### 5. Cursor
- **URL:** https://cursor.sh
- **What it does:** AI-first code editor (fork of VS Code)
- **Tech Stack:**
  - VS Code foundation
  - GPT-4 integration
  - Custom code context system
  - Codebase indexing
- **Features:**
  - "Cmd+K" to edit code with AI
  - Chat with your codebase
  - AI understands your entire project
- **Why it's impressive:** Game-changing for developers
- **Pricing:** $20/month (free tier available)

### 6. Durable
- **URL:** https://durable.co
- **What it does:** Website builder via conversational AI
- **Tech Stack:**
  - GPT-4 for understanding business needs
  - Template generation system
  - React/Next.js for site rendering
- **User Flow:** Describe business → AI generates complete website → Edit via chat → Deploy
- **Why it's impressive:** 30 seconds to launch a business website
- **Target:** Small business owners, non-technical users

### 7. Jasper AI
- **URL:** https://jasper.ai
- **What it does:** AI content generation for marketing
- **Features:** Blog posts, social media, ads, emails
- **Tech Stack:** GPT-4 + custom fine-tuning
- **Business:** $10M+ ARR, unicorn valuation
- **Why it matters:** Proof of AI business viability

### 8. Copy.ai
- **URL:** https://copy.ai
- **Similar to Jasper:** Marketing copy generation
- **Difference:** More affordable, simpler interface
- **Tech Stack:** GPT-4 API + prompt templates
- **Why it matters:** Shows you can build profitable AI businesses on top of APIs

### 9. Mem
- **URL:** https://mem.ai
- **What it does:** AI-powered note-taking with automatic organization
- **Features:**
  - Automatic tagging and categorization
  - AI-powered search (semantic, not keyword)
  - Knowledge graph of your notes
- **Tech Stack:** GPT-4 + embeddings + vector database

### 10. Otter.ai
- **URL:** https://otter.ai
- **What it does:** AI meeting transcription and notes
- **Features:**
  - Real-time transcription
  - Speaker identification
  - Action item extraction
  - Meeting summaries
- **Tech Stack:** Whisper (speech-to-text) + GPT-4 (summarization)
- **Business model:** Freemium, used by millions

---

## CODE TEMPLATES

### Template 1: Basic Chatbot (chatbot.py)
```python
"""
Project 1: Basic AI Chatbot
Description: Simple CLI chatbot that responds to user input
Author: Workshop participants
"""

from openai import OpenAI
import os

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Use environment variable

def main():
    print("=== AI Chatbot ===")
    print("Type 'quit' to exit\n")
    
    # Get user input
    user_message = input("You: ")
    
    # Check for exit
    if user_message.lower() == 'quit':
        print("Goodbye!")
        return
    
    # Make API call
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0.7,
            messages=[
                {
                    "role": "system", 
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )
        
        # Print response
        ai_message = response.choices[0].message.content
        print(f"\nAI: {ai_message}\n")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
```

### Template 2: Memory Chatbot (chatbot_memory.py)
```python
"""
Project 2: Chatbot with Memory
Description: Chatbot that remembers conversation history
Author: Workshop participants
"""

from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def main():
    print("=== AI Chatbot with Memory ===")
    print("Type 'quit' to exit\n")
    
    # Initialize conversation history
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant with a friendly personality."
        }
    ]
    
    # Conversation loop
    while True:
        # Get user input
        user_input = input("You: ")
        
        # Check for exit
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break
        
        # Add user message to history
        messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Get AI response
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                temperature=0.7,
                messages=messages  # Send full history
            )
            
            # Extract AI message
            ai_message = response.choices[0].message.content
            print(f"\nAI: {ai_message}\n")
            
            # Add AI response to history
            messages.append({
                "role": "assistant",
                "content": ai_message
            })
            
        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    main()
```

### Template 3: Function-Calling Bot (function_chatbot.py)
```python
"""
Project 3: Function-Calling Chatbot
Description: Chatbot that can call functions (tools)
Author: Workshop participants
"""

from openai import OpenAI
import os
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define available functions
def get_weather(location):
    """Simulated weather function"""
    # In real app, call weather API
    weather_data = {
        "Delhi": "Sunny, 28°C",
        "Mumbai": "Rainy, 26°C",
        "Bangalore": "Cloudy, 24°C"
    }
    return weather_data.get(location, "Weather data not available")

# Function definitions for LLM
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
                        "description": "City name, e.g. Delhi"
                    }
                },
                "required": ["location"]
            }
        }
    }
]

def main():
    print("=== AI Assistant with Tools ===")
    print("Try: 'What's the weather in Delhi?'\n")
    
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that can check weather."
        }
    ]
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() == 'quit':
            break
        
        messages.append({"role": "user", "content": user_input})
        
        try:
            # First API call - check if function needed
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )
            
            response_message = response.choices[0].message
            
            # Check if function call requested
            if response_message.tool_calls:
                # Execute function
                function_name = response_message.tool_calls[0].function.name
                function_args = json.loads(
                    response_message.tool_calls[0].function.arguments
                )
                
                if function_name == "get_weather":
                    function_response = get_weather(
                        location=function_args.get("location")
                    )
                    
                    # Add function result to messages
                    messages.append(response_message)
                    messages.append({
                        "role": "tool",
                        "tool_call_id": response_message.tool_calls[0].id,
                        "name": function_name,
                        "content": function_response
                    })
                    
                    # Get final response
                    final_response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=messages
                    )
                    
                    ai_message = final_response.choices[0].message.content
                    print(f"\nAI: {ai_message}\n")
                    
                    messages.append({
                        "role": "assistant",
                        "content": ai_message
                    })
            else:
                # No function call, regular response
                ai_message = response_message.content
                print(f"\nAI: {ai_message}\n")
                messages.append({"role": "assistant", "content": ai_message})
                
        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    main()
```

---

## 5-PROJECT ROADMAP (Detailed Breakdown)

### PROJECT 1: Personal Chatbot (Week 1)
**Status:** ✅ You built this today!

**What to do next:**
1. Add error handling
2. Deploy to Replit or Streamlit Cloud
3. Add web interface (Flask or Streamlit)
4. Customize personality
5. Share on LinkedIn

**Resources:**
- Streamlit docs: https://docs.streamlit.io
- Replit: https://replit.com
- Flask quickstart: https://flask.palletsprojects.com

---

### PROJECT 2: RAG Chatbot (Week 2)
**Goal:** Build "Chat with your PDFs" application

**What you'll learn:**
- Embeddings and vector representations
- Vector databases (Pinecone/ChromaDB)
- Semantic search
- RAG architecture

**Tech Stack:**
- LangChain or LlamaIndex
- OpenAI embeddings
- Pinecone or ChromaDB (vector DB)
- Streamlit (UI)

**Steps:**
1. Load PDF documents
2. Split into chunks (RecursiveCharacterTextSplitter)
3. Generate embeddings for each chunk
4. Store in vector database
5. For queries: Embed query → Find similar chunks → Pass to LLM → Generate answer

**Code starter:**
```python
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

# Load PDF
loader = PyPDFLoader("document.pdf")
documents = loader.load()

# Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
texts = text_splitter.split_documents(documents)

# Create embeddings and store
embeddings = OpenAIEmbeddings()
vectorstore = Pinecone.from_documents(texts, embeddings)

# Create QA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    retriever=vectorstore.as_retriever()
)

# Query
answer = qa_chain.run("What is this document about?")
```

**Resources:**
- LangChain docs: https://docs.langchain.com
- Pinecone quickstart: https://docs.pinecone.io
- Tutorial: https://www.youtube.com/watch?v=... [add link]

---

### PROJECT 3: Function-Calling Assistant (Week 3)
**Status:** ✅ You built the basics today!

**What to expand:**
1. Add more functions (search web, send email, etc.)
2. Add error handling for API failures
3. Create multi-tool agent
4. Add authentication for sensitive functions

**Additional functions to add:**
- Web search (using SerpAPI)
- Send email (using Gmail API)
- Check calendar (Google Calendar API)
- Get news (NewsAPI)
- Search Wikipedia

---

### PROJECT 4: AI Automation Workflow (Week 4)
**Goal:** Build "Gmail → AI Extract → Update Notion" automation

**What you'll learn:**
- Workflow automation
- n8n or Make.com
- API integrations
- Event-driven architecture

**Use n8n (open source):**
1. Gmail Trigger: New email arrives
2. LLM Node: Extract key info (using OpenAI)
3. Notion Node: Create/update page with extracted data

**Real-world use cases:**
- Auto-categorize support tickets
- Extract invoice data → Update spreadsheet
- Social media monitoring → Sentiment analysis → Slack alert
- Meeting transcription → Action items → Task creation

**Resources:**
- n8n docs: https://docs.n8n.io
- Make.com: https://make.com
- Zapier AI: https://zapier.com/ai

---

### PROJECT 5: AI Research Agent (Week 5)
**Goal:** Build autonomous research agent

**What you'll learn:**
- Agent architecture
- ReAct pattern (Reasoning + Acting)
- Multi-step reasoning
- Tool orchestration

**Agent capabilities:**
1. Take research query
2. Plan research approach
3. Search web for sources
4. Read and extract key info
5. Synthesize findings
6. Generate comprehensive report

**Tech Stack:**
- LangChain Agents
- SerpAPI (web search)
- Web scraping (BeautifulSoup)
- OpenAI GPT-4

**Code starter:**
```python
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from langchain.utilities import SerpAPIWrapper

# Define tools
search = SerpAPIWrapper()
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="Search the web for information"
    )
]

# Initialize agent
agent = initialize_agent(
    tools=tools,
    llm=OpenAI(temperature=0),
    agent="zero-shot-react-description",
    verbose=True
)

# Run agent
result = agent.run("Research the latest trends in AI development")
```

---

## COMMON ERRORS & SOLUTIONS

### Error 1: "Module 'openai' not found"
**Solution:**
```bash
pip install openai --break-system-packages  # If on system Python
# OR
pip install openai  # In virtual environment
```

### Error 2: "Invalid API key"
**Check:**
1. Key is correct (starts with sk-...)
2. No extra spaces
3. Using environment variable correctly
4. Account has credits

### Error 3: "Rate limit exceeded"
**Solution:**
- Wait a few seconds between requests
- Use exponential backoff
- Upgrade API plan if needed

### Error 4: "Context length exceeded"
**Solution:**
- Reduce message history
- Implement sliding window (keep only recent N messages)
- Use summarization for old messages

---

## RESOURCES CHECKLIST

### Free Learning Resources
- [ ] Andrew Ng's ChatGPT Prompt Engineering (DeepLearning.AI)
- [ ] LangChain Documentation
- [ ] OpenAI Cookbook
- [ ] Full Stack Deep Learning
- [ ] Pinecone learning center

### People to Follow
- [ ] @AndrewYNg (Andrew Ng)
- [ ] @karpathy (Andrej Karpathy)
- [ ] @codewitharjit (Workshop instructor)
- [ ] @LangChainAI
- [ ] @OpenAI

### Communities
- [ ] LangChain Discord
- [ ] OpenAI Community Forum
- [ ] Workshop Discord/WhatsApp group
- [ ] r/LangChain subreddit
- [ ] AI Builders community

---

## DEPLOYMENT GUIDES

### Deploy to Streamlit Cloud (Free)
1. Push code to GitHub
2. Sign up at streamlit.io/cloud
3. Connect GitHub repo
4. Add secrets (API keys)
5. Deploy!

### Deploy to Replit (Free tier)
1. Go to replit.com
2. Import from GitHub
3. Add .env file with API key
4. Click "Run"
5. Share public URL

### Deploy to Railway (Free tier)
1. railway.app
2. Connect GitHub
3. Add environment variables
4. Deploy

---

## PORTFOLIO TIPS

### GitHub README Template
```markdown
# My AI Projects

## About Me
[Your introduction]

## Projects

### 1. AI Chatbot with Memory
- **Tech:** Python, OpenAI API, Streamlit
- **Features:** Conversation memory, custom personalities
- **Demo:** [link]
- **Code:** [link]

### 2. Chat with PDFs (RAG)
- **Tech:** LangChain, Pinecone, OpenAI
- **Features:** Semantic search, document QA
- **Demo:** [link]

[Continue for all projects...]

## Skills
- LLM Integration (OpenAI, Anthropic)
- RAG Architecture
- Vector Databases
- Prompt Engineering
- Python, FastAPI, React

## Contact
- LinkedIn: [link]
- Twitter: [link]
- Email: [email]
```

---

## INTERVIEW PREPARATION

### Common Questions
1. "Walk me through a project you built with LLMs"
2. "How does RAG work and when would you use it?"
3. "How do you optimize prompt performance?"
4. "How do you handle LLM hallucinations?"
5. "Explain the difference between fine-tuning and RAG"
6. "How do you manage API costs?"
7. "How do you handle rate limits?"

### How to Answer
- Use STAR method (Situation, Task, Action, Result)
- Show actual code/GitHub
- Discuss trade-offs
- Mention metrics (latency, cost, accuracy)

---

## COST OPTIMIZATION TIPS

1. **Use cheaper models when possible**
   - GPT-3.5 for simple tasks
   - GPT-4 only when needed

2. **Cache responses**
   - Store common queries
   - Use Redis for caching

3. **Optimize prompts**
   - Shorter prompts = lower cost
   - Clear instructions reduce retries

4. **Batch requests**
   - Process multiple items together
   - Use async when possible

5. **Monitor usage**
   - Set up alerts
   - Track cost per feature
   - Log every API call

---

END OF SUPPLEMENTARY RESOURCES DOCUMENT
