"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import type { NavigationConfig } from "@/types/navigation";

type Props = { navigation: NavigationConfig };

export function SiteHeader({ navigation }: Props) {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);
  const sorted = [...navigation.header].sort((a, b) => a.order - b.order);

  return (
    <header className="sticky top-0 z-50 border-b border-slate-200 bg-white/95 backdrop-blur">
      <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-4 py-3">
        <Link
          href="/"
          className="text-lg font-semibold tracking-tight text-slate-900"
        >
          Sharma Law
        </Link>
        <nav className="hidden md:block" aria-label="Primary">
          <ul className="flex flex-wrap items-center gap-1 lg:gap-2">
            {sorted.map((item) => {
              const active =
                item.href === "/"
                  ? pathname === "/"
                  : pathname.startsWith(item.href);
              return (
                <li key={item.id}>
                  <Link
                    href={item.href}
                    className={`rounded-md px-2 py-2 text-sm font-medium transition-colors lg:px-3 ${
                      active
                        ? "bg-slate-100 text-slate-900"
                        : "text-slate-700 hover:bg-slate-50 hover:text-slate-900"
                    }`}
                  >
                    {item.label}
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>
        <button
          type="button"
          className="inline-flex items-center justify-center rounded-md border border-slate-300 p-2 text-slate-800 md:hidden"
          aria-expanded={open}
          aria-controls="mobile-nav"
          onClick={() => setOpen((v) => !v)}
        >
          <span className="sr-only">Open menu</span>
          <span aria-hidden className="text-lg leading-none">
            {open ? "✕" : "☰"}
          </span>
        </button>
      </div>
      {open ? (
        <nav
          id="mobile-nav"
          className="border-t border-slate-200 bg-white md:hidden"
          aria-label="Mobile primary"
        >
          <ul className="flex flex-col px-4 py-2">
            {sorted.map((item) => (
              <li key={item.id}>
                <Link
                  href={item.href}
                  className="block rounded-md py-3 text-base font-medium text-slate-800 hover:bg-slate-50"
                  onClick={() => setOpen(false)}
                >
                  {item.label}
                </Link>
              </li>
            ))}
          </ul>
        </nav>
      ) : null}
    </header>
  );
}
