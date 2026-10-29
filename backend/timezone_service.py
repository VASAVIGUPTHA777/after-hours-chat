"""Timezone and timestamp formatting services for After Hours Chat.

Utilizes standard library zoneinfo.ZoneInfo for accurate, lightweight
UTC to local timezone conversions across the 9 supported regions.
"""

from __future__ import annotations

from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from config.settings import DEFAULT_TIMEZONE


def get_timezone(selection: str | None) -> str:
    """Validate and return a valid IANA timezone string.

    Falls back to DEFAULT_TIMEZONE ("Asia/Kolkata") if invalid or missing.
    """
    if not selection:
        return DEFAULT_TIMEZONE
    try:
        ZoneInfo(selection)
        return selection
    except Exception:
        return DEFAULT_TIMEZONE


def now_utc() -> str:
    """Return the current UTC timestamp formatted as ISO 8601 string."""
    return datetime.now(timezone.utc).isoformat()


def format_time(timestamp: str, zone: str | None = None) -> str:
    """Convert an ISO UTC timestamp into a human-readable local time string.

    Format: DD Mon YYYY, hh:mm AM/PM (e.g. '24 Oct 2026, 07:35 PM').
    Returns '--:--' on parse errors or invalid timestamps.
    """
    try:
        tz = ZoneInfo(get_timezone(zone))
        return (
            datetime.fromisoformat(timestamp)
            .astimezone(tz)
            .strftime("%d %b %Y, %I:%M %p")
        )
    except Exception:
        return "--:--"
