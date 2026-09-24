# backend/test_pipeline.py
import os
from dotenv import load_dotenv
from backend.workflow import OutreachWorkflow
from backend.models import OutreachConfig

load_dotenv()

if __name__ == "__main__":
    workflow = OutreachWorkflow()
    
    # 1. Create your structured configuration payload
    config = OutreachConfig(
        criteria="Series A B2B SaaS startups in San Francisco",
        target_role="VP of Engineering or CTO"
    )
    
    # 2. Run the workflow
    result = workflow.run(config)
    
    print("\n--- FINAL PIPELINE OUTPUT ---")
    print(f"Total Companies Found: {len(result.companies)}")
    print(f"Total Contacts Found: {len(result.contacts)}")
    print(f"Total Research Triggers: {len(result.research)}")
    print(f"Total Emails Generated: {len(result.emails)}\n")
    
    # 3. Print out the generated emails cleanly using dot notation
    for i, email in enumerate(result.emails, 1):
        print(f"--- Email {i}: {email.company_name} ({email.recipient_name}) ---")
        print(f"Subject: {email.subject_line}")
        print(f"Body:\n{email.email_body}\n")