# Calm Money: launch status

Last updated 10 October 2026. Live site: https://www.calmmoneycommunity.com, published by Netlify (`calmmoneysalespage`) from the `main` branch with auto publishing **on**. Work happens on `claude/website-build-3w8rav` and is copied to `main` to go live. All Join and price buttons go to https://app.calmmoneycommunity.com/register.

## What the page does now

- **Hero:** "Clear debt. Build a safety net. Start investing." with the tagline "For people who earn well but still feel stressed about money."
- **Story:** a tap-through timeline (Childhood, 2006, 2020, Number 10, Today). No scrolling needed.
- **Inside the platform:** five tools in a list with a large preview that opens full size, framed as "a few of the tools", with the Quick Debt Check and Risk Check named as more inside.
- **Pricing:**

  | Option | Price | Includes |
  |---|---|---|
  | At your pace | £397 | Modules, personality test, tools, community, monthly update, workshop library, 12 months' access |
  | At your pace with coaching | £1,297 (or £397 then 9 × £100) | Everything above, plus an onboarding call and 4 quarterly 1:1s |
  | 12 months of full support | £2,997, instalments available | Everything in coaching, plus an onboarding review of exercises, 12 monthly live group calls, WhatsApp and 2 meet-ups. 10 places per intake, waitlist |

  A collapsible comparison table sits under the cards.
- **Closing card:** Jean M.'s quote is the headline.
- **Terms:** updated to match all of the above (sections 4 to 7).

## Must be done before launch

### Payments and access
- [ ] Thank-you pages `/thank-you/at-your-pace/` and `/thank-you/with-coaching/` (checkout already sends buyers there).
- [ ] Grant platform access after payment. Plan: the Stripe webhook (`netlify/functions/stripe-webhook.mjs`) invites the buyer in Supabase and records their option and a 12-month end date. **Needs:** how the platform checks access (table and fields, or the platform repo), and `SUPABASE_URL` plus `SUPABASE_SERVICE_ROLE_KEY` set in Netlify environment variables (never shared in chat).
- [ ] The platform must enforce the 12-month end date.
- [ ] Remove access on refund (30-day guarantee), via the same webhook.
- [ ] Decide whether access continues while an instalment is overdue (terms allow pausing coaching).
- [ ] Admission for full support, which is paid after the waitlist.
- [ ] Stripe: secret key in Netlify (test first), Terms URL in Stripe settings, webhook for `checkout.session.completed`, coaching product ID, test purchase on the deploy preview.
- [ ] Confirm the Netlify build passes since the build command was restored.

### Legal
- [ ] Analytics decision: cookie-free tool, or Facebook Pixel with a consent banner. The privacy policy currently describes the Pixel and cookie settings that do not exist.
- [ ] Solicitor review: terms (section 6, guarantee condition, instalments, 10-place intakes), privacy policy, monthly update wording, and which company sells (UK Ltd or UAE business). Prices shown to UK consumers must include any VAT.
- [ ] Bank of England consent for the £50 note image.

### Going live
- [ ] Real domain: update `site` in `astro.config.mjs`, robots.txt and link previews (currently `calm-money.netlify.app`).
- [ ] New social sharing image (still shows the old wordmark).
- [ ] `/admin` content editor: set up Netlify Identity or remove it.
- [ ] Make the GitHub repo private.
- [ ] Create `main` at launch (with Peter's OK), then unlock publishing in Netlify.

## Decisions waiting on Peter
- [ ] What founding members keep (live sessions, renewal discount), and telling them before launch.
- [ ] WhatsApp reply promise (card still says "get support when you need it").
- [ ] Length of 1:1 sessions, for the terms.
- [ ] Full support instalment schedule (12 payments or fewer, within 12 months, no fees, to stay outside consumer credit rules).
- [ ] Evidence for "From September 2028, children in England as young as five will learn the fundamentals of money in school."
- [ ] Klaviyo double opt-in and welcome email.

## Content waiting on Peter
- [ ] Quick Debt Check screenshot with example debts, and a Risk Check screenshot.
- [ ] Cleaner workshop still (no browser bar) and a mid-quiz personality test screenshot.
- [ ] Platform credit card calculator: fix its interest maths (it divides APR by 12 and overstates interest) or keep it off the site.

## Optional copy fixes
- [ ] For-you card 1 opens "You earn well, but…", which echoes the hero tagline.
- [ ] Pricing says the personality test comes "with practical tips". Remove if there are none.
- [ ] Google description in `src/data/site.json` still opens "You earn well…".
