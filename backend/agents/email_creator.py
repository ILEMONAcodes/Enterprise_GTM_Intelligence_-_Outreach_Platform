
from __future__ import annotations
import os
from typing import List
from pydantic import BaseModel, Field
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from backend.models import OutreachEmail

class EmailCreatorResponse(BaseModel):
    emails: List[OutreachEmail] = Field(..., description="Hyper-personalized cold outreach email drafts")

def build_email_creator() -> Agent:
    model = OpenAIChat(
        id="openrouter/free",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
    )

    return Agent(
        name="Email Creator",
        model=model,

        instructions=[
            "Using the provided company details, contact information, and research triggers, draft hyper-personalized cold outreach emails.",
            "Ensure each email references a specific research trigger, avoids corporate buzzwords, stays under 120 words, and ends with a low-friction CTA.",
            "Return the data strictly structured according to the response model.",
        ],
    )