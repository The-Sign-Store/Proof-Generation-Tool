#!/usr/bin/env bash
# For each commit "vX.Y: ..." on the current branch (oldest first) without a release:
#   zip that commit's files as Sign_Proof_Generator_vX.Y/  (repo-only files left out)
#   take the release notes from the "### [X.Y]" section of README.md's changelog
#   publish release vX.Y at that commit
set -euo pipefail
DRY="${DRY_RUN:-}"
made=0
while read -r sha subject; do
  [[ "$subject" =~ ^v([0-9]+\.[0-9]+(\.[0-9]+)?):\  ]] || continue
  v="${BASH_REMATCH[1]}"
  if [ -z "$DRY" ] && gh release view "v$v" >/dev/null 2>&1; then echo "v$v: already released"; continue; fi
  name="Sign_Proof_Generator_v$v"
  rm -rf dist && mkdir -p dist
  git archive --format=tar --prefix="$name/" "$sha" -- . ':(exclude)proof-package.ico' ':(exclude).github' | tar -x -C dist
  (cd dist && zip -qrX "$name.zip" "$name")
  awk -v h="### [$v]" 'index($0, h) == 1 { f = 1; next } f && (/^### \[/ || /^---/) { exit } f' README.md \
    | sed 's/^#### /### /' > dist/notes.md
  printf '\n---\nDownload **%s.zip** below. Setup steps are in README.txt inside the zip.\n' "$name" >> dist/notes.md
  if [ -n "$DRY" ]; then echo "v$v: would release $(du -h "dist/$name.zip" | cut -f1) at ${sha:0:7}, notes $(grep -c . dist/notes.md) lines"; cp "dist/$name.zip" "$DRY/"; cp dist/notes.md "$DRY/notes_v$v.md"; continue; fi
  gh release create "v$v" "dist/$name.zip" --target "$sha" --title "Sign Proof Generator v$v" --notes-file dist/notes.md --latest=false
  made=$((made + 1))
done < <(git log --format='%H %s' --reverse HEAD)
rm -rf dist
if [ -z "$DRY" ] && [ "$made" -gt 0 ]; then
  latest=$(gh release list --limit 200 --json tagName --jq '.[].tagName' | sort -V | tail -1)
  gh release edit "$latest" --latest
  echo "Published $made release(s); latest is $latest"
fi
