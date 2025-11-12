# Project 5: Multi-Agent System

**Timeline:** 4-8 weeks to complete
**Difficulty:** 🌶️🌶️🌶️🌶️ Advanced

## What are Multi-Agent Systems?

Instead of one AI doing everything, you have multiple specialized AI agents working together!

### Single Agent (Limited)
```
User: "Create a blog post about AI"
     ↓
One AI does everything
     ↓
Result: Okay-ish blog post
```

### Multi-Agent (Powerful)
```
User: "Create a blog post about AI"
     ↓
Researcher Agent → Finds latest info
     ↓
Writer Agent → Writes draft
     ↓
Editor Agent → Improves writing
     ↓
SEO Agent → Optimizes for search
     ↓
Result: High-quality, optimized blog post!
```

## Why Multi-Agent?

### Specialization
- Each agent is expert in one task
- Better prompts for specific roles
- Higher quality output

### Parallelization
- Agents can work simultaneously
- Faster completion
- Better resource utilization

### Scalability
- Add new agents without changing others
- Easy to extend functionality
- Modular architecture

## Architecture Patterns

### 1. Sequential Pipeline
```
Agent 1 → Agent 2 → Agent 3 → Final Output
```
Example: Research → Write → Edit → Publish

### 2. Hierarchical
```
        Manager Agent
        /    |    \
    Agent1 Agent2 Agent3
```
Example: Manager delegates tasks to worker agents

### 3. Collaborative
```
Agent1 ←→ Agent2 ←→ Agent3
```
Example: Agents discuss and iterate together

## Tech Stack

### Frameworks

1. **LangGraph** (Recommended for beginners)
   - Built by LangChain team
   - Graph-based agent orchestration
   - Great documentation

2. **AutoGen** (Microsoft)
   - Conversational agents
   - Complex multi-agent scenarios
   - Group chat capabilities

3. **CrewAI**
   - Role-based agents
   - Process-oriented
   - Easy to use

### Core Components
- **LLM**: GPT-4 or Claude (better for complex tasks)
- **Tools**: Function calling for agent actions
- **Memory**: Shared state between agents
- **Orchestrator**: Controls agent flow

## Example Use Cases

### Content Creation Team
```
Agents:
1. Researcher - Gathers information
2. Writer - Creates content
3. Editor - Improves quality
4. Fact-Checker - Verifies accuracy
5. SEO Specialist - Optimizes
```

### Customer Support
```
Agents:
1. Triage - Categorizes requests
2. Technical Support - Handles tech issues
3. Billing - Handles payments
4. Escalation - Manages complex cases
```

### Research Assistant
```
Agents:
1. Search - Finds relevant papers
2. Summarizer - Condenses content
3. Analyzer - Identifies patterns
4. Presenter - Creates report
```

## Files

- `simple_agents.py` - Basic 2-agent system
- `langgraph_example.py` - Using LangGraph framework
- `autogen_example.py` - Using AutoGen framework
- `agent_tools.py` - Shared tools for agents

## Quick Start

```bash
# Install dependencies
pip install langgraph autogen-agentchat

# Run simple example
python simple_agents.py

# Run LangGraph example
python langgraph_example.py
```

## Code Example (LangGraph)

### Define Agents

```python
from langgraph.graph import StateGraph, END
from langchain.llms import OpenAI
from langchain.agents import create_openai_tools_agent

# Define state
class State(TypedDict):
    task: str
    research_notes: str
    draft: str
    final: str

# Researcher Agent
def researcher_agent(state: State) -> State:
    llm = OpenAI(temperature=0.7)

    prompt = f"Research the following topic and provide key points: {state['task']}"
    research = llm(prompt)

    return {"research_notes": research}

# Writer Agent
def writer_agent(state: State) -> State:
    llm = OpenAI(temperature=0.8)

    prompt = f"Write a blog post based on this research:\n{state['research_notes']}"
    draft = llm(prompt)

    return {"draft": draft}

# Editor Agent
def editor_agent(state: State) -> State:
    llm = OpenAI(temperature=0.3)

    prompt = f"Edit and improve this blog post:\n{state['draft']}"
    final = llm(prompt)

    return {"final": final}

# Create workflow
workflow = StateGraph(State)

# Add nodes
workflow.add_node("researcher", researcher_agent)
workflow.add_node("writer", writer_agent)
workflow.add_node("editor", editor_agent)

# Add edges (flow)
workflow.add_edge("researcher", "writer")
workflow.add_edge("writer", "editor")
workflow.add_edge("editor", END)

# Set entry point
workflow.set_entry_point("researcher")

# Compile
app = workflow.compile()

# Run
result = app.invoke({"task": "AI in healthcare"})
print(result["final"])
```

## Agent Communication Patterns

### 1. Direct Handoff
```python
# Agent 1 finishes → Agent 2 starts
result1 = agent1.run(task)
result2 = agent2.run(result1)
```

### 2. Shared Memory
```python
# Agents read/write to shared state
memory = {"context": "", "results": []}
agent1.run(memory)
agent2.run(memory)
```

### 3. Message Passing
```python
# Agents send messages to each other
agent1.send_message(agent2, "Here's my analysis")
response = agent2.receive_message()
```

## Best Practices

### 1. Clear Agent Roles
```python
researcher = {
    "role": "Research Specialist",
    "goal": "Find accurate, recent information",
    "backstory": "Expert researcher with attention to detail"
}
```

### 2. Avoid Circular Loops
```python
# Bad: Agents can loop forever
# Good: Set max iterations
max_iterations = 5
```

### 3. Error Handling
```python
try:
    result = agent.run(task)
except Exception as e:
    # Fallback to simpler approach
    result = fallback_agent.run(task)
```

### 4. Cost Management
```python
# Multi-agent = More API calls = Higher cost
# Solution: Cache results, use cheaper models when possible

if task_complexity < 5:
    model = "gpt-3.5-turbo"  # Cheaper
else:
    model = "gpt-4"  # More capable
```

## Performance Tips

### 1. Parallel Execution
```python
import asyncio

# Run independent agents in parallel
results = await asyncio.gather(
    agent1.arun(task1),
    agent2.arun(task2),
    agent3.arun(task3)
)
```

### 2. Smart Routing
```python
# Route to appropriate agent based on task type
def route_task(task):
    if "code" in task.lower():
        return code_agent
    elif "write" in task.lower():
        return writer_agent
    else:
        return general_agent
```

### 3. Caching
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def expensive_agent_call(input_text):
    return agent.run(input_text)
```

## Common Challenges

### 1. Coordination Overhead
- Solution: Keep agent count reasonable (3-5 agents)
- Use manager agent for complex coordination

### 2. Inconsistent Quality
- Solution: Add validation agent
- Implement retry logic

### 3. High Costs
- Solution: Use cheaper models for simple tasks
- Implement caching and batching

### 4. Debugging
- Solution: Log all agent interactions
- Use LangSmith for tracing

## Advanced Patterns

### Self-Improving Agents
```python
# Agent evaluates its own output and improves
result = agent.run(task)
evaluation = evaluator_agent.run(result)

if evaluation.score < 8:
    improved_result = agent.run(task, feedback=evaluation)
```

### Dynamic Agent Creation
```python
# Create agents on-the-fly based on task
def create_specialist(domain):
    return Agent(
        role=f"{domain} Specialist",
        tools=get_tools_for_domain(domain)
    )
```

## Real-World Applications

1. **Software Development**
   - Code Writer → Code Reviewer → Tester → Documenter

2. **Content Production**
   - Researcher → Writer → Editor → Designer → Publisher

3. **Data Analysis**
   - Data Collector → Cleaner → Analyzer → Visualizer → Reporter

4. **Customer Service**
   - Classifier → Specialist → QA Checker → Responder

## Learning Path

### Week 1-2: Basics
- Build 2-agent system (researcher + writer)
- Understand state management
- Learn agent communication

### Week 3-4: Frameworks
- Master LangGraph
- Try AutoGen
- Compare approaches

### Week 5-6: Advanced
- Implement error handling
- Add complex workflows
- Optimize performance

### Week 7-8: Production
- Add monitoring
- Implement caching
- Deploy system

## Resources

- **LangGraph Docs**: https://langchain-ai.github.io/langgraph/
- **AutoGen Docs**: https://microsoft.github.io/autogen/
- **CrewAI**: https://github.com/joaomdmoura/crewAI
- **Paper**: "Communicative Agents for Software Development"

## Next Steps

After completing this project:
1. Build your own multi-agent application
2. Combine with RAG (Project 4) for powerful systems
3. Deploy as production service
4. **Move to Project 6**: Full-stack AI application!

---

**Starter Code**: See `simple_agents.py` to get started
**Framework Example**: See `langgraph_example.py`
**Documentation**: Follow README step-by-step
