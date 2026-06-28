"""Email tool.

Sending email is a WRITE action and therefore always approval-gated. The
underlying connector is a mock that never delivers mail.
"""

from __future__ import annotations

from typing import Any

from ..connectors.base import EmailConnector
from .base import Permission, Tool


class SendEmailTool(Tool):
    name = "email.send_email"
    description = "Draft and 'send' an email (mock only). Requires approval."
    permission = Permission.WRITE

    def __init__(self, connector: EmailConnector) -> None:
        self.connector = connector

    def run(self, to: str, subject: str, body: str, **_: Any) -> dict:
        return self.connector.send_email(to=to, subject=subject, body=body)

    def summarize(self, **params: Any) -> str:
        return f"Send email to {params.get('to')!r} — {params.get('subject')!r}"
