from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.models import CampaignRequest, CampaignResult
from backend.workflow import OutreachWorkflow

app = FastAPI(title="GTM Agent API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

workflow = OutreachWorkflow()


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/generate-campaign", response_model=CampaignResult)
async def generate_campaign(request: CampaignRequest) -> CampaignResult:
    return await workflow.run(request)
