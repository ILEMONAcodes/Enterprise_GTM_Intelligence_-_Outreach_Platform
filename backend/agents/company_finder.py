
from __future__ import annotations
import os
from typing import List
from pydantic import BaseModel, Field
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.exa import ExaTools
from backend.models import CompanyInfo

# Container model so the LLM outputs a clean JSON object containing the list
class CompanyFinderResponse(BaseModel):
    companies: List[CompanyInfo] = Field(..., description="List of discovered target companies")

def build_company_finder() -> Agent:
    model = OpenAIChat(
        id="openrouter/free",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
    )

    return Agent(
        name="Company Finder",
        model=model,
        tools=[ExaTools(api_key=os.getenv("EXA_API_KEY"))],

        instructions=[
            "Given a target criteria, use web search to find matching companies.",
            "Extract the company name, website, a 1-sentence description, size, and location.",
            "Return the data strictly structured according to the response model.",
        ],
    )