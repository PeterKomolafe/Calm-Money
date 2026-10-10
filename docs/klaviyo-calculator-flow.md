# Klaviyo: calculator result email

When someone asks for their result, the site sends two things to Klaviyo:

1. A **"Calculated goal"** event with their result. This triggers the email.
2. A sign-up to the **calculator list (VG43J7)**, so they get Peter's emails afterwards.

The event appears in Klaviyo after the first real sign-up. Do one test on the live site with your own email first, then build the flow.

## Build the flow (about 15 minutes)

1. **Flows > Create flow > Build your own.** Name it "Calculator result".
2. **Trigger:** Metric > **Calculated goal**.
3. Add a **Trigger split** on the property `goal`:
   - `goal` equals `debt` → Email 1
   - otherwise, add a second Trigger split: `goal` equals `secure` → Email 2, otherwise → Email 3
4. Put one email on each branch, with no delay. Turn **Smart Sending off** on all three, so they always send (people asked for them).
5. Turn the flow **Live**.

Sign off each email as Peter. The links go to the pricing on the site.

**Ready-made templates:** `docs/klaviyo/calculator-debt.html`, `calculator-secure.html` and `calculator-wealth.html`. In Klaviyo go to **Templates > Create template > Code your own**, paste one in and save it. Then pick that template for the matching email in the flow and add the subject line below. The copy below is the same as in the templates.

## Email 1: Debt free (`goal` = debt)

**Subject:** Debt free by {{ event.date }}

**Preview text:** And the first thing to do today.

> Hi,
>
> Here's the date you asked for.
>
> **You could be debt free by {{ event.date }}.**
>
> {{ event.note }}
>
> That interest is money you've already earned, going to someone else. The sooner the debt goes, the more of it you keep.
>
> **Your first step**
>
> {{ event.first_step }}
>
> **What gets you there**
>
> Paying {{ event.monthly }} every month, without missing one, until {{ event.date }}. Most people don't miss because they don't care. They miss because life happens: a big bill, a birthday, a tough month. Willpower won't carry you that far. A system will.
>
> That's what Calm Money builds with you: a plan for every debt, a way to stop new borrowing creeping back, and the safety net that means one bad month doesn't undo your progress.
>
> [See how Calm Money works](https://www.calmmoneycommunity.com/#pricing)
>
> Peter
>
> *This is an estimate. It assumes a fixed interest rate and no new borrowing. It is not financial advice.*

## Email 2: Safety net (`goal` = secure)

**Subject:** Your safety net by {{ event.date }}

**Preview text:** And the first thing to do today.

> Hi,
>
> Here's the date you asked for.
>
> **{{ event.headline }} {{ event.date }}.**
>
> {{ event.note }}
>
> That's the point where a broken boiler or a quiet month at work is an inconvenience, not a crisis.
>
> **Your first step**
>
> {{ event.first_step }}
>
> **What gets you there**
>
> Saving {{ event.monthly }} every month, without dipping into it, until {{ event.date }}. The hard part isn't saving. It's leaving it alone when something comes up. Willpower won't carry you that far. A system will.
>
> That's what Calm Money builds with you: your savings set up to run on their own, the right amount for your life, and a clear next step once your safety net is in place.
>
> [See how Calm Money works](https://www.calmmoneycommunity.com/#pricing)
>
> Peter
>
> *This is an estimate based on your essential monthly costs. It is not financial advice.*

## Email 3: Investing (`goal` = wealth)

**Subject:** Your first £10,000 invested by {{ event.date }}

**Preview text:** And the first thing to do today.

> Hi,
>
> Here's the date you asked for.
>
> **You could have your first £10,000 invested by {{ event.date }}.**
>
> {{ event.note }}
>
> That date only counts what you put in. It doesn't count any growth, so think of it as the point where your money starts working for you, not the finish line.
>
> **Your first step**
>
> {{ event.first_step }}
>
> **What gets you there**
>
> Investing {{ event.monthly }} every month, including the months when the news is bad and the value drops, until {{ event.date }}. Staying steady is what makes the difference, and it's the part most people find hardest. Willpower won't carry you that far. A system will.
>
> That's what Calm Money builds with you: knowing your debt and safety net are sorted first, understanding what you're investing in, and having support from me when you have questions.
>
> [See how Calm Money works](https://www.calmmoneycommunity.com/#pricing)
>
> Peter
>
> *This counts the money you put in, not investment growth. The value of investments can go down as well as up and you may get back less than you put in. This is not financial advice.*

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
