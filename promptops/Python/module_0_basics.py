"""
Module 0: Python Basics Revision
Run with: python3 module_0_basics.py

Companion file: prompt_utils.py must be in the same folder
(see below — create that file too).
"""

import prompt_utils
from prompt_utils import truncate


# ── Variables, data types, strings, numbers, booleans ──────────────────────

def section_variables():
    print("\n--- Variables & Types ---")
    x = 5
    print(type(x))          # <class 'int'>
    x = "hello"              # totally legal - x now points to a string
    print(type(x))

    # No int vs Integer/long vs Long distinction - arbitrary precision ints
    big = 2 ** 100
    print(big)

    # Booleans are True/False (capitalized), not true/false
    flag = True
    print(flag and not flag)

    # f-strings are Python's StringBuilder/String.format equivalent
    name = "Aliek"
    age = 26
    print(f"{name} is {age} years old, next year: {age + 1}")


# ── Lists, tuples, sets, and dictionaries ───────────────────────────────────

def section_collections():
    print("\n--- Collections ---")
    # LIST - like ArrayList<Object>, mutable, ordered, mixed types allowed
    prompts = ["summarize", "translate", "classify"]
    prompts.append("extract")
    print(prompts)
    print(prompts[0], prompts[-1])      # negative indexing: -1 = last element
    print(prompts[1:3])                  # slicing: indices 1,2 (stop exclusive)

    # TUPLE - immutable list. Like a 'final' array or lightweight value object
    point = (10, 20)
    x, y = point                         # destructuring/unpacking
    print(f"x={x}, y={y}")

    # SET - like HashSet, no duplicates, no guaranteed order
    tags = {"llm", "agent", "llm", "rag"}
    print(tags)                          # duplicate 'llm' silently dropped

    # DICT - like HashMap<K,V>, preserves insertion order since Python 3.7
    model_config = {"model": "gpt-4", "temperature": 0.7, "max_tokens": 500}
    print(model_config["model"])
    model_config["top_p"] = 0.9
    print(model_config)


# ── Loops and conditionals ──────────────────────────────────────────────────

def section_loops():
    print("\n--- Loops & Conditionals ---")
    temperature = 0.7
    if temperature > 1.0:
        print("too random")
    elif temperature < 0.2:
        print("too deterministic")
    else:
        print("reasonable range")

    prompts = ["summarize", "translate", "classify"]
    for p in prompts:
        print(f"running: {p}")

    for i, p in enumerate(prompts):      # need index + value -> enumerate()
        print(f"{i}: {p}")

    for i in range(3):                   # classic counting loop
        print(f"iteration {i}")

    count = 0
    while count < 3:
        count += 1                       # no ++ operator in Python
    print(f"final count: {count}")


# ── Functions and return values ─────────────────────────────────────────────

def greet(name):
    return f"Hello, {name}!"


def call_model(prompt, model="gpt-4", temperature=0.7):
    return f"Calling {model} with prompt={prompt!r} at temp={temperature}"


def min_max(numbers):
    return min(numbers), max(numbers)    # multiple return values via tuple


def log_event(event_name, *args, **kwargs):
    print(f"EVENT: {event_name}, args={args}, kwargs={kwargs}")


def section_functions():
    print("\n--- Functions ---")
    print(greet("Future"))

    print(call_model("summarize this"))                          # uses defaults
    print(call_model("summarize this", temperature=0.2))          # keyword arg
    print(call_model("summarize this", model="claude-sonnet"))    # override one default

    low, high = min_max([4, 1, 9, 2])
    print(f"low={low}, high={high}")

    log_event("prompt_sent", "gpt-4", user="future", tokens=120)


# ── Scope, imports, and modules ─────────────────────────────────────────────

counter = 0  # module-level "global" variable


def increment():
    global counter            # needed to MODIFY a module-level variable
    counter += 1


def outer():
    x = 10

    def inner():
        nonlocal x             # without this, inner() makes a NEW local x
        x += 5

    inner()
    return x


def section_scope():
    print("\n--- Scope & Imports ---")
    print(prompt_utils.DEFAULT_MODEL)
    print(prompt_utils.word_count("this is a test prompt"))
    print(truncate("one two three four five", max_words=3))

    print(outer())  # 15

    increment()
    increment()
    print(counter)  # 2

    # Python is function-scoped, NOT block-scoped like Java.
    # if/for/while do NOT create a new scope:
    if True:
        leaked = 100
    print(leaked)  # works fine outside the if-block

    for i in range(3):
        last_value = i
    print(f"loop variable survives: {last_value}")  # i is still 2 here


if __name__ == "__main__":
    section_variables()
    section_collections()
    section_loops()
    section_functions()
    section_scope()
