"""
Module 1: Pythonic Data Handling
Run with: python3 module_1_pythonic_data.py

Standalone file - no companion modules required.
"""

import json
import pprint
from functools import reduce


# ── List comprehensions ──────────────────────────────────────────────────────

def section_list_comprehensions():
    print("\n--- List Comprehensions ---")
    prompts = ["summarize", "translate", "classify", "extract", "rank"]

    # The old/Java-ish way: accumulator pattern
    result = []
    for p in prompts:
        if len(p) > 6:
            result.append(p.upper())
    print(result)

    # The Pythonic way: list comprehension
    # [ expression  for item in iterable  if condition ]
    result2 = [p.upper() for p in prompts if len(p) > 6]
    print(result2)

    # This is the EXACT equivalent of Java's:
    # prompts.stream().filter(p -> p.length() > 6).map(String::toUpperCase).collect(Collectors.toList())

    # comprehension without filter - just transform
    lengths = [len(p) for p in prompts]
    print(lengths)

    # nested comprehension - flatten a list of lists
    batches = [["a", "b"], ["c", "d"], ["e"]]
    flat = [item for batch in batches for item in batch]
    print(flat)


# ── Dictionary comprehensions ────────────────────────────────────────────────

def section_dict_comprehensions():
    print("\n--- Dictionary Comprehensions ---")
    prompts = ["summarize", "translate", "classify", "extract"]

    # { key_expr: value_expr  for item in iterable }
    length_map = {p: len(p) for p in prompts}
    print(length_map)

    # with a filter condition
    long_ones = {p: len(p) for p in prompts if len(p) > 7}
    print(long_ones)

    # building a dict from two parallel lists (like zipping two arrays in Java)
    models = ["gpt-4", "claude-sonnet", "gemini-pro"]
    costs = [0.03, 0.015, 0.01]
    cost_map = {m: c for m, c in zip(models, costs)}
    print(cost_map)

    # inverting a dict (swap keys and values) - common real-world need
    inverted = {v: k for k, v in cost_map.items()}
    print(inverted)


# ── Nested dictionaries and JSON-like data ──────────────────────────────────

def section_nested_json():
    print("\n--- Nested Dicts & JSON-like Data ---")

    # A realistic LLM-API-shaped response, just as a Python literal
    response = {
        "id": "chatcmpl-123",
        "model": "gpt-4",
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": "Paris is the capital of France."},
                "finish_reason": "stop",
            }
        ],
        "usage": {"prompt_tokens": 12, "completion_tokens": 8, "total_tokens": 20},
    }

    # Navigating nested dicts: chain [] like .get() chains in Java,
    # but without null-checking ceremony at every step (careful - this can KeyError!)
    content = response["choices"][0]["message"]["content"]
    print(content)

    total_tokens = response["usage"]["total_tokens"]
    print(total_tokens)

    # json.dumps() <-> json.loads() are your serialize/deserialize pair
    # (like Jackson's writeValueAsString / readValue, but built into the stdlib)
    json_string = json.dumps(response, indent=2)
    print(json_string[:120], "...")

    parsed_back = json.loads(json_string)
    print(parsed_back["model"])

    # pretty-printing nested structures for debugging - nicer than println on a Map
    pprint.pprint(response["usage"])


# ── Sorting, filtering, mapping, and reducing ───────────────────────────────

def section_sort_filter_map_reduce():
    print("\n--- Sorting, Filtering, Mapping, Reducing ---")

    logs = [
        {"prompt": "summarize", "tokens": 120, "cost": 0.003},
        {"prompt": "translate", "tokens": 80, "cost": 0.002},
        {"prompt": "classify", "tokens": 200, "cost": 0.006},
        {"prompt": "extract", "tokens": 50, "cost": 0.001},
    ]

    # SORTING - sorted() returns a NEW list, doesn't mutate (like Stream.sorted())
    # key= takes a function that extracts what to sort by - this is your Comparator
    by_tokens = sorted(logs, key=lambda log: log["tokens"])
    print([l["prompt"] for l in by_tokens])

    # descending - reverse=True, no need for Comparator.reversed()
    by_tokens_desc = sorted(logs, key=lambda log: log["tokens"], reverse=True)
    print([l["prompt"] for l in by_tokens_desc])

    # FILTERING - usually just done with a list comprehension (more Pythonic than filter())
    expensive = [l for l in logs if l["cost"] > 0.002]
    print([l["prompt"] for l in expensive])

    # filter() exists too (lazy, like Stream.filter) but comprehensions are preferred in practice
    expensive_v2 = list(filter(lambda l: l["cost"] > 0.002, logs))
    print([l["prompt"] for l in expensive_v2])

    # MAPPING - again, comprehension preferred over map()
    prompt_names = [l["prompt"] for l in logs]
    print(prompt_names)

    # REDUCING - sum(), max(), min() cover 90% of cases without needing reduce() at all
    # generator expression, no [] needed when passed directly to a function
    total_cost = sum(l["cost"] for l in logs)
    print(round(total_cost, 4))

    # reduce() itself - for when sum()/max() aren't enough (rare in practice)
    total_tokens = reduce(lambda acc, l: acc + l["tokens"], logs, 0)
    print(total_tokens)


# ── Handling None, optional values, and defaults ────────────────────────────

def section_none_and_falsy():
    print("\n--- None Handling & Falsy Values ---")

    config = {"model": "gpt-4", "temperature": 0.7}

    # .get() with a default - avoids KeyError, like Java's Map.getOrDefault()
    max_tokens = config.get("max_tokens", 512)
    print(max_tokens)   # 512, key doesn't exist, default used

    model = config.get("model", "default-model")
    print(model)         # gpt-4, key exists, default ignored

    # direct [] access throws if missing - like Map.get() returning null,
    # but here it's a KeyError exception
    try:
        print(config["max_tokens"])
    except KeyError as e:
        print(f"KeyError: {e}")

    # checking for None explicitly
    result = None
    if result is None:        # use 'is None', NOT '== None' - strong Python convention
        print("no result yet")

    # falsy values - Python treats several things as 'falsy' in an if-check:
    # None, False, 0, 0.0, '', [], {}, set() are all falsy
    def describe(value):
        if not value:
            return "empty or falsy"
        return f"has value: {value}"

    print(describe(None))
    print(describe(""))
    print(describe([]))
    print(describe(0))
    print(describe("hello"))
    print(describe([1, 2]))

    # the walrus operator := lets you assign AND check in one expression (Python 3.8+)
    data = {"tokens": 0}
    if (t := data.get("tokens")) is not None:
        print(f"tokens present: {t}")


if __name__ == "__main__":
    section_list_comprehensions()
    section_dict_comprehensions()
    section_nested_json()
    section_sort_filter_map_reduce()
    section_none_and_falsy()
