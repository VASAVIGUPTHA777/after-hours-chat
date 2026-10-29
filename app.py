"""After Hours — Netflix-themed / late-night group chat application.

Main application entry point. Assembles the modular Gradio UI and launches
the server with queueing, public URL sharing, and local media path permissions.
"""

from __future__ import annotations

import os

from config import settings
from frontend.layout import build_app


def main() -> None:
    """Initialize and launch the After Hours chat application."""
    print(f"Starting {settings.APP_TITLE}...")
    print(f"Media storage path: {settings.MEDIA_DIR}")

    app = build_app()

    # Determine share setting: allow environment variable override or default
    share_env = os.environ.get("AFTER_HOURS_SHARE")
    share = (
        share_env.lower() in ("true", "1", "yes")
        if share_env is not None
        else settings.DEFAULT_SHARE
    )

    port = int(
        os.environ.get("PORT", os.environ.get("GRADIO_SERVER_PORT", settings.DEFAULT_SERVER_PORT))
    )

    print(f"Launching Gradio server on port {port} (share={share})...")
    app.queue().launch(
        share=share,
        debug=settings.DEFAULT_DEBUG,
        server_port=port,
        allowed_paths=[settings.MEDIA_DIR],
    )


if __name__ == "__main__":
    main()
