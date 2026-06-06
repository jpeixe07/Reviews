"use client";

import Link from "next/link";

const CARDS = [
  { href: "/users", title: "Users", desc: "Create, edit, ban and delete accounts." },
  { href: "/artists", title: "Catalog", desc: "Register and search artists, authors and voice actors." },
  { href: "/news", title: "News", desc: "Publish tagged news to the public feed." },
  { href: "/audit", title: "Audit log", desc: "Review every administrative mutation." },
  { href: "/feed", title: "Public feed", desc: "See what visitors see (no auth)." },
];

export default function DashboardPage() {
  return (
    <div data-cy="dashboard">
      <h1>Dashboard</h1>
      <p className="muted">Keep the catalog, community and editorial content organised.</p>
      <div className="grid" style={{ marginTop: "1.2rem" }}>
        {CARDS.map((c) => (
          <Link key={c.href} href={c.href} className="card" data-cy={`card-${c.title.toLowerCase().split(" ")[0]}`}>
            <h3>{c.title}</h3>
            <p className="muted">{c.desc}</p>
          </Link>
        ))}
      </div>
    </div>
  );
}
