"""
Module 3: Error Handling & Debugging
Run with: python3 module_3_error_handling.py

Standalone file - no companion modules required.
"""

import logging


# ── Exceptions and try/except ───────────────────────────────────────────────

def section_try_except():
    print("\n--- Exceptions & try/except ---")

    # try/except, not try/catch - same idea, different keyword
    def call_model(prompt):
        if not prompt:
            raise ValueError("prompt cannot be empty")  # 'raise', not 'throw'
        return f"response to: {prompt}"

    try:
        call_model("")
    except ValueError as e:  # 'as e' binds the exception, like Java's 'catch (Exception e)'
        print(f"Caught: {e}")

    # multiple except blocks - like multiple catch blocks, most specific first
    def parse_token_count(value):
        return int(value)

    for test_value in ["100", "abc", None]:
        try:
            count = parse_token_count(test_value)
            print(f"parsed: {count}")
        except ValueError:
            print(f"{test_value!r} is not a valid number")
        except TypeError:
            print(f"{test_value!r} is the wrong type entirely")

    # catching multiple exception types in ONE except - no Java equivalent this concise
    try:
        int("abc")
    except (ValueError, TypeError) as e:
        print(f"one of two possible errors: {type(e).__name__}")

    # else and finally - else runs ONLY if no exception was raised, finally ALWAYS runs
    def risky_call(should_fail):
        try:
            if should_fail:
                raise RuntimeError("API call failed")
            return "success"
        except RuntimeError as e:
            print(f"handled: {e}")
            return None
        else:
            print("no exception happened - else block runs")
        finally:
            print("finally always runs - cleanup goes here")  # like Java's finally

    print(risky_call(should_fail=False))
    print("---")
    print(risky_call(should_fail=True))


# ── Custom exceptions ────────────────────────────────────────────────────────

class PromptOpsError(Exception):
    """Base exception for all PromptOps-specific errors."""
    pass


class InvalidPromptError(PromptOpsError):
    """Raised when a prompt template is malformed."""

    def __init__(self, prompt_name, reason):
        self.prompt_name = prompt_name
        self.reason = reason
        super().__init__(f"Invalid prompt {prompt_name!r}: {reason}")  # builds the message string


class ModelCallError(PromptOpsError):
    """Raised when the underlying model API call fails."""

    def __init__(self, model, status_code):
        self.model = model
        self.status_code = status_code
        super().__init__(f"Model {model!r} call failed with status {status_code}")


def render_prompt(name, template, **kwargs):
    try:
        return template.format(**kwargs)
    except KeyError as e:
        # wrapping a low-level error into a domain-specific one - very common pattern
        raise InvalidPromptError(name, f"missing variable {e}") from e  # 'from e' preserves the cause


def section_custom_exceptions():
    print("\n--- Custom Exceptions ---")

    try:
        render_prompt("summarizer", "Summarize: {text}")  # 'text' kwarg missing on purpose
    except InvalidPromptError as e:
        print(f"Caught domain error: {e}")
        print(f"  prompt_name={e.prompt_name}, reason={e.reason}")

    # catching the BASE class catches all subclasses too - same as Java exception hierarchies
    def simulate_call(error_type):
        if error_type == "invalid":
            raise InvalidPromptError("test", "bad template")
        elif error_type == "model":
            raise ModelCallError("gpt-4", 503)

    for err in ["invalid", "model"]:
        try:
            simulate_call(err)
        except PromptOpsError as e:  # catches BOTH InvalidPromptError and ModelCallError
            print(f"{type(e).__name__}: {e}")


# ── Logging basics ───────────────────────────────────────────────────────────

def section_logging():
    print("\n--- Logging ---")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )
    logger = logging.getLogger("promptops")  # getLogger(__name__) is the standard real-world pattern

    logger.debug("this is debug detail - hidden by default since level=INFO")
    logger.info("prompt rendered successfully")
    logger.warning("prompt template is using a deprecated variable name")
    logger.error("model API call failed")
    logger.critical("unable to load any prompt templates - shutting down")

    def call_model():
        raise ConnectionError("could not reach API endpoint")

    try:
        call_model()
    except ConnectionError:
        logger.error("model call failed", exc_info=True)  # includes full traceback in the log output


# ── Debugging common Python issues ──────────────────────────────────────────

def section_common_errors():
    print("\n--- Common Error Types ---")

    # NameError - using a variable before it's defined, or a typo in the name
    try:
        print(undefined_variable)  # noqa: F821 (intentional for the demo)
    except NameError as e:
        print(f"NameError: {e}")

    # AttributeError - calling a method/attribute that doesn't exist on this object
    try:
        x = 5
        x.append(10)  # int has no .append - that's a list method
    except AttributeError as e:
        print(f"AttributeError: {e}")

    # TypeError - wrong type passed, or mixing incompatible types in an operation
    try:
        "5" + 5  # cannot concatenate str and int directly - need str(5) or int('5')
    except TypeError as e:
        print(f"TypeError: {e}")

    # IndexError - list index out of range (Python's ArrayIndexOutOfBoundsException)
    try:
        items = [1, 2, 3]
        print(items[10])
    except IndexError as e:
        print(f"IndexError: {e}")

    # The 'mutable default argument' bug - one of THE most common real Python bugs
    def add_tag(tag, tags=[]):  # BUG: shared across every call without an explicit tags=
        tags.append(tag)
        return tags

    print(add_tag("a"))  # ['a']
    print(add_tag("b"))  # ['a', 'b']  <- surprising! Expected ['b'], got accumulated state


# ── Writing clean error messages ────────────────────────────────────────────

def call_model_good(prompt, model, max_tokens):
    if not prompt:
        raise ValueError(f"prompt must be a non-empty string, got: {prompt!r}")
    if max_tokens <= 0:
        raise ValueError(f"max_tokens must be positive, got: {max_tokens}")
    if model not in ("gpt-4", "claude-sonnet", "gemini-pro"):
        raise ValueError(f"unsupported model {model!r}, expected one of: gpt-4, claude-sonnet, gemini-pro")
    return f"calling {model} with {max_tokens} max tokens"


def section_clean_errors():
    print("\n--- Clean Error Messages ---")

    try:
        call_model_good("summarize this", "unknown-model", 100)
    except ValueError as e:
        print(f"Clear error: {e}")

    # fail fast with assertions for things that should NEVER happen (programmer errors, not user errors)
    # assert is stripped out when Python runs with -O (optimized mode) - don't use it for real
    # validation, only for internal invariants/sanity checks during development
    def render(template, variables):
        assert isinstance(variables, dict), "variables must always be a dict by this point in the pipeline"
        return template.format(**variables)

    print(render("Hello {name}", {"name": "Future"}))


if __name__ == "__main__":
    section_try_except()
    section_custom_exceptions()
    section_logging()
    section_common_errors()
    section_clean_errors()
