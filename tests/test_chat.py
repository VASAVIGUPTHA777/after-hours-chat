"""Unit tests for backend.chat_service and user_service."""

import threading
import unittest

from backend.chat_service import (
    add_join_event,
    add_media_message,
    add_text_message,
    clear_messages,
    get_latest_join_event,
    get_messages_snapshot,
    message_count,
)
from backend.user_service import (
    get_registered_users,
    is_user_registered,
    register_user,
    reset_users,
    validate_username,
)


class TestChatService(unittest.TestCase):
    def setUp(self):
        clear_messages()
        reset_users()

    def tearDown(self):
        clear_messages()
        reset_users()

    def test_user_registration(self):
        """User registration should be case-insensitive and trimmed."""
        self.assertEqual(validate_username("  Alice  "), "Alice")
        self.assertTrue(register_user("Alice"))
        self.assertFalse(register_user("alice"))  # Duplicate
        self.assertTrue(is_user_registered("ALICE"))
        self.assertFalse(is_user_registered("Bob"))
        self.assertIn("alice", get_registered_users())

    def test_add_join_event(self):
        """Joining should append a join record and update count."""
        msg = add_join_event("Alice")
        self.assertEqual(msg["kind"], "join")
        self.assertEqual(msg["name"], "Alice")
        self.assertEqual(message_count(), 1)
        self.assertEqual(get_latest_join_event(), msg)

    def test_add_text_message(self):
        """Text messages should store name, text, and timestamp."""
        msg = add_text_message("Alice", "Hello world!")
        self.assertEqual(msg["kind"], "message")
        self.assertEqual(msg["name"], "Alice")
        self.assertEqual(msg["text"], "Hello world!")
        self.assertIn("time", msg)
        self.assertEqual(message_count(), 1)

    def test_add_media_message(self):
        """Media records should preserve kind, filename, path, and size."""
        msg = add_media_message(
            name="Alice",
            kind="image",
            filename="photo.jpg",
            path="/tmp/photo.jpg",
            size=1024,
        )
        self.assertEqual(msg["kind"], "image")
        self.assertEqual(msg["filename"], "photo.jpg")
        self.assertEqual(msg["size"], 1024)

    def test_message_ordering(self):
        """Messages should be retrieved in the exact order added."""
        add_join_event("Alice")
        add_text_message("Alice", "First")
        add_text_message("Bob", "Second")

        snapshot = get_messages_snapshot()
        self.assertEqual(len(snapshot), 3)
        self.assertEqual(snapshot[0]["kind"], "join")
        self.assertEqual(snapshot[1]["text"], "First")
        self.assertEqual(snapshot[2]["text"], "Second")

    def test_thread_safety_concurrent_writes(self):
        """Multiple threads writing concurrently should not drop messages."""
        num_threads = 10
        messages_per_thread = 20

        def worker(thread_id):
            for i in range(messages_per_thread):
                add_text_message(f"User{thread_id}", f"Msg {i}")

        threads = [
            threading.Thread(target=worker, args=(t,))
            for t in range(num_threads)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(message_count(), num_threads * messages_per_thread)


if __name__ == "__main__":
    unittest.main()
