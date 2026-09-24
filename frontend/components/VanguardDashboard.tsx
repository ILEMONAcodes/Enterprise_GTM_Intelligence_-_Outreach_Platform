"use client";

import { FormEvent, useMemo, useState } from "react";
import {
  Activity,
  ArrowUpRight,
  BarChart3,
  Bell,
  BriefcaseBusiness,
  Building2,
  Check,
  ChevronDown,
  ChevronRight,
  CircleHelp,
  Clipboard,
  FileText,
  Globe2,
  Layers3,
  LayoutDashboard,
  Menu,
  Network,
  Search,
  Send,
  Settings,
  SlidersHorizontal,
  Sparkles,
  Target,
  TrendingUp,
  Users,
  X,
  Zap,
} from "lucide-react";
import {
  CompanyInfo,
  CompanyResearch,
  ContactInfo,
  OutreachEmail,
  PipelineResult,
  runPipeline,
} from "@/lib/backendService";

type Icon = typeof LayoutDashboard;

type View = "dashboard" | "accounts" | "signals" | "campaigns" | "settings";

const navigation: { id: View; label: string; icon: Icon }[] = [
  { id: "dashboard", label: "Dashboard", icon: LayoutDashboard },
  { id: "accounts", label: "Target accounts", icon: Target },
  { id: "signals", label: "Research signals", icon: Activity },
  { id: "campaigns", label: "Outreach campaigns", icon: Send },
];

export function VanguardDashboard() {
  const [activeNav, setActiveNav] = useState<View>("dashboard");
  const [isSidebarOpen, setSidebarOpen] = useState(false);
  const [criteria, setCriteria] = useState("B2B SaaS companies scaling their revenue team");
  const [targetRole, setTargetRole] = useState("VP of Revenue or Founder");
  const [isSearching, setSearching] = useState(false);
  const [result, setResult] = useState<PipelineResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [copiedEmail, setCopiedEmail] = useState<string | null>(null);
  const [selectedCompany, setSelectedCompany] = useState<CompanyInfo | null>(null);

  const contactsByCompany = useMemo(() => indexByCompany(result?.contacts ?? [], "company_name"), [result]);
  const researchByCompany = useMemo(() => indexByCompany(result?.research ?? [], "company_name"), [result]);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!criteria.trim() || isSearching) return;
    setSearching(true);
    setError(null);
    try {
      const nextResult = await runPipeline({ criteria: criteria.trim(), target_role: targetRole.trim() });
      setResult(nextResult);
      setSelectedCompany(nextResult.companies[0] ?? null);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Unable to run the discovery pipeline.");
    } finally {
      setSearching(false);
    }
  }

  async function copyEmail(email: OutreachEmail) {
    const content = `Subject: ${email.subject_line}\n\n${email.email_body}`;
    try {
      await navigator.clipboard.writeText(content);
      setCopiedEmail(email.company_name);
      window.setTimeout(() => setCopiedEmail(null), 1800);
    } catch {
      setError("Clipboard access is unavailable. Select the email text and copy it manually.");
    }
  }

  function changeView(view: View) {
    setActiveNav(view);
    setSidebarOpen(false);
  }

  const activeLabel = navigation.find((item) => item.id === activeNav)?.label ?? "Settings";

  return (
    <div className="app-shell">
      <aside className={`sidebar ${isSidebarOpen ? "sidebar-open" : ""}`}>
        <div className="brand-row">
          <div className="brand-mark">V</div>
          <span className="brand-name">vanguard<span>.</span></span>
          <button className="icon-button mobile-close" onClick={() => setSidebarOpen(false)} aria-label="Close navigation"><X size={18} /></button>
        </div>
        <div className="workspace-switcher"><span className="workspace-dot" /> Acme Corporation <ChevronDown size={14} /></div>
        <nav className="main-nav" aria-label="Main navigation">
          <p className="nav-caption">Workspace</p>
          {navigation.map(({ id, label, icon: NavIcon }) => (
            <button key={id} className={`nav-item ${activeNav === id ? "nav-active" : ""}`} onClick={() => changeView(id)}>
              <NavIcon size={17} strokeWidth={1.8} /><span>{label}</span>{id === "accounts" && result && <small>{result.companies.length}</small>}{id === "signals" && result && <small>{result.research.length}</small>}
            </button>
          ))}
          <p className="nav-caption nav-caption-lower">Manage</p>
          <button className={`nav-item ${activeNav === "settings" ? "nav-active" : ""}`} onClick={() => changeView("settings")}><Settings size={17} strokeWidth={1.8} /><span>Settings</span></button>
        </nav>
        <div className="sidebar-bottom">
          <div className="usage-label"><span>Monthly enrichment</span><strong>68%</strong></div>
          <div className="usage-track"><span /></div>
          <p className="usage-copy">6,820 of 10,000 credits used</p>
          <div className="user-row"><div className="avatar avatar-dark">JD</div><div><strong>Jordan Davis</strong><span>Admin</span></div><ChevronRight size={15} /></div>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <button className="icon-button menu-trigger" onClick={() => setSidebarOpen(true)} aria-label="Open navigation"><Menu size={20} /></button>
          <div className="breadcrumb"><span>Workspace</span><ChevronRight size={14} /><strong>{activeLabel}</strong></div>
          <div className="topbar-actions"><button className="icon-button" aria-label="Search"><Search size={18} /></button><button className="icon-button notification-button" aria-label="Notifications"><Bell size={18} /><i /></button><div className="avatar avatar-green">JD</div></div>
        </header>

        <div className="dashboard-wrap">
          {activeNav !== "dashboard" && <ViewHeader activeNav={activeNav} result={result} />}
          {activeNav === "settings" ? <SettingsView apiUrl={process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"} /> : activeNav === "accounts" ? <AccountsView companies={result?.companies ?? []} contactsByCompany={contactsByCompany} selectedCompany={selectedCompany} setSelectedCompany={setSelectedCompany} /> : activeNav === "signals" ? <SignalsView research={result?.research ?? []} /> : activeNav === "campaigns" ? <CampaignsView emails={result?.emails ?? []} copiedEmail={copiedEmail} copyEmail={copyEmail} /> : <>
          <section className="welcome-row"><div><p className="eyebrow">Thursday, September 24, 2026</p><h1>Good morning, Jordan<span>.</span></h1><p className="welcome-copy">Here is what is moving across your go-to-market universe.</p></div><button className="outline-button"><CircleHelp size={16} /> Help center</button></section>

          <section className="discovery-panel">
            <div className="discovery-heading"><div className="spark-icon"><Zap size={18} fill="currentColor" /></div><div><h2>Discover your next best accounts</h2><p>Tell Vanguard what you are looking for. We will find the signal.</p></div></div>
            <form onSubmit={handleSubmit} className="discovery-form"><div className="input-shell"><Search size={18} /><input value={criteria} onChange={(event) => setCriteria(event.target.value)} aria-label="Account discovery criteria" /><button type="button" className="input-filter" aria-label="Add filter"><SlidersHorizontal size={16} /></button></div><div className="input-shell target-role-shell"><Users size={17} /><input value={targetRole} onChange={(event) => setTargetRole(event.target.value)} aria-label="Target decision maker role" /></div><button className="primary-button" disabled={isSearching}>{isSearching ? <><span className="button-spinner" /> Finding accounts</> : <><Sparkles size={16} /> Run discovery</>}</button></form>
            <div className="suggestions"><span>Try a template:</span><button onClick={() => setCriteria("Fintech companies hiring VP-level sales leaders")}>Fintech hiring leaders</button><button onClick={() => setCriteria("Series B SaaS companies in North America")}>Series B SaaS in North America</button><button onClick={() => setCriteria("Healthcare companies expanding into enterprise")}>Healthcare expansion</button></div>
          </section>

          {error && <div className="search-error"><X size={15} /> {error}</div>}
          {result && !error && <div className="search-success"><Check size={15} /> Discovery complete. {result.companies.length} accounts matched your criteria.</div>}

          <section className="metric-grid">
            <Metric icon={Building2} label="Accounts discovered" value={String(result?.companies.length ?? 0)} change={result ? "Live" : "—"} detail="from pipeline" />
            <Metric icon={Activity} label="Active research triggers" value={String(result?.research.length ?? 0).padStart(2, "0")} change={result ? "Live" : "—"} detail="from research" />
            <Metric icon={Send} label="Emails generated" value={String(result?.emails.length ?? 0)} change={result ? "Live" : "—"} detail="from pipeline" />
            <Metric icon={BarChart3} label="Contacts found" value={String(result?.contacts.length ?? 0)} change={result ? "Live" : "—"} detail="decision makers" />
          </section>

          <div className="content-grid">
            <section className="section-block accounts-block"><div className="section-heading"><div><p className="eyebrow">Your pipeline</p><h2>Top target accounts</h2></div><button className="text-button" onClick={() => changeView("accounts")}>View all accounts <ArrowUpRight size={15} /></button></div><div className="company-grid">{(result?.companies ?? []).slice(0, 4).map((company) => <CompanyCard key={company.name} company={company} contact={contactsByCompany[company.name]?.[0]} research={researchByCompany[company.name]?.[0]} selected={selectedCompany?.name === company.name} onSelect={() => setSelectedCompany(company)} />)}{!result && <EmptyState text="Run discovery to populate your target accounts." />}</div></section>
            <SignalsView research={(result?.research ?? []).slice(0, 4)} compact />
          </div>

          <CampaignsView emails={(result?.emails ?? []).slice(0, 1)} copiedEmail={copiedEmail} copyEmail={copyEmail} compact />
          <footer className="footer"><span>Vanguard Intelligence Platform</span><span>Data refreshed 2 min ago <span className="live-dot" /></span></footer>
          </>}
        </div>
      </main>
    </div>
  );
}

function Metric({ icon: MetricIcon, label, value, change, detail }: { icon: Icon; label: string; value: string; change: string; detail: string }) {
  return <div className="metric-card"><div className="metric-icon"><MetricIcon size={18} /></div><div className="metric-label">{label}</div><div className="metric-value">{value}</div><div className="metric-change"><TrendingUp size={13} /> {change} <span>{detail}</span></div></div>;
}

function CompanyCard({ company, contact, research, selected, onSelect }: { company: CompanyInfo; contact?: ContactInfo; research?: CompanyResearch; selected: boolean; onSelect: () => void }) {
  const initials = company.name.split(/\s+/).map((part) => part[0]).join("").slice(0, 2);
  const trigger = research?.triggers[0] ?? "No trigger recorded";
  return <button className={`company-card ${selected ? "company-selected" : ""}`} onClick={onSelect}><div className="company-card-head"><div className="company-brand"><div className="company-logo" style={{ background: colorFor(company.name) }}>{initials}</div><div><strong>{company.name}</strong><span>{company.website}</span></div></div><span className="score-ring">{contact ? "ICP" : "—"}</span></div><div className="company-category"><BriefcaseBusiness size={13} /> {company.description}</div><div className="company-details"><span><Users size={13} /> {company.size ?? "Size n/a"}</span><span><Zap size={13} /> {trigger}</span></div><div className="company-card-footer"><div className="contact-mini"><div className="avatar avatar-tan">{contact ? contact.full_name.split(" ").map((part) => part[0]).join("") : "—"}</div><span><strong>{contact?.full_name ?? "No contact found"}</strong><small>{contact?.title ?? "Awaiting enrichment"}</small></span></div><Network size={15} className="linkedin-icon" /></div></button>;
}

function indexByCompany<T extends { [key: string]: unknown }>(items: T[], key: string) {
  return items.reduce<Record<string, T[]>>((groups, item) => {
    const company = String(item[key] ?? "");
    if (company) groups[company] = [...(groups[company] ?? []), item];
    return groups;
  }, {});
}

function colorFor(value: string) {
  const colors = ["#315c9a", "#d06d4c", "#b78330", "#31594b", "#7558a6"];
  return colors[value.length % colors.length];
}

function ViewHeader({ activeNav, result }: { activeNav: View; result: PipelineResult | null }) {
  const titles: Record<View, [string, string]> = {
    dashboard: ["Dashboard", "Your GTM intelligence at a glance."],
    accounts: ["Target accounts", "Every account discovered by your latest pipeline run."],
    signals: ["Research signals", "Recent triggers and context from your target market."],
    campaigns: ["Outreach campaigns", "Review and copy personalized drafts generated for your contacts."],
    settings: ["Settings", "Manage the connection between Vanguard and your workspace."],
  };
  return <section className="welcome-row page-view-header"><div><p className="eyebrow">{result ? `${result.companies.length} accounts in current run` : "No pipeline run yet"}</p><h1>{titles[activeNav][0]}<span>.</span></h1><p className="welcome-copy">{titles[activeNav][1]}</p></div></section>;
}

function AccountsView({ companies, contactsByCompany, selectedCompany, setSelectedCompany }: { companies: CompanyInfo[]; contactsByCompany: Record<string, ContactInfo[]>; selectedCompany: CompanyInfo | null; setSelectedCompany: (company: CompanyInfo) => void }) {
  return <section className="section-block full-view-block"><div className="section-heading"><div><p className="eyebrow">Live pipeline data</p><h2>{companies.length} target accounts</h2></div><button className="outline-button"><SlidersHorizontal size={15} /> Filter accounts</button></div><div className="company-grid">{companies.map((company) => <CompanyCard key={company.name} company={company} contact={contactsByCompany[company.name]?.[0]} selected={selectedCompany?.name === company.name} onSelect={() => setSelectedCompany(company)} />)}{!companies.length && <EmptyState text="Run discovery from the Dashboard to find target accounts." />}</div></section>;
}

function SignalsView({ research, compact = false }: { research: CompanyResearch[]; compact?: boolean }) {
  return <section className={`section-block signals-block ${compact ? "signals-compact" : "full-view-block"}`}><div className="section-heading"><div><p className="eyebrow">Live intelligence</p><h2>Research signals <span className="live-dot" /></h2></div>{!compact && <button className="icon-button" aria-label="Signal settings"><SlidersHorizontal size={17} /></button>}</div><div className="signal-list">{research.map((item, index) => <div className="signal-row" key={`${item.company_name}-${index}`}><div className={`signal-icon signal-${["green", "blue", "amber", "purple"][index % 4]}`}><Activity size={16} /></div><div className="signal-copy"><p><strong>{item.company_name}</strong> {item.triggers.join(" · ")}</p><span>{item.summary}</span></div></div>)}{!research.length && <EmptyState text="Research signals will appear after a discovery run." />}</div>{compact && <button className="view-feed">Open signal feed <ChevronRight size={15} /></button>}</section>;
}

function CampaignsView({ emails, copiedEmail, copyEmail, compact = false }: { emails: OutreachEmail[]; copiedEmail: string | null; copyEmail: (email: OutreachEmail) => void; compact?: boolean }) {
  const visibleEmails = compact ? emails.slice(0, 1) : emails;
  return <section className={`outreach-section ${compact ? "" : "full-view-block"}`}><div className="section-heading"><div><p className="eyebrow">Ready to personalize</p><h2>Generated outreach</h2></div>{compact && <span className="text-button">{emails.length} drafts ready <ArrowUpRight size={15} /></span>}</div><div className="outreach-grid">{visibleEmails.map((item) => <div className="email-card" key={`${item.company_name}-${item.recipient_name}`}><div className="email-card-top"><div className="recipient"><div className="avatar avatar-purple">{item.recipient_name.split(" ").map((part) => part[0]).join("")}</div><div><strong>{item.recipient_name}</strong><span>{item.recipient_title} · {item.company_name}</span></div></div><span className="status-pill"><span /> Draft ready</span></div><div className="email-meta"><span>Subject</span><strong>{item.subject_line}</strong></div><p className="email-preview">{item.email_body}</p><div className="email-actions"><button className="secondary-button" onClick={() => copyEmail(item)}>{copiedEmail === item.company_name ? <Check size={15} /> : <Clipboard size={15} />} {copiedEmail === item.company_name ? "Copied" : "Copy email"}</button><button className="primary-button small-button"><Send size={15} /> Review & send</button></div></div>)}{!visibleEmails.length && <EmptyState text="Generated outreach will appear after the pipeline finds contacts." />}</div></section>;
}

function SettingsView({ apiUrl }: { apiUrl: string }) {
  return <section className="settings-view"><div className="settings-card"><div className="mini-icon"><Network size={17} /></div><div><h2>Backend connection</h2><p>Vanguard sends discovery requests to the configured FastAPI service.</p></div><span className="status-pill"><span /> Configured</span></div><div className="settings-field"><label htmlFor="api-url">API base URL</label><input id="api-url" value={apiUrl} readOnly /></div><p className="settings-note">Set <code>NEXT_PUBLIC_API_URL</code> in the frontend environment to change this URL.</p></section>;
}

function EmptyState({ text }: { text: string }) {
  return <div className="empty-state"><Layers3 size={18} /><span>{text}</span></div>;
}