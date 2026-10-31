"""Full UI assembly and event routing for After Hours Chat."""

from __future__ import annotations

import gradio as gr

from config.settings import (
    APP_TITLE,
    CSS_DIR,
    DEFAULT_TIMEZONE,
    REFRESH_INTERVAL,
    ROOM_AVATAR,
    ROOM_DESCRIPTION,
    ROOM_NAME,
    SUBTITLE,
    TIMEZONES,
)
from frontend.attachment_ui import (
    select_upload_type,
    share_media,
    toggle_attachment,
)
from frontend.chat_ui import refresh_chat, render_chat
from frontend.composer import join_room, send_message
from frontend.download_menu import (
    download_chat,
    open_download_panel,
    toggle_three_dot_menu,
)
from frontend.emoji_picker import get_emoji_widget_html, load_emoji_picker_js


def get_combined_css() -> str:
    """Concatenate modular CSS files in cascade order."""
    css_files = ["main.css", "chat.css", "composer.css", "responsive.css"]
    parts: list[str] = []
    for fname in css_files:
        fpath = CSS_DIR / fname
        if fpath.exists():
            parts.append(fpath.read_text(encoding="utf-8"))
    return "\n\n".join(parts)


def build_app() -> gr.Blocks:
    """Build and return the complete After Hours Gradio Blocks application."""
    css = get_combined_css()
    theme = gr.themes.Base(primary_hue="teal", neutral_hue="slate")

    with gr.Blocks(theme=theme, css=css) as app:
        gr.Markdown(f"# {APP_TITLE}", elem_id="main-title")
        gr.HTML(f'<div id="subtitle">{SUBTITLE}</div>')

        # Join row
        with gr.Row(elem_id="join-row"):
            name_input = gr.Textbox(
                label="YOUR ALIAS",
                placeholder="Enter your name",
                scale=3,
            )
            timezone_input = gr.Dropdown(
                choices=TIMEZONES,
                value=DEFAULT_TIMEZONE,
                label="TIME ZONE",
                scale=2,
            )
            join_button = gr.Button(
                "JOIN ROOM",
                variant="primary",
                elem_id="join-button",
                scale=1,
            )

        alert = gr.Markdown("🍿 Your room is ready.", elem_id="join-alert")

        # Chat header and three-dot menu
        with gr.Row(elem_id="chat-header"):
            gr.HTML(
                f'<div class="room-identity">'
                f'<div class="room-avatar">{ROOM_AVATAR}</div>'
                f'<div>'
                f'<div class="room-name">{ROOM_NAME}</div>'
                f'<div class="room-description">{ROOM_DESCRIPTION}</div>'
                f'</div></div>'
            )

            with gr.Column(elem_id="menu-column", scale=0, min_width=42):
                three_dot_button = gr.Button("⋮", elem_id="three-dot-button")

        # Persistent States
        menu_state = gr.State(False)
        attachment_state = gr.State(False)
        joined_state = gr.State(False)

        # Three-dot popup menu
        with gr.Group(visible=False, elem_id="three-dot-menu") as three_dot_menu:
            download_menu_button = gr.Button(
                "↓  Download Chat", elem_id="download-menu-item"
            )

        # Chat feed panel
        chat_feed = gr.HTML(
            value=render_chat(DEFAULT_TIMEZONE), elem_id="chat-feed-panel"
        )

        # Composer row: emoji, plus, text, send
        with gr.Row(elem_id="composer-row", equal_height=False):
            with gr.Column(elem_id="emoji-column", scale=0, min_width=54):
                gr.HTML(get_emoji_widget_html())

            with gr.Column(elem_id="attachment-column", scale=0, min_width=54):
                attachment_button = gr.Button("", elem_id="attachment-toggle")

            with gr.Column(elem_id="message-column", scale=1, min_width=0):
                message_input = gr.Textbox(
                    label="YOUR MESSAGE",
                    placeholder="Type your message...",
                    elem_id="message-input",
                    lines=2,
                    max_lines=5,
                )

            with gr.Column(elem_id="send-column", scale=0, min_width=100):
                send_button = gr.Button(
                    "SEND ➤", variant="primary", elem_id="send-button"
                )

        status = gr.Markdown("", elem_id="message-status")

        # Attachment drawer
        with gr.Group(
            visible=False, elem_id="attachment-panel"
        ) as attachment_panel:
            gr.Markdown("### Share a file")

            with gr.Row(elem_id="attachment-options"):
                image_option = gr.Button("▧  Images", elem_id="image-option")
                document_option = gr.Button(
                    "▤  Documents", elem_id="document-option"
                )

            with gr.Group(
                visible=False, elem_id="image-upload-panel"
            ) as image_upload_panel:
                image_files = gr.File(
                    label="Choose images",
                    file_count="multiple",
                    file_types=["image"],
                    type="filepath",
                )
                send_images = gr.Button("SEND IMAGES", variant="primary")
                image_status = gr.Markdown("")

            with gr.Group(
                visible=False, elem_id="document-upload-panel"
            ) as document_upload_panel:
                document_files = gr.File(
                    label="Choose PDF documents",
                    file_count="multiple",
                    file_types=[".pdf"],
                    type="filepath",
                )
                send_documents = gr.Button("SEND DOCUMENTS", variant="primary")
                document_status = gr.Markdown("")

        # Download section
        with gr.Group(
            visible=False, elem_id="download-section"
        ) as download_section:
            download_button = gr.Button(
                "↓  Download chat (.txt)", elem_id="download-button"
            )
            download_file = gr.File(
                label="",
                interactive=False,
                visible=False,
                elem_id="download-file",
            )

        # ------------------------------------------------------------
        # Event Registrations
        # ------------------------------------------------------------
        join_button.click(
            join_room,
            inputs=[name_input, timezone_input],
            outputs=[
                chat_feed,
                alert,
                status,
                join_button,
                joined_state,
            ],
        )

        send_button.click(
            send_message,
            inputs=[
                name_input,
                message_input,
                joined_state,
                timezone_input,
            ],
            outputs=[chat_feed, message_input, status],
        )

        message_input.submit(
            send_message,
            inputs=[
                name_input,
                message_input,
                joined_state,
                timezone_input,
            ],
            outputs=[chat_feed, message_input, status],
        )

        attachment_button.click(
            toggle_attachment,
            inputs=[attachment_state],
            outputs=[attachment_panel, attachment_state],
        )

        image_option.click(
            lambda: select_upload_type("image"),
            inputs=[],
            outputs=[image_upload_panel, document_upload_panel],
        )

        document_option.click(
            lambda: select_upload_type("document"),
            inputs=[],
            outputs=[image_upload_panel, document_upload_panel],
        )

        send_images.click(
            lambda name, files, joined, tz: share_media(
                name, files, joined, tz, "image"
            ),
            inputs=[
                name_input,
                image_files,
                joined_state,
                timezone_input,
            ],
            outputs=[chat_feed, image_files, image_status],
        )

        send_documents.click(
            lambda name, files, joined, tz: share_media(
                name, files, joined, tz, "pdf"
            ),
            inputs=[
                name_input,
                document_files,
                joined_state,
                timezone_input,
            ],
            outputs=[chat_feed, document_files, document_status],
        )

        three_dot_button.click(
            toggle_three_dot_menu,
            inputs=[menu_state],
            outputs=[three_dot_menu, menu_state],
        )

        download_menu_button.click(
            open_download_panel,
            inputs=[],
            outputs=[
                three_dot_menu,
                menu_state,
                download_section,
                download_file,
            ],
        )

        download_button.click(
            download_chat,
            inputs=[timezone_input],
            outputs=[download_file],
        )

        timer = gr.Timer(REFRESH_INTERVAL)
        timer.tick(
            refresh_chat,
            inputs=[timezone_input],
            outputs=[chat_feed, alert],
        )

        timezone_input.change(
            refresh_chat,
            inputs=[timezone_input],
            outputs=[chat_feed, alert],
        )

        # Client-side emoji picker JavaScript
        emoji_js = load_emoji_picker_js()
        if emoji_js:
            app.load(fn=None, inputs=None, outputs=None, js=emoji_js)

    return app
