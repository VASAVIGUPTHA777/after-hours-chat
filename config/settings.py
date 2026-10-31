"""Application configuration and constants for After Hours Chat.

All constants, paths, supported timezones, emoji palette, and limits
are centralized here.
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import Final

# ---------------------------------------------------------------------------
# Project Paths
# ---------------------------------------------------------------------------
BASE_DIR: Final[Path] = Path(__file__).resolve().parent.parent
STATIC_DIR: Final[Path] = BASE_DIR / "static"
CSS_DIR: Final[Path] = STATIC_DIR / "css"
JS_DIR: Final[Path] = STATIC_DIR / "js"
DOCS_DIR: Final[Path] = BASE_DIR / "docs"

# ---------------------------------------------------------------------------
# Media Storage and File Limits
# ---------------------------------------------------------------------------
# Temporary directory used for storing uploaded chat images and PDFs.
MEDIA_DIR: Final[str] = os.path.join(tempfile.gettempdir(), "after_hours_media")
os.makedirs(MEDIA_DIR, exist_ok=True)

# Maximum file size per upload: 5 MB (in bytes)
MAX_FILE_SIZE: Final[int] = 5 * 1024 * 1024

# Maximum number of files allowed per upload action
MAX_FILES: Final[int] = 5

# Supported file extensions and magic byte headers
ALLOWED_IMAGE_EXTENSIONS: Final[tuple[str, ...]] = (
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
)

# ---------------------------------------------------------------------------
# Timezones
# ---------------------------------------------------------------------------
# Timezone selection choices matching the original Colab application:
# Tuple of (Display Label, IANA Timezone Identifier)
TIMEZONES: Final[list[tuple[str, str]]] = [
    ("India (IST)", "Asia/Kolkata"),
    ("United Kingdom", "Europe/London"),
    ("New York", "America/New_York"),
    ("Los Angeles", "America/Los_Angeles"),
    ("Singapore", "Asia/Singapore"),
    ("Tokyo", "Asia/Tokyo"),
    ("Sydney", "Australia/Sydney"),
    ("Berlin", "Europe/Berlin"),
    ("UTC", "UTC"),
]

DEFAULT_TIMEZONE: Final[str] = "Asia/Kolkata"

# ---------------------------------------------------------------------------
# Emoji Palette
# ---------------------------------------------------------------------------
# The exact 36 emojis supported by the After Hours emoji picker
EMOJIS: Final[list[str]] = [
    "😀", "😂", "🥹", "😍", "🥰", "😎",
    "😭", "🤔", "😴", "🙄", "😏", "🤭",
    "🤗", "😈", "❤️", "🖤", "💀", "✨",
    "🔥", "🎬", "🍿", "🌙", "⭐", "💌",
    "💔", "🫶", "👏", "👍", "👀", "🥳",
    "🤍", "☕", "💯", "🎉", "🙏", "😊",
]

# ---------------------------------------------------------------------------
# Server and UI Settings
# ---------------------------------------------------------------------------
APP_TITLE: Final[str] = "AFTER HOURS"
SUBTITLE: Final[str] = "Your late-night corner of the internet"
ROOM_NAME: Final[str] = "After Hours"
ROOM_DESCRIPTION: Final[str] = "Group chat"
ROOM_AVATAR: Final[str] = "AH"

# Chat polling interval in seconds
REFRESH_INTERVAL: Final[float] = 2.0

# Server launch defaults
DEFAULT_SERVER_PORT: Final[int] = 7860
DEFAULT_SHARE: Final[bool] = True
DEFAULT_DEBUG: Final[bool] = True
