#!/usr/bin/env python3
"""Peter's HQ: today's Stripe and Klaviyo numbers for the dashboard, as JSON on stdout.

The API keys are added by the environment's network secrets, so they never appear here.
YouTube and Instagram come from the vidIQ connector, which the HQ session calls itself.

  python3 .claude/scripts/hq_numbers.py
"""
import datetime, json, subprocess, sys, time
from zoneinfo import ZoneInfo

UK = ZoneInfo('Europe/London')
import os
# refunded payments (the Stripe key can't read refunds), see hq_refunds.json
REFUNDED = {r['payment_intent'] for r in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hq_refunds.json')))['refunded']}
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
    for attempt in range(8):  # Klaviyo allows only a few list-size lookups per second, so wait and retry when throttled
        out = subprocess.run(['curl', '-g', '-sS', '-m', '30', 'https://a.klaviyo.com/api/' + path, '-H', 'revision: 2025-07-15',
                              '-H', 'accept: application/vnd.api+json'], capture_output=True, text=True).stdout
        d = json.loads(out)
        if 'data' in d:
            return d
        time.sleep(2 + attempt * 2)
    sys.exit('Klaviyo: ' + json.dumps(d.get('errors', d))[:300])


def month_start(d):
    return d.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


now = datetime.datetime.now(UK)
this_m = month_start(now)
prev_m = month_start(this_m - datetime.timedelta(days=1))
ts = lambda d: int(d.timestamp())

pis = [p for p in stripe_all(f'payment_intents?limit=100&created[gte]={ts(prev_m)}') if p['status'] == 'succeeded' and p['amount_received'] >= TEST_UNDER and p['id'] not in REFUNDED]
this = [p for p in pis if p['created'] >= ts(this_m)]
prev = [p for p in pis if p['created'] < ts(this_m)]

sessions = [s for s in stripe_all('checkout/sessions?limit=100&status=complete') if s.get('payment_link') == THREE_NIGHT_LINK]
paid = [s for s in sessions if (s['amount_total'] or 0) >= TEST_UNDER and s.get('payment_intent') not in REFUNDED]
refunded = [s for s in sessions if s.get('payment_intent') in REFUNDED]
tests = len(sessions) - len(paid) - len(refunded)

# Calm Money revenue, all time. Three kinds of payment count:
#  - learning-platform payments (founders): checkout sessions with metadata type "learner_payment" (paid in full or a
#    first instalment), plus payments with metadata type "second_instalment" (those have no checkout session)
#  - website checkouts paid in one go: checkout session metadata plan "at-your-pace" or "coaching-full"
#  - the coaching payment plan: subscription payments from customers who checked out with plan "coaching-payment-plan"
#    (this key can't read invoices, so plan instalments are matched by customer and the "Subscription" payment description)
# If any of it fails, the refresh carries on and the card keeps yesterday's figure.
calm = None
try:
    CM_START = ts(datetime.datetime(2026, 1, 1, tzinfo=UK))
    cm = []  # (created, pence, payer)
    sess = stripe_all(f'checkout/sessions?limit=100&status=complete&created[gte]={CM_START}')
    plan_customers = {c.get('customer') for c in sess if (c.get('metadata') or {}).get('plan') == 'coaching-payment-plan' and c.get('customer')}
    for c in sess:
        m = c.get('metadata') or {}
        if (m.get('plan') in ('at-your-pace', 'coaching-full') or m.get('type') == 'learner_payment') and (c['amount_total'] or 0) >= TEST_UNDER:
            cm.append((c['created'], c['amount_total'], m.get('user_id') or c.get('customer') or (c.get('customer_details') or {}).get('email') or c['id']))
    for p in stripe_all(f'payment_intents?limit=100&created[gte]={CM_START}'):
        m = p.get('metadata') or {}
        if p['status'] != 'succeeded' or p['amount_received'] < TEST_UNDER or p['id'] in REFUNDED:
            continue
        if m.get('type') == 'second_instalment':
            cm.append((p['created'], p['amount_received'], m.get('user_id') or p.get('customer') or p['id']))
        elif p.get('customer') in plan_customers and (p.get('description') or '').startswith('Subscription'):
            cm.append((p['created'], p['amount_received'], p['customer']))
    calm = {'total': round(sum(x[1] for x in cm) / 100, 2), 'payments': len(cm), 'payers': len({x[2] for x in cm}),
            'thisMonth': round(sum(x[1] for x in cm if x[0] >= ts(this_m)) / 100, 2),
            'prevMonth': round(sum(x[1] for x in cm if ts(prev_m) <= x[0] < ts(this_m)) / 100, 2), 'prevLabel': prev_m.strftime('%b')}
except BaseException as e:  # stripe() exits on an API error; don't let that stop the other numbers
    print('Calm Money revenue skipped: ' + str(e), file=sys.stderr)

lst = klaviyo(f'lists/{MAIN_LIST}/?additional-fields[list]=profile_count')['data']['attributes']

# every list with its size, biggest first, for the mailing list card's details
lists, url = [], 'lists/?fields[list]=name'
while url:
    d = klaviyo(url)
    for x in d['data']:
        c = klaviyo(f"lists/{x['id']}/?additional-fields[list]=profile_count")['data']['attributes'].get('profile_count') or 0
        if c:
            lists.append({'name': x['attributes']['name'], 'count': c})
    nxt = (d.get('links') or {}).get('next')
    url = nxt.split('/api/', 1)[1] if nxt else None
lists.sort(key=lambda x: -x['count'])

# content queue: scheduled emails (soonest first) and recent unscheduled drafts, which get flagged
import urllib.parse
def campaigns(status):
    f = urllib.parse.quote(f"and(equals(messages.channel,'email'),equals(status,'{status}'))")
    return klaviyo(f"campaigns/?filter={f}&fields[campaign]=name,send_time,updated_at")['data']
queue = []
for c in campaigns('Scheduled'):
    t = datetime.datetime.fromisoformat(c['attributes']['send_time']).astimezone(UK)
    queue.append({'when': t.isoformat(), 'dateText': t.strftime('%a %-d %b, %-I:%M%p').replace(':00', '').replace('AM', 'am').replace('PM', 'pm'),
                  'channel': 'Email', 'title': c['attributes']['name'], 'draft': False})
queue.sort(key=lambda x: x['when'])
recent = now - datetime.timedelta(days=21)
for c in campaigns('Draft'):
    u = c['attributes'].get('updated_at')
    if u and datetime.datetime.fromisoformat(u) >= recent:
        queue.insert(0, {'when': '', 'dateText': '', 'channel': 'Email', 'title': c['attributes']['name'], 'draft': True})

# each Stripe payment this month, named by what it was for (no customer details), so Peter can remove one on the page
def label_for(p):
    try:
        cs = stripe(f"checkout/sessions?payment_intent={p['id']}&limit=1")['data']
    except BaseException:
        cs = []
    c = cs[0] if cs else {}
    m = {**(c.get('metadata') or {}), **(p.get('metadata') or {})}
    if c.get('payment_link') == THREE_NIGHT_LINK: return '3-Night Money Plan booking'
    if m.get('type') in ('learner_payment', 'second_instalment') or m.get('plan') in ('at-your-pace', 'coaching-full', 'coaching-payment-plan'):
        return 'Calm Money' + (' (' + m['plan'].replace('-', ' ') + ')' if m.get('plan') else '')
    if (p.get('description') or '').startswith('Subscription'): return 'Subscription payment'
    return p.get('description') or 'Stripe payment'
sale_items = [{'id': p['id'], 'amount': round(p['amount_received'] / 100, 2), 'date': datetime.datetime.fromtimestamp(p['created'], UK).strftime('%Y-%m-%d'), 'label': label_for(p)} for p in sorted(this, key=lambda p: p['created'])]

print(json.dumps({
    'updated': now.isoformat(timespec='minutes'),
    'sales': {'total': round(sum(p['amount_received'] for p in this) / 100, 2), 'count': len(this), 'items': sale_items,
              'prevLabel': prev_m.strftime('%b'), 'prevTotal': round(sum(p['amount_received'] for p in prev) / 100, 2)},
    'bookings': {'paid': len(paid), 'revenue': round(sum(s['amount_total'] for s in paid) / 100, 2),
                 'note': ' · '.join(x for x in [f'{len(refunded)} refunded' if refunded else '', f'Plus {tests} test payment{"s" if tests != 1 else ""}, not counted' if tests else ''] if x) or f'£{sum(s["amount_total"] for s in paid) / 100:,.2f} taken',
                 },
    'list': {'count': lst['profile_count'], 'note': 'Klaviyo Main List', 'lists': lists},
    'queue': queue[:10],
    **({'calmMoney': calm} if calm else {}),
}, indent=1))
