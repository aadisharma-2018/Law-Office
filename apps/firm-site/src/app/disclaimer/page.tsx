import type { Metadata } from "next";
import { Prose } from "@/components/Prose";

export const metadata: Metadata = {
  title: "Disclaimer",
  description: "Legal disclaimer for the Sharma Law website.",
};

export default function DisclaimerPage() {
  return (
    <Prose>
      <article>
        <h1>Disclaimer</h1>
        <p>
          Any information provided on this website is information of general
          nature and should not be substituted for competent legal advice.
          Application of this information does not constitute an attorney-client
          relationship. Immigration laws change constantly and some information
          on this website may be outdated. We do not guarantee accuracy of the
          contents of the information provided on this website.
        </p>
      </article>
    </Prose>
  );
}
