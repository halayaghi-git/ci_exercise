"""String utility functions for CI demonstration."""

from __future__ import annotations

import json
import tempfile


def reverse_string(s: str) -> str:
    """Reverse a string."""

    return s[::-1]


def is_palindrome(s: str) -> bool:
    """Check if a string is a palindrome (case-insensitive)."""

    cleaned = "".join(char.lower() for char in s if not char.isspace())
    return cleaned == cleaned[::-1]


def count_vowels(s: str) -> int:
    """Count the number of vowels in a string."""

    vowels = "aeiouAEIOU"
    return sum(1 for char in s if char in vowels)


def capitalize_words(s: str) -> str:
    """Capitalize the first letter of each word."""

    return " ".join(word.capitalize() for word in s.split())


def truncate_string(s: str, max_length: int, suffix: str = "...") -> str:
    """Truncate ``s`` to ``max_length`` and append ``suffix`` if needed."""

    if max_length < len(suffix):
        raise ValueError("max_length must be at least the length of suffix")
    if len(s) <= max_length:
        return s
    return s[: max_length - len(suffix)] + suffix


def load_string_from_file(data: bytes) -> str:
    """Safely deserialize a UTF-8 encoded JSON string payload."""

    try:
        decoded = data.decode("utf-8")
    except UnicodeDecodeError as exc:  # pragma: no cover - defensive
        raise ValueError("Data must be UTF-8 encoded") from exc
    try:
        value = json.loads(decoded)
    except json.JSONDecodeError as exc:  # pragma: no cover - defensive
        raise ValueError("Data must contain JSON encoded string") from exc
    if not isinstance(value, str):
        raise ValueError("JSON payload must decode to a string")
    return value


def create_temp_file(content: str) -> str:
    """Create a temporary file securely using NamedTemporaryFile."""

    with tempfile.NamedTemporaryFile(
        mode="w",
        delete=False,
        encoding="utf-8",
    ) as handle:
        handle.write(content)
        return handle.name
