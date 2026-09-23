from __future__ import annotations

import os
from typing import Optional

from backend.models import CompanyInfo


class CompanyResearcherAgent:
    """Enhance a company profile with research details."""

    async def research_company(self, company_name: str) -> CompanyInfo:
        # Replace with real OpenRouter/Agno research logic when wired up.
        api_key = os.getenv("OPENROUTER_API_KEY")
        _ = api_key

        return CompanyInfo(
            name=company_name,
            website="https://example.com",
            industry="SaaS",
            description=(
                f"{company_name} is a software company operating in a fast-moving market "
                "with a strong growth profile and active outbound sales opportunities."
            ),
            location="United States",
            funding="Series A",
            employees="11-50",
        )
