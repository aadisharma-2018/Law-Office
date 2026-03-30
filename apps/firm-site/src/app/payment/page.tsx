import type { Metadata } from "next";
import { Prose } from "@/components/Prose";

export const metadata: Metadata = {
  title: "Payment",
  description: "Payment options for Sharma Law clients.",
};

export default function PaymentPage() {
  return (
    <Prose>
      <article>
        <h1>Payment</h1>
        <p>
          Payment links and processor embeds should be placed here per the
          firm’s merchant setup. Third-party payment pages are governed by their
          terms and privacy policies.
        </p>
      </article>
    </Prose>
  );
}
