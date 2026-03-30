import type { ReactNode } from "react";

/** Constrained reading column — no horizontal scroll on main column (FR-003). */
export function Prose({ children }: { children: ReactNode }) {
  return (
    <main className="mx-auto w-full max-w-3xl px-4 py-10 sm:px-6">
      <div className="space-y-4 text-base leading-relaxed text-slate-800 [&_a]:font-medium [&_a]:text-blue-800 [&_a]:underline [&_a]:underline-offset-2 [&_h1]:text-3xl [&_h1]:font-semibold [&_h1]:tracking-tight [&_h1]:text-slate-900 [&_h2]:mt-8 [&_h2]:text-xl [&_h2]:font-semibold [&_h2]:text-slate-900 [&_ul]:list-disc [&_ul]:pl-6 [&_li]:marker:text-slate-400">
        {children}
      </div>
    </main>
  );
}
