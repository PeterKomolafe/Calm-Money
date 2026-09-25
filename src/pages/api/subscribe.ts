import type { APIRoute } from 'astro';

export const prerender = false;

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

async function addToKit(email: string, firstName: string) {
  const key = process.env.KIT_API_KEY;
  const formId = process.env.KIT_FORM_ID;
  if (!key || !formId) throw new Error('Kit is not configured');
  const headers = { 'Content-Type': 'application/json', 'X-Kit-Api-Key': key };
  const create = await fetch('https://api.kit.com/v4/subscribers', {
    method: 'POST',
    headers,
    body: JSON.stringify({ email_address: email, first_name: firstName || undefined }),
  });
  if (!create.ok) throw new Error(`Kit subscriber error ${create.status}`);
  const add = await fetch(`https://api.kit.com/v4/forms/${formId}/subscribers`, {
    method: 'POST',
    headers,
    body: JSON.stringify({ email_address: email }),
  });
  if (!add.ok) throw new Error(`Kit form error ${add.status}`);
}

async function addToMailerLite(email: string, firstName: string) {
  const key = process.env.MAILERLITE_API_KEY;
  const group = process.env.MAILERLITE_GROUP_ID;
  if (!key) throw new Error('MailerLite is not configured');
  const res = await fetch('https://connect.mailerlite.com/api/subscribers', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Accept: 'application/json', Authorization: `Bearer ${key}` },
    body: JSON.stringify({ email, fields: firstName ? { name: firstName } : undefined, groups: group ? [group] : undefined }),
  });
  if (!res.ok) throw new Error(`MailerLite error ${res.status}`);
}

export const POST: APIRoute = async ({ request, redirect }) => {
  const wantsJson = request.headers.get('accept')?.includes('application/json');
  const reply = (status: number, error?: string) =>
    wantsJson
      ? new Response(JSON.stringify(error ? { error } : { ok: true }), { status, headers: { 'Content-Type': 'application/json' } })
      : error
        ? new Response(error, { status })
        : redirect('/thanks', 303);

  const form = await request.formData();
  // Honeypot: bots fill hidden fields, people don't. Pretend success.
  if (String(form.get('company') ?? '')) return reply(200);

  const email = String(form.get('email') ?? '').trim().toLowerCase();
  const firstName = String(form.get('first_name') ?? '').trim().slice(0, 80);
  if (!EMAIL_RE.test(email)) return reply(400, 'Please enter a valid email address.');

  const provider = process.env.EMAIL_PROVIDER;
  try {
    if (provider === 'kit') await addToKit(email, firstName);
    else if (provider === 'mailerlite') await addToMailerLite(email, firstName);
    else if (import.meta.env.DEV) console.log('[subscribe] no EMAIL_PROVIDER set; would add', { email, firstName });
    else throw new Error('EMAIL_PROVIDER is not set');
  } catch (err) {
    console.error('[subscribe]', err);
    return reply(502, 'Sorry, we could not sign you up just now. Please try again shortly.');
  }
  return reply(200);
};
