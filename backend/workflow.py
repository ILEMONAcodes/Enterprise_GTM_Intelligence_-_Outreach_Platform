# backend/workflow.py
from __future__ import annotations
import os
import json
from typing import List, Optional
from pydantic import BaseModel, Field

from backend.models import (
    OutreachConfig,
    CompanyInfo,
    ContactInfo,
    CompanyResearch,
    OutreachEmail,
    PipelineResult,
)

from backend.agents.company_finder import build_company_finder
from backend.agents.contact_finder import build_contact_finder
from backend.agents.company_researcher import build_company_researcher
from backend.agents.email_creator import build_email_creator

class OutreachWorkflow:
    def __init__(self):
        self.company_finder = build_company_finder()
        self.contact_finder = build_contact_finder()
        self.company_researcher = build_company_researcher()
        self.email_creator = build_email_creator()

    def run(self, config: OutreachConfig) -> PipelineResult:
        print(f"\nRunning OutreachWorkflow for criteria: '{config.criteria}'")

        # -------------------------------------------------------------
        # STEP 1: Company Discovery
        # -------------------------------------------------------------
        print("Step 1: Discovering target companies...")
        company_prompt = (
            f"Find 5 to 10 companies matching this criteria: {config.criteria}. "
            "Return the output as a clean JSON list of objects with keys: name, website, description, size, location."
        )
        company_res = self.company_finder.run(company_prompt)

        companies: List[CompanyInfo] = []
        try:
            content = company_res.content
            if isinstance(content, str):
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()
                parsed = json.loads(content)
                if isinstance(parsed, dict):
                    parsed = parsed.get("companies", list(parsed.values())[0])
                companies = [CompanyInfo(**c) for c in parsed]
            elif isinstance(content, dict):
                raw_list = content.get("companies", [])
                companies = [CompanyInfo(**c) for c in raw_list]
        except Exception as e:
            print(f"Warning parsing companies: {e}. Raw content was:\n{company_res.content}")

        print(f"Discovered {len(companies)} companies.")
        if not companies:
            companies = [CompanyInfo(name="Sample SaaS Corp", website="https://samplesaas.com", description="B2B SaaS platform.", size="50-100", location="San Francisco, CA")]

        # -------------------------------------------------------------
        # STEP 2: Contact Finding
        # -------------------------------------------------------------
        print("Step 2: Finding decision-makers...")
        company_summaries = ", ".join([f"{c.name} ({c.website})" for c in companies])
        contact_prompt = (
            f"For these companies: {company_summaries}, find key decision-makers "
            f"matching the target role: {config.target_role}. "
            "Return as a JSON list with keys: company_name, full_name, title, background_context."
        )
        contact_res = self.contact_finder.run(contact_prompt)

        contacts: List[ContactInfo] = []
        try:
            content = contact_res.content
            if isinstance(content, str):
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()
                parsed = json.loads(content)
                if isinstance(parsed, dict):
                    parsed = parsed.get("contacts", list(parsed.values())[0])
                contacts = [ContactInfo(**ct) for ct in parsed]
            elif isinstance(content, dict):
                contacts = [ContactInfo(**ct) for ct in content.get("contacts", [])]
        except Exception as e:
            print(f"Warning parsing contacts: {e}")

        print(f"Found {len(contacts)} contacts.")

        # -------------------------------------------------------------
        # STEP 3: Company Research & Triggers
        # -------------------------------------------------------------
        print("Step 3: Conducting deep research and identifying triggers...")
        research_prompt = f"Perform research and find recent news or product updates for these companies: {company_summaries}. Return as a JSON list with keys: company_name, triggers (list of strings), summary."
        research_res = self.company_researcher.run(research_prompt)

        research_list: List[CompanyResearch] = []
        try:
            content = research_res.content
            if isinstance(content, str):
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()
                parsed = json.loads(content)
                if isinstance(parsed, dict):
                    parsed = parsed.get("research", list(parsed.values())[0])
                research_list = [CompanyResearch(**r) for r in parsed]
            elif isinstance(content, dict):
                research_list = [CompanyResearch(**r) for r in content.get("research", [])]
        except Exception as e:
            print(f"Warning parsing research: {e}")

        print(f"Gathered research for target companies.")

        # -------------------------------------------------------------
        # STEP 4: Email Generation
        # -------------------------------------------------------------
        print("Step 4: Crafting hyper-personalized cold emails...")
        context_payload = {
            "companies": [c.model_dump() for c in companies],
            "contacts": [ct.model_dump() for ct in contacts],
            "research": [r.model_dump() for r in research_list],
        }

        email_prompt = (
            f"Using this data payload: {json.dumps(context_payload)}, write short (<120 words) "
            "cold emails. Return as a JSON list with keys: company_name, recipient_name, recipient_title, subject_line, email_body."
        )
        email_res = self.email_creator.run(email_prompt)

        emails: List[OutreachEmail] = []
        try:
            content = email_res.content
            if isinstance(content, str):
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()
                parsed = json.loads(content)
                if isinstance(parsed, dict):
                    parsed = parsed.get("emails", list(parsed.values())[0])
                emails = [OutreachEmail(**e) for e in parsed]
            elif isinstance(content, dict):
                emails = [OutreachEmail(**e) for e in content.get("emails", [])]
        except Exception as e:
            print(f"Warning parsing emails: {e}")

        print(f"Generated {len(emails)} personalized emails.")

        return PipelineResult(
            criteria=config.criteria,
            companies=companies,
            contacts=contacts,
            research=research_list,
            emails=emails,
        )