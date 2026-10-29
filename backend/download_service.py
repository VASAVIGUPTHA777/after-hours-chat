"""Chat transcript export service for After Hours Chat.

Generates a formatted text file transcript of the chat history adjusted
to the user's selected timezone.
"""

from __future__ import annotations

import tempfile
from typing import Any

from backend.timezone_service import format_time, get_timezone, now_utc


def generate_transcript_lines(
    snapshot: list[dict[str, Any]], zone: str | None = None
) -> list[str]:
    """Generate human-readable transcript lines from message records."""
    tz = get_timezone(zone)
    lines: list[str] = [
        "AFTER HOURS — CHAT HISTORY",
        "=" * 40,
        f"Exported: {format_time(now_utc(), tz)}",
        f"Time zone: {tz}",
        "",
    ]

    for msg in snapshot:
        timestamp = format_time(msg.get("time", ""), tz)
        name = msg.get("name", "User")
        kind = msg.get("kind", "message")

        if kind == "join":
            line = f"[{timestamp}] {name} joined the chat"
        elif kind in ("image", "pdf"):
            filename = msg.get("filename", "file")
            line = f"[{timestamp}] {name} shared {kind}: {filename}"
        else:
            text = msg.get("text", "")
            line = f"[{timestamp}] {name}: {text}"

        lines.extend([line, ""])

    return lines


def create_transcript_file(
    snapshot: list[dict[str, Any]], zone: str | None = None
) -> str:
    """Write the transcript to a temporary text file and return its file path.

    Raises ValueError if snapshot is empty.
    """
    if not snapshot:
        raise ValueError("There are no messages to download yet.")

    lines = generate_transcript_lines(snapshot, zone)

    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        suffix=".txt",
        prefix="after_hours_",
        delete=False,
    ) as file:
        file.write("\n".join(lines))
        return file.name
