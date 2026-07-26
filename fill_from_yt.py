#!/usr/bin/env python3
"""유튜브(@ThhaTube) 업로드 제품 → 쿠팡 top1 매칭 → 링크보드 products.json 재구성.
🔴 증분 저장: 매 제품 성공 시 즉시 products.json + index.html 갱신(중간에 죽어도 안 날아감).
🔴 재개(resume): 이미 가격까지 매칭된 label은 건너뜀 → 재실행하면 이어서.
각 제품 순차로 coupang_shorts_feed.js 실행(동시금지, SKIP_MEDIA=썸네일만). 조회수 desc 정렬. 로그: fill_log.txt.
"""
import json, os, sys, subprocess, time
LH = os.path.dirname(os.path.abspath(__file__))
SKILL = "/mnt/c/Users/ha861/agents/shared/skills/coupang-affiliate-link"
FEED = f"{SKILL}/coupang_feed.json"
PROD = f"{LH}/products.json"
DATE = "2026-07-27"
LOG = f"{LH}/fill_log.txt"
sys.path.insert(0, LH)
import build

def log(m):
    line = f"[{time.strftime('%H:%M:%S')}] {m}"
    print(line, flush=True)
    open(LOG, "a", encoding="utf-8").write(line + "\n")

def load_products():
    try: return json.load(open(PROD, encoding="utf-8"))
    except Exception: return []

def save(products, push=True):
    products.sort(key=lambda p: p.get("views", 0), reverse=True)
    json.dump(products, open(PROD, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    build.build()  # index.html 즉시 재생성
    if push:  # 실시간 사이트(ht-pick.com) 반영 — 형이 채워지는 걸 바로 봄
        subprocess.run(["git", "add", "-A"], cwd=LH, capture_output=True)
        subprocess.run(["git", "-c", "user.email=thha301@gmail.com", "-c", "user.name=taehyun1121",
                        "commit", "-q", "-m", "링크보드 자동갱신"], cwd=LH, capture_output=True)
        subprocess.run(["git", "push", "-q", "origin", "main"], cwd=LH, capture_output=True, timeout=90)

def main():
    items = json.load(open(f"{LH}/yt_products.json", encoding="utf-8"))
    # 재개: 가격까지 매칭된 것만 완료로 간주(원본 4개는 price 없어 재매칭됨)
    result = [p for p in load_products() if p.get("price")]
    done = {p["label"] for p in result}
    log(f"시작: {len(items)}개 목표, 기완료 {len(done)}개 → 남은 {len(items)-len(done)}개")
    env = {**os.environ, "LD_LIBRARY_PATH": "/tmp/nspr_libs", "COUPANG_SUBID": "ytshorts01", "SKIP_MEDIA": "1"}
    for i, it in enumerate(items):
        if it["label"] in done:
            continue
        term = it["search"]
        try:
            subprocess.run(["node", "coupang_shorts_feed.js", term, "1"],
                           cwd=SKILL, env=env, capture_output=True, text=True, timeout=200)
            feed = json.load(open(FEED, encoding="utf-8"))
            if feed.get("searchTerm") != term:  # 쿠팡 실행 실패 → 이전 feed 잔존 → 오매칭 방지
                log(f"[{i+1}/{len(items)}] STALE  {it['label']} (feed 미갱신 → 스킵)")
                continue
            top = next((p for p in feed.get("products", []) if p.get("affiliateUrl")), None)
            if top:
                result = [p for p in result if p["label"] != it["label"]]  # 중복 label 제거
                result.append({
                    "label": it["label"], "name": top.get("name", ""),
                    "url": top["affiliateUrl"], "thumbnail": top.get("thumbnail", ""),
                    "date": DATE, "price": top.get("price", "") or "", "views": it.get("views", 0),
                })
                save(result)  # 🔴 증분 저장
                done.add(it["label"])
                log(f"[{i+1}/{len(items)}] OK  {it['label']} | {top.get('price','?')} | {top.get('name','')[:22]}  (누적 {len(result)})")
            else:
                log(f"[{i+1}/{len(items)}] NO_AFF  {it['label']} (검색:{term})")
        except Exception as e:
            log(f"[{i+1}/{len(items)}] ERR  {it['label']}: {str(e)[:60]}")
    ok = sum(1 for p in result if p.get("price"))
    log(f"완료: {len(result)}개 카드(가격 {ok}개). products.json + index.html 갱신됨.")

if __name__ == "__main__":
    main()
