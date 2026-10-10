# Klaviyo: calculator result email

When someone asks for their result, the site sends two things to Klaviyo:

1. A **"Calculated goal"** event with their result. This triggers the email.
2. A sign-up to the **calculator list (VG43J7)**, so they get Peter's emails afterwards.

The event appears in Klaviyo after the first real sign-up. Do one test on the live site with your own email first, then build the flow.

## Build the flow (about 10 minutes)

1. **Flows > Create flow > Build your own.** Name it "Calculator result".
2. **Trigger:** Metric > **Calculated goal**.
3. **Flow filter:** none. Leave "Smart Sending" **off** on the email, so it always sends (they asked for it).
4. Add an **Email** straight after the trigger (no delay).
5. Turn the flow **Live**.

## The email

**Subject:** Your date: {{ event.date }}

**Preview text:** Here's your first step.

**Body:**

> Hi,
>
> {{ event.headline }}
>
> **{{ event.date }}**
>
> {{ event.note }}
>
> **Your first step**
>
> {{ event.first_step }}
>
> Getting there depends on putting {{ event.monthly }} aside every month for {{ event.months }} months. Willpower won't carry you that far. A system will.
>
> That's what Calm Money builds with you.
>
> [Join Calm Money](https://www.calmmoneycommunity.com/#pricing)
>
> Peter
>
> *This is an estimate, not financial advice.*

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
