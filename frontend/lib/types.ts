export type OutreachConfig = {
  company_name: string;
  industry: string;
  target_role: string;
  geography: string;
  tone: string;
  max_contacts: number;
};

export type CompanyInfo = {
  name: string;
  website?: string | null;
  industry?: string | null;
  description?: string | null;
  location?: string | null;
  funding?: string | null;
  employees?: string | null;
};

export type ContactInfo = {
  name: string;
  title: string;
  email?: string | null;
  linkedin?: string | null;
  company?: string | null;
};

export type CampaignRequest = {
  config: OutreachConfig;
};

export type CampaignResult = {
  company: CompanyInfo;
  contacts: ContactInfo[];
  email_subject: string;
  email_body: string;
  summary: string;
  status: string;
};
