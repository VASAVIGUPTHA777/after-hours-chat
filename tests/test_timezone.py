"""Unit tests for backend.timezone_service."""

import unittest
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from backend.timezone_service import format_time, get_timezone, now_utc
from config.settings import DEFAULT_TIMEZONE, TIMEZONES


class TestTimezoneService(unittest.TestCase):
    def test_default_timezone_fallback(self):
        """Invalid or None timezone should fall back to Asia/Kolkata."""
        self.assertEqual(get_timezone(None), DEFAULT_TIMEZONE)
        self.assertEqual(get_timezone(""), DEFAULT_TIMEZONE)
        self.assertEqual(get_timezone("Invalid/NonExistent"), DEFAULT_TIMEZONE)

    def test_supported_timezones(self):
        """All configured timezones in TIMEZONES must be valid."""
        for label, tz_identifier in TIMEZONES:
            with self.subTest(tz=tz_identifier):
                self.assertEqual(get_timezone(tz_identifier), tz_identifier)

    def test_now_utc_format(self):
        """now_utc should return a valid ISO 8601 string."""
        ts = now_utc()
        parsed = datetime.fromisoformat(ts)
        self.assertIsNotNone(parsed.tzinfo)

    def test_format_time_accuracy(self):
        """format_time should correctly convert UTC time to target timezone."""
        # 2026-10-24 12:00:00 UTC -> 17:30 IST
        utc_ts = datetime(2026, 10, 24, 12, 0, 0, tzinfo=timezone.utc).isoformat()
        ist_str = format_time(utc_ts, "Asia/Kolkata")
        self.assertIn("24 Oct 2026", ist_str)
        self.assertIn("05:30 PM", ist_str)

    def test_format_time_invalid_input(self):
        """Invalid timestamp returns fallback string '--:--'."""
        self.assertEqual(format_time("not-a-timestamp", "Asia/Kolkata"), "--:--")


if __name__ == "__main__":
    unittest.main()
