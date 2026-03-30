import type { Metadata } from "next";
import Link from "next/link";
import { Prose } from "@/components/Prose";

export const metadata: Metadata = {
  title: "Book online",
  description: "Schedule an appointment with Sharma Law.",
};

export default function BookOnlinePage() {
  return (
    <Prose>
      <article>
        <h1 className="sr-only">Book online</h1>
        <p>
          When the firm embeds a scheduling provider (e.g. Calendly, Wix
          Bookings), place the iframe or widget here per vendor documentation.
        </p>
        <div className="aspect-video w-full rounded-lg border border-dashed border-slate-300 bg-slate-50 p-6 text-center text-slate-500">
          Booking embed placeholder
        </div>
        <div className="mt-6 rounded-lg border border-slate-200 bg-white p-4">
          <h2 className="text-base font-semibold text-slate-900">
            Payment (placeholder)
          </h2>
          <p className="mt-2 text-sm text-slate-600">
            Payment will be embedded as part of the booking flow later. For now,
            use this page as a placeholder.
          </p>
          <p className="mt-3">
            <Link
              href="/payment"
              className="text-sm font-semibold text-blue-800 hover:text-blue-900 hover:underline"
            >
              Go to payment
            </Link>
          </p>
        </div>
      </article>
    </Prose>
  );
}
