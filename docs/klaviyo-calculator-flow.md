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

**Template:** `docs/klaviyo/calculator-forecast.html` is the money forecast email (design 4, a letter from Peter). It works for every result, so paste the whole file into the HTML editor of **all three** branch emails. The debt paragraph only shows when `goal` is debt, and the "Clear skies" row only shows when they have debt. It loads Peter's photo from `www.calmmoneycommunity.com/images/email/peter.jpg`, so that file must be live.

Use the same subject and preview text on all three:

| Subject | Preview text |
|---|---|
| Your money forecast: sunny by {{ event.sunny }} | And the one thing to do this week. |

The older per-goal templates (`calculator-debt.html`, `calculator-secure.html`, `calculator-wealth.html`) are kept for reference but no longer match the forecast.

## What each field holds

| Field | Example |
|---|---|
| `event.goal` | First milestone: debt, secure or wealth |
| `event.headline` | The headline shown on the site |
| `event.date` | First milestone date, e.g. January 2030 |
| `event.note` | That's 3 years and 3 months away, with roughly £3,112 paid in interest. |
| `event.months` | 39 |
| `event.monthly` | £300 |
| `event.first_step` | Write down every debt with its balance, interest rate and minimum payment. |
| `event.debt_free` | Debt free date, e.g. January 2030 (empty if no debt) |
| `event.safety_net` | 3-month safety net date, e.g. October 2030 |
| `event.sunny` | First £10,000 invested date, e.g. April 2033 |
| `event.card_image` | Link to a picture of their forecast card, e.g. https://www.calmmoneycommunity.com/card/….jpg (empty if it couldn't be made) |
| `event.forecast_headline`, `event.forecast_sub`, `event.days` | The card's headline, the line under it and the four days, used if there's no picture |

**The card picture:** when someone clicks "Send it", the site draws their card at email width in a hidden frame (`src/pages/forecast-card.astro`), at the end of the forecast and without the play button, takes a picture and stores it on Netlify (`netlify/functions/forecast-card.mjs`). Pictures are deleted after 12 months (`forecast-card-cleanup.mjs`), so the card in emails older than that no longer shows.

## Check in Klaviyo

- **List VG43J7 opt-in:** if it's double opt-in, people get a confirm email as well as the result. Single opt-in avoids two emails at once.
- The site says "One email with your forecast, then occasional emails from Peter." Make sure that matches what you will actually send.
