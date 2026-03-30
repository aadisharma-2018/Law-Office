import Link from "next/link";
import type { NavigationConfig } from "@/types/navigation";

type Props = { navigation: NavigationConfig };

export function SiteFooter({ navigation }: Props) {
  const sorted = [...navigation.footer].sort((a, b) => a.order - b.order);

  return (
    <footer className="border-t border-slate-200 bg-slate-50">
      <div className="mx-auto flex max-w-6xl flex-col gap-6 px-4 py-10 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p className="font-semibold text-slate-900">Sharma Law</p>
          <p className="mt-1 max-w-sm text-sm text-slate-600">
            Bay Area immigration counsel.
          </p>
        </div>
        <nav aria-label="Footer">
          <ul className="flex flex-col gap-2 sm:flex-row sm:flex-wrap sm:gap-6">
            {sorted.map((item) => (
              <li key={item.id}>
                <Link
                  href={item.href}
                  className="text-sm font-medium text-slate-700 hover:text-slate-900 hover:underline"
                >
                  {item.label}
                </Link>
              </li>
            ))}
          </ul>
        </nav>
      </div>
      <div className="border-t border-slate-200/80 py-4 text-center text-xs text-slate-500">
        © {new Date().getFullYear()} Sharma Law. All rights reserved.
      </div>
    </footer>
  );
}
