"""Chat rendering and feed refresh UI functions for After Hours Chat."""

from __future__ import annotations

from html import escape

from backend.chat_service import get_latest_join_event, get_messages_snapshot
from backend.media_service import media_url
from backend.timezone_service import format_time, get_timezone
from config.settings import DEFAULT_TIMEZONE


def render_chat(zone: str = DEFAULT_TIMEZONE) -> str:
    """Render the chat feed HTML with all join events, messages, and attachments."""
    snapshot = get_messages_snapshot()

    if not snapshot:
        return """
        <div class="empty-chat">
            <div class="empty-icon">🍿</div>
            <div class="empty-title">Welcome to After Hours</div>
            <div class="empty-subtitle">
                Your late-night conversations start here.
            </div>
        </div>
        """

    output = ['<div class="chat-feed">']

    for msg in snapshot:
        name = escape(msg.get("name", "User"))
        timestamp = escape(format_time(msg["time"], zone))
        kind = msg["kind"]

        if kind == "join":
            output.append(
                '<div class="join-event">'
                f'<b>{name}</b> joined After Hours'
                f'<span class="event-time">{timestamp}</span>'
                '</div>'
            )
            continue

        output.append('<div class="chat-message">')
        output.append(
            '<div class="message-heading">'
            f'<span class="sender">{name}</span>'
            f'<span class="timestamp">{timestamp}</span>'
            '</div>'
        )

        if kind == "message":
            text = escape(msg.get("text", "")).replace("\n", "<br>")
            output.append(f'<div class="message-bubble">{text}</div>')

        elif kind == "image":
            url = escape(media_url(msg["path"]), quote=True)
            filename = escape(msg["filename"])

            output.append(
                '<div class="media-card">'
                f'<a href="{url}" target="_blank" rel="noopener noreferrer">'
                f'<img class="chat-image" src="{url}" alt="{filename}" loading="lazy">'
                '</a>'
                f'<div class="media-caption">{filename}</div>'
                '</div>'
            )

        elif kind == "pdf":
            url = escape(media_url(msg["path"]), quote=True)
            filename = escape(msg["filename"])
            size_kb = msg.get("size", 0) / 1024

            output.append(
                '<div class="media-card pdf-card">'
                '<div class="pdf-icon">PDF</div>'
                '<div class="pdf-details">'
                f'<div class="pdf-name">{filename}</div>'
                f'<div class="pdf-meta">{size_kb:.1f} KB</div>'
                '</div>'
                f'<a class="pdf-download" href="{url}" download="{filename}">Download</a>'
                '</div>'
            )

        output.append('</div>')

    output.append('</div>')
    return "".join(output)


def render_alert(zone: str = DEFAULT_TIMEZONE) -> str:
    """Render the room header alert markdown showing latest join event."""
    latest = get_latest_join_event()
    if latest:
        name = escape(latest["name"])
        return f"**{name} joined the chat** · {format_time(latest['time'], zone)}"

    return "🍿 Your room is ready."


def refresh_chat(selection: str | None) -> tuple[str, str]:
    """Callback triggered every 2 seconds to refresh feed and room alert."""
    zone = get_timezone(selection)
    return render_chat(zone), render_alert(zone)
