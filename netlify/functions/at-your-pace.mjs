// Starts Stripe Checkout for At your pace: £397, paid upfront.
// Needs STRIPE_SECRET_KEY set in Netlify (Site configuration > Environment variables).
import { startCheckout } from './coaching-plan.mjs';

export const PRICE = 39700; // pence
// The At your pace product in Stripe, so every sale is reported under it.
// Test mode has its own product IDs: set STRIPE_PRODUCT_AT_YOUR_PACE in Netlify to use a test one.
export const PRODUCT = process.env.STRIPE_PRODUCT_AT_YOUR_PACE || 'prod_VKrmaUuxc9SU4o';

// At your pace has no coaching, so no refund once the content starts (Terms, section 7)
export const CONSENT = 'I agree to the Terms and Conditions. I want my access to the Calm Money content library to start straight away, and I understand that once it starts I lose my right to cancel and it is not eligible for a refund.';

export const checkoutForm = (origin) => {
  const f = new URLSearchParams();
  f.set('mode', 'payment');
  f.set('line_items[0][price_data][currency]', 'gbp');
  f.set('line_items[0][price_data][product]', PRODUCT);
  f.set('line_items[0][price_data][unit_amount]', String(PRICE));
  f.set('line_items[0][quantity]', '1');
  f.set('invoice_creation[enabled]', 'true');
  f.set('metadata[plan]', 'at-your-pace');
  // The terms tickbox (needs the Terms of service URL set in Stripe's public business details)
  f.set('consent_collection[terms_of_service]', 'required');
  f.set('custom_text[terms_of_service_acceptance][message]', CONSENT);
  f.set('success_url', `${origin}/thank-you/at-your-pace/?session_id={CHECKOUT_SESSION_ID}`);
  f.set('cancel_url', `${origin}/#pricing`);
  return f;
};

export default (req) => startCheckout(checkoutForm(new URL(req.url).origin));

export const config = { path: '/pay/at-your-pace' };
