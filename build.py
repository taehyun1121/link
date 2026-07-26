#!/usr/bin/env python3
"""링크인바이오 자동 생성기 — products.json → index.html.
파이프라인이 매일 쿠팡링크 뽑으면 add_product()로 products.json에 append → build.py로 재생성 → git push.
디자인: 모바일 단일컬럼 카드(썸네일+이름+CTA), 최신 상단, 대가성문구. (2026 link-in-bio 벤치마킹 반영)
"""
import json, os, sys, html
LH = os.path.dirname(os.path.abspath(__file__))
PROD = os.path.join(LH, 'products.json')

TITLE = "요즘 난리난 아이템 모음 🛒"
SUBTITLE = "쇼츠에서 본 그 제품, 여기서 최저가로 만나요!"
CHANNEL = "ThhaTube"
GREETING = "알뜰하게 쇼핑하고 행복하세요! 😘"

def load():
    try: return json.load(open(PROD, encoding='utf-8'))
    except Exception: return []

def add_product(label, name, url, thumbnail, date, price=''):
    """파이프라인에서 호출: 새 상품을 맨 앞에 추가(중복 url 제거). price 옵션."""
    ps = [p for p in load() if p.get('url') != url]
    ps.insert(0, {'label': label, 'name': name, 'url': url, 'thumbnail': thumbnail, 'date': date, 'price': price})
    json.dump(ps, open(PROD, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    return len(ps)

def esc(s): return html.escape(s or '')

def build():
    ps = load()
    # 최신 date 우선, 같은 날은 입력순 유지
    ps = sorted(ps, key=lambda p: p.get('date',''), reverse=True)
    rows = []
    for p in ps:
        thumb = esc(p.get('thumbnail',''))
        img = f'<div class="thumb" style="background-image:url(\'{thumb}\')"></div>' if thumb else '<div class="thumb noimg">🛒</div>'
        price = esc(p.get('price',''))
        pr = f'<div class="price">{price}</div>' if price else ''
        title = esc(p.get('label','')) or esc(p.get('name',''))
        rows.append(f'''<a class="row" href="{esc(p['url'])}" target="_blank" rel="nofollow noopener">
  {img}
  <div class="meta"><div class="pname">{title}</div>{pr}</div>
  <div class="go">›</div>
</a>''')
    rows_html = "\n".join(rows) if rows else '<p class="empty">곧 상품이 올라옵니다 🙌</p>'
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
:root{{--bg:#f6f7f9;--fg:#1a1c22;--sub:#8b909b;--acc:#ff5a1f;--line:#ececf1}}
body{{background:var(--bg);color:var(--fg);font-family:'Pretendard','Apple SD Gothic Neo',system-ui,sans-serif;
 min-height:100vh;padding:26px 14px calc(40px + env(safe-area-inset-bottom));line-height:1.35}}
.wrap{{max-width:480px;margin:0 auto}}
header{{text-align:center;margin-bottom:18px}}
.ava{{width:66px;height:66px;border-radius:50%;margin:0 auto 10px;
 background:conic-gradient(from 210deg,var(--acc),#ffd60a,var(--acc));
 display:flex;align-items:center;justify-content:center;font-size:30px;box-shadow:0 6px 20px rgba(255,90,31,.3)}}
.chan{{font-size:12.5px;color:var(--sub);font-weight:600}}
h1{{font-size:19px;font-weight:800;margin:3px 0 4px;letter-spacing:-.01em}}
.sub{{font-size:12.5px;color:var(--sub)}}
.greet{{text-align:center;font-size:13px;font-weight:700;color:var(--acc);margin:12px 0 14px}}
.list{{background:#fff;border:1px solid var(--line);border-radius:16px;overflow:hidden;box-shadow:0 4px 20px rgba(20,22,30,.05)}}
.row{{display:flex;align-items:center;gap:12px;padding:10px 12px;text-decoration:none;color:inherit;
 border-bottom:1px solid var(--line);transition:background .1s}}
.row:last-child{{border-bottom:none}}
.row:active{{background:#f0f1f4}}
.thumb{{width:54px;height:54px;border-radius:11px;flex:0 0 54px;background-size:cover;background-position:center;background-color:#eef0f3}}
.thumb.noimg{{display:flex;align-items:center;justify-content:center;font-size:24px}}
.meta{{min-width:0;flex:1}}
.pname{{font-size:14px;font-weight:650;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}}
.price{{font-size:13px;font-weight:800;color:var(--acc);margin-top:2px}}
.go{{font-size:22px;color:#c4c8d0;flex:0 0 auto;font-weight:400}}
.empty{{text-align:center;color:var(--sub);padding:36px 0}}
footer{{margin-top:20px;text-align:center;font-size:10.5px;color:#a7abb5;line-height:1.6}}
</style></head>
<body><div class="wrap">
<header>
 <div class="ava">🔥</div>
 <div class="chan">@{esc(CHANNEL)}</div>
 <h1>{esc(TITLE)}</h1>
 <div class="sub">{esc(SUBTITLE)}</div>
</header>
<div class="greet">{esc(GREETING)}</div>
<div class="list">
{rows_html}
</div>
<footer>
 이 페이지는 쿠팡 파트너스 활동의 일환으로,<br>이에 따른 일정액의 수수료를 제공받습니다.
</footer>
</div></body></html>'''
    open(os.path.join(LH, 'index.html'), 'w', encoding='utf-8').write(out)
    print(f"index.html 생성됨 ({len(ps)}개 상품)")

if __name__ == '__main__':
    build()
