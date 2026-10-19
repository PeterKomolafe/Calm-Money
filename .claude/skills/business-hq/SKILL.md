---
name: business-hq
description: Refresh and look after Peter's HQ, his business dashboard (sales, 3-Night bookings, mailing list, YouTube, Instagram, to-do list, coming up). Use for the 7am morning refresh, when Peter asks for his numbers or to update the dashboard, or to add, tick or change his to-dos and dates.
---

# Peter's HQ

The dashboard: https://claude.ai/artifact/WkA6GQixmitLsqjdkxpyYt

The page reads everything from its own database, so updating numbers never needs a republish. Write with the `ArtifactData` tool on that url.

- `metrics/current`: one document with `updated`, `sales`, `bookings`, `list`, `youtube`, `instagram`, `upcoming`.
- `todos/<id>`: `{text, done, created, order}`. Peter ticks and adds these on the page.
- `deals/<id>`: `{name, kind ("Brand deal" or "Work"), value, currency ("GBP" or "AED"), stage, created, order}`. The Pipeline tile. Stages: Lead, In talks, Agreed, Delivering, then Done or Lost (hidden). Peter adds these on the page; add or move one when he asks. Never invent a value.
- `history/<YYYY-MM-DD>`: one small document per day `{youtube, instagram, list}`, used for growth figures.

## Morning refresh (7am, every day)

1. Stripe and Klaviyo: `python3 .claude/scripts/hq_numbers.py` prints `updated`, `sales`, `bookings`, `list`.
2. YouTube: `vidiq_user_channels` (free) gives Conversation of Money's `subscriberCount`. `gained30` = today minus the `history` document from 30 days ago. If there's no history that old yet, use `vidiq_channel_stats` for the last 30 days (5 credits) and take `growth.subscribersGained`.
3. Instagram: `vidiq_ig_profile` for `conversationofmoney` (5 credits) gives followers. Set `instagram.note` to the change since yesterday's `history` document (for example "+40 since yesterday"); with no history, "Growth shows from tomorrow".
4. Read `metrics/current` and write it back with `update`, pinned to the version you read: the new `updated`, `sales`, `bookings`, `list`, `youtube: {subs, gained30}`, `instagram: {followers, note}`. Drop `upcoming` entries whose date has passed. Keep the rest.
5. `set` `history/<today>`.
6. Stop. Don't message Peter unless something failed. If a source fails, keep yesterday's figure and say so in that tile's note ("Stripe didn't answer, figure from yesterday").

## Rules

- Numbers come only from the sources above. Never estimate or round up. Payments under £1 are test payments and are not counted.
- Calm Money members are on the learning platform, which isn't connected. Don't show a figure for it unless Peter gives one.
- Dates in UK style ("Tue 3 Nov"). No em dashes. Always "Peter".
- To-dos: add or change them when Peter asks, or when a session agrees a task with him. Never delete one he added without being asked.
- Never send emails, change Stripe or change Klaviyo from this skill. It only reads them.
