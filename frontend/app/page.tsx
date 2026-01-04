"use client";

import { useEffect, useState } from "react";

type Health = {
  status?: string;
  env?: string;
  database_configured?: boolean;
  redis_configured?: boolean;
  missing?: string[];
  detail?: string;
};

export default function Page() {
  const apiBase = process.env.NEXT_PUBLIC_API_BASE_URL;

  const [health, setHealth] = useState<Health | null>(null);
  const [excelPing, setExcelPing] = useState<any>(null);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    if (!apiBase) {
      setErr("NEXT_PUBLIC_API_BASE_URL is not set");
      return;
    }

    (async () => {
      try {
        setErr(null);

        const h = await fetch(`${apiBase}/health`, { cache: "no-store" });
        setHealth(await h.json());

        const p = await fetch(`${apiBase}/excel/ping`, { cache: "no-store" });
        setExcelPing(await p.json());
      } catch (e: any) {
        setErr(e?.message ?? String(e));
      }
    })();
  }, [apiBase]);

  const badge = (ok: boolean | undefined, warn = false) => {
    if (ok === true) return <span className="badge good">OK</span>;
    if (warn) return <span className="badge warn">CHECK</span>;
    return <span className="badge bad">NOT OK</span>;
  };

  return (
    <main className="grid">
      <section className="card">
        <div className="row" style={{ justifyContent: "space-between" }}>
          <div>
            <div style={{ fontWeight: 700 }}>Backend connectivity</div>
            <div style={{ color: "var(--muted)", fontSize: 13, marginTop: 4 }}>
              API Base URL: <code>{apiBase ?? "(not set)"}</code>
            </div>
          </div>
          {badge(Boolean(apiBase), true)}
        </div>

        {err && (
          <pre>
            <code>Error: {err}</code>
          </pre>
        )}
      </section>

      <section className="card">
        <div className="row" style={{ justifyContent: "space-between" }}>
          <div>
            <div style={{ fontWeight: 700 }}>/health</div>
            <div style={{ color: "var(--muted)", fontSize: 13, marginTop: 4 }}>
              Shows if env vars like DATABASE_URL are configured
            </div>
          </div>
          {badge(health?.status === "ok", true)}
        </div>

        <pre>
          <code>{JSON.stringify(health, null, 2)}</code>
        </pre>
      </section>

      <section className="card">
        <div className="row" style={{ justifyContent: "space-between" }}>
          <div>
            <div style={{ fontWeight: 700 }}>/excel/ping</div>
            <div style={{ color: "var(--muted)", fontSize: 13, marginTop: 4 }}>
              Tests database connectivity
            </div>
          </div>
          {badge(excelPing?.ok === true, true)}
        </div>

        <pre>
          <code>{JSON.stringify(excelPing, null, 2)}</code>
        </pre>
      </section>
    </main>
  );
}
