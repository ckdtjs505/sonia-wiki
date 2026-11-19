#!/bin/bash
# 블로그 _posts를 data/posts로 가져와, 바뀐 게 있으면 재적재·서버 재시작·커밋까지 한다.
# 서버가 127.0.0.1이라 GitHub 웹훅이 닿지 않아 launchd가 1시간마다 실행한다 (dev.sonia.wiki.sync.plist).
set -euo pipefail
cd "$(dirname "$0")"

BLOG=.cache/blog
if [ -d "$BLOG" ]; then
  git -C "$BLOG" fetch -q --depth 1 origin master && git -C "$BLOG" reset -q --hard FETCH_HEAD
else
  git clone -q --depth 1 https://github.com/ckdtjs505/ckdtjs505.github.io "$BLOG"
fi

TMP=$(mktemp -d)
for f in "$BLOG"/_posts/*.md; do
  n=$(basename "$f" .md)
  # 첫 줄 '---' 다음에 원문 링크(출처 카드용) 끼워 넣기
  { echo '---'; echo "url: https://ckdtjs505.github.io/posts/$n"; tail -n +2 "$f"; } > "$TMP/$n.md"
done
cp data/posts/about-this-wiki.md "$TMP/"

if diff -rq "$TMP" data/posts >/dev/null; then echo "$(date '+%F %T') 변경 없음"; rm -rf "$TMP"; exit 0; fi

rm -rf data/posts && mv "$TMP" data/posts
.venv/bin/python -m app.ingest
launchctl kickstart -k "gui/$(id -u)/dev.sonia.wiki"  # 새 컬렉션을 서버가 다시 열도록

git add data/posts
git commit -qm "블로그 글 동기화" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
git push -q origin HEAD:main
echo "$(date '+%F %T') 동기화 완료"
