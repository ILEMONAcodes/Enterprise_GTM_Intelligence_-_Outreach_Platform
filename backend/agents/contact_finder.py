from __future__ import annotations

import os
from typing import List

from backend.models import ContactInfo


class ContactFinderAgent:
    """Find relevant people to contact at a company."""

    async def find_contacts(self, company_name: str, target_role: str, max_contacts: int) -> List[ContactInfo]:
        # Replace with Exa/Agno enrichment calls in production.
        _ = os.getenv("EXA_API_KEY")

        contacts = [
            ContactInfo(
                name="Jordan Lee",
                title=target_role or "VP of Growth",
                email="jordan@company.com",
                linkedin="https://linkedin.com/in/jordanlee",
                company=company_name,
            ),
            ContactInfo(
                name="Priya Shah",
                title="Head of Revenue Operations",
                email="priya@company.com",
                linkedin="https://linkedin.com/in/priyashah",
                company=company_name,
            ),
        ]

        return contacts[:max_contacts]
