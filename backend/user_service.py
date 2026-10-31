"""User alias validation and session tracking service for After Hours Chat.

Maintains registered user aliases in a case-insensitive set.
"""

from __future__ import annotations

import threading

_joined_users: set[str] = set()
_user_lock = threading.Lock()


def validate_username(name: str | None) -> str:
    """Strip whitespace from a display name and return cleaned string."""
    return (name or "").strip()


def is_user_registered(name: str) -> bool:
    """Check if a case-insensitive user alias has already joined."""
    cleaned = validate_username(name).casefold()
    if not cleaned:
        return False
    with _user_lock:
        return cleaned in _joined_users


def register_user(name: str) -> bool:
    """Register a new user alias.

    Returns True if user was newly registered, False if already present
    or name is empty.
    """
    cleaned = validate_username(name).casefold()
    if not cleaned:
        return False
    with _user_lock:
        if cleaned not in _joined_users:
            _joined_users.add(cleaned)
            return True
        return False


def get_registered_users() -> set[str]:
    """Return a copy of all registered usernames."""
    with _user_lock:
        return set(_joined_users)


def reset_users() -> None:
    """Reset registered users (primarily used for test isolation)."""
    with _user_lock:
        _joined_users.clear()
