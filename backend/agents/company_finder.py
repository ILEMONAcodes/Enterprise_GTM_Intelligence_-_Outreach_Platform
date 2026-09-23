import os
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.exa import ExaTools


def build_company_finder() -> Agent:
    model = OpenAIChat(
        id="nvidia/nemotron-3-ultra-550b-a55b:free",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
    )

    return Agent(
        name="Company Finder",
        model=model,
        tools=[ExaTools(api_key=os.getenv("EXA_API_KEY"))],
        instructions=[
            "You find real companies matching the given criteria using web search.",
            "For each company, return: name, website URL, a 1-sentence description, "
            "estimated size, and location.",
            "Only include companies you found evidence for via search — never invent one.",
        ],
    )