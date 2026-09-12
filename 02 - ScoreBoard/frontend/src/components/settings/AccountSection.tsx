"use client";

import { useState } from "react";
import { CircleUserRound } from "lucide-react";
import { signIn, signOut, signUp, useAuthUser } from "@/lib/auth/auth-store";

export function AccountSection() {
  const user = useAuthUser();
  const [mode, setMode] = useState<"signin" | "signup">("signin");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [formError, setFormError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !password) {
      setFormError("Enter an email and password.");
      return;
    }
    setFormError(null);
    setSubmitting(true);
    try {
      await (mode === "signin" ? signIn(email, password) : signUp(email, password));
      setPassword("");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="rounded-xl border border-border bg-surface p-5">
      <h2 className="mb-1 text-sm font-semibold text-fg">Account</h2>
      <p className="mb-4 text-xs text-fg-muted">
        Optional — you can use Scoreboard fully without an account. Followed teams are saved on this
        device either way.
      </p>

      {user ? (
        <div className="flex items-center justify-between gap-3">
          <div className="flex items-center gap-2.5">
            <span className="flex h-9 w-9 items-center justify-center rounded-full bg-accent-soft text-accent">
              <CircleUserRound size={18} />
            </span>
            <div>
              <p className="text-sm font-medium text-fg">{user.email}</p>
              <p className="text-xs text-fg-muted">Signed in on this device</p>
            </div>
          </div>
          <button
            onClick={signOut}
            className="rounded-md border border-border-strong px-3 py-1.5 text-sm font-medium text-fg transition-colors hover:bg-surface-2"
          >
            Sign out
          </button>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="flex flex-col gap-3">
          <div className="flex gap-4 text-sm">
            <button
              type="button"
              onClick={() => setMode("signin")}
              className={`font-medium ${mode === "signin" ? "text-fg" : "text-fg-muted"}`}
            >
              Sign in
            </button>
            <button
              type="button"
              onClick={() => setMode("signup")}
              className={`font-medium ${mode === "signup" ? "text-fg" : "text-fg-muted"}`}
            >
              Create account
            </button>
          </div>
          <input
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Email"
            className="rounded-lg border border-border bg-surface-2 px-3 py-2 text-sm text-fg placeholder:text-fg-faint focus:border-border-strong focus:outline-none"
          />
          <input
            type="password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
            className="rounded-lg border border-border bg-surface-2 px-3 py-2 text-sm text-fg placeholder:text-fg-faint focus:border-border-strong focus:outline-none"
          />
          {formError ? <p className="text-xs text-danger">{formError}</p> : null}
          <button
            type="submit"
            disabled={submitting}
            className="self-start rounded-md bg-accent px-4 py-1.5 text-sm font-semibold text-bg transition-opacity hover:opacity-90 disabled:opacity-50"
          >
            {submitting ? "Please wait…" : mode === "signin" ? "Sign in" : "Create account"}
          </button>
        </form>
      )}
    </div>
  );
}
