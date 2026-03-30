"use server";

export type ContactState = {
  ok: boolean;
  message: string;
};

export async function submitContact(
  _prevState: ContactState,
  _formData: FormData,
): Promise<ContactState> {
  void _formData;
  return {
    ok: false,
    message:
      "Contact form is disabled until email/CRM credentials are configured. Call the office or use booking links where available.",
  };
}
