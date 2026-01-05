// app/page.tsx
"use client";

import { useEffect, useState } from "react";

export default function Page() {
  const apiBase = process.env.NEXT_PUBLIC_API_BASE_URL;

  const [health, setHealth] = useState<any>(null);
  const [excelPing, setExcelPing] = useState<any>(null);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    if (!apiBase) {
      setErr("NEXT_PUBLIC_API_BASE_URL is not set");
      return;
    }

    (async () => {
      try {
        const h = await fetch(`${apiBase}/health`, { cache: "no-store" });
        setHealth(await h.json());

        const p = await fetch(`${apiBase}/excel/ping`, { cache: "no-store" });
        setExcelPing(await p.json());
      } catch (e: any) {
        setErr(e?.message ?? String(e));
      }
    })();
  }, [apiBase]);

  return (
    <main style={{ fontFamily: "system-ui", padding: 24 }}>
      <h1>KCW CRM Admin Dashboard</h1>
      <p>
        API Base: <code>{apiBase ?? "(not set)"}</code>
      </p>

      {err && (
        <pre>
          <code>{err}</code>
        </pre>
      )}

      <h2>/health</h2>
      <pre>
        <code>{JSON.stringify(health, null, 2)}</code>
      </pre>

      <h2>/excel/ping</h2>
      <pre>
        <code>{JSON.stringify(excelPing, null, 2)}</code>
      </pre>
    </main>
  );
}
