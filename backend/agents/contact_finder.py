
from __future__ import annotations
import os
from typing import List
from pydantic import BaseModel, Field
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.exa import ExaTools
from backend.models import ContactInfo

class ContactFinderResponse(BaseModel):
    contacts: List[ContactInfo] = Field(..., description="List of key decision-makers found for the target companies")

def build_contact_finder() -> Agent:
    model = OpenAIChat(
        id="openrouter/free",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
    )

    return Agent(
        name="Contact Finder",
        model=model,
        tools=[ExaTools(api_key=os.getenv("EXA_API_KEY"))],

        instructions=[
            "Given target companies and a target role, use web search to find real decision-makers.",
            "Extract their company name, full name, job title, and any relevant background context.",
            "Return the data strictly structured according to the response model.",
        ],
    )