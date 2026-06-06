"use client";

import { useEffect, useState, type ReactNode } from "react";
import { usePathname, useRouter } from "next/navigation";
import Link from "next/link";
import { clearSession, getRole, getUsername, isLoggedIn } from "@/lib/auth";

const NAV = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/users", label: "Users" },
  { href: "/artists", label: "Catalog" },
  { href: "/news", label: "News" },
  { href: "/audit", label: "Audit log" },
];

export default function AdminLayout({ children }: { children: ReactNode }) {
  const router = useRouter();
  const pathname = usePathname();
  const [ready, setReady] = useState(false);
  const [role, setRole] = useState<string | null>(null);
  const [username, setUsername] = useState<string | null>(null);

  useEffect(() => {
    if (!isLoggedIn()) {
      router.replace("/login");
      return;
    }
    setRole(getRole());
    setUsername(getUsername());
    setReady(true);
  }, [router]);

  function logout() {
    clearSession();
    router.replace("/login");
  }

  // Avoid flashing protected content before the session check resolves.
  if (!ready) return null;

  return (
    <div className="shell">
      <aside className="sidebar">
        <div className="brand">Reviews Admin</div>
        <nav data-cy="sidebar">
          {NAV.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              data-cy={`nav-${item.label.toLowerCase().split(" ")[0]}`}
              className={pathname === item.href ? "active" : ""}
            >
              {item.label}
            </Link>
          ))}
        </nav>
        <div className="spacer" />
        <div className="muted" style={{ fontSize: "0.8rem", marginBottom: "0.5rem" }}>
          <div data-cy="session-username">{username}</div>
          <span className="badge role" data-cy="session-role">
            {role}
          </span>
        </div>
        <button className="secondary" data-cy="logout" onClick={logout}>
          Log out
        </button>
      </aside>
      <main className="content">{children}</main>
    </div>
  );
}
