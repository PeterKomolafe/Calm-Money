# Builds quiz/index.html (one self-contained file) from template.html. Run: python3 quiz/build.py, then upload quiz/index.html to Netlify.
import base64, math, pathlib

here = pathlib.Path(__file__).parent
site = pathlib.Path('/home/user/Calm-Money/public')
b64 = lambda p: base64.b64encode(p.read_bytes()).decode()

# Calm Money ring, same geometry as src/components/Logo.astro
c, r, w = 50, 34.6, 13
cols = {'teal': '#557170', 'sage': '#7d9d90', 'blush': '#e6a89c', 'terracotta': '#b5695a', 'cream': '#f5e8d8'}
def pt(d):
    a = math.radians(d); return c + r * math.cos(a), c + r * math.sin(a)
def arc(f, t):
    x1, y1 = pt(f); x2, y2 = pt(t); large = 1 if t - f > 180 else 0
    return f'M {x1:.3f} {y1:.3f} A {r} {r} 0 {large} 1 {x2:.3f} {y2:.3f}'
segs = [(-72, 72, 'teal'), (72, 119, 'sage'), (119, 171, 'blush'), (171, 231, 'terracotta'), (231, 288, 'cream')]
caps = [(72, 'sage'), (119, 'blush'), (171, 'terracotta'), (231, 'cream'), (-72, 'teal')]
inner = ''.join(f'<path d="{arc(f, t)}" fill="none" stroke="{cols[k]}" stroke-width="{w}"/>' for f, t, k in segs)
inner += ''.join(f'<circle cx="{pt(a)[0]:.3f}" cy="{pt(a)[1]:.3f}" r="{w/2}" fill="{cols[k]}"/>' for a, k in caps)
ring = f'<svg class="ring" viewBox="0 0 100 100" role="img" aria-label="Calm Money">{inner}</svg>'
fav = base64.b64encode(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">{inner}</svg>'.encode()).decode()

html = (here / 'template.html').read_text()
html = (html.replace('{{RING}}', ring).replace('{{FAVICON}}', fav)
        .replace('{{SATOSHI}}', b64(site / 'fonts/Satoshi-Variable.woff2'))
        .replace('{{WORDMARK}}', b64(site / 'images/peter/wordmark.png'))
        .replace('{{PETER}}', b64(site / 'images/peter/peter.webp')))
assert '{{' not in html
out = here / 'index.html'
out.write_text(html)
print(out, len(html) // 1024, 'KB')
