# After Hours Chat

> A Netflix-inspired / late-night, text-only group chat application built with Python and Gradio.

[![Python](https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)](https://www.python.org/)
[![Gradio](https://img.shields.io/badge/Gradio-6.30.0-orange)](https://gradio.app/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-19%20passed-brightgreen)](#running-automated-tests)

---

## Overview

**After Hours** is a group chat application tailored for late-night community conversations. It provides an in-memory, synchronized room where users can join with a custom alias, send text messages, share images and PDF documents, pick emojis from a dedicated palette, format timestamps in their local timezone, and export complete chat transcripts.

Originally developed in Google Colab, After Hours has been restructured into a modular, production-ready Python package while preserving **100% of its original features and behavior**.

---

## Features

- **User Alias & Join Management**: Register a display name to join the room. Prevents duplicate case-insensitive aliases and locks the join button upon entry.
- **Thread-Safe In-Memory Store**: Synchronized message queue using Python's `threading.Lock` across concurrent user sessions.
- **Real-Time Polling Refresh**: Auto-updates chat feed and room notifications every 2 seconds via `gr.Timer`.
- **Global Timezone Support**: Converts UTC timestamps to any of 9 supported global timezones using Python standard library `zoneinfo.ZoneInfo`:
  - India (IST) `Asia/Kolkata`
  - United Kingdom `Europe/London`
  - New York `America/New_York`
  - Los Angeles `America/Los_Angeles`
  - Singapore `Asia/Singapore`
  - Tokyo `Asia/Tokyo`
  - Sydney `Australia/Sydney`
  - Berlin `Europe/Berlin`
  - UTC `UTC`
- **Emoji Palette & JS Integration**: 36-emoji grid popup triggered by an SVG button, with DOM injection into the message box.
- **Attachment Drawer**:
  - Image sharing (PNG, JPEG, GIF, WEBP) with magic byte validation and inline preview cards.
  - PDF document sharing with magic byte verification (`%PDF-`), file size display, and download cards.
  - Enforced limits: Maximum 5 files per upload, maximum 5 MB per file.
- **Chat Transcript Downloads**: Generate and download formatted `.txt` transcripts adjusted to the selected timezone.
- **Dark Late-Night Styling**: Custom responsive CSS with WhatsApp/Netflix dark accents, optimized for both desktop and mobile screens (`<= 600px`).

---

## Project Structure

```
chatroom/
├── .github/
│   └── pull_request_template.md    # Standard GitHub Pull Request template
├── config/
│   ├── __init__.py
│   ├── chatroom.ipynb              # Original Google Colab notebook (preserved source of truth)
│   └── settings.py                 # Central configuration, timezones, emojis, limits, and paths
├── backend/
│   ├── __init__.py
│   ├── chat_service.py             # Thread-safe in-memory message store and synchronization
│   ├── user_service.py             # User alias validation and session tracking
│   ├── timezone_service.py         # ZoneInfo timestamp conversions and formatting
│   ├── media_service.py            # Magic byte validation, media storage, and URL generation
│   └── download_service.py         # Plaintext transcript generation
├── frontend/
│   ├── __init__.py
│   ├── chat_ui.py                  # HTML chat feed and room alert rendering
│   ├── composer.py                 # Message sending and join room callbacks
│   ├── emoji_picker.py             # HTML emoji widget and JS loader
│   ├── attachment_ui.py            # Attachment drawer and media upload callbacks
│   ├── download_menu.py            # Three-dot menu and transcript export callbacks
│   └── layout.py                   # Gradio Blocks layout assembly and event wiring
├── static/
│   ├── css/
│   │   ├── main.css                # Global layout, container, typography, join row
│   │   ├── chat.css                # Chat feed, empty placeholder, bubbles, media cards
│   │   ├── composer.css            # Composer bar, emoji popup, buttons, attachment drawer
│   │   └── responsive.css          # Mobile media queries (<= 600px)
│   ├── js/
│   │   └── emoji_picker.js         # Client-side emoji click and textarea insertion script
│   └── uploads/
│       └── .gitkeep                # Track directory without checking in user media
├── tests/
│   ├── __init__.py
│   ├── test_chat.py                # Tests for chat storage, joins, and thread safety
│   ├── test_timezone.py            # Tests for timezone validation and formatting
│   ├── test_media.py               # Tests for image/PDF magic bytes and file limits
│   └── test_download.py            # Tests for transcript generation and file export
├── docs/
│   ├── architecture.md             # Architecture overview and design documentation
│   ├── COLAB_SETUP.md              # Detailed instructions for running in Google Colab
│   └── PR_HISTORY.md               # Pull request index, objectives, and test records
├── app.py                          # Application entry point
├── requirements.txt                # Pinned dependencies (Gradio 6.30.0, Pillow, tzdata)
├── CHANGELOG.md                    # Detailed version change history
└── .gitignore                      # Exclusions for virtual environments, caches, and uploads
```

---

## Running in Google Colab

To run After Hours in Google Colab with a live public URL:

1. Open [Google Colab](https://colab.research.google.com/).
2. Run the following in a code cell:
   ```bash
   !git clone https://github.com/VASAVIGUPTHA777/after-hours-chat.git
   %cd after-hours-chat
   %pip install -r requirements.txt
   !python app.py
   ```
3. Click the generated `https://<id>.gradio.live` link to open the chat room.

For detailed Colab configuration and sharing options, see [docs/COLAB_SETUP.md](docs/COLAB_SETUP.md).

---

## Local Setup & Execution

### Prerequisites
- Python 3.9+ (tested on Python 3.9, 3.10, 3.11, 3.12, 3.13)
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/VASAVIGUPTHA777/after-hours-chat.git
cd after-hours-chat
```

### 2. Create and Activate a Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Launch the Application
```bash
python app.py
```
Open your browser to `http://localhost:7860`.

---

## Running Automated Tests

The test suite requires no external test runners and runs directly with Python's built-in `unittest` (also 100% compatible with `pytest`):

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

### Test Coverage Summary
- **Timezone Service (`tests/test_timezone.py`)**: 5 tests verifying default fallback, all 9 configured timezones, UTC ISO strings, and formatting accuracy.
- **Chat & User Service (`tests/test_chat.py`)**: 6 tests verifying alias validation, join event creation, text message ordering, media metadata storage, and concurrent multi-threaded write safety.
- **Media Service (`tests/test_media.py`)**: 5 tests verifying media URL paths, binary magic byte headers for all supported image and PDF formats, 5 MB file size rejection, and valid file saving.
- **Download Service (`tests/test_download.py`)**: 3 tests verifying empty history rejection, transcript line formatting, and temporary file generation.

---

## Contributing & Git Workflow

We follow a strict branch → pull request → review → merge workflow:

1. **`main` Branch**: Contains reviewed, stable, production-ready code. Committing directly to `main` is disallowed.
2. **Feature Branches**: All refactorings, enhancements, and bug fixes are developed on dedicated branches:
   ```bash
   git checkout -b feature/<feature-name>
   ```
3. **Commit Messages**: Write clear, descriptive commit messages adhering to standard conventions:
   ```bash
   git commit -m "feat(backend): add magic byte verification for PDF attachments"
   ```
4. **Pull Requests**:
   - Push your feature branch to the remote repository.
   - Open a Pull Request targeting `main`.
   - Fill in the PR template (`.github/pull_request_template.md`) with testing results.
   - Wait for explicit lead developer review and approval before merging.

For full pull request history, see [docs/PR_HISTORY.md](docs/PR_HISTORY.md).
For recent changes, see [CHANGELOG.md](CHANGELOG.md).
