
"""Unit tests for backend.media_service."""

import os
import tempfile
import unittest

from backend.media_service import (
    media_url,
    process_media_item,
    validate_image_header,
    validate_pdf_header,
)
from config.settings import MAX_FILE_SIZE


class TestMediaService(unittest.TestCase):

    def test_media_url_formatting(self):
        """media_url must generate quoted Gradio file URLs."""
        url = media_url("/tmp/test image.png")
        self.assertTrue(url.startswith("/gradio_api/file="))
        self.assertIn("test%20image.png", url)

    def test_validate_image_header(self):
        """Supported image signatures should pass."""
        self.assertTrue(
            validate_image_header(b"\x89PNG\r\n\x1a\n" + b"\x00" * 8, ".png")
        )
        self.assertTrue(
            validate_image_header(b"\xff\xd8\xff" + b"\x00" * 13, ".jpg")
        )
        self.assertTrue(
            validate_image_header(b"GIF87a" + b"\x00" * 10, ".gif")
        )
        self.assertTrue(
            validate_image_header(b"GIF89a" + b"\x00" * 10, ".gif")
        )
        self.assertTrue(
            validate_image_header(b"RIFF\x00\x00\x00\x00WEBP", ".webp")
        )

        self.assertFalse(validate_image_header(b"NOTANIMAGE", ".png"))
        self.assertFalse(
            validate_image_header(b"\x89PNG\r\n\x1a\n", ".exe")
        )

    def test_validate_pdf_header(self):
        """PDF header must start with %PDF- and have .pdf extension."""
        self.assertTrue(validate_pdf_header(b"%PDF-1.4\n", ".pdf"))
        self.assertFalse(validate_pdf_header(b"NOTPDF", ".pdf"))
        self.assertFalse(validate_pdf_header(b"%PDF-1.4\n", ".txt"))

    def test_process_media_file_size_limit(self):
        """Files exceeding MAX_FILE_SIZE must be rejected."""
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            f.write(b"\x89PNG\r\n\x1a\n")
            f.seek(MAX_FILE_SIZE + 10)
            f.write(b"\x00")
            temp_name = f.name

        try:
            success, msg, info = process_media_item(temp_name, "image")
            self.assertFalse(success)
            self.assertIn("exceeds the 5 MB limit", msg)
            self.assertIsNone(info)
        finally:
            if os.path.exists(temp_name):
                os.remove(temp_name)
    
    def test_rejects_png_header_with_jpg_extension(self):
        self.assertFalse(
            validate_image_header(
                b"\x89PNG\r\n\x1a\n" + b"\x00" * 8,
                ".jpg",
            )
        )

    def test_rejects_jpeg_header_with_png_extension(self):
        self.assertFalse(
            validate_image_header(
                b"\xff\xd8\xff" + b"\x00" * 13,
                ".png",
            )
        )

    def test_rejects_gif_header_with_webp_extension(self):
        self.assertFalse(
            validate_image_header(
                b"GIF89a" + b"\x00" * 10,
                ".webp",
            )
        )

    def test_accepts_jpeg_header_with_jpeg_extension(self):
        self.assertTrue(
            validate_image_header(
                b"\xff\xd8\xff" + b"\x00" * 13,
                ".jpeg",
            )
        )
    
    def test_process_rejects_mismatched_image_extension(self):
        """A PNG file renamed as JPG must not be accepted."""
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
            f.write(b"\x89PNG\r\n\x1a\n" + b"\x00" * 32)
            temp_name = f.name

        try:
            success, msg, info = process_media_item(temp_name, "image")
            self.assertFalse(success)
            self.assertIn("invalid image file", msg)
            self.assertIsNone(info)
        finally:
            if os.path.exists(temp_name):
                os.remove(temp_name)

    def test_process_valid_image(self):
        """A PNG-signature file should be accepted by current validation."""
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            f.write(b"\x89PNG\r\n\x1a\n" + b"\x00" * 32)
            temp_name = f.name

        try:
            success, msg, info = process_media_item(temp_name, "image")
            self.assertTrue(success)
            self.assertIsNotNone(info)
            self.assertEqual(info["kind"], "image")
            self.assertTrue(os.path.exists(info["path"]))
            os.remove(info["path"])
        finally:
            if os.path.exists(temp_name):
                os.remove(temp_name)

    def test_rejects_png_header_with_jpg_extension(self):
        self.assertFalse(
            validate_image_header(
                b"\x89PNG\r\n\x1a\n" + b"\x00" * 8,
                ".jpg",
            )
        )

    def test_rejects_jpeg_header_with_png_extension(self):
        self.assertFalse(
            validate_image_header(
                b"\xff\xd8\xff" + b"\x00" * 13,
                ".png",
            )
        )

    def test_rejects_gif_header_with_webp_extension(self):
        self.assertFalse(
            validate_image_header(
                b"GIF89a" + b"\x00" * 10,
                ".webp",
            )
        )

    def test_accepts_jpeg_header_with_jpeg_extension(self):
        self.assertTrue(
            validate_image_header(
                b"\xff\xd8\xff" + b"\x00" * 13,
                ".jpeg",
            )
        )

    def test_process_rejects_mismatched_image_extension(self):
        """A PNG file renamed as JPG must be rejected."""
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
            f.write(b"\x89PNG\r\n\x1a\n" + b"\x00" * 32)
            temp_name = f.name

        try:
            success, msg, info = process_media_item(temp_name, "image")
            self.assertFalse(success)
            self.assertIn("invalid image file", msg)
            self.assertIsNone(info)
        finally:
            if os.path.exists(temp_name):
                os.remove(temp_name)


if __name__ == "__main__":
    unittest.main()
