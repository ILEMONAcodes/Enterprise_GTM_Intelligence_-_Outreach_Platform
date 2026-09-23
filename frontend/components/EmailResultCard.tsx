import { CampaignResult } from "@/lib/types";

export function EmailResultCard({ result }: { result: CampaignResult }) {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
      <h3 className="text-lg font-semibold text-slate-900">{result.company.name}</h3>
      <p className="mt-2 text-sm text-slate-600">{result.summary}</p>
      <div className="mt-4 rounded-lg bg-slate-50 p-4 text-sm text-slate-700">
        <div className="font-medium text-slate-900">Subject</div>
        <div>{result.email_subject}</div>
      </div>
      <div className="mt-4 whitespace-pre-line text-sm text-slate-700">{result.email_body}</div>
    </div>
  );
}
