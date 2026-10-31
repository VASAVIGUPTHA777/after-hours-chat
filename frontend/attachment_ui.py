"""Attachment drawer and media upload callbacks for After Hours Chat."""

from __future__ import annotations

from typing import Any

import gradio as gr

from backend.chat_service import add_media_message
from backend.media_service import process_media_item
from backend.timezone_service import get_timezone
from backend.user_service import validate_username
from config.settings import MAX_FILES
from frontend.chat_ui import render_chat


def toggle_attachment(is_open: bool) -> tuple[dict[str, Any], bool]:
    """Toggle visibility of the attachment selection panel."""
    new_state = not is_open
    return gr.update(visible=new_state), new_state


def select_upload_type(kind: str) -> tuple[dict[str, Any], dict[str, Any]]:
    """Switch active upload box between image and document upload panels."""
    if kind == "image":
        return gr.update(visible=True), gr.update(visible=False)
    return gr.update(visible=False), gr.update(visible=True)


def share_media(
    name: str | None,
    files: Any,
    joined: bool,
    selection: str | None,
    expected_kind: str,
) -> tuple[str, list[Any], str]:
    """Validate and upload selected image or document files into chat."""
    zone = get_timezone(selection)
    cleaned_name = validate_username(name)

    if not joined:
        return render_chat(zone), [], "Join the room before sharing files."

    if not files:
        return render_chat(zone), [], "Choose a file first."

    file_list = files if isinstance(files, list) else [files]

    if len(file_list) > MAX_FILES:
        return render_chat(zone), file_list, "Select no more than 5 files."

    count = 0
    errors: list[str] = []

    for item in file_list:
        success, err_msg, file_info = process_media_item(item, expected_kind)
        if not success or not file_info:
            errors.append(err_msg)
            continue

        add_media_message(
            name=cleaned_name,
            kind=file_info["kind"],
            filename=file_info["filename"],
            path=file_info["path"],
            size=file_info["size"],
        )
        count += 1

    if errors:
        status = f"Shared {count} file(s). " + " ".join(errors)
    elif count:
        status = f"Successfully shared {count} file(s)."
    else:
        status = "No files were shared."

    return render_chat(zone), [], status
