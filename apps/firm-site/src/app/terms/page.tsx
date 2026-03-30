import type { Metadata } from "next";
import { Prose } from "@/components/Prose";

export const metadata: Metadata = {
  title: "Terms and Conditions",
  description: "Terms governing use of this website.",
};

export default function TermsPage() {
  return (
    <Prose>
      <article>
        <h1>Terms and Conditions</h1>
        <h2>10-minute phone consultation*</h2>
        <p>
          This service is for 1-2 simple question scenario. It is not suitable
          for complex cases or discussion.
        </p>

        <h2>15-minute phone consultation*</h2>
        <p>
          This is appropriate for cases with some details and multiple question
          (2-3). For non-complex queries only.
        </p>

        <h2>20-minute phone consultation*</h2>
        <p>
          This is suitable for multiple question (1-5) scenario or with case
          history, dates and events. Does not include extensive research and
          analysis.
        </p>

        <h2>30-minute phone consultation*</h2>
        <p>
          Choose this option if you wish to discuss your case and ponder
          immigration options.
        </p>

        <h2>Follow up phone consultation*</h2>
        <p>
          Offered to existing clients for up to 10 minutes to discuss missed,
          follow up questions related to the same issue. This feature is
          available only for next day of initial meeting. Attorney will rely on
          notes taken during prior consultations; so please inform us of the
          date(s) of prior meetings to enable us to retrieve the information.
        </p>

        <p>
          <em>
            *Phone consultations do not include document review, help with
            completing forms, legal research and analysis. It is geared to guide
            and answer legal questions prospective clients have about their
            case. Choose from below options for document and form review, or
            contact our office for a custom quote for your legal needs.
          </em>
        </p>

        <h2>All other consultation*</h2>
        <p>
          All other consultations and services are offered at $250 - $450 per
          hour attorney fee depending on complexity of service.
        </p>

        <h2>In-office consultation*</h2>
        <p>
          Initial consultation offered for up to 45 minutes and includes brief
          review of related paper work. Follow up or elaborate document review
          is not included. Contact our office for the appointment.
        </p>

        <h2>Review of RFE and advice*</h2>
        <p>
          We usually review the underlying application and supporting documents
          filed with USCIS, the RFE (5 pages maximum) and schedule a 30-minute
          discussion on the issue to be addressed. If your case or RFE is
          complex, we will quote you the fee accordingly. This service does not
          include drafting a response. We work with you to understand your needs
          and you may seek a quote if you wish our office file the RFE response
          for you.
        </p>

        <h2>Review of one form*</h2>
        <p>
          We assist with completing one form and guide with documents you submit
          to support your application. Review of supporting documents not
          included.
        </p>

        <h2>Review of one application*</h2>
        <p>
          We review your application and basic supporting documents that go with
          every application. If your case is unique and requires review of
          criminal file, sponsorship documents, drafting affidavits, preparing
          support letters, write ups, elaborate photographs and details to
          explain any deficiencies, that will not be included and we will
          provide a quote for the extensive review. If you do not wish to
          proceed with our additional quote, we will proceed with review of the
          form and the basic supporting documents.
        </p>

        <h2>Review of documents for filing*</h2>
        <p>Contact our office for a quote.</p>

        <h2>Immigration consequences of criminal actions* - review / advice</h2>
        <p>
          This service includes review of charge sheet, police statement, and
          final disposition. Ideally send us a certified copy of your criminal
          record (not exceeding 15 pages.) Ask for quote for extensive review of
          file. If record is expunged (not recommended for immigration purposes)
          you may submit a photocopy.
        </p>

        <p>
          <em>
            This service does not include a written advisory memo or opinion. It
            includes review, research, analysis and a 30-minute discussion to
            advise you of the potential immigration consequences of your
            criminal actions.
          </em>
        </p>

        <p>
          If the charges are pending and you are considering a plea bargain, the
          consultation fees may vary depending on options you are being offered.
          Contact our office for a quote.
        </p>

        <p>
          If you need a written opinion following the discussion, we quote you
          the fee after the consultation depending on the complexity of the
          case.
        </p>

        <h2>Other Terms and Conditions*</h2>
        <p>
          All consultations start and end promptly at the time scheduled. If you
          wish to exceed the time slot chosen, you may be asked to pay
          additional fees. We start working on your case immediately and so if
          you wish to cancel a service, immediately call our office for a full
          refund. Cancellations are accepted only before any work is done on
          cases. Contact our office immediately if you do not wish to avail of
          our services. For forms and documents submitted and reviewed, analysis
          provided or any work done and attorney fees considered earned and
          refunds will not be provided.
        </p>
      </article>
    </Prose>
  );
}
