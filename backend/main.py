# backend/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from backend.workflow import OutreachWorkflow
from backend.models import OutreachConfig, PipelineResult

load_dotenv()

app = FastAPI(
    title="GTM Agent API",
    description="Multi-agent GTM outreach and research pipeline backend",
    version="1.0.0"
)

# Enable CORS so your frontend application can talk to this server smoothly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the workflow engine globally
workflow = OutreachWorkflow()

@app.get("/")
def health_check():
    return {"status": "healthy", "service": "GTM Agent Pipeline API"}

@app.post("/api/run-pipeline", response_model=PipelineResult)
def run_outreach_pipeline(config: OutreachConfig):
    """
    Triggers the 4-agent GTM pipeline using strict Pydantic validation.
    """
    try:
        result = workflow.run(config)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))