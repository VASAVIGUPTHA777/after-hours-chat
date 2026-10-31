/**
 * After Hours Chat — Client-side Emoji Picker Integration
 *
 * Attaches event handlers to the custom HTML emoji widget:
 * - Toggles popup on click
 * - Inserts chosen emoji at current cursor position in message textarea
 * - Dispatches input event so Gradio state recognizes textarea change
 * - Closes popup on outside click
 */

() => {
    function installEmojiPicker() {
        const widget = document.querySelector("#emoji-widget");
        const popup = document.querySelector("#emoji-popup");
        const toggle = document.querySelector("#emoji-toggle");
        const textbox = document.querySelector("#message-input textarea");

        if (!widget || !popup || !toggle || !textbox) return;
        if (widget.dataset.ready === "true") return;

        widget.dataset.ready = "true";

        toggle.addEventListener("click", event => {
            event.preventDefault();
            event.stopPropagation();
            popup.classList.toggle("open");
        });

        popup.addEventListener("click", event => {
            const button = event.target.closest(".emoji-choice");
            if (!button) return;

            event.preventDefault();
            event.stopPropagation();

            const start = textbox.selectionStart ?? textbox.value.length;
            const end = textbox.selectionEnd ?? textbox.value.length;

            textbox.setRangeText(
                button.dataset.emoji,
                start,
                end,
                "end"
            );

            textbox.dispatchEvent(
                new Event("input", { bubbles: true })
            );

            textbox.focus();
        });

        document.addEventListener("click", event => {
            if (!widget.contains(event.target)) {
                popup.classList.remove("open");
            }
        });
    }

    installEmojiPicker();
    setTimeout(installEmojiPicker, 500);
    setTimeout(installEmojiPicker, 1500);
}
