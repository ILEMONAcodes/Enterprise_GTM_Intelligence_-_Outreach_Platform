from __future__ import annotations

from typing import List

from backend.agents.company_finder import CompanyFinderAgent
from backend.agents.company_researcher import CompanyResearcherAgent
from backend.agents.contact_finder import ContactFinderAgent
from backend.agents.email_creator import EmailCreatorAgent
from backend.models import CampaignRequest, CampaignResult, ContactInfo


class OutreachWorkflow:
    def __init__(self) -> None:
        self.company_finder = CompanyFinderAgent()
        self.company_researcher = CompanyResearcherAgent()
        self.contact_finder = ContactFinderAgent()
        self.email_creator = EmailCreatorAgent()

    async def run(self, request: CampaignRequest) -> CampaignResult:
        config = request.config

        companies = await self.company_finder.find_companies(config)
        company = companies[0]
        enriched_company = await self.company_researcher.research_company(company.name)

        contacts: List[ContactInfo] = await self.contact_finder.find_contacts(
            enriched_company.name,
            config.target_role,
            config.max_contacts,
        )

        first_contact = contacts[0] if contacts else ContactInfo(
            name="Target Contact",
            title=config.target_role or "Decision Maker",
            email="contact@company.com",
            company=enriched_company.name,
        )

        subject, body = await self.email_creator.draft_email(
            enriched_company,
            first_contact,
            config.tone,
        )

        return CampaignResult(
            company=enriched_company,
            contacts=contacts,
            email_subject=subject,
            email_body=body,
            summary=(
                f"Prepared outreach for {enriched_company.name} with {len(contacts)} contact(s) "
                f"and a ready-to-send email draft."
            ),
        )
