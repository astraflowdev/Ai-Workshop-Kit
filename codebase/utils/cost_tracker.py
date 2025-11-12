"""
Cost tracking utility for AI API usage.
Helps monitor and control spending on LLM APIs.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional


# Pricing per 1000 tokens (as of November 2025)
PRICING = {
    "gpt-4": {"input": 0.03, "output": 0.06},
    "gpt-4-turbo": {"input": 0.01, "output": 0.03},
    "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
    "claude-3-opus": {"input": 0.015, "output": 0.075},
    "claude-3-sonnet": {"input": 0.003, "output": 0.015},
    "claude-3-haiku": {"input": 0.00025, "output": 0.00125},
    "gemini-pro": {"input": 0.00025, "output": 0.0005},
}


class CostTracker:
    """Track and analyze API costs"""

    def __init__(self, log_file: str = "cost_log.json"):
        """
        Initialize cost tracker.

        Args:
            log_file: Path to JSON file for cost logging
        """
        self.log_file = Path(log_file)
        self.costs = self._load_log()

    def _load_log(self) -> list:
        """Load existing cost log"""
        if self.log_file.exists():
            with open(self.log_file, "r") as f:
                return json.load(f)
        return []

    def _save_log(self):
        """Save cost log to file"""
        with open(self.log_file, "w") as f:
            json.dump(self.costs, f, indent=2)

    def calculate_cost(
        self, model: str, input_tokens: int, output_tokens: int
    ) -> float:
        """
        Calculate cost for a single API call.

        Args:
            model: Model name
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens

        Returns:
            Cost in dollars
        """
        if model not in PRICING:
            print(f"Warning: Pricing not found for {model}, using gpt-3.5-turbo rates")
            model = "gpt-3.5-turbo"

        pricing = PRICING[model]
        input_cost = (input_tokens / 1000) * pricing["input"]
        output_cost = (output_tokens / 1000) * pricing["output"]

        return input_cost + output_cost

    def log_request(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int,
        project: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> float:
        """
        Log an API request and return cost.

        Args:
            model: Model used
            input_tokens: Input tokens count
            output_tokens: Output tokens count
            project: Project name (optional)
            notes: Additional notes (optional)

        Returns:
            Cost of this request
        """
        cost = self.calculate_cost(model, input_tokens, output_tokens)

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost": cost,
            "project": project,
            "notes": notes,
        }

        self.costs.append(log_entry)
        self._save_log()

        return cost

    def get_total_cost(self, project: Optional[str] = None) -> float:
        """
        Get total cost, optionally filtered by project.

        Args:
            project: Filter by project name (optional)

        Returns:
            Total cost in dollars
        """
        if project:
            filtered_costs = [c for c in self.costs if c.get("project") == project]
        else:
            filtered_costs = self.costs

        return sum(c["cost"] for c in filtered_costs)

    def get_stats(self) -> dict:
        """
        Get usage statistics.

        Returns:
            Dictionary with various stats
        """
        if not self.costs:
            return {
                "total_cost": 0,
                "total_requests": 0,
                "total_tokens": 0,
                "avg_cost_per_request": 0,
            }

        total_cost = sum(c["cost"] for c in self.costs)
        total_requests = len(self.costs)
        total_tokens = sum(
            c["input_tokens"] + c["output_tokens"] for c in self.costs
        )

        # Cost by model
        cost_by_model = {}
        for entry in self.costs:
            model = entry["model"]
            cost_by_model[model] = cost_by_model.get(model, 0) + entry["cost"]

        # Cost by project
        cost_by_project = {}
        for entry in self.costs:
            project = entry.get("project", "Unknown")
            cost_by_project[project] = cost_by_project.get(project, 0) + entry["cost"]

        return {
            "total_cost": total_cost,
            "total_requests": total_requests,
            "total_tokens": total_tokens,
            "avg_cost_per_request": total_cost / total_requests if total_requests > 0 else 0,
            "cost_by_model": cost_by_model,
            "cost_by_project": cost_by_project,
        }

    def print_summary(self):
        """Print cost summary"""
        stats = self.get_stats()

        print("=" * 60)
        print("API COST SUMMARY")
        print("=" * 60)
        print(f"Total Cost: ${stats['total_cost']:.4f}")
        print(f"Total Requests: {stats['total_requests']}")
        print(f"Total Tokens: {stats['total_tokens']:,}")
        print(f"Avg Cost/Request: ${stats['avg_cost_per_request']:.4f}")

        print("\nCost by Model:")
        for model, cost in stats["cost_by_model"].items():
            print(f"  {model}: ${cost:.4f}")

        if stats["cost_by_project"]:
            print("\nCost by Project:")
            for project, cost in stats["cost_by_project"].items():
                print(f"  {project}: ${cost:.4f}")

        print("=" * 60)

    def reset(self):
        """Clear all cost logs"""
        self.costs = []
        self._save_log()
        print("Cost log has been reset.")


# Convenience function
def track_cost(
    model: str,
    input_tokens: int,
    output_tokens: int,
    project: Optional[str] = None,
    tracker: Optional[CostTracker] = None,
) -> float:
    """
    Quick function to track a single request cost.

    Args:
        model: Model name
        input_tokens: Input token count
        output_tokens: Output token count
        project: Project name (optional)
        tracker: Existing tracker instance (optional)

    Returns:
        Cost in dollars
    """
    if tracker is None:
        tracker = CostTracker()

    return tracker.log_request(model, input_tokens, output_tokens, project)


# Example usage
if __name__ == "__main__":
    # Create tracker
    tracker = CostTracker("example_cost_log.json")

    # Log some example requests
    print("Logging example API requests...\n")

    # GPT-3.5 request
    cost1 = tracker.log_request(
        model="gpt-3.5-turbo",
        input_tokens=100,
        output_tokens=50,
        project="project-1",
        notes="Basic chatbot test",
    )
    print(f"Request 1 cost: ${cost1:.4f}")

    # GPT-4 request
    cost2 = tracker.log_request(
        model="gpt-4",
        input_tokens=500,
        output_tokens=300,
        project="project-2",
        notes="Complex reasoning task",
    )
    print(f"Request 2 cost: ${cost2:.4f}")

    # Claude request
    cost3 = tracker.log_request(
        model="claude-3-sonnet",
        input_tokens=200,
        output_tokens=150,
        project="project-1",
        notes="Alternative model test",
    )
    print(f"Request 3 cost: ${cost3:.4f}\n")

    # Print summary
    tracker.print_summary()

    # Get project-specific cost
    project1_cost = tracker.get_total_cost(project="project-1")
    print(f"\nProject 1 total cost: ${project1_cost:.4f}")
