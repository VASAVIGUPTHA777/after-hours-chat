"""Three-dot menu and chat transcript download callbacks for After Hours Chat."""

from __future__ import annotations

from typing import Any

import gradio as gr

from backend.chat_service import get_messages_snapshot
from backend.download_service import create_transcript_file
from backend.timezone_service import get_timezone


def toggle_three_dot_menu(is_open: bool) -> tuple[dict[str, Any], bool]:
    """Toggle visibility of the header three-dot options menu."""
    new_state = not is_open
    return gr.update(visible=new_state), new_state


def open_download_panel() -> tuple[
    dict[str, Any], bool, dict[str, Any], dict[str, Any]
]:
    """Open the download section and close the three-dot popup menu."""
    return (
        gr.update(visible=False),
        False,
        gr.update(visible=True),
        gr.update(value=None, visible=False),
    )


def download_chat(selection: str | None) -> dict[str, Any]:
    """Generate and return transcript file for client download."""
    zone = get_timezone(selection)
    snapshot = get_messages_snapshot()

    if not snapshot:
        raise gr.Error("There are no messages to download yet.")

    file_path = create_transcript_file(snapshot, zone)
    return gr.update(value=file_path, visible=True)
