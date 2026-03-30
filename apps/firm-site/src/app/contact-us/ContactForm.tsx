"use client";

import { useActionState } from "react";
import type { ContactState } from "./actions";
import { submitContact } from "./actions";

const initial: ContactState = { ok: false, message: "" };

export function ContactForm() {
  const [state, formAction] = useActionState(submitContact, initial);

  return (
    <form action={formAction} className="mt-8 max-w-md space-y-4">
      <div>
        <label
          htmlFor="name"
          className="block text-sm font-medium text-slate-700"
        >
          Name
        </label>
        <input
          id="name"
          name="name"
          type="text"
          autoComplete="name"
          className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-slate-900 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
          disabled
        />
      </div>
      <div>
        <label
          htmlFor="email"
          className="block text-sm font-medium text-slate-700"
        >
          Email
        </label>
        <input
          id="email"
          name="email"
          type="email"
          autoComplete="email"
          className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-slate-900 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
          disabled
        />
      </div>
      <div>
        <label
          htmlFor="message"
          className="block text-sm font-medium text-slate-700"
        >
          Message
        </label>
        <textarea
          id="message"
          name="message"
          rows={4}
          className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-slate-900 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
          disabled
        />
      </div>
      <p className="text-sm text-slate-500">
        Fields are disabled until privacy review and mail integration are
        complete (FR-007).
      </p>
      <button
        type="submit"
        className="rounded-md bg-slate-900 px-4 py-2 text-sm font-semibold text-white hover:bg-slate-800"
      >
        Send (stub)
      </button>
      {state.message ? (
        <p className="text-sm text-amber-800" role="status">
          {state.message}
        </p>
      ) : null}
    </form>
  );
}
