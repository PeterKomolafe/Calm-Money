#!/usr/bin/env python3
"""Peter's HQ: today's Stripe and Klaviyo numbers for the dashboard, as JSON on stdout.

The API keys are added by the environment's network secrets, so they never appear here.
YouTube and Instagram come from the vidIQ connector, which the HQ session calls itself.

  python3 .claude/scripts/hq_numbers.py
"""
import datetime, json, subprocess, sys
from zoneinfo import ZoneInfo

UK = ZoneInfo('Europe/London')
THREE_NIGHT_LINK = 'plink_1UOZJFGYq0laa7Atf46h4C8o'   # 3-Night Money Plan payment link
MAIN_LIST = 'SjUbWK'                                   # Klaviyo "Main List"
TEST_UNDER = 100                                       # payments under £1 are test payments (the 47p code)


def stripe(path):
    out = subprocess.run(['curl', '-g', '-sS', '-m', '30', 'https://api.stripe.com/v1/' + path], capture_output=True, text=True).stdout
    d = json.loads(out)
    if 'error' in d:
        sys.exit('Stripe: ' + d['error'].get('message', 'error'))
    return d


def stripe_all(path):
    res, after = [], None
    while True:
        d = stripe(path + (f'&starting_after={after}' if after else ''))
        res += d['data']
        if not d.get('has_more'):
            return res
        after = d['data'][-1]['id']


def klaviyo(path):
    out = subprocess.run(['curl', '-g', '-sS', '-m', '30', 'https://a.klaviyo.com/api/' + path, '-H', 'revision: 2025-07-15',
                          '-H', 'accept: application/vnd.api+json'], capture_output=True, text=True).stdout
    return json.loads(out)


def month_start(d):
    return d.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


now = datetime.datetime.now(UK)
this_m = month_start(now)
prev_m = month_start(this_m - datetime.timedelta(days=1))
ts = lambda d: int(d.timestamp())

pis = [p for p in stripe_all(f'payment_intents?limit=100&created[gte]={ts(prev_m)}') if p['status'] == 'succeeded' and p['amount_received'] >= TEST_UNDER]
this = [p for p in pis if p['created'] >= ts(this_m)]
prev = [p for p in pis if p['created'] < ts(this_m)]

sessions = [s for s in stripe_all('checkout/sessions?limit=100&status=complete') if s.get('payment_link') == THREE_NIGHT_LINK]
paid = [s for s in sessions if (s['amount_total'] or 0) >= TEST_UNDER]
tests = len(sessions) - len(paid)

lst = klaviyo(f'lists/{MAIN_LIST}/?additional-fields[list]=profile_count')['data']['attributes']

print(json.dumps({
    'updated': now.isoformat(timespec='minutes'),
    'sales': {'total': round(sum(p['amount_received'] for p in this) / 100, 2), 'count': len(this),
              'prevLabel': prev_m.strftime('%b'), 'prevTotal': round(sum(p['amount_received'] for p in prev) / 100, 2)},
    'bookings': {'paid': len(paid), 'revenue': round(sum(s['amount_total'] for s in paid) / 100, 2),
                 'note': (f'Plus {tests} test payment{"s" if tests != 1 else ""}, not counted' if tests else f'£{sum(s["amount_total"] for s in paid) / 100:,.2f} taken'),
                 },
    'list': {'count': lst['profile_count'], 'note': 'Klaviyo Main List'},
}, indent=1))
