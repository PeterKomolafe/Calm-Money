// Starts Stripe Checkout for the At your pace with coaching payment plan:
// £697 today, then two monthly payments of £300. £1,297 in total, with no interest or extra charge.
// The subscription is told to stop after the second £300 by stripe-webhook.mjs.
// Needs STRIPE_SECRET_KEY set in Netlify (Site configuration > Environment variables).

export const PLAN = {
  firstPayment: 69700, // pence, charged at checkout
  monthlyPayment: 30000, // pence, charged a month later and a month after that
  monthlyPayments: 2,
};

// The same day next month, in seconds (short months fall back to their last day, as Stripe does)
export const oneMonthFrom = (date) => {
  const d = new Date(date);
  const day = d.getUTCDate();
  d.setUTCDate(1);
  d.setUTCMonth(d.getUTCMonth() + 1);
  const last = new Date(Date.UTC(d.getUTCFullYear(), d.getUTCMonth() + 1, 0)).getUTCDate();
  d.setUTCDate(Math.min(day, last));
  return Math.floor(d.getTime() / 1000);
};

// The terms tickbox wording, shared with coaching-full.mjs
export const CONSENT = 'I agree to the Terms and Conditions. I want my access to the Calm Money content library to start straight away, and I understand that once it starts I lose my right to cancel it within 14 days. If my coaching starts within 14 days and I then cancel, I will pay for the sessions already provided.';

export const checkoutForm = (origin, now = Date.now()) => {
  const anchor = oneMonthFrom(now); // first £300 is taken a month after checkout
  const f = new URLSearchParams();
  f.set('mode', 'subscription');
  // Today: the first payment, as a one-off item on the first invoice
  f.set('line_items[0][price_data][currency]', 'gbp');
  f.set('line_items[0][price_data][product_data][name]', 'At your pace with coaching: first payment');
  f.set('line_items[0][price_data][unit_amount]', String(PLAN.firstPayment));
  f.set('line_items[0][quantity]', '1');
  // Then: £300 a month, starting a month from today
  f.set('line_items[1][price_data][currency]', 'gbp');
  f.set('line_items[1][price_data][product_data][name]', 'At your pace with coaching: 2 monthly payments of £300');
  f.set('line_items[1][price_data][unit_amount]', String(PLAN.monthlyPayment));
  f.set('line_items[1][price_data][recurring][interval]', 'month');
  f.set('line_items[1][quantity]', '1');
  f.set('subscription_data[billing_cycle_anchor]', String(anchor));
  f.set('subscription_data[proration_behavior]', 'none');
  f.set('subscription_data[description]', 'At your pace with coaching: £697 today, then 2 monthly payments of £300 (£1,297 in total)');
  f.set('metadata[plan]', 'coaching-payment-plan');
  f.set('metadata[anchor]', String(anchor));
  // The terms tickbox (needs the Terms of service URL set in Stripe's public business details)
  f.set('consent_collection[terms_of_service]', 'required');
  f.set('custom_text[terms_of_service_acceptance][message]', CONSENT);
  f.set('success_url', `${origin}/thank-you/with-coaching/?session_id={CHECKOUT_SESSION_ID}`);
  f.set('cancel_url', `${origin}/join/coaching/`);
  return f;
};

// Creates the Checkout session and sends the buyer to it (shared with coaching-full.mjs)
export const startCheckout = async (form) => {
  const key = process.env.STRIPE_SECRET_KEY;
  if (!key) return new Response('Checkout isn’t set up yet. Please email hello@peterkomolafe.com.', { status: 503 });
  const res = await fetch('https://api.stripe.com/v1/checkout/sessions', {
    method: 'POST',
    headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/x-www-form-urlencoded' },
    body: form,
  });
  const session = await res.json();
  if (!res.ok) {
    console.error('Stripe checkout failed', session?.error?.message);
    return new Response('We couldn’t start checkout. Please try again, or email hello@peterkomolafe.com.', { status: 502 });
  }
  return Response.redirect(session.url, 303);
};

export default (req) => startCheckout(checkoutForm(new URL(req.url).origin));

export const config = { path: '/pay/coaching-plan' };
