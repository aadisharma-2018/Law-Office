import type { Metadata } from "next";
import Image from "next/image";

export const metadata: Metadata = {
  title: "Practice areas",
  description:
    "Practice areas for immigration matters including consultations, forms, and filings.",
};

export default function PracticeAreasPage() {
  return (
    <main className="mx-auto w-full max-w-6xl px-4 py-10 sm:px-6">
      <article>
        <h1 className="sr-only">Practice areas</h1>
        <p className="mt-3 max-w-2xl text-base leading-relaxed text-slate-700">
          The firm assists individuals and employers with U.S. immigration
          matters. The categories below describe common areas we support.
        </p>

        <div className="mt-6 overflow-hidden rounded-xl border border-slate-200 bg-slate-50">
          <Image
            src="/images/practice-areas-banner.png"
            alt="Law office building"
            width={1200}
            height={450}
            priority
            sizes="(max-width: 768px) 100vw, 1200px"
            className="h-56 w-full object-cover sm:h-64"
          />
        </div>

        <section className="mt-10 rounded-xl bg-slate-100 px-6 py-8 sm:px-10">
          <div className="grid gap-10 md:grid-cols-3">
            {/* FAMILY-BASED APPLICATIONS */}
            <div className="space-y-7">
              <h2 className="text-sm font-bold uppercase tracking-wide text-slate-900">
                Family-based applications
              </h2>

              <div className="space-y-5">
                <h3 className="text-sm font-semibold uppercase tracking-wide text-blue-800">
                  U.S. citizens
                </h3>
                <p className="text-sm leading-relaxed text-slate-700">
                  Apply for Spouse, Children, Parents, and Siblings
                  <br />
                  Immediate relative petitions include Employment Authorization
                  and Advance Parole
                  <br />
                  Certificate of citizenship for children
                </p>

                <h3 className="text-sm font-semibold uppercase tracking-wide text-blue-800">
                  Permanent residents
                </h3>
                <p className="text-sm leading-relaxed text-slate-700">
                  Apply for Spouse and Children
                  <br />
                  Naturalization application
                  <br />
                  Re-entry Permit
                </p>

                <h3 className="text-sm font-semibold uppercase tracking-wide text-blue-800">
                  Asylees
                </h3>
                <p className="text-sm leading-relaxed text-slate-700">
                  Apply for Residency
                  <br />
                  Application for Spouse and Children
                  <br />
                  Employment Authorization
                </p>

                <h3 className="text-sm font-semibold uppercase tracking-wide text-blue-800">
                  Waivers
                </h3>
                <p className="text-sm leading-relaxed text-slate-700">
                  Entered without inspection - qualifying relatives can petition
                  to bring you back
                </p>
              </div>
            </div>

            {/* EMPLOYMENT-BASED PETITIONS */}
            <div className="space-y-7">
              <h2 className="text-sm font-bold uppercase tracking-wide text-slate-900">
                Employment-based petitions
              </h2>

              <div className="space-y-5">
                <h3 className="text-sm font-semibold uppercase tracking-wide text-blue-800">
                  E-3 visa
                </h3>
                <p className="text-sm leading-relaxed text-slate-700">
                  For Australian specialty workers
                </p>

                <h3 className="text-sm font-semibold uppercase tracking-wide text-blue-800">
                  H-1B specialty workers
                </h3>
                <p className="text-sm leading-relaxed text-slate-700">
                  Jobs requiring a minimum of a Bachelor&apos;s degree
                </p>

                <h3 className="text-sm font-semibold uppercase tracking-wide text-blue-800">
                  L visas
                </h3>
                <p className="text-sm leading-relaxed text-slate-700">
                  Intracompany Transfers
                  <br />
                  Petitions for technical workers and managers
                </p>

                <h3 className="text-sm font-semibold uppercase tracking-wide text-blue-800">
                  O-1 visa
                </h3>
                <p className="text-sm leading-relaxed text-slate-700">
                  Extraordinary Ability or Achievers
                </p>

                <h3 className="text-sm font-semibold uppercase tracking-wide text-blue-800">
                  P visa
                </h3>
                <p className="text-sm leading-relaxed text-slate-700">
                  Artist and Performers coming to show their craft
                </p>

                <h3 className="text-sm font-semibold uppercase tracking-wide text-blue-800">
                  R-1 visa
                </h3>
                <p className="text-sm leading-relaxed text-slate-700">
                  Religious Workers for Tax-Exempt Organizations
                </p>

                <h3 className="text-sm font-semibold uppercase tracking-wide text-blue-800">
                  TN NAFTA professionals
                </h3>
                <p className="text-sm leading-relaxed text-slate-700">
                  Work visa for certain professionals from Canada and Mexico
                </p>

                <h3 className="text-sm font-semibold uppercase tracking-wide text-blue-800">
                  Immigrant visa petitions
                </h3>
                <p className="text-sm leading-relaxed text-slate-700">
                  I-140 for EB-1, EB-2, EB-3 and non skilled workers
                </p>
              </div>
            </div>

            {/* MISCELLANEOUS */}
            <div className="space-y-7">
              <h2 className="text-sm font-bold uppercase tracking-wide text-slate-900">
                Miscellaneous
              </h2>

              <div className="space-y-5">
                <h3 className="text-sm font-semibold uppercase tracking-wide text-blue-800">
                  B-1/2 visa
                </h3>
                <p className="text-sm leading-relaxed text-slate-700">
                  Business and tourist visa for temporary travel to the U.S.
                  <br />
                  Letters of invitation
                  <br />
                  Financial sponsorship
                </p>

                <h3 className="text-sm font-semibold uppercase tracking-wide text-blue-800">
                  F-1 visa
                </h3>
                <p className="text-sm leading-relaxed text-slate-700">
                  Students applying for education in the U.S.
                  <br />
                  OPT Guidance
                  <br />
                  SEVIS
                  <br />
                  Maintaining status
                </p>

                <h3 className="text-sm font-semibold uppercase tracking-wide text-blue-800">
                  Change of status
                </h3>
                <p className="text-sm leading-relaxed text-slate-700">
                  Change in plans, status ended abruptly - you may be eligible
                  to stay
                </p>

                <h3 className="text-sm font-semibold uppercase tracking-wide text-blue-800">
                  Extension of status
                </h3>
                <p className="text-sm leading-relaxed text-slate-700">
                  Need more time to achieve your goals, you may be able to apply
                  for extension of your current status
                </p>

                <h3 className="text-sm font-semibold uppercase tracking-wide text-blue-800">
                  Advisory opinion
                </h3>
                <p className="text-sm leading-relaxed text-slate-700">
                  Convicted for petty offenses and need assistance with visa
                  application
                </p>

                <h3 className="text-sm font-semibold uppercase tracking-wide text-blue-800">
                  Green card, employment authorization and advance parole
                </h3>
                <p className="text-sm leading-relaxed text-slate-700">
                  Adjusting status in the U.S. based on family or employment
                  based petition
                </p>

                <h3 className="text-sm font-semibold uppercase tracking-wide text-blue-800">
                  U visa
                </h3>
                <p className="text-sm leading-relaxed text-slate-700">
                  Victims of violent crimes qualify to stay to testify in the
                  criminal proceedings
                </p>
              </div>
            </div>
          </div>
        </section>
      </article>
    </main>
  );
}
