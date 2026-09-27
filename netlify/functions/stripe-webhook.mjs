// Receives Stripe's "checkout completed" event and tells a coaching payment plan to stop after its
// second monthly payment, so nobody is charged a third £300.
// Needs STRIPE_SECRET_KEY and STRIPE_WEBHOOK_SECRET set in Netlify, and a Stripe webhook pointing at
// https://<your domain>/stripe/webhook for the event checkout.session.completed.
import { createHmac, timingSafeEqual } from 'node:crypto';
import { oneMonthFrom } from './coaching-plan.mjs';

// Stripe signs each event; reject anything not signed with our secret, or older than five minutes
export const verify = (body, header, secret, now = Date.now()) => {
  const parts = Object.fromEntries((header || '').split(',').map((p) => p.split('=')));
  const t = Number(parts.t);
  if (!t || !parts.v1 || Math.abs(now / 1000 - t) > 300) return false;
  const expected = createHmac('sha256', secret).update(`${t}.${body}`).digest('hex');
  const a = Buffer.from(expected), b = Buffer.from(parts.v1);
  return a.length === b.length && timingSafeEqual(a, b);
};

// End the plan halfway between the second and a third monthly payment
export const cancelAt = (anchor) => {
  const second = oneMonthFrom(anchor * 1000);
  const third = oneMonthFrom(second * 1000);
  return Math.floor((second + third) / 2);
};

export default async (req) => {
  const body = await req.text();
  if (!verify(body, req.headers.get('stripe-signature'), process.env.STRIPE_WEBHOOK_SECRET || '')) {
    return new Response('Bad signature', { status: 400 });
  }
  const event = JSON.parse(body);
  const session = event.data?.object;
  if (event.type !== 'checkout.session.completed' || session?.metadata?.plan !== 'coaching-payment-plan' || !session.subscription) {
    return new Response('Ignored', { status: 200 });
  }
  const f = new URLSearchParams({ cancel_at: String(cancelAt(Number(session.metadata.anchor))), proration_behavior: 'none' });
  const res = await fetch(`https://api.stripe.com/v1/subscriptions/${session.subscription}`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${process.env.STRIPE_SECRET_KEY}`, 'Content-Type': 'application/x-www-form-urlencoded' },
    body: f,
  });
  if (!res.ok) {
    // A failure here means Stripe retries the event; the plan must not be left running
    console.error('Could not set the plan end date', session.subscription, (await res.json())?.error?.message);
    return new Response('Retry', { status: 500 });
  }
  return new Response('OK', { status: 200 });
};

export const config = { path: '/stripe/webhook' };
