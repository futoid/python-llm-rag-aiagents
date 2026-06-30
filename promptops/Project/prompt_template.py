"""
PromptOps CLI — Module 2 contribution

Introduces the OOP backbone of the project:
- PromptConfig: a dataclass holding model/temperature/etc settings
- PromptTemplate: base class for a renderable prompt
- SummarizePrompt / TranslatePrompt: concrete subclasses
- PromptRunner: composition example - HAS a logger, doesn't extend one
"""

from dataclasses import dataclass, field


@dataclass
class PromptConfig:
    """Plain data holder for model settings. Auto-generates __init__, __repr__, __eq__."""
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 512
    tags: list = field(default_factory=list)  # mutable default - MUST use default_factory


class PromptTemplate:
    """Base class for any renderable prompt. Subclasses must implement render()."""

    def __init__(self, name, config: PromptConfig = None):
        self.name = name
        self.config = config or PromptConfig()
        self.call_count = 0

    def render(self):
        raise NotImplementedError("Subclasses must implement render()")

    def describe(self):
        return f"{self.name} (model={self.config.model}, temp={self.config.temperature})"

    def __str__(self):
        return f"PromptTemplate(name={self.name!r})"

    def __repr__(self):
        return f"PromptTemplate(name={self.name!r}, config={self.config!r})"


class SummarizePrompt(PromptTemplate):
    def __init__(self, name, text, config: PromptConfig = None):
        super().__init__(name, config)
        self.text = text

    def render(self):
        self.call_count += 1
        preview = self.text[:50] + ("..." if len(self.text) > 50 else "")
        return f"Summarize the following text:\n{preview}"


class TranslatePrompt(PromptTemplate):
    def __init__(self, name, text, target_lang, config: PromptConfig = None):
        super().__init__(name, config)
        self.text = text
        self.target_lang = target_lang

    def render(self):
        self.call_count += 1
        return f"Translate the following text to {self.target_lang}:\n{self.text}"


class Logger:
    """Tiny logger used via composition by PromptRunner, not inheritance."""

    def log(self, message):
        print(f"[LOG] {message}")


class PromptRunner:
    """
    Composition example: PromptRunner HAS a Logger, it does not extend one.
    Runs any PromptTemplate (or subclass) polymorphically via .render().
    """

    def __init__(self):
        self.logger = Logger()
        self.history = []

    def run(self, prompt: PromptTemplate):
        self.logger.log(f"Running prompt: {prompt.name}")
        rendered = prompt.render()
        self.history.append({"name": prompt.name, "rendered": rendered})
        return rendered


if __name__ == "__main__":
    config = PromptConfig(model="claude-sonnet", temperature=0.3, tags=["nlp"])

    summarizer = SummarizePrompt(
        name="summarizer",
        text="Distributed systems are notoriously difficult to test because of partial failures.",
        config=config,
    )
    translator = TranslatePrompt(
        name="translator",
        text="hello world",
        target_lang="French",
    )

    runner = PromptRunner()

    for prompt in [summarizer, translator]:
        print(prompt.describe())
        output = runner.run(prompt)
        print(output)
        print()

    print(f"Total prompts run: {len(runner.history)}")
    print(f"Summarizer call count: {summarizer.call_count}")

    print(isinstance(summarizer, PromptTemplate))    # True - polymorphism check
    print(issubclass(TranslatePrompt, PromptTemplate))  # True
