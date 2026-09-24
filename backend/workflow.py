# backend/workflow.py
from __future__ import annotations
import os
import json
import re
from typing import List, Optional, Any
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

def extract_and_parse_json(content: Any) -> Any:
    """Robustly extracts JSON from raw LLM output strings or objects."""
    if isinstance(content, (dict, list)):
        return content
        
    if not isinstance(content, str):
        return []

    # Try standard load first
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass

    # Clean markdown code blocks
    cleaned = content
    if "```json" in cleaned:
        cleaned = cleaned.split("```json")[1].split("```")[0].strip()
    elif "```" in cleaned:
        cleaned = cleaned.split("```")[1].split("```")[0].strip()
        
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # Regex fallback to find any JSON array or object bracket block
    match = re.search(r'(\[.*\]|\{.*\})', content, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass
            
    return []

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
            "Return your response as a valid JSON array of objects with keys: name, website, description, size, location."
        )
        company_res = self.company_finder.run(company_prompt)
        
        raw_companies = extract_and_parse_json(company_res.content)
        if isinstance(raw_companies, dict):
            raw_companies = raw_companies.get("companies", list(raw_companies.values())[0] if raw_companies else [])
            
        companies: List[CompanyInfo] = []
        if isinstance(raw_companies, list):
            for item in raw_companies:
                if isinstance(item, dict):
                    try:
                        companies.append(CompanyInfo(**item))
                    except Exception:
                        pass
                        
        print(f"Discovered {len(companies)} companies.")

        if not companies:
            # Absolute last resort fallback if search returns completely empty
            companies = [CompanyInfo(name="Target Startup", website="https://example.com", description="Target company matching criteria.", size="50-200", location="Boston, MA")]

        # -------------------------------------------------------------
        # STEP 2: Contact Finding
        # -------------------------------------------------------------
        print("Step 2: Finding decision-makers...")
        company_summaries = ", ".join([f"{c.name} ({c.website})" for c in companies])
        contact_prompt = (
            f"For these companies: {company_summaries}, find key decision-makers "
            f"matching the target role: {config.target_role}. "
            "Return as a valid JSON array with keys: company_name, full_name, title, background_context."
        )
        contact_res = self.contact_finder.run(contact_prompt)
        
        raw_contacts = extract_and_parse_json(contact_res.content)
        if isinstance(raw_contacts, dict):
            raw_contacts = raw_contacts.get("contacts", list(raw_contacts.values())[0] if raw_contacts else [])
            
        contacts: List[ContactInfo] = []
        if isinstance(raw_contacts, list):
            for item in raw_contacts:
                if isinstance(item, dict):
                    try:
                        contacts.append(ContactInfo(**item))
                    except Exception:
                        pass
                        
        print(f"Found {len(contacts)} contacts.")

        # -------------------------------------------------------------
        # STEP 3: Company Research & Triggers
        # -------------------------------------------------------------
        print("Step 3: Conducting deep research and identifying triggers...")
        research_prompt = (
            f"Perform research and find recent news or product updates for these companies: {company_summaries}. "
            "Return as a valid JSON array with keys: company_name, triggers (list of strings), summary."
        )
        research_res = self.company_researcher.run(research_prompt)
        
        raw_research = extract_and_parse_json(research_res.content)
        if isinstance(raw_research, dict):
            raw_research = raw_research.get("research", list(raw_research.values())[0] if raw_research else [])
            
        research_list: List[CompanyResearch] = []
        if isinstance(raw_research, list):
            for item in raw_research:
                if isinstance(item, dict):
                    try:
                        research_list.append(CompanyResearch(**item))
                    except Exception:
                        pass
                        
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
            "cold emails. Return as a valid JSON array with keys: company_name, recipient_name, recipient_title, subject_line, email_body."
        )
        email_res = self.email_creator.run(email_prompt)
        
        raw_emails = extract_and_parse_json(email_res.content)
        if isinstance(raw_emails, dict):
            raw_emails = raw_emails.get("emails", list(raw_emails.values())[0] if raw_emails else [])
            
        emails: List[OutreachEmail] = []
        if isinstance(raw_emails, list):
            for item in raw_emails:
                if isinstance(item, dict):
                    try:
                        emails.append(OutreachEmail(**item))
                    except Exception:
                        pass
                        
        print(f"Generated {len(emails)} personalized emails.")

        return PipelineResult(
            criteria=config.criteria,
            companies=companies,
            contacts=contacts,
            research=research_list,
            emails=emails,
        )