#!/usr/bin/env python3
"""Talks only to the Klaviyo API (https://a.klaviyo.com/api/). The key is added by the
environment's network secret, so it never appears here.

  klaviyo.py request METHOD PATH [BODY.json]   one API call, e.g. GET lists/
  klaviyo.py members LIST_ID OUT.json           every profile on a list, with email consent
  klaviyo.py relate add|remove LIST_ID IDS.json add or remove profiles (JSON array of ids), 500 at a time
"""
import json, subprocess, sys, time

BASE = 'https://a.klaviyo.com/api/'

def call(method, path, body=None):
    url = path if path.startswith(BASE) else BASE + path.lstrip('/')
    if not url.startswith(BASE):
        sys.exit('Only https://a.klaviyo.com/api/ is allowed')
    cmd = ['curl', '-sS', '-m', '60', '-X', method, url, '-H', 'revision: 2025-07-15',
           '-H', 'accept: application/vnd.api+json', '-H', 'content-type: application/vnd.api+json',
           '-w', '\n%{http_code}']
    if body is not None:
        cmd += ['--data', json.dumps(body)]
    for _ in range(10):
        out = subprocess.run(cmd, capture_output=True, text=True).stdout
        text, code = out.rsplit('\n', 1)
        if code == '429':
            time.sleep(2)
            continue
        return code, (json.loads(text) if text.strip() else None)
    sys.exit('Rate limited too many times')

def main(a):
    if a[0] == 'request':
        body = json.load(open(a[3])) if len(a) > 3 else None
        code, data = call(a[1].upper(), a[2], body)
        print(code)
        print(json.dumps(data, indent=1) if data else '')
    elif a[0] == 'members':
        res, url = {}, f'lists/{a[1]}/profiles/?additional-fields%5Bprofile%5D=subscriptions&fields%5Bprofile%5D=subscriptions&page%5Bsize%5D=100'
        while url:
            code, d = call('GET', url)
            for p in d['data']:
                m = ((p['attributes'].get('subscriptions') or {}).get('email') or {}).get('marketing') or {}
                res[p['id']] = {'consent': m.get('consent'), 'can_email': bool(m.get('can_receive_email_marketing'))}
            url = d['links'].get('next')
            time.sleep(0.2)
        json.dump(res, open(a[2], 'w'))
        print(len(res), 'profiles saved to', a[2])
    elif a[0] == 'relate':
        method = {'add': 'POST', 'remove': 'DELETE'}[a[1]]
        ids = json.load(open(a[3]))
        for i in range(0, len(ids), 500):
            chunk = ids[i:i + 500]
            code, d = call(method, f'lists/{a[2]}/relationships/profiles/', {'data': [{'type': 'profile', 'id': x} for x in chunk]})
            print(a[1], len(chunk), 'profiles:', code)
            if code not in ('200', '202', '204'):
                sys.exit(json.dumps(d))
    else:
        sys.exit(__doc__)

main(sys.argv[1:])
