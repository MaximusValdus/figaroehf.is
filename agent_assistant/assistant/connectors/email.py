"""Mock email connector.

IMPORTANT: this connector never contacts a mail server. "Sent" messages are
captured in a local outbox so the rest of the system can be exercised safely.
"""

from __future__ import annotations

from .base import EmailConnector


class MockEmailConnector(EmailConnector):
    def __init__(self) -> None:
        self._outbox: list[dict] = []

    def send_email(self, to: str, subject: str, body: str) -> dict:
        # Deliberately does NOT send. It only records the message locally.
        message = {
            "to": to,
            "subject": subject,
            "body": body,
            "delivered": False,  # always False — this is a mock
        }
        self._outbox.append(message)
        return message

    def outbox(self) -> list[dict]:
        return list(self._outbox)
