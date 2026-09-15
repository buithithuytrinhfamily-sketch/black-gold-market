"""Apply the existing BGM logo to all HTML pages without rewriting article content."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
LOCKUP='''<a class="bgm-brand" href="/" translate="no" aria-label="Black Gold Market — Home"><img class="bgm-logo" src="/assets/brand/black-gold-market.jpg" width="60" height="60" alt=""><span class="bgm-brand-copy"><span class="bgm-name">BLACK GOLD MARKET</span><span class="bgm-tagline">Protect. Master. Grow.</span></span></a>'''
def apply_branding():
 changed=0
 for p in ROOT.rglob('*.html'):
  if '.git' in p.parts or 'scripts' in p.parts:continue
  s=p.read_text();old=s
  # The legacy kit header is a container with image + wordmark, not a link.
  s=re.sub(r'<div class="brand">\s*<img[^>]+>\s*<span class="wordmark">.*?</span>\s*</div>',lambda m:LOCKUP,s,flags=re.S)
  # Only replace short brand-only elements, never whole layout containers.
  s=re.sub(r'<(a|div)\b([^>]*class="(?:brand|wordmark|fmark)"[^>]*)>(.*?)</\1>',lambda m:LOCKUP if len(m[3])<250 and re.search(r'BLACK|Black Gold',m[3]) else m[0],s,flags=re.S)
  s=re.sub(r'(<img\b[^>]*class="lp-logo"[^>]*src=")[^"]+("[^>]*>)',r'\1/assets/brand/black-gold-market.jpg\2',s)
  s=s.replace('<h1 class="lp-name">Black Gold Market</h1>','<h1 class="lp-name" translate="no">Black Gold Market</h1>')
  # Publisher logo metadata and legacy logo portraits use the exact same artwork.
  s=s.replace('https://blackgoldmarket.us/avatar.jpg','https://blackgoldmarket.us/assets/brand/black-gold-market.jpg')
  if p.relative_to(ROOT).as_posix()=='book/the-long-game/index.html' and 'class="bgm-brand"' not in s:
   s=s.replace('<header><b>THE LONG GAME</b>','<header>'+LOCKUP+'<br><b>THE LONG GAME</b>')
  if '</head>' in s and '/assets/brand.css' not in s:s=s.replace('</head>','<link rel="stylesheet" href="/assets/brand.css"></head>')
  if s!=old:p.write_text(s);changed+=1
 return changed
if __name__=='__main__':print('Branded pages:',apply_branding())
