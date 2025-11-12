"""
Project 5: Simple Multi-Agent System
Two agents working together: Researcher + Writer

This is a starter template. You'll build this in weeks 5-8!
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.config import Config
from utils.helpers import print_colored

print_colored("=" * 70, "cyan")
print_colored("SIMPLE MULTI-AGENT SYSTEM - Project 5 (Starter)", "green")
print_colored("=" * 70, "cyan")
print("\nTwo agents working together: Researcher → Writer")
print("This demonstrates the basics of multi-agent coordination!\n")

client = Config.get_openai_client()


class Agent:
    """Simple agent that can perform a task"""

    def __init__(self, name: str, role: str, goal: str):
        self.name = name
        self.role = role
        self.goal = goal

    def run(self, task: str, context: str = "") -> str:
        """Execute the agent's task"""

        print_colored(f"\n[{self.name} is working...]", "yellow")

        # Create specialized prompt for this agent
        system_prompt = (
            f"You are {self.name}, a {self.role}. "
            f"Your goal is: {self.goal}\n"
            f"Stay focused on your specific role and provide concise, high-quality output."
        )

        # Build messages
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{task}\n\nContext:\n{context}"},
        ]

        # Call LLM
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", temperature=0.7, messages=messages
        )

        result = response.choices[0].message.content
        print_colored(f"✓ {self.name} completed their task!", "green")

        return result


# Create agents
researcher = Agent(
    name="Researcher",
    role="Research Specialist",
    goal="Find accurate, relevant information and key points about the topic",
)

writer = Agent(
    name="Writer",
    role="Content Writer",
    goal="Create engaging, well-structured content based on research",
)


def multi_agent_workflow(topic: str) -> dict:
    """
    Orchestrate multiple agents to complete a task.

    Flow: Researcher → Writer
    """

    print_colored(f"\n{'='*70}", "cyan")
    print_colored(f"Starting multi-agent workflow for: {topic}", "green")
    print_colored(f"{'='*70}", "cyan")

    # Step 1: Researcher gathers information
    research_task = f"Research the topic: {topic}\n" f"Provide 5-7 key points and insights."

    research_notes = researcher.run(research_task)

    # Show research output
    print_colored("\n--- Research Notes ---", "cyan")
    print(research_notes[:200] + "..." if len(research_notes) > 200 else research_notes)

    # Step 2: Writer creates content based on research
    writing_task = (
        f"Write a short blog post (200-300 words) about: {topic}\n"
        f"Use the research notes provided."
    )

    blog_post = writer.run(writing_task, context=research_notes)

    # Show final output
    print_colored("\n--- Final Blog Post ---", "cyan")
    print(blog_post)

    return {"research": research_notes, "blog_post": blog_post}


# Main execution
if __name__ == "__main__":
    print("Example: Let's create a blog post about AI in healthcare\n")

    # Run the workflow
    result = multi_agent_workflow("AI in Healthcare")

    print_colored("\n" + "=" * 70, "cyan")
    print_colored("WORKFLOW COMPLETE!", "green")
    print_colored("=" * 70, "cyan")

    print("\nWhat happened:")
    print("1. Researcher agent gathered information about AI in healthcare")
    print("2. Writer agent used that research to create a blog post")
    print("3. Each agent had specialized role and focused output")

    print_colored("\n" + "=" * 70, "yellow")
    print_colored("Next Steps:", "yellow")
    print_colored("=" * 70, "yellow")
    print("\n1. Add more agents (Editor, SEO Specialist, Fact-Checker)")
    print("2. Implement feedback loops (agents can iterate)")
    print("3. Add tools for agents (web search, database access)")
    print("4. Use frameworks like LangGraph or AutoGen")
    print("5. Build a web interface\n")

    print("Try modifying the code:")
    print("  - Change the topic")
    print("  - Adjust agent prompts")
    print("  - Add a third agent (Editor)")
    print("  - Implement error handling\n")

    print_colored("See README.md for detailed multi-agent patterns!", "green")
