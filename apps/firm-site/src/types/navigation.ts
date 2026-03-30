export type NavPlacement = "header" | "footer" | "mobile";

export type NavLink = {
  id: string;
  label: string;
  href: string;
  placement: NavPlacement;
  order: number;
};

export type NavigationConfig = {
  header: NavLink[];
  footer: NavLink[];
};
