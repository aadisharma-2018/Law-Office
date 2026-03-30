import type { Metadata } from "next";
import { Prose } from "@/components/Prose";
import { ContactForm } from "./ContactForm";

export const metadata: Metadata = {
  title: "Contact us",
  description: "Reach Sharma Law regarding your immigration matter.",
};

export default function ContactPage() {
  return (
    <Prose>
      <article>
        <h1 className="sr-only">Contact us</h1>
        <p>
          Use the form below once enabled, or call the office. The legacy site
          included a duplicate URL (<code>/copy-of-contact-us</code>) which now
          redirects here.
        </p>
        <aside className="mt-6 rounded-lg bg-slate-200/80 p-5">
          <p className="text-sm font-semibold text-slate-700">Call Today</p>
          <p className="mt-1 text-lg font-semibold tracking-tight text-slate-900">
            <a href="tel:+14159557846" className="hover:underline">
              415-955-7846
            </a>
          </p>
        </aside>
        <ContactForm />
      </article>
    </Prose>
  );
}
