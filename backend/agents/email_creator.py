from __future__ import annotations

import os
from typing import Tuple

from backend.models import CompanyInfo, ContactInfo


class EmailCreatorAgent:
    """Generate an email subject and body for a campaign."""

    async def draft_email(self, company: CompanyInfo, contact: ContactInfo, tone: str) -> Tuple[str, str]:
        _ = os.getenv("OPENROUTER_API_KEY")

        subject = f"Quick idea for {company.name}"
        body = (
            f"Hi {contact.name},\n\n"
            f"I noticed {company.name} is doing strong work in {company.industry or 'your market'}, and I think there may be a straightforward opportunity to improve your outbound performance. "
            f"We help teams like yours streamline lead generation and conversion with a stronger, more focused outreach system.\n\n"
            f"I’d love to connect briefly to share a few ideas that could be relevant to {company.name}. "
            f"If this is useful, I’d be glad to set up a short conversation.\n\n"
            f"Best,\n"
            f"Your Name\n"
        )

        if tone.lower() == "friendly":
            body = body.replace("Best,", "Thanks,")

        return subject, body
