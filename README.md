# 링크인바이오 (하태현 쇼츠 쿠팡 링크허브)
- `products.json` : 상품 데이터(파이프라인이 매일 append)
- `build.py` : products.json → index.html 생성기
- `index.html` : GitHub Pages가 서빙하는 페이지
갱신: `python3 build.py && git add -A && git commit -m update && git push`
