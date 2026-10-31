# Changelog

All notable changes to the **After Hours** chat application will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased] — 2026-10-29

### Added
- **Modular Project Architecture**:
  - `config/settings.py`: Centralized configuration for timezones, 36-emoji palette, file limits, paths, and server settings.
  - `backend/timezone_service.py`: Standard library `zoneinfo.ZoneInfo` integration supporting 9 timezones with UTC normalization.
  - `backend/user_service.py`: User alias registration, whitespace trimming, and duplicate check.
  - `backend/chat_service.py`: Thread-safe message store synchronized via `threading.Lock` for joins, messages, and attachments.
  - `backend/media_service.py`: Binary magic byte verification for PNG, JPEG, GIF, WEBP, and PDF files, file size enforcement (5 MB limit), and UUID-based storage.
  - `backend/download_service.py`: Plaintext chat transcript generator with timezone offset formatting.
  - `frontend/chat_ui.py`: Semantic HTML chat feed, empty room placeholder, and room alert rendering.
  - `frontend/composer.py`: Message submission and room join callbacks.
  - `frontend/emoji_picker.py`: Custom HTML emoji palette with client-side JavaScript textarea insertion.
  - `frontend/attachment_ui.py`: Attachment drawer with image and PDF document upload panels.
  - `frontend/download_menu.py`: Three-dot menu and transcript download section.
  - `frontend/layout.py`: Complete Gradio Blocks layout assembly and event wiring.
  - `static/css/`: Modular stylesheets (`main.css`, `chat.css`, `composer.css`, `responsive.css`).
  - `static/js/emoji_picker.js`: Client-side DOM event integration for emoji popup.
- **Automated Test Suite**:
  - `tests/test_timezone.py`: 5 tests covering fallback, configured zones, UTC timestamps, and time formatting.
  - `tests/test_chat.py`: 6 tests covering user registration, join events, text messages, media records, message ordering, and multi-threaded write safety.
  - `tests/test_media.py`: 5 tests covering media URL formatting, magic byte validation, 5 MB file size limits, and valid upload saving.
  - `tests/test_download.py`: 3 tests covering empty history validation, transcript line formatting, and temporary file generation.
  - All 19 tests pass successfully with 0 failures and 0 errors.
- **Documentation**:
  - `docs/COLAB_SETUP.md`: Step-by-step Google Colab execution guide.
  - `docs/PR_HISTORY.md`: History of pull requests, objectives, test results, and merge records.
  - `.github/pull_request_template.md`: Standardized GitHub Pull Request submission template.

### Preserved
- 100% of features and behavior from the original `config/chatroom.ipynb` Colab notebook.
- Original dark teal late-night styling, responsive layouts, 2-second polling refresh interval, and Gradio live sharing.
