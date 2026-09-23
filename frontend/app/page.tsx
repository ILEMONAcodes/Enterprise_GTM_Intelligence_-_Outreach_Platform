import { OutreachForm } from "@/components/OutreachForm";

export default function HomePage() {
  return (
    <main className="min-h-screen bg-slate-100 px-6 py-12">
      <div className="mx-auto max-w-5xl">
        <div className="mb-8 text-center">
          <p className="text-xs font-medium uppercase tracking-[0.3em] text-slate-500">GTM Agent</p>
          <h1 className="mt-3 text-4xl font-bold tracking-tight text-slate-900">Generate outbound campaign drafts</h1>
        </div>

        <OutreachForm />
      </div>
    </main>
  );
}
