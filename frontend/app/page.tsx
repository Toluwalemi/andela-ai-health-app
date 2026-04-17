import { SignedIn, SignedOut, SignInButton, UserButton } from "@clerk/nextjs";
import Link from "next/link";

export default function HomePage() {
  return (
    <main style={{ padding: 32, maxWidth: 720 }}>
      <h1>Health App</h1>
      <p>Consultation notes assistant powered by an LLM.</p>

      <SignedOut>
        <SignInButton mode="modal" />
      </SignedOut>

      <SignedIn>
        <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
          <UserButton />
          <Link href="/consult">Open consultation assistant →</Link>
        </div>
      </SignedIn>
    </main>
  );
}
