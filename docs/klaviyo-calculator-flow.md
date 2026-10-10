# Klaviyo: calculator result email

When someone asks for their result, the site sends two things to Klaviyo:

1. A **"Calculated goal"** event with their result. This triggers the email.
2. A sign-up to the **calculator list (VG43J7)**, so they get Peter's emails afterwards.

The event appears in Klaviyo after the first real sign-up. Do one test on the live site with your own email first, then build the flow.

## Build the flow (about 15 minutes)

1. **Flows > Create flow > Build your own.** Name it "Calculator result".
2. **Trigger:** Metric > **Calculated goal**.
3. Add a **Split** with path criteria **Properties of Calculated goal**:
   - `goal` equals `debt` → Debt free email
   - Everyone else → a second Split: `goal` equals `secure` → Safety net email, Everyone else → Investing email
4. Put one email on each branch, with no delay. Turn **Smart Sending off** on all three, so they always send (people asked for them).
5. Turn the flow **Live**.

Sign off each email as Peter. The links go to the pricing on the site.

**Templates:** `docs/klaviyo/calculator-debt.html`, `calculator-secure.html` and `calculator-wealth.html` hold the final emails (design 4, a letter from Peter). Paste each whole file into its email's HTML editor in Klaviyo. They load Peter's photo from `www.calmmoneycommunity.com/images/email/peter.jpg`, so that file must be live.

| Email | Subject | Preview text |
|---|---|---|
| Debt free (`goal` = debt) | Debt free by {{ event.date }} | And the first thing to do today. |
| Safety net (`goal` = secure) | Your safety net by {{ event.date }} | And the first thing to do today. |
| Investing (`goal` = wealth) | Your first £10,000 invested by {{ event.date }} | And the first thing to do today. |

## What each field holds

| Field | Example |
|---|---|
| `event.goal` | debt, secure or wealth |
| `event.headline` | You could be debt free by |
| `event.date` | January 2030 |
| `event.note` | That's 3 years and 3 months away, with roughly £3,112 paid in interest. |
| `event.months` | 39 |
| `event.monthly` | £300 |
| `event.first_step` | Write down every debt with its balance, interest rate and minimum payment. |

## Check in Klaviyo

- **List VG43J7 opt-in:** if it's double opt-in, people get a confirm email as well as the result. Single opt-in avoids two emails at once.
- The site says "One email with your date, then occasional emails from Peter." Make sure that matches what you'll actually send.
