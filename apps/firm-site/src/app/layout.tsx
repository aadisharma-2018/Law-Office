import type { Metadata } from "next";
import { Jura } from "next/font/google";
import "./globals.css";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteHeader } from "@/components/SiteHeader";
import { absoluteUrl } from "@/lib/site";
import type { NavigationConfig } from "@/types/navigation";
import rawNavigation from "../../content/navigation.json";

const navigation = rawNavigation as NavigationConfig;

const jura = Jura({
  subsets: ["latin"],
  variable: "--font-jura",
  display: "swap",
});

export const metadata: Metadata = {
  metadataBase: new URL(absoluteUrl("/")),
  title: {
    default: "Sharma Law | Immigration Attorney",
    template: "%s | Sharma Law",
  },
  description:
    "Bay Area Immigration Attorney — solutions for visas, green cards, and naturalization.",
  openGraph: {
    type: "website",
    locale: "en_US",
    siteName: "Sharma Law",
    url: absoluteUrl("/"),
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${jura.variable} flex min-h-screen flex-col bg-white font-sans text-slate-900 antialiased`}
      >
        <SiteHeader navigation={navigation} />
        <div className="flex flex-1 flex-col">{children}</div>
        <SiteFooter navigation={navigation} />
      </body>
    </html>
  );
}
