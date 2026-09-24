export type OutreachConfig = {
  criteria: string;
  target_role: string;
};

export type CompanyInfo = {
  name: string;
  website: string;
  description: string;
  size?: string | null;
  location?: string | null;
  [key: string]: unknown;
};

export type ContactInfo = {
  company_name: string;
  full_name: string;
  title: string;
  background_context?: string | null;
};

export type CompanyResearch = {
  company_name: string;
  triggers: string[];
  summary: string;
};

export type OutreachEmail = {
  company_name: string;
  recipient_name: string;
  recipient_title: string;
  subject_line: string;
  email_body: string;
};

export type PipelineResult = {
  criteria: string;
  companies: CompanyInfo[];
  contacts: ContactInfo[];
  research: CompanyResearch[];
  emails: OutreachEmail[];
};

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export async function runPipeline(payload: OutreachConfig): Promise<PipelineResult> {
  const response = await fetch(`${API_URL}/api/run-pipeline`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    let detail = `Pipeline request failed (${response.status})`;
    try {
      const error = (await response.json()) as { detail?: string };
      detail = error.detail ?? detail;
    } catch {
      // Keep the HTTP status when the backend did not return JSON.
    }
    throw new Error(detail);
  }

  return response.json() as Promise<PipelineResult>;
}
