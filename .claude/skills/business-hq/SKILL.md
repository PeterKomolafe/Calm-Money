---
name: business-hq
description: Refresh and look after Peter's HQ, his business dashboard (sales, 3-Night bookings, unpaid invoices, mailing list, YouTube, Instagram, to-do list, coming up). Use for the 7am morning refresh, when Peter asks for his numbers or to update the dashboard, or to add, tick or change his to-dos and dates.
---

# Peter's HQ

The dashboard: https://claude.ai/artifact/WkA6GQixmitLsqjdkxpyYt

The page reads everything from its own database, so updating numbers never needs a republish. Write with the `ArtifactData` tool on that url.

- `metrics/current`: one document with `updated`, `sales`, `bookings`, `list`, `youtube`, `instagram`, `upcoming`.
- `todos/<id>`: `{text, done, created, order}`. Peter ticks and adds these on the page.
- `history/<YYYY-MM-DD>`: one small document per day `{youtube, instagram, list}`, used for growth figures.

## Morning refresh (7am, every day)

1. Stripe and Klaviyo: `python3 .claude/scripts/hq_numbers.py` prints `updated`, `sales`, `bookings`, `list`.
2. YouTube: `vidiq_user_channels` (free) gives Conversation of Money's `subscriberCount`. `gained30` = today minus the `history` document from 30 days ago. If there's no history that old yet, use `vidiq_channel_stats` for the last 30 days (5 credits) and take `growth.subscribersGained`.
3. Instagram: `vidiq_ig_profile` for `conversationofmoney` (5 credits) gives followers. Set `instagram.note` to the change since yesterday's `history` document (for example "+40 since yesterday"); with no history, "Growth shows from tomorrow".
4. Zoho Books (the "ZohoBooks_Mine" connector, read-only): `ZohoBooks_list_invoices` with `organization_id: ""` (blank uses Peter's organisation, Conversation of Money Ltd), `status: "unpaid"`, `per_page: 200`. Build `invoices: {total, count, overdueCount, overdueTotal, items}`, where each item is `{customer, number, amount, due, dueText, overdue}` (`due` is the due date as yyyy-mm-dd; the page uses it for the "Needs you" list). `amount` is the invoice's `balance`. `dueText` is "Overdue N days (was due 8 Oct)" when overdue, else the due date ("Wed 21 Oct"). Sort with overdue first, then by due date. Never call any Zoho tool that changes anything. If any are added to the connector, leave them alone.
   UAE: the same again with the "ZohoBooksUAE" connector and `organization_id: "938313218"` (Moneytelligence Services FZCO, invoices in AED), saved as `invoicesUAE` in the same shape. Keep AED separate: never convert it or add it to the £ total. That login also holds an organisation called "Conversation of Money Ltd" (939976654), which isn't the live UK books. Ignore it.
4b. YouTube analytics, **Mondays only** (10 credits; YouTube's figures lag 2 to 3 days anyway): `vidiq_channel_analytics` for channel `UChG3TKNbIc7PzOqd2S31RdA`, once for the 28 days ending 2 days ago and once for the 28 days before that, with metrics views, engagedViews, subscribersGained, subscribersLost, estimatedRevenue. Save `youtube28: {from, to, toText ("18 Oct"), views, engaged, engagedPrev, gained, lost, net, netPrev, revenue, revenuePrev, currency: "USD"}`. Revenue comes back in US dollars. Peter wants it shown in pounds: look up that day's USD to GBP mid-market rate (a web search; if two sources disagree, use the lower figure), then save `revenueGbp` and `revenuePrevGbp` (dollars times the rate, to 2 decimals), `fxRate`, and `fxText` such as "about £0.75 per $1 on 19 Oct". Keep `revenue` and `revenuePrev` in dollars too, because the page shows the dollar figure as the source. Compare engaged views, not views: YouTube changed how it counts views on 27 Aug 2026, so raw views across that date aren't comparable. On other days, leave `youtube28` as it is.
5. Read `metrics/current` and write it back with `update`, pinned to the version you read: the new `updated`, `sales`, `bookings`, `list`, `youtube: {subs, gained30}`, `instagram: {followers, note}`, `invoices`, `invoicesUAE`, and `youtube28` on Mondays. Drop `upcoming` entries whose date has passed. Keep the rest.
6. `set` `history/<today>`.
7. Stop. Don't message Peter unless something failed. If a source fails, keep yesterday's figure and say so in that tile's note ("Stripe didn't answer, figure from yesterday").

## Rules

- Numbers come only from the sources above. Never estimate or round up. Payments under £1 are test payments and are not counted.
- Calm Money members are on the learning platform, which isn't connected. Don't show a figure for it unless Peter gives one.
- Dates in UK style ("Tue 3 Nov"). No em dashes. Always "Peter".
- To-dos: add or change them when Peter asks, or when a session agrees a task with him. Never delete one he added without being asked.
- Never send emails, change Stripe, change Klaviyo or change Zoho Books from this skill. It only reads them.
