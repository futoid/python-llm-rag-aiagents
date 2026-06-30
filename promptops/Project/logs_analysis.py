"""
PromptOps CLI — Module 1 contribution

Simulates a log of past prompt calls (this is the shape we'll eventually
get from real API responses + our own logging in later modules) and
applies Pythonic data handling to analyze it.
"""

PROMPT_LOGS = [
    {"prompt": "summarize this article", "model": "gpt-4", "tokens": 120, "cost": 0.0036, "success": True},
    {"prompt": "translate to french", "model": "claude-sonnet", "tokens": 80, "cost": 0.0012, "success": True},
    {"prompt": "classify sentiment", "model": "gpt-4", "tokens": 200, "cost": 0.006, "success": False},
    {"prompt": "extract entities", "model": "gemini-pro", "tokens": 50, "cost": 0.0005, "success": True},
    {"prompt": "rank these options", "model": "claude-sonnet", "tokens": 300, "cost": 0.0045, "success": True},
]


def total_cost(logs):
    """Sum cost across all logs. Generator expression -> sum(), no accumulator loop needed."""
    return sum(log["cost"] for log in logs)


def successful_only(logs):
    """Filter via list comprehension - the Pythonic default over filter()."""
    return [log for log in logs if log["success"]]


def by_model(logs):
    """
    Group logs by model into a dict of lists.
    No Java Collectors.groupingBy() needed - just a plain dict + comprehension-friendly loop.
    """
    grouped = {}
    for log in logs:
        model = log["model"]
        grouped.setdefault(model, []).append(log)  # setdefault avoids a manual 'if key not in dict' check
    return grouped


def most_expensive(logs, top_n=3):
    """sorted() with key= and reverse=True is your Comparator.reversed() equivalent."""
    return sorted(logs, key=lambda log: log["cost"], reverse=True)[:top_n]


def average_tokens_per_model(logs):
    """Dict comprehension combined with a nested generator expression."""
    grouped = by_model(logs)
    return {
        model: sum(log["tokens"] for log in entries) / len(entries)
        for model, entries in grouped.items()
    }


def prompt_word_counts(logs):
    """Dict comprehension mapping each prompt to its word count."""
    return {log["prompt"]: len(log["prompt"].split()) for log in logs}


if __name__ == "__main__":
    print("All logs:", len(PROMPT_LOGS))

    print("\nTotal cost across all calls:", round(total_cost(PROMPT_LOGS), 4))

    success_logs = successful_only(PROMPT_LOGS)
    print("\nSuccessful calls:", [log["prompt"] for log in success_logs])

    grouped = by_model(PROMPT_LOGS)
    print("\nGrouped by model:")
    for model, entries in grouped.items():
        print(f"  {model}: {[e['prompt'] for e in entries]}")

    top_3 = most_expensive(PROMPT_LOGS, top_n=3)
    print("\nTop 3 most expensive calls:")
    for log in top_3:
        print(f"  {log['prompt']} -> ${log['cost']}")

    print("\nAverage tokens per model:", average_tokens_per_model(PROMPT_LOGS))

    print("\nWord counts per prompt:", prompt_word_counts(PROMPT_LOGS))
