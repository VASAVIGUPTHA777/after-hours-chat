"""Emoji picker UI generator and client-side script loader for After Hours Chat."""

from __future__ import annotations

from html import escape

from config.settings import EMOJIS, JS_DIR


def get_emoji_buttons_html() -> str:
    """Generate HTML buttons for each emoji in the palette."""
    return "".join(
        f'<button type="button" class="emoji-choice" '
        f'data-emoji="{escape(e, quote=True)}">{e}</button>'
        for e in EMOJIS
    )


def get_emoji_widget_html() -> str:
    """Generate complete HTML snippet for the emoji trigger and popup."""
    buttons = get_emoji_buttons_html()
    return f"""
<div id="emoji-widget">
    <button type="button" id="emoji-toggle" aria-label="Choose emoji">
        <svg viewBox="0 0 24 24" aria-hidden="true">
            <circle cx="12" cy="12" r="9"></circle>
            <circle cx="9" cy="10" r="0.8" class="eye"></circle>
            <circle cx="15" cy="10" r="0.8" class="eye"></circle>
            <path d="M8 14c1 2 2.3 3 4 3s3-1 4-3"></path>
        </svg>
    </button>
    <div id="emoji-popup">
        <div class="popup-title">Choose an emoji</div>
        <div class="emoji-grid">{buttons}</div>
    </div>
</div>
"""


def load_emoji_picker_js() -> str:
    """Load the client-side JavaScript for emoji selection."""
    js_file = JS_DIR / "emoji_picker.js"
    if js_file.exists():
        return js_file.read_text(encoding="utf-8")
    return ""
