import { NextResponse } from "next/server";

export function GET() {
  return NextResponse.json(
    { status: "ok", service: "firm-site" },
    { status: 200 },
  );
}
