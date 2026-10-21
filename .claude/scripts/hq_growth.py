#!/usr/bin/env python3
"""Peter's HQ, Growth section: month-by-month figures from Stripe and Klaviyo, as JSON on stdout.

For every month from Jan 2026 to now:
  - sales: all Stripe payments (total, count), test payments under £1 left out
  - calmMoney: Calm Money revenue (same rules as hq_numbers.py)
  - bookings: paid 3-Night Money Plan bookings
  - listJoined: people on the Klaviyo Main List today who joined that month
  - list28 (top level): Main List sign-ups in the last 28 days and the 28 days before
  - listEnd: Main List size at the end of the month, counting only people still on it today
    (Klaviyo keeps no record of people who have left, so earlier months read a little low)

YouTube, Instagram and invoices come from the connectors, which the HQ session calls itself.

  python3 .claude/scripts/hq_growth.py
"""
import datetime, json, subprocess, sys, time, urllib.parse
from zoneinfo import ZoneInfo

UK = ZoneInfo('Europe/London')
THREE_NIGHT_LINK = 'plink_1UOZJFGYq0laa7Atf46h4C8o'
MAIN_LIST = 'SjUbWK'
TEST_UNDER = 100
START = datetime.datetime(2026, 1, 1, tzinfo=UK)


def stripe_all(path):
    res, after = [], None
    while True:
        out = subprocess.run(['curl', '-g', '-sS', '-m', '30', 'https://api.stripe.com/v1/' + path + (f'&starting_after={after}' if after else '')],
                             capture_output=True, text=True).stdout
        d = json.loads(out)
        if 'error' in d:
            sys.exit('Stripe: ' + d['error'].get('message', 'error'))
        res += d['data']
        if not d.get('has_more'):
            return res
        after = d['data'][-1]['id']


def klaviyo(url):
    for attempt in range(8):
        out = subprocess.run(['curl', '-g', '-sS', '-m', '30', url, '-H', 'revision: 2025-07-15', '-H', 'accept: application/vnd.api+json'],
                             capture_output=True, text=True).stdout
        d = json.loads(out)
        if 'data' in d:
            return d
        time.sleep(2 + attempt * 2)
    sys.exit('Klaviyo: ' + json.dumps(d.get('errors', d))[:300])


now = datetime.datetime.now(UK)
key = lambda t: datetime.datetime.fromtimestamp(t, UK).strftime('%Y-%m')
months = []
m = START
while m <= now:
    months.append(m.strftime('%Y-%m'))
    m = (m + datetime.timedelta(days=32)).replace(day=1)
row = {k: {'month': k, 'sales': {'total': 0, 'count': 0}, 'calmMoney': 0, 'bookings': 0, 'listJoined': 0} for k in months}
s0 = int(START.timestamp())

# Stripe sales
for p in stripe_all(f'payment_intents?limit=100&created[gte]={s0}'):
    if p['status'] == 'succeeded' and p['amount_received'] >= TEST_UNDER and key(p['created']) in row:
        r = row[key(p['created'])]['sales']; r['total'] += p['amount_received']; r['count'] += 1

# Calm Money and 3-Night bookings (rules as in hq_numbers.py)
sess = stripe_all(f'checkout/sessions?limit=100&status=complete&created[gte]={s0}')
plan_customers = {c.get('customer') for c in sess if (c.get('metadata') or {}).get('plan') == 'coaching-payment-plan' and c.get('customer')}
for c in sess:
    md = c.get('metadata') or {}
    amt = c['amount_total'] or 0
    if amt < TEST_UNDER or key(c['created']) not in row:
        continue
    if md.get('plan') in ('at-your-pace', 'coaching-full') or md.get('type') == 'learner_payment':
        row[key(c['created'])]['calmMoney'] += amt
    if c.get('payment_link') == THREE_NIGHT_LINK:
        row[key(c['created'])]['bookings'] += 1
for p in stripe_all(f'payment_intents?limit=100&created[gte]={s0}'):
    md = p.get('metadata') or {}
    if p['status'] != 'succeeded' or p['amount_received'] < TEST_UNDER or key(p['created']) not in row:
        continue
    if md.get('type') == 'second_instalment' or (p.get('customer') in plan_customers and (p.get('description') or '').startswith('Subscription')):
        row[key(p['created'])]['calmMoney'] += p['amount_received']

# Klaviyo Main List: when each current member joined
joined = []
url = f'https://a.klaviyo.com/api/lists/{MAIN_LIST}/profiles/?page[size]=100&fields[profile]=joined_group_at'
while url:
    d = klaviyo(url)
    joined += [x['attributes'].get('joined_group_at') for x in d['data'] if x['attributes'].get('joined_group_at')]
    url = (d.get('links') or {}).get('next')
jm = [j[:7] for j in joined]
for k in months:
    row[k]['listJoined'] = sum(1 for j in jm if j == k)
    row[k]['listEnd'] = sum(1 for j in jm if j <= k)

# Main List sign-ups over the last 28 days (today included) and the 28 days before, for the Mailing list tile
today = now.date()
d28 = lambda n: today - datetime.timedelta(days=n)
jd = [datetime.datetime.fromisoformat(j.replace('Z', '+00:00')).astimezone(UK).date() for j in joined]
list28 = {'joined': sum(1 for d in jd if d28(27) <= d <= today), 'joinedPrev': sum(1 for d in jd if d28(55) <= d <= d28(28)),
          'from': d28(27).isoformat(), 'to': today.isoformat(), 'prevFrom': d28(55).isoformat(), 'prevTo': d28(28).isoformat()}

out = []
for k in months:
    r = row[k]
    r['sales'] = {'total': round(r['sales']['total'] / 100, 2), 'count': r['sales']['count']}
    r['calmMoney'] = round(r['calmMoney'] / 100, 2)
    out.append(r)
print(json.dumps({'updated': now.isoformat(timespec='minutes'), 'listMembersNow': len(joined), 'list28': list28, 'months': out}, indent=1))
