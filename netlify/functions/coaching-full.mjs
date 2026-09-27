// Starts Stripe Checkout for At your pace with coaching, paid in one go: £1,297.
// Needs STRIPE_SECRET_KEY set in Netlify (Site configuration > Environment variables).
import { CONSENT, startCheckout } from './coaching-plan.mjs';

export const PRICE = 129700; // pence

export const checkoutForm = (origin) => {
  const f = new URLSearchParams();
  f.set('mode', 'payment');
  f.set('line_items[0][price_data][currency]', 'gbp');
  f.set('line_items[0][price_data][product_data][name]', 'At your pace with coaching');
  f.set('line_items[0][price_data][unit_amount]', String(PRICE));
  f.set('line_items[0][quantity]', '1');
  f.set('invoice_creation[enabled]', 'true'); // an invoice and receipt, as the payment plan gets
  f.set('metadata[plan]', 'coaching-full');
  // The terms tickbox (needs the Terms of service URL set in Stripe's public business details)
  f.set('consent_collection[terms_of_service]', 'required');
  f.set('custom_text[terms_of_service_acceptance][message]', CONSENT);
  f.set('success_url', `${origin}/thank-you/with-coaching/?session_id={CHECKOUT_SESSION_ID}`);
  f.set('cancel_url', `${origin}/join/coaching/`);
  return f;
};

export default (req) => startCheckout(checkoutForm(new URL(req.url).origin));

export const config = { path: '/pay/coaching-full' };
