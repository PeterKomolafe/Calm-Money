# Builds the five Money Personality Guides as A4 HTML, then PDF (via Playwright, see render.js).
import base64, html, math, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from content import TYPES, COMMON_CLOSE

here = pathlib.Path(__file__).parent
site = pathlib.Path('/home/user/Calm-Money/public')
b64 = lambda p: base64.b64encode(pathlib.Path(p).read_bytes()).decode()
e = html.escape

FONT = b64(site / 'fonts/Satoshi-Variable.woff2')
FONT_I = b64(site / 'fonts/Satoshi-VariableItalic.woff2')
PETER = b64(site / 'images/peter/peter.webp')
LOGO_DARK = b64(here / 'logo-dark.svg')  # the cover logo, lifted from the original guides
WORDMARK = b64(site / 'images/peter/wordmark.png')

# Calm Money ring, same geometry as the site logo
c, r, w = 50, 34.6, 13
cols = {'teal': '#557170', 'sage': '#7d9d90', 'blush': '#e6a89c', 'terracotta': '#b5695a', 'cream': '#f5e8d8'}
def pt(d):
    a = math.radians(d); return c + r * math.cos(a), c + r * math.sin(a)
def arc(f, t):
    x1, y1 = pt(f); x2, y2 = pt(t)
    return f'M {x1:.2f} {y1:.2f} A {r} {r} 0 {1 if t - f > 180 else 0} 1 {x2:.2f} {y2:.2f}'
segs = [(-72, 72, 'teal'), (72, 119, 'sage'), (119, 171, 'blush'), (171, 231, 'terracotta'), (231, 288, 'cream')]
caps = [(72, 'sage'), (119, 'blush'), (171, 'terracotta'), (231, 'cream'), (-72, 'teal')]
RING = ''.join(f'<path d="{arc(f, t)}" fill="none" stroke="{cols[k]}" stroke-width="{w}"/>' for f, t, k in segs)
RING += ''.join(f'<circle cx="{pt(a)[0]:.2f}" cy="{pt(a)[1]:.2f}" r="{w/2}" fill="{cols[k]}"/>' for a, k in caps)
ring = lambda cls: f'<svg class="{cls}" viewBox="0 0 100 100" aria-hidden="true">{RING}</svg>'

ORDINAL = ['one', 'two', 'three', 'four', 'five', 'six', 'seven']

CSS = """
@font-face { font-family: 'Satoshi'; src: url(data:font/woff2;base64,%(font)s) format('woff2'); font-weight: 300 900; font-style: normal; }
@font-face { font-family: 'Satoshi'; src: url(data:font/woff2;base64,%(font_i)s) format('woff2'); font-weight: 300 900; font-style: italic; }
@page { size: A4; margin: 0; }
:root {
  --teal: #557170; --teal-dark: #3e5553; --deep: #34494a; --sage: #7d9d90; --blush: #e6a89c;
  --terracotta: #b5695a; --terracotta-dark: #a0584a; --cream: #f5e8d8; --ink: #1f2624; --muted: #5b6664;
  --line: #e7e2db; --rule: #edf0ee;
  --accent: %(accent)s; --accent-ink: %(ink)s; --soft: %(soft)s;
}
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; background: #d9d6d1; }
body { font-family: 'Satoshi', system-ui, sans-serif; color: var(--ink); -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.page { position: relative; width: 210mm; height: 297mm; overflow: hidden; background: #fff; page-break-after: always; break-after: page; display: flex; flex-direction: column; padding: 18mm 20mm 16mm; }
.page:last-child { page-break-after: auto; break-after: auto; }
/* faint ledger grid, as on the Calm Money site */
.page.ledger::before { content: ''; position: absolute; inset: 0; z-index: 0; background-image: linear-gradient(to right, var(--rule) 1px, transparent 1px), linear-gradient(to bottom, var(--rule) 1px, transparent 1px); background-size: 26.25mm 26.25mm; }
.page > * { position: relative; z-index: 1; }
@media screen { body { padding: 24px 0; display: grid; gap: 24px; justify-content: center; } .page { box-shadow: 0 6px 24px rgb(0 0 0 / .18); } }

.head, .foot { display: flex; justify-content: space-between; align-items: center; font-size: 8.5pt; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: var(--muted); }
.head { padding-bottom: 5mm; border-bottom: 1px solid var(--line); margin-bottom: 14mm; }
.head .brand { display: flex; align-items: center; gap: 3mm; color: var(--teal-dark); }
.head .ring { width: 6mm; height: 6mm; }
.foot { margin-top: auto; padding-top: 5mm; border-top: 1px solid var(--line); font-weight: 500; }
.foot .n { font-variant-numeric: tabular-nums; color: var(--teal-dark); font-weight: 700; }

.eyebrow { margin: 0 0 4mm; font-size: 9pt; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: var(--terracotta-dark); }
h1 { margin: 0 0 6mm; font-size: 30pt; line-height: 1.05; letter-spacing: -0.03em; color: var(--teal-dark); font-weight: 700; text-wrap: balance; }
h1 .q { color: var(--accent-ink); }
.lede { font-size: 12.5pt; line-height: 1.5; color: var(--muted); max-width: 140mm; margin: 0 0 10mm; }
p { margin: 0 0 4.5mm; font-size: 11.5pt; line-height: 1.62; }
.cols { display: grid; grid-template-columns: 38mm 1fr; gap: 8mm; }
.label { font-size: 8.5pt; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: var(--accent-ink); padding-top: 1mm; }

/* cover */
.cover { background: #557170; color: var(--cream); padding: 16mm 18mm 14mm; }
.cover .top { display: flex; justify-content: space-between; align-items: center; }
.cover .brand { display: flex; align-items: center; gap: 3.5mm; font-size: 14pt; font-weight: 700; letter-spacing: -0.01em; }
.cover .logo { height: 13.4mm; width: auto; margin-left: -0.4mm; }
.cover .tag { font-size: 8.5pt; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; color: rgb(245 232 216 / .7); }
.cover .letter { position: absolute; right: -14mm; top: 34mm; font-size: 300pt; line-height: .8; font-weight: 800; color: rgb(245 232 216 / .06); letter-spacing: -0.05em; z-index: 0; }
.cover .type { margin: 26mm 0 6mm; display: inline-flex; align-items: center; gap: 3mm; font-size: 10pt; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; color: var(--blush); }
.cover .type i { width: 3.2mm; height: 3.2mm; border-radius: 50%%; background: var(--accent); box-shadow: 0 0 0 1.2px rgb(245 232 216 / .5); }
.cover h1 { color: var(--cream); font-size: 50pt; line-height: .98; margin: 0 0 9mm; max-width: 150mm; }
.cover h2 { margin: 0; font-size: 22pt; line-height: 1.18; font-weight: 500; letter-spacing: -0.02em; max-width: 110mm; color: #fff; }
.cover h2 em { font-style: normal; color: var(--blush); }
.cover .sub { margin-top: 6mm; font-size: 11pt; color: rgb(245 232 216 / .72); max-width: 92mm; }
.cover .photo { position: absolute; right: 8mm; bottom: 30mm; height: 118mm; width: auto; z-index: 1; }
.cover .bottom { margin-top: auto; display: flex; justify-content: space-between; align-items: center; padding-top: 6mm; border-top: 1px solid rgb(245 232 216 / .22); position: relative; z-index: 2; }
.byline { display: flex; align-items: center; gap: 3mm; font-size: 10pt; }
.byline img { width: 10mm; height: 10mm; border-radius: 50%%; object-fit: cover; border: 1.5px solid rgb(245 232 216 / .8); }
.byline .wm { display: block; height: 3.4mm; aspect-ratio: 467/57; background: var(--cream); -webkit-mask: url(data:image/png;base64,%(wordmark)s) center / contain no-repeat; mask: url(data:image/png;base64,%(wordmark)s) center / contain no-repeat; margin-bottom: 1.2mm; }
.byline small { display: block; font-size: 8pt; letter-spacing: .12em; text-transform: uppercase; color: rgb(245 232 216 / .7); }

/* statements checklist */
.checks { list-style: none; margin: 0; padding: 0; display: grid; gap: 4mm; }
.checks li { display: grid; grid-template-columns: 9mm 1fr; gap: 5mm; align-items: center; padding: 7mm 7mm; background: #fff; border: 1px solid var(--line); border-radius: 4mm; font-size: 12.5pt; line-height: 1.4; font-weight: 500; }
.checks .box { width: 8mm; height: 8mm; border-radius: 50%%; border: 2.4px solid var(--accent); }
.hint { margin-top: 8mm; font-size: 10.5pt; color: var(--muted); }

/* quote */
.quote { margin-top: 10mm; padding: 10mm 11mm; border-radius: 5mm; background: linear-gradient(180deg, #3d5453, #34494a 45%%); color: var(--cream); box-shadow: 0 8px 24px -8px rgb(31 38 36 / .35); }
.quote .mark { font-size: 40pt; line-height: .6; color: var(--blush); font-weight: 800; display: block; margin-bottom: 3mm; }
.quote p { font-size: 13pt; line-height: 1.6; font-style: italic; color: #f3ece2; margin: 0 0 5mm; }
.quote .by { font-size: 8.5pt; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: var(--blush); }

/* costs */
.grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 6mm; }
.cost { padding: 7mm; background: #fff; border: 1px solid var(--line); border-radius: 4mm; }
.cost h3, .step h3 { margin: 0 0 3mm; font-size: 12.5pt; line-height: 1.25; letter-spacing: -0.01em; color: var(--teal-dark); }
.cost p { font-size: 10.5pt; line-height: 1.55; margin: 0; }
.cost .fig { display: block; margin: 0 0 3mm; font-size: 20pt; font-weight: 700; letter-spacing: -0.02em; color: var(--accent-ink); font-variant-numeric: tabular-nums; }
.grid2.three .cost:first-child { grid-column: 1 / -1; }

/* strengths */
.strengths { display: grid; gap: 6mm; }
.strength { display: grid; grid-template-columns: 12mm 1fr; gap: 6mm; align-items: start; padding-bottom: 6mm; border-bottom: 1px solid var(--line); }
.strength:last-child { border-bottom: 0; }
.strength .dot { width: 10mm; height: 10mm; border-radius: 50%%; border: 3px solid var(--sage); display: grid; place-items: center; }
.strength .dot::after { content: ''; width: 3.4mm; height: 1.8mm; border-left: 2.4px solid var(--sage); border-bottom: 2.4px solid var(--sage); transform: translateY(-.4mm) rotate(-45deg); }
.strength p { font-size: 12.5pt; line-height: 1.6; margin: 1mm 0 0; }

/* steps */
.steps { display: grid; gap: 5mm; }
.step { display: grid; grid-template-columns: 14mm 1fr; gap: 5mm; padding: 6mm 7mm; background: #fff; border: 1px solid var(--line); border-radius: 4mm; }
.step .n { width: 11mm; height: 11mm; border-radius: 50%%; background: var(--soft); color: var(--accent-ink); display: grid; place-items: center; font-weight: 700; font-size: 13pt; font-variant-numeric: tabular-nums; }
.step p { font-size: 10.5pt; line-height: 1.55; margin: 0; }

/* close */
.cta { margin-top: 8mm; padding: 11mm; border-radius: 5mm; background: linear-gradient(180deg, #3d5453, #34494a 45%%); color: var(--cream); display: grid; gap: 5mm; box-shadow: 0 8px 24px -8px rgb(31 38 36 / .35); }
.cta h3 { margin: 0; font-size: 20pt; line-height: 1.15; letter-spacing: -0.02em; color: var(--cream); }
.cta p { margin: 0; color: #e4dccf; font-size: 11pt; }
.cta a.btn { justify-self: start; display: inline-block; padding: 4mm 7mm; border-radius: 1.6mm; background: var(--cream); color: var(--ink); font-weight: 700; font-size: 11pt; text-decoration: none; }
.cta .url { font-size: 9.5pt; color: rgb(245 232 216 / .7); }
.sign { display: flex; align-items: center; gap: 3mm; margin-top: 6mm; font-size: 10pt; color: var(--muted); }
.sign img { width: 9mm; height: 9mm; border-radius: 50%%; object-fit: cover; }
.legal { margin-top: 6mm; font-size: 7.5pt; line-height: 1.5; color: var(--muted); }
"""

def money_fig(text):
    """Pull the headline £ figure out of a cost paragraph, if it has one."""
    import re
    m = re.findall(r'£[\d,]+', text)
    return m[-1] if m else None

def build(key, t):
    photo = b64(here / f'img/{key}.webp')
    total = 8
    def head(part):
        return f'<div class="head"><span class="brand">{ring("ring")}Calm Money</span><span>{e(t["name"])} · Part {part} of 7</span></div>'
    def foot(n):
        return f'<div class="foot"><span>Money personality guide · {e(t["short"])}</span><span class="n">{n:02d} / {total:02d}</span></div>'
    pages = []
    # 1 cover
    pages.append(f'''<section class="page cover">
  <div class="letter" aria-hidden="true">{t["letter"]}</div>
  <div class="top"><img class="logo" src="data:image/svg+xml;base64,{LOGO_DARK}" alt="Calm Money"><span class="tag">Money personality guide</span></div>
  <span class="type"><i></i>Your money personality</span>
  <h1>{e(t["name"])}</h1>
  <h2>{e(t["cover_pre"])} <em>{e(t["cover_em"])}</em> {e(t["cover_post"])}</h2>
  <p class="sub">{e(t["cover_sub"])}</p>
  <img class="photo" src="data:image/webp;base64,{photo}" alt="">
  <div class="bottom">
    <div class="byline"><div><span class="wm" role="img" aria-label="Peter Komolafe"></span><small>Founder, Calm Money</small></div></div>
    <span class="tag">calmmoneycommunity.com</span>
  </div>
</section>''')
    # 2 statements
    items = ''.join(f'<li><span class="box"></span><span>{e(s)}</span></li>' for s in t['statements'])
    pages.append(f'''<section class="page ledger">{head(1)}
  <p class="eyebrow">Part one · Do you recognise yourself?</p>
  <h1>Before we go any further, read these five statements.</h1>
  <p class="lede">If you recognise yourself in three or more of them, this guide is about you. Not someone like you. You.</p>
  <ul class="checks">{items}</ul>
  <p class="hint">The rest of this guide is an honest reading of what this pattern tends to mean, why it tends to happen, what it tends to cost, and what you can actually do about it.</p>
  {foot(2)}</section>''')
    # 3 identity
    pat = ''.join(f'<p>{e(x)}</p>' for x in t['pattern'])
    pages.append(f'''<section class="page ledger">{head(2)}
  <p class="eyebrow">Part two · Identity</p>
  <h1>{e(t["name"])}, honestly.</h1>
  <div class="cols"><div class="label">The pattern</div><div>{pat}</div></div>
  <figure class="quote" style="margin-left:0;margin-right:0"><span class="mark">“</span><p>{e(t["quote"])}</p><figcaption class="by">{e(t["quote_by"])}</figcaption></figure>
  {foot(3)}</section>''')
    # 4 research
    res = ''.join(f'<p>{e(x)}</p>' for x in t['research'])
    pages.append(f'''<section class="page ledger">{head(3)}
  <p class="eyebrow">Part three · Why it happens</p>
  <h1>This is not a character flaw. It is a <span class="q">documented pattern.</span></h1>
  <div class="cols" style="margin-top:4mm"><div class="label">The research</div><div>{res}</div></div>
  {foot(4)}</section>''')
    # 5 costs
    cards = ''
    for h, p in t['costs']:
        cards += f'<div class="cost"><h3>{e(h)}</h3><p>{e(p)}</p></div>'
    three = ' three' if len(t['costs']) == 3 else ''
    pages.append(f'''<section class="page ledger">{head(4)}
  <p class="eyebrow">Part four · Cost</p>
  <h1>The financial cost of this pattern is real.</h1>
  <p class="lede">Not as a judgement. As a number. These are the costs this pattern tends to produce when it runs unchecked for years or decades.</p>
  <div class="grid2{three}">{cards}</div>
  {foot(5)}</section>''')
    # 6 strengths
    st = ''.join(f'<div class="strength"><span class="dot"></span><p>{e(x)}</p></div>' for x in t['strengths'])
    pages.append(f'''<section class="page ledger">{head(5)}
  <p class="eyebrow">Part five · Strengths</p>
  <h1>You are not starting from nothing.</h1>
  <p class="lede">Every type has genuine strengths. Not as flattery. As the actual foundation progress is built on.</p>
  <div class="strengths">{st}</div>
  {foot(6)}</section>''')
    # 7 progress
    steps = ''.join(f'<div class="step"><span class="n">{i}</span><div><h3>{e(h)}</h3><p>{e(p)}</p></div></div>' for i, (h, p) in enumerate(t['progress'], 1))
    pages.append(f'''<section class="page ledger">{head(6)}
  <p class="eyebrow">Part six · Direction</p>
  <h1>What progress actually looks like for you.</h1>
  <p class="lede">{e(t["progress_intro"])}</p>
  <div class="steps">{steps}</div>
  {foot(7)}</section>''')
    # 8 close
    close = ''.join(f'<p>{e(x)}</p>' for x in COMMON_CLOSE)
    pages.append(f'''<section class="page ledger">{head(7)}
  <p class="eyebrow">Part seven · Beginning</p>
  <h1>You did not choose this pattern. <span class="q">But you can choose what happens next.</span></h1>
  <div style="max-width:150mm">{close}</div>
  <div class="cta">
    <h3>Begin the programme</h3>
    <p>Join Calm Money and start with the module built for {e(t["short"])}s.</p>
    <a class="btn" href="https://calmmoneycommunity.com/">Join Calm Money →</a>
    <span class="url">calmmoneycommunity.com</span>
  </div>
  <div class="sign"><img src="data:image/webp;base64,{PETER}" alt=""><span>Peter Komolafe, Founder, Calm Money</span></div>
  <p class="legal">Calm Money is financial education, not regulated financial advice. Nothing in this guide constitutes personalised advice under the Financial Services and Markets Act 2000. Always consider your own circumstances, and seek regulated advice where appropriate. The value of investments can go down as well as up, and you may get back less than you invest. © 2026 Conversation of Money Ltd.</p>
  {foot(8)}</section>''')

    css = CSS % dict(font=FONT, font_i=FONT_I, wordmark=WORDMARK, accent=t['accent'], ink=t['ink'], soft=t['soft'])
    doc = f'<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><title>{e(t["name"])}: Money Personality Guide</title><style>{css}</style></head><body>{"".join(pages)}</body></html>'
    out = here / f'out/{t["short"]}_Personality_Guide.html'
    out.parent.mkdir(exist_ok=True)
    out.write_text(doc)
    return out

for k, t in TYPES.items():
    print(build(k, t))
