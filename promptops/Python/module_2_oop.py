"""
Module 2: Object-Oriented Python
Run with: python3 module_2_oop.py

Standalone file - no companion modules required.
"""

from dataclasses import dataclass, field


# ── Classes and objects ──────────────────────────────────────────────────────

def section_classes_and_objects():
    print("\n--- Classes & Objects ---")

    # class keyword, no 'public class Foo { }' ceremony, no separate file required per class
    class PromptTemplateBasic:
        pass  # 'pass' = no-op, Python's equivalent of an empty {} block

    p = PromptTemplateBasic()
    print(p)                 # default repr - shows memory address, like Java's default toString()
    print(type(p))
    print(isinstance(p, PromptTemplateBasic))   # like Java's instanceof


# ── Constructors and instance methods ───────────────────────────────────────

class PromptTemplate:
    # __init__ is the constructor body - like Java's PromptTemplate(...) {...}
    # 'self' is EXPLICIT - it's like Java's implicit 'this', but Python never hides it.
    # self must be the first parameter of every instance method, always.
    def __init__(self, name, template, model="gpt-4"):
        self.name = name              # like 'this.name = name;' - no field declarations needed above
        self.template = template      # attributes are created simply by assigning to self.X
        self.model = model
        self.call_count = 0           # you can add fields the constructor never received as args

    # instance method - self gives access to the object's own state, same idea as Java's 'this'
    def render(self, **kwargs):
        self.call_count += 1
        return self.template.format(**kwargs)   # .format() fills in {placeholders}

    # __str__ is like overriding toString() in Java
    def __str__(self):
        return f"PromptTemplate(name={self.name!r}, model={self.model!r})"

    # __repr__ is the 'developer-facing' string - shown in REPL/debugger, vs __str__ for end users
    def __repr__(self):
        return f"PromptTemplate(name={self.name!r}, template={self.template!r}, model={self.model!r})"


def section_constructors_and_methods():
    print("\n--- Constructors & Instance Methods ---")

    t = PromptTemplate(name="summarizer", template="Summarize this in {n} words: {text}")
    print(t)                       # uses __str__
    print(repr(t))                 # uses __repr__

    rendered = t.render(n=20, text="a long article about Python")
    print(rendered)
    print(f"called {t.call_count} time(s)")

    # attributes are just public by convention - no private/public/protected keywords in Python
    print(t.model)
    t.model = "claude-sonnet"   # nothing stops external code from changing this directly
    print(t.model)


# ── Inheritance and composition ─────────────────────────────────────────────

class BasePrompt:
    def __init__(self, name, model="gpt-4"):
        self.name = name
        self.model = model

    def render(self):
        raise NotImplementedError("Subclasses must implement render()")  # like an abstract method

    def describe(self):
        return f"{self.name} using {self.model}"


class SummarizePrompt(BasePrompt):
    def __init__(self, name, text, model="gpt-4"):
        super().__init__(name, model)   # like Java's super(...) - calls parent constructor
        self.text = text

    def render(self):                   # overriding a method - same idea as Java @Override
        return f"Summarize: {self.text[:50]}..."


class TranslatePrompt(BasePrompt):
    def __init__(self, name, text, target_lang, model="gpt-4"):
        super().__init__(name, model)
        self.text = text
        self.target_lang = target_lang

    def render(self):
        return f"Translate to {self.target_lang}: {self.text}"


class Logger:
    def log(self, message):
        print(f"[LOG] {message}")


class Agent:
    """COMPOSITION example - 'has-a' instead of 'is-a'. Agent HAS a Logger, doesn't extend one."""

    def __init__(self, name):
        self.name = name
        self.logger = Logger()

    def run(self, task):
        self.logger.log(f"{self.name} running task: {task}")
        return f"done: {task}"


def section_inheritance_and_composition():
    print("\n--- Inheritance & Composition ---")

    prompts = [
        SummarizePrompt("summarizer", "a very long article about distributed systems..."),
        TranslatePrompt("translator", "hello world", target_lang="French"),
    ]

    # polymorphism - same call, different behavior, exactly like Java
    for p in prompts:
        print(p.describe())
        print(p.render())
        print()

    # isinstance() and issubclass() - like instanceof and checking class hierarchy
    print(isinstance(prompts[0], BasePrompt))      # True - SummarizePrompt IS a BasePrompt
    print(issubclass(SummarizePrompt, BasePrompt))  # True

    agent = Agent("research-agent")
    print(agent.run("summarize report"))


# ── Dataclasses ──────────────────────────────────────────────────────────────

@dataclass
class PromptConfig:
    name: str
    model: str = "gpt-4"           # default value, like a field initializer
    temperature: float = 0.7
    max_tokens: int = 512
    tags: list = field(default_factory=list)  # mutable defaults need default_factory, NEVER tags=[]


@dataclass(frozen=True)
class ImmutableConfig:
    name: str
    model: str


def section_dataclasses():
    print("\n--- Dataclasses ---")

    config1 = PromptConfig(name="summarizer")
    print(config1)              # auto-generated __repr__ - readable out of the box

    config2 = PromptConfig(name="summarizer")
    print(config1 == config2)   # auto-generated __eq__ - compares field values, not identity

    config3 = PromptConfig(
        name="translator", model="claude-sonnet", temperature=0.3, tags=["nlp", "translation"]
    )
    print(config3)

    # frozen=True makes instances immutable - like a Java record, or 'final' fields everywhere
    frozen = ImmutableConfig(name="x", model="gpt-4")
    try:
        frozen.model = "changed"
    except Exception as e:
        print(f"{type(e).__name__}: {e}")


if __name__ == "__main__":
    section_classes_and_objects()
    section_constructors_and_methods()
    section_inheritance_and_composition()
    section_dataclasses()
