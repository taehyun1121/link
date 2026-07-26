#!/usr/bin/env python3
"""링크인바이오 자동 생성기 — products.json → index.html.
파이프라인이 매일 쿠팡링크 뽑으면 add_product()로 products.json에 append → build.py로 재생성 → git push.
디자인: 모바일 단일컬럼 카드(썸네일+이름+CTA), 최신 상단, 대가성문구. (2026 link-in-bio 벤치마킹 반영)
"""
import json, os, sys, html
LH = os.path.dirname(os.path.abspath(__file__))
PROD = os.path.join(LH, 'products.json')

TITLE = "요즘 난리난 아이템 모음 🛒"
SUBTITLE = "쇼츠에서 본 그 제품, 여기서 최저가 확인하세요"
CHANNEL = "하태현유튜브"

def load():
    try: return json.load(open(PROD, encoding='utf-8'))
    except Exception: return []

def add_product(label, name, url, thumbnail, date):
    """파이프라인에서 호출: 새 상품을 맨 앞에 추가(중복 url 제거)."""
    ps = [p for p in load() if p.get('url') != url]
    ps.insert(0, {'label': label, 'name': name, 'url': url, 'thumbnail': thumbnail, 'date': date})
    json.dump(ps, open(PROD, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    return len(ps)

def esc(s): return html.escape(s or '')

def build():
    ps = load()
    # 최신 date 우선, 같은 날은 입력순 유지
    ps = sorted(ps, key=lambda p: p.get('date',''), reverse=True)
    cards = []
    for p in ps:
        thumb = esc(p.get('thumbnail',''))
        img = f'<div class="thumb" style="background-image:url(\'{thumb}\')"></div>' if thumb else '<div class="thumb noimg">🛒</div>'
        cards.append(f'''<a class="card" href="{esc(p['url'])}" target="_blank" rel="nofollow noopener">
  {img}
  <div class="meta"><div class="label">{esc(p['label'])}</div>
  <div class="name">{esc(p.get('name',''))}</div>
  <div class="cta">쿠팡 최저가 보기 →</div></div>
</a>''')
    cards_html = "\n".join(cards) if cards else '<p class="empty">곧 상품이 올라옵니다 🙌</p>'
    out = f'''<!doctype html>
<html lang="ko"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(TITLE)}</title>
<meta name="description" content="{esc(SUBTITLE)}">
<meta property="og:title" content="{esc(TITLE)}">
<meta property="og:description" content="{esc(SUBTITLE)}">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bg:#0e0f13;--card:#181a20;--card2:#20232c;--fg:#f4f5f7;--sub:#9aa0ad;--acc:#ff5a1f;--acc2:#ffd60a}}
body{{background:radial-gradient(120% 90% at 50% 0%,#1c1f2b 0%,var(--bg) 55%);color:var(--fg);
 font-family:'Pretendard','Apple SD Gothic Neo',system-ui,sans-serif;min-height:100vh;
 padding:32px 16px calc(48px + env(safe-area-inset-bottom));line-height:1.4}}
.wrap{{max-width:520px;margin:0 auto}}
header{{text-align:center;margin-bottom:26px}}
.ava{{width:76px;height:76px;border-radius:50%;margin:0 auto 14px;
 background:conic-gradient(from 210deg,var(--acc),var(--acc2),var(--acc));
 display:flex;align-items:center;justify-content:center;font-size:34px;box-shadow:0 8px 30px rgba(255,90,31,.35)}}
.chan{{font-size:13px;color:var(--sub);letter-spacing:.02em}}
h1{{font-size:22px;font-weight:800;margin:4px 0 6px;letter-spacing:-.01em}}
.sub{{font-size:13.5px;color:var(--sub)}}
.cards{{display:flex;flex-direction:column;gap:12px;margin-top:8px}}
.card{{display:flex;align-items:center;gap:14px;background:var(--card);border:1px solid #262a34;
 border-radius:18px;padding:12px;text-decoration:none;color:inherit;transition:transform .12s ease,border-color .12s ease,background .12s}}
.card:active{{transform:scale(.98)}}
.card:hover{{border-color:var(--acc);background:var(--card2)}}
.thumb{{width:74px;height:74px;border-radius:13px;flex:0 0 74px;background-size:cover;background-position:center;background-color:#2a2e39}}
.thumb.noimg{{display:flex;align-items:center;justify-content:center;font-size:30px}}
.meta{{min-width:0;flex:1}}
.label{{font-size:15.5px;font-weight:750;margin-bottom:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.name{{font-size:11.5px;color:var(--sub);display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;margin-bottom:6px}}
.cta{{display:inline-block;font-size:12.5px;font-weight:800;color:#111;background:linear-gradient(90deg,var(--acc2),var(--acc));
 padding:5px 12px;border-radius:999px}}
.empty{{text-align:center;color:var(--sub);padding:40px 0}}
footer{{margin-top:28px;text-align:center;font-size:11px;color:#6b7180;line-height:1.6}}
footer a{{color:#8a90a0}}
</style></head>
<body><div class="wrap">
<header>
 <div class="ava">🔥</div>
 <div class="chan">@{esc(CHANNEL)}</div>
 <h1>{esc(TITLE)}</h1>
 <div class="sub">{esc(SUBTITLE)}</div>
</header>
<div class="cards">
{cards_html}
</div>
<footer>
 이 페이지는 쿠팡 파트너스 활동의 일환으로,<br>이에 따른 일정액의 수수료를 제공받습니다.
</footer>
</div></body></html>'''
    open(os.path.join(LH, 'index.html'), 'w', encoding='utf-8').write(out)
    print(f"index.html 생성됨 ({len(ps)}개 상품)")

if __name__ == '__main__':
    build()
