
"""
Media handling, validation, storage, and URL generation for After Hours Chat.

Handles image previews and PDF document attachments with magic byte header
verification, size limits, and Gradio file serving URLs.
"""

from __future__ import annotations

import os
import shutil
import uuid
from typing import Any
from urllib.parse import quote

from config.settings import (
    ALLOWED_IMAGE_EXTENSIONS,
    MAX_FILE_SIZE,
    MAX_FILES,
    MEDIA_DIR,
)


def media_url(path: str) -> str:
    """Generate Gradio internal file serving URL for local media."""
    return "/gradio_api/file=" + quote(os.path.abspath(path), safe="/")


def validate_image_header(header: bytes, ext: str) -> bool:
    """Validate that image magic bytes match the supplied file extension."""

    extension_signatures = {
        ".png": b"\x89PNG\r\n\x1a\n",
        ".jpg": b"\xff\xd8\xff",
        ".jpeg": b"\xff\xd8\xff",
        ".gif": (b"GIF87a", b"GIF89a"),
        ".webp": b"WEBP",
    }

    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        return False

    if ext == ".webp":
        return (
            len(header) >= 12
            and header[:4] == b"RIFF"
            and header[8:12] == b"WEBP"
        )

    signature = extension_signatures.get(ext)

    if isinstance(signature, tuple):
        return header.startswith(signature)

    return signature is not None and header.startswith(signature)


def validate_pdf_header(header: bytes, ext: str) -> bool:
    """Validate binary magic bytes for PDF document attachments."""
    return ext == ".pdf" and header.startswith(b"%PDF-")


def process_media_item(
    source_path: str, expected_kind: str
) -> tuple[bool, str, dict[str, Any] | None]:
    """Validate and copy a single uploaded file to the media directory.

    Returns:
        (success: bool, error_or_success_message: str, file_info_dict or None)
    """
    source = str(source_path)

    if not os.path.isfile(source):
        return False, "A selected file could not be read.", None

    filename = os.path.basename(source)
    ext = os.path.splitext(filename)[1].lower()
    size = os.path.getsize(source)

    if size > MAX_FILE_SIZE:
        return False, f"{filename}: exceeds the 5 MB limit.", None

    try:
        with open(source, "rb") as file:
            header = file.read(16)
    except OSError:
        return False, f"{filename}: could not be read.", None

    if expected_kind == "pdf":
        if not validate_pdf_header(header, ext):
            return False, f"{filename}: select a valid PDF.", None
        kind = "pdf"
    else:
        if ext not in ALLOWED_IMAGE_EXTENSIONS:
            return False, f"{filename}: unsupported image format.", None
        if not validate_image_header(header, ext):
            return False, f"{filename}: invalid image file.", None
        kind = "image"

    destination = os.path.join(MEDIA_DIR, uuid.uuid4().hex + ext)

    try:
        shutil.copy2(source, destination)
    except OSError:
        return False, f"{filename}: could not save.", None

    file_info = {
        "kind": kind,
        "filename": filename,
        "path": destination,
        "size": size,
    }

    return True, "", file_info
