export default function Loading() {
  return (
    <div
      className="flex flex-1 flex-col items-center justify-center py-24"
      role="status"
      aria-live="polite"
    >
      <span className="h-8 w-8 animate-spin rounded-full border-2 border-slate-300 border-t-slate-800" />
      <span className="sr-only">Loading</span>
    </div>
  );
}
