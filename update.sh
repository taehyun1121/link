#!/bin/bash
# 링크허브 자동갱신 — 파이프라인이 쿠팡링크 뽑은 뒤 호출.
# 사용: update.sh "<라벨>" "<상품명>" "<affiliateUrl>" "<thumbnailUrl>" "<YYYY-MM-DD>"
# 동작: products.json 맨앞 추가(중복url제거) → index.html 재생성 → git commit/push → Pages 자동 재배포.
set -e
LH="$(cd "$(dirname "$0")" && pwd)"
LABEL="$1"; NAME="$2"; URL="$3"; THUMB="$4"; DATE="${5:-$(date +%F)}"
[ -z "$URL" ] && { echo "URL 필수"; exit 1; }
cd "$LH"
python3 -c "import build; n=build.add_product('''$LABEL''','''$NAME''','''$URL''','''$THUMB''','''$DATE'''); print('상품', n, '개')"
python3 build.py
git add -A
git -c user.email=thha301@gmail.com -c user.name=taehyun1121 commit -q -m "링크허브 갱신: $LABEL ($DATE)" || { echo "변경없음"; exit 0; }
git push -q origin main && echo "푸시 완료 → https://taehyun1121.github.io/link/ (1분 내 반영)"
