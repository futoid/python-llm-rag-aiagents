"""
A Python file is automatically a 'module'. No package declaration needed like Java's
`package com.future.promptops;` - the file path + folder structure IS the module path.
"""

DEFAULT_MODEL = "gpt-4"  # module-level "global" variable


def word_count(text):
    return len(text.split())


def truncate(text, max_words=50):
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words]) + "..."
