"""
PromptOps CLI — Module 2 contribution, extended in Module 3 with error handling + logging

Introduces the OOP backbone of the project:
- PromptConfig: a dataclass holding model/temperature/etc settings
- PromptTemplate: base class for a renderable prompt
- SummarizePrompt / TranslatePrompt: concrete subclasses
- PromptRunner: composition example - HAS a logger, doesn't extend one
  (Module 3 update: now uses the logging module + raises InvalidPromptError on failure)
"""

import logging
from dataclasses import dataclass, field

from exceptions import InvalidPromptError

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("promptops.prompt_template")


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


class PromptRunner:
    """
    Composition example: PromptRunner HAS a logger, it does not extend one.
    Runs any PromptTemplate (or subclass) polymorphically via .render().

    Module 3 update: failures during render() are caught, logged with full
    traceback (exc_info=True), and re-raised as a domain-specific
    InvalidPromptError using 'raise ... from e' to preserve the original cause.
    """

    def __init__(self):
        self.logger = logger
        self.history = []

    def run(self, prompt: PromptTemplate):
        self.logger.info(f"Running prompt: {prompt.name}")
        try:
            rendered = prompt.render()
        except Exception as e:
            self.logger.error(f"Prompt {prompt.name!r} failed to render", exc_info=True)
            raise InvalidPromptError(prompt.name, str(e)) from e

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

    # --- Module 3 addition: demonstrate the error-handling path ---
    class BrokenPrompt(PromptTemplate):
        def render(self):
            raise KeyError("missing_variable")  # simulate a low-level failure during render

    broken = BrokenPrompt(name="broken-prompt")
    try:
        runner.run(broken)
    except InvalidPromptError as e:
        print(f"\nCaught domain error as expected: {e}")
        print(f"  prompt_name={e.prompt_name}")
        print(f"  reason={e.reason}")
