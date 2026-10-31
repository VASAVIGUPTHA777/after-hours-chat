# Running After Hours in Google Colab

This guide explains how to run the modular **After Hours** chat application directly in Google Colab.

---

## Quick Start (Colab Notebook Cell)

Open a new notebook in [Google Colab](https://colab.research.google.com/) and paste the following commands into a code cell:

```bash
# 1. Clone the repository
!git clone https://github.com/VASAVIGUPTHA777/after-hours-chat.git
%cd after-hours-chat

# 2. Install required dependencies
%pip install -r requirements.txt

# 3. Launch After Hours
!python app.py
```

---

## How It Works in Colab

1. **Automatic Public URL:**
   - In Google Colab, Gradio automatically generates a public `https://<id>.gradio.live` link when launched with `share=True` (enabled by default in `config/settings.py`).
   - Anyone with this URL can open the application in their browser and join the chat room in real time.

2. **Temporary Media Storage:**
   - Media uploads (images and PDF documents) are saved to Colab's `/tmp/after_hours_media` directory.
   - Gradio serves these files through its internal `/gradio_api/file=` endpoint via `allowed_paths=[settings.MEDIA_DIR]`.

3. **Multi-User Live Testing:**
   - Multiple browser tabs or different devices can join the shared chat room simultaneously.
   - The UI auto-refreshes every 2 seconds via `gr.Timer`.

---

## Optional Environment Variables

You can configure execution parameters before starting the app:

```python
import os

# Set custom port (default is 7860)
os.environ["GRADIO_SERVER_PORT"] = "7860"

# Explicitly toggle public sharing (True/False)
os.environ["AFTER_HOURS_SHARE"] = "True"
```

---

## Running Unit Tests in Colab

To verify backend services and validation logic inside Colab:

```bash
!python -m unittest discover -s tests -p "test_*.py" -v
```
