// Starts Stripe Checkout for the At your pace with coaching payment plan:
// £397 today, then nine monthly payments of £100. £1,297 in total, with no interest or extra charge.
// The subscription is told to stop after the ninth £100 by stripe-webhook.mjs.
// Ten payments, all within 12 months and with no charges, keeps the plan outside consumer credit rules.
// Needs STRIPE_SECRET_KEY set in Netlify (Site configuration > Environment variables).

export const PLAN = {
  firstPayment: 39700, // pence, charged at checkout (the same as At your pace)
  monthlyPayment: 10000, // pence, charged every month from a month after checkout
  monthlyPayments: 9,
};
const gbp = (pence) => `£${(pence / 100).toLocaleString('en-GB')}`;
export const PLAN_TOTAL = PLAN.firstPayment + PLAN.monthlyPayment * PLAN.monthlyPayments; // 129700, £1,297

// The same day n months later, in seconds (short months fall back to their last day, as Stripe does).
// Always counted from the original date, so the 31st stays the 31st after a short month
export const monthsFrom = (date, n) => {
  const d = new Date(date);
  const day = d.getUTCDate();
  d.setUTCDate(1);
  d.setUTCMonth(d.getUTCMonth() + n);
  const last = new Date(Date.UTC(d.getUTCFullYear(), d.getUTCMonth() + 1, 0)).getUTCDate();
  d.setUTCDate(Math.min(day, last));
  return Math.floor(d.getTime() / 1000);
};
export const oneMonthFrom = (date) => monthsFrom(date, 1);

// The terms tickbox wording, shared with coaching-full.mjs
export const CONSENT = 'I agree to the Terms and Conditions. I want my access to the Calm Money content library to start straight away, and I understand that once it starts I lose my right to cancel it within 14 days. If my coaching starts within 14 days and I then cancel, I will pay for the sessions already provided.';

export const checkoutForm = (origin, now = Date.now()) => {
  const anchor = oneMonthFrom(now); // the first monthly payment is taken a month after checkout
  const f = new URLSearchParams();
  f.set('mode', 'subscription');
  // Today: the first payment, as a one-off item on the first invoice
  f.set('line_items[0][price_data][currency]', 'gbp');
  f.set('line_items[0][price_data][product_data][name]', 'At your pace with coaching: first payment');
  f.set('line_items[0][price_data][unit_amount]', String(PLAN.firstPayment));
  f.set('line_items[0][quantity]', '1');
  // Then: the monthly payment, starting a month from today
  f.set('line_items[1][price_data][currency]', 'gbp');
  f.set('line_items[1][price_data][product_data][name]', `At your pace with coaching: ${PLAN.monthlyPayments} monthly payments of ${gbp(PLAN.monthlyPayment)}`);
  f.set('line_items[1][price_data][unit_amount]', String(PLAN.monthlyPayment));
  f.set('line_items[1][price_data][recurring][interval]', 'month');
  f.set('line_items[1][quantity]', '1');
  f.set('subscription_data[billing_cycle_anchor]', String(anchor));
  f.set('subscription_data[proration_behavior]', 'none');
  f.set('subscription_data[description]', `At your pace with coaching: ${gbp(PLAN.firstPayment)} today, then ${PLAN.monthlyPayments} monthly payments of ${gbp(PLAN.monthlyPayment)} (${gbp(PLAN_TOTAL)} in total)`);
  f.set('metadata[plan]', 'coaching-payment-plan');
  f.set('metadata[anchor]', String(anchor));
  f.set('metadata[payments]', String(PLAN.monthlyPayments)); // so a plan keeps its own length if PLAN changes later
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
