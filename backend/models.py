

from pydantic import BaseModel, Field
from typing import List, Optional


class OutreachConfig(BaseModel):
    """Configuration input from the user/frontend to start the pipeline."""
    criteria: str = Field(..., description="Target criteria for companies, e.g., 'Series A fintech startups in Lagos'")
    target_role: Optional[str] = Field("CTO or Founder", description="Target decision-maker title to search for")


class CompanyInfo(BaseModel):
    model_config = {"extra": "allow"}  # <--- Clean Pydantic v2 configuration

    name: str = Field(..., description="Company name")
    website: str = Field(..., description="Official website URL")
    description: str = Field(..., description="1-sentence description of the company")
    size: Optional[str] = Field(None, description="Estimated company size or headcount")
    location: Optional[str] = Field(None, description="Headquarters location")


class ContactInfo(BaseModel):
    company_name: str = Field(..., description="Name of the company they work for")
    full_name: str = Field(..., description="Decision-maker's full name")
    title: str = Field(..., description="Job title, e.g., CTO, Founder")
    background_context: Optional[str] = Field(None, description="Relevant professional history or context")


class CompanyResearch(BaseModel):
    company_name: str = Field(..., description="Name of the company")
    triggers: List[str] = Field(..., description="Recent news, product updates, or funding triggers found")
    summary: str = Field(..., description="Actionable 2-3 sentence intelligence summary")


class OutreachEmail(BaseModel):
    company_name: str = Field(..., description="Target company name")
    recipient_name: str = Field(..., description="Recipient's name")
    recipient_title: str = Field(..., description="Recipient's title")
    subject_line: str = Field(..., description="Personalized email subject line")
    email_body: str = Field(..., description="The hyper-personalized cold email text")


class PipelineResult(BaseModel):
    """Final unified response returned to the frontend dashboard."""
    criteria: str
    companies: List[CompanyInfo]
    contacts: List[ContactInfo]
    research: List[CompanyResearch]
    emails: List[OutreachEmail]