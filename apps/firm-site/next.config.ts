import type { NextConfig } from "next";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const nextConfig: NextConfig = {
  outputFileTracingRoot: path.join(__dirname, "../.."),
  allowedDevOrigins: ["127.0.0.1"],
  async redirects() {
    return [
      {
        source: "/copy-of-contact-us",
        destination: "/contact-us",
        permanent: true,
      },
      {
        source: "/service-page/:slug",
        destination: "/book-online",
        permanent: false,
      },
    ];
  },
};

export default nextConfig;
