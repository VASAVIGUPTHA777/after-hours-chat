"""Unit tests for backend.download_service."""

import os
import unittest

from backend.download_service import (
    create_transcript_file,
    generate_transcript_lines,
)


class TestDownloadService(unittest.TestCase):
    def test_empty_snapshot_raises(self):
        """Empty message history should raise ValueError."""
        with self.assertRaises(ValueError):
            create_transcript_file([], "Asia/Kolkata")

    def test_generate_transcript_lines(self):
        """Transcript should format header, joins, messages, and attachments."""
        snapshot = [
            {
                "kind": "join",
                "name": "Alice",
                "time": "2026-10-24T12:00:00+00:00",
            },
            {
                "kind": "message",
                "name": "Alice",
                "text": "Hello all!",
                "time": "2026-10-24T12:01:00+00:00",
            },
            {
                "kind": "image",
                "name": "Bob",
                "filename": "sunset.jpg",
                "time": "2026-10-24T12:02:00+00:00",
            },
            {
                "kind": "pdf",
                "name": "Alice",
                "filename": "notes.pdf",
                "time": "2026-10-24T12:03:00+00:00",
            },
        ]

        lines = generate_transcript_lines(snapshot, "Asia/Kolkata")
        content = "\n".join(lines)

        self.assertIn("AFTER HOURS — CHAT HISTORY", content)
        self.assertIn("Time zone: Asia/Kolkata", content)
        self.assertIn("Alice joined the chat", content)
        self.assertIn("Alice: Hello all!", content)
        self.assertIn("Bob shared image: sunset.jpg", content)
        self.assertIn("Alice shared pdf: notes.pdf", content)

    def test_create_transcript_file(self):
        """create_transcript_file should generate a readable .txt file on disk."""
        snapshot = [
            {
                "kind": "message",
                "name": "Alice",
                "text": "Test message",
                "time": "2026-10-24T12:00:00+00:00",
            }
        ]
        file_path = create_transcript_file(snapshot, "Asia/Kolkata")
        try:
            self.assertTrue(os.path.exists(file_path))
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
            self.assertIn("Alice: Test message", text)
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)


if __name__ == "__main__":
    unittest.main()
