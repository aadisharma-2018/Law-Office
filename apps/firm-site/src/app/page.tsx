import Image from "next/image";
import type { Metadata } from "next";
import Link from "next/link";
import { SERVICES } from "@/data/services";

export const metadata: Metadata = {
  title: "Immigration Attorney",
  description:
    "Bay Area Immigration Attorney, for all your immigration solutions!",
};

export default function HomePage() {
  const highlights = SERVICES;

  return (
    <>
      <section className="border-b border-slate-100 bg-gradient-to-b from-slate-50 to-white">
        <div className="mx-auto grid max-w-6xl gap-10 px-4 py-14 md:grid-cols-2 md:items-center md:py-20">
          <div className="min-w-0">
            <h1 className="text-4xl font-bold tracking-tight text-slate-900 md:text-5xl">
              Immigration Attorney
            </h1>
            <p className="mt-4 text-lg text-slate-600">
              Bay Area Immigration Attorney, for all your immigration solutions.
            </p>
            <div className="mt-8 flex flex-wrap gap-4">
              <Link
                href="/contact-us"
                className="inline-flex items-center justify-center rounded-md bg-slate-900 px-5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-slate-800"
              >
                Contact us
              </Link>
              <Link
                href="/practice-areas"
                className="inline-flex items-center justify-center rounded-md border border-slate-300 bg-white px-5 py-2.5 text-sm font-semibold text-slate-900 hover:bg-slate-50"
              >
                Practice areas
              </Link>
            </div>
            <p className="mt-4 text-sm text-slate-600">
              Call Today{" "}
              <a
                href="tel:+14159557846"
                className="font-semibold text-slate-900 hover:underline"
              >
                415-955-7846
              </a>
            </p>
          </div>
          <div className="relative aspect-[4/3] w-full min-w-0 overflow-hidden rounded-xl bg-slate-200 shadow-sm ring-1 ring-slate-200/60">
            <Image
              src="/images/home-hero.png"
              alt="Law office building"
              width={800}
              height={600}
              priority
              sizes="(max-width: 768px) 100vw, 50vw"
              className="h-full w-full object-cover"
            />
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-4 py-14">
        <h2 className="text-2xl font-semibold text-slate-900">
          Personal and professional guidance
        </h2>
        <div className="mt-4 max-w-3xl space-y-4 text-slate-600">
          <p>
            Counsel Sharma is committed to providing businesses and individuals
            personal and professional guidance in the complex world of
            immigration law.
          </p>
          <p>
            Attorney takes time to understand clients&apos; requirements and
            work zealously to achieve their goals. The firm has acquired one of
            the finest reputations in the Bay Area for its commitment to the
            practice of immigration law.
          </p>
          <p>
            The reputation of our firm has been earned through hard work and
            dedicated service to our clients. We do our best to ensure our high
            standards are upheld in each case.
          </p>
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-4 py-14">
        <h2 className="text-2xl font-semibold text-slate-900">
          Services at a glance
        </h2>
        <p className="mt-2 max-w-2xl text-slate-600">
          Representative offerings aligned with our reference site. Confirm
          scope and fees with the firm before retaining.
        </p>
        <ul className="mt-8 grid gap-4 sm:grid-cols-2">
          {highlights.map((s) => (
            <li
              key={s.slug}
              className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm"
            >
              <Link
                href="/book-online"
                className="font-medium text-blue-800 hover:text-blue-900 hover:underline"
              >
                {s.title}
              </Link>
              <p className="mt-2 text-sm text-slate-600">{s.summary}</p>
            </li>
          ))}
        </ul>
      </section>

      <section className="border-t border-slate-100 bg-slate-50 py-14">
        <div className="mx-auto max-w-6xl px-4 text-center">
          <h2 className="text-xl font-semibold text-slate-900">
            Ready to talk?
          </h2>
          <p className="mt-2 text-slate-600">
            Schedule a consultation or reach us on our contact page.
          </p>
          <div className="mt-6 flex flex-col items-center justify-center gap-3 sm:flex-row">
            <Link
              href="/book-online"
              className="inline-flex rounded-md bg-slate-900 px-5 py-2.5 text-sm font-semibold text-white hover:bg-slate-800"
            >
              Book online
            </Link>
            <Link
              href="/contact-us"
              className="inline-flex rounded-md border border-slate-300 bg-white px-5 py-2.5 text-sm font-semibold text-slate-900 hover:bg-slate-50"
            >
              Contact us
            </Link>
          </div>
        </div>
      </section>
    </>
  );
}
