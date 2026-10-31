"""In-memory thread-safe chat message service for After Hours Chat.

Stores chat messages, join events, and media records with synchronization
via threading.Lock for safe multi-session access.
"""

from __future__ import annotations

import threading
from typing import Any

from backend.timezone_service import now_utc

# In-memory shared message store
_messages: list[dict[str, Any]] = []
_room_lock = threading.Lock()


def add_join_event(name: str) -> dict[str, Any]:
    """Record a user join event in the chat history."""
    msg = {
        "kind": "join",
        "name": name,
        "time": now_utc(),
    }
    with _room_lock:
        _messages.append(msg)
    return msg


def add_text_message(name: str, text: str) -> dict[str, Any]:
    """Record a user text message in the chat history."""
    msg = {
        "kind": "message",
        "name": name,
        "text": text,
        "time": now_utc(),
    }
    with _room_lock:
        _messages.append(msg)
    return msg


def add_media_message(
    name: str, kind: str, filename: str, path: str, size: int
) -> dict[str, Any]:
    """Record a shared image or PDF document message in the chat history."""
    msg = {
        "kind": kind,
        "name": name,
        "filename": filename,
        "path": path,
        "size": size,
        "time": now_utc(),
    }
    with _room_lock:
        _messages.append(msg)
    return msg


def get_messages_snapshot() -> list[dict[str, Any]]:
    """Return a thread-safe shallow copy of all messages."""
    with _room_lock:
        return list(_messages)


def get_latest_join_event() -> dict[str, Any] | None:
    """Return the most recent user join event, if any."""
    with _room_lock:
        return next(
            (m for m in reversed(_messages) if m.get("kind") == "join"),
            None,
        )


def message_count() -> int:
    """Return total number of messages in the store."""
    with _room_lock:
        return len(_messages)


def clear_messages() -> None:
    """Empty the message store (primarily used for test isolation)."""
    with _room_lock:
        _messages.clear()
