"use client";

import { useAuth, UserButton } from "@clerk/nextjs";
import { useState } from "react";

type Result = {
  summary: string;
  next_steps: string[];
  patient_email: string;
};

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "";

export default function ConsultPage() {
  const { getToken } = useAuth();
  const [notes, setNotes] = useState("");
  const [result, setResult] = useState<Result | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const submit = async () => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const token = await getToken();
      const response = await fetch(`${API_URL}/api/consultations`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ notes }),
      });
      if (!response.ok) {
        throw new Error(`Request failed (${response.status})`);
      }
      setResult((await response.json()) as Result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main style={{ padding: 32, maxWidth: 720 }}>
      <header
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <h1>Consultation assistant</h1>
        <UserButton />
      </header>

      <textarea
        value={notes}
        onChange={(event) => setNotes(event.target.value)}
        rows={10}
        placeholder="Paste raw consultation notes here..."
        style={{
          width: "100%",
          padding: 12,
          fontFamily: "inherit",
          fontSize: 14,
          boxSizing: "border-box",
        }}
      />

      <button
        type="button"
        onClick={submit}
        disabled={loading || notes.trim().length < 10}
        style={{ marginTop: 12, padding: "8px 16px" }}
      >
        {loading ? "Summarising…" : "Summarise"}
      </button>

      {error && <p style={{ color: "crimson" }}>{error}</p>}

      {result && (
        <section style={{ marginTop: 32, display: "grid", gap: 16 }}>
          <div>
            <h2>Summary</h2>
            <p>{result.summary}</p>
          </div>
          <div>
            <h2>Next steps</h2>
            <ul style={{ margin: 0, paddingLeft: 20 }}>
              {result.next_steps.map((step, i) => (
                <li key={i}>{step}</li>
              ))}
            </ul>
          </div>
          <div>
            <h2>Patient email</h2>
            <pre style={{ whiteSpace: "pre-wrap", margin: 0 }}>
              {result.patient_email}
            </pre>
          </div>
        </section>
      )}
    </main>
  );
}
