import type { Metadata } from "next";
import Image from "next/image";
import { Prose } from "@/components/Prose";

export const metadata: Metadata = {
  title: "About us",
  description: "Learn about Sharma Law and our immigration practice.",
};

export default function AboutPage() {
  return (
    <Prose>
      <article>
        <div className="overflow-hidden rounded-xl border border-slate-200 bg-slate-50">
          <Image
            src="/images/about-banner.png"
            alt="Law office building"
            width={1200}
            height={450}
            sizes="(max-width: 768px) 100vw, 700px"
            className="h-56 w-full object-cover sm:h-64"
            priority
          />
        </div>
        <div className="mt-10 grid gap-6 md:grid-cols-[1fr_260px] md:items-start">
          <div className="space-y-4">
            <p className="italic text-slate-700">
              Being an immigrant, I relate to my clients and understand their
              needs. Be it a family member needing immigration assistance or a
              company in need of technical workers, my office has created a
              reputation and goodwill to meet diverse requirements.
            </p>
            <p className="italic text-slate-700">
              I work zealously to achieve client&apos;s goals and my office is
              always supportive of individual needs.
            </p>
            <p className="text-sm italic text-slate-600">— Sharma, Esq.</p>
          </div>

          <aside className="rounded-lg bg-slate-200/80 p-5">
            <p className="text-sm font-semibold text-slate-700">Call Today</p>
            <p className="mt-1 text-lg font-semibold tracking-tight text-slate-900">
              <a href="tel:+14159557846" className="hover:underline">
                415-955-7846
              </a>
            </p>
          </aside>
        </div>
        <p className="mt-10">
          Counsel Sharma has worked with leading law firms and gained extensive
          experience in filing complex immigration cases. Externing at the Ninth
          Circuit Court of Appeals in San Francisco, California, was a rewarding
          experience and accomplishment for this immigrant lawyer. Counsel
          Sharma remains grateful for that opportunity.
        </p>
        <p>
          Counsel Sharma has been a member of several legal and professional
          organizations.
        </p>
      </article>
    </Prose>
  );
}
