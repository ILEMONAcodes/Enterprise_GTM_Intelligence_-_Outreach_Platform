# backend/agents/company_researcher.py
from __future__ import annotations
import os
from typing import List
from pydantic import BaseModel, Field
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.exa import ExaTools
from backend.models import CompanyResearch

class CompanyResearchResponse(BaseModel):
    research: List[CompanyResearch] = Field(..., description="Deep research findings and triggers for target companies")

def build_company_researcher() -> Agent:
    model = OpenAIChat(
        id="openrouter/free",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
    )

    return Agent(
        name="Company Researcher",
        model=model,
        tools=[ExaTools(api_key=os.getenv("EXA_API_KEY"))],

        instructions=[
            "Perform deep web research on the given target companies.",
            "Identify recent news, product updates, funding rounds, or hiring spikes as triggers.",
            "Provide an actionable 2-3 sentence intelligence summary for each company.",
            "Return the data strictly structured according to the response model.",
        ],
    )