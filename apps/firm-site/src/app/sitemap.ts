import type { MetadataRoute } from "next";
import { getSiteUrl } from "@/lib/site";
import { getAllInternalPaths } from "@/lib/site-paths";

export default function sitemap(): MetadataRoute.Sitemap {
  const base = getSiteUrl();
  const paths = getAllInternalPaths();
  return paths.map((path) => ({
    url: `${base}${path === "/" ? "" : path}`,
    lastModified: new Date(),
    changeFrequency: path === "/" ? "weekly" : "monthly",
    priority: path === "/" ? 1 : 0.7,
  }));
}
