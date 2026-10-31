"""Composer input and room joining callbacks for After Hours Chat."""

from __future__ import annotations

from typing import Any

import gradio as gr

from backend.chat_service import add_join_event, add_text_message
from backend.timezone_service import get_timezone
from backend.user_service import register_user, validate_username
from frontend.chat_ui import render_alert, render_chat


def join_room(
    name: str | None, selection: str | None
) -> tuple[str, str, str, dict[str, Any], bool]:
    """Callback when clicking JOIN ROOM.

    Validates alias, adds join event if new, disables join button,
    and enables joined state.
    """
    cleaned_name = validate_username(name)
    zone = get_timezone(selection)

    if not cleaned_name:
        return (
            render_chat(zone),
            render_alert(zone),
            "Enter a display name to join.",
            gr.update(interactive=True),
            False,
        )

    is_new = register_user(cleaned_name)
    if is_new:
        add_join_event(cleaned_name)

    return (
        render_chat(zone),
        render_alert(zone),
        f"Welcome to After Hours, {cleaned_name}!",
        gr.update(interactive=False),
        True,
    )


def send_message(
    name: str | None, text: str | None, joined: bool, selection: str | None
) -> tuple[str, str, str]:
    """Callback when clicking SEND or pressing Enter in message textarea.

    Appends message, clears textarea, and returns updated chat feed.
    """
    zone = get_timezone(selection)
    cleaned_name = validate_username(name)
    cleaned_text = (text or "").strip()

    if not joined:
        return render_chat(zone), cleaned_text, "Join the room before sending."

    if not cleaned_text:
        return render_chat(zone), "", ""

    add_text_message(cleaned_name, cleaned_text)
    return render_chat(zone), "", ""
