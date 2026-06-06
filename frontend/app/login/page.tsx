"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { api, ApiError } from "@/lib/api";
import { setSession } from "@/lib/auth";

export default function LoginPage() {
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const res = await api.login(username, password);
      setSession({ token: res.access_token, role: res.role, username: res.username });
      router.replace("/dashboard");
    } catch (err) {
      const msg = err instanceof ApiError ? err.message : "could not reach the server";
      setError(msg);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="centered">
      <div className="card auth-card" data-cy="login-card">
        <h1>Reviews Admin</h1>
        <p className="muted">Sign in to manage users, catalog and news.</p>

        {error && (
          <div className="alert error" data-cy="login-error">
            {error}
          </div>
        )}

        <form onSubmit={onSubmit}>
          <label htmlFor="username">Username or email</label>
          <input
            id="username"
            data-cy="login-username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            autoComplete="username"
          />

          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            data-cy="login-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoComplete="current-password"
          />

          <button type="submit" data-cy="login-submit" disabled={loading}>
            {loading ? "Signing in…" : "Sign in"}
          </button>
        </form>
      </div>
    </div>
  );
}
