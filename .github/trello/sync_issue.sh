#!/usr/bin/env bash
# Keeps one Trello card per GitHub issue (see .github/trello/SETUP.md).
#   opened / reopened -> card in the Inbox column (created if missing)
#   edited            -> card title + description updated
#   closed            -> card moved to the Done column
#   backfill          -> a card for every open issue that has none yet
# Cards are matched by their name prefix "#<issue number> ".
set -euo pipefail
API="${TRELLO_API:-https://api.trello.com/1}"
AUTH=(--data-urlencode "key=$TRELLO_KEY" --data-urlencode "token=$TRELLO_TOKEN")
: "${TRELLO_KEY:?secret TRELLO_KEY is missing}" "${TRELLO_TOKEN:?secret TRELLO_TOKEN is missing}"
: "${TRELLO_BOARD:?variable TRELLO_BOARD is missing}" "${TRELLO_INBOX_LIST:?variable TRELLO_INBOX_LIST is missing}" "${TRELLO_DONE_LIST:?variable TRELLO_DONE_LIST is missing}"

trello() {  # trello METHOD PATH [curl args...]
  local m="$1" p="$2"; shift 2
  if [ "$m" = GET ]; then curl -sS --fail-with-body -G "$API$p" "${AUTH[@]}" "$@"
  else curl -sS --fail-with-body -X "$m" "$API$p" "${AUTH[@]}" "$@"; fi   # long descriptions go in the body, not the URL
}
find_card() {  # prints the card id for issue $1, or nothing
  trello GET "/boards/$TRELLO_BOARD/cards/all" --data-urlencode "fields=name,closed" \
    | jq -r --arg p "#$1 " '[.[] | select(.name | startswith($p))] | sort_by(.closed) | .[0].id // empty'
}
describe() {  # issue body (trimmed to Trello's limit) + link back
  printf '%s\n\n---\nGitHub issue: %s' "$(printf '%s' "$2" | head -c 15000)" "$1"
}
create_card() {  # number title body url list
  local id
  id=$(trello POST /cards --data-urlencode "idList=$5" --data-urlencode "name=#$1 $2" \
         --data-urlencode "desc=$(describe "$4" "$3")" --data-urlencode "pos=top" | jq -r .id)
  trello POST "/cards/$id/attachments" --data-urlencode "url=$4" --data-urlencode "name=GitHub issue #$1" >/dev/null
  echo "created card $id for issue #$1"
}
sync_one() {  # action number title body url
  local action="$1" n="$2" title="$3" body="$4" url="$5" id
  id=$(find_card "$n")
  case "$action" in
    opened|reopened|backfill)
      if [ -z "$id" ]; then create_card "$n" "$title" "$body" "$url" "$TRELLO_INBOX_LIST"
      elif [ "$action" = reopened ]; then
        trello PUT "/cards/$id" --data-urlencode "idList=$TRELLO_INBOX_LIST" --data-urlencode "closed=false" --data-urlencode "pos=top" >/dev/null
        echo "moved card $id back to the Inbox (issue #$n reopened)"
      else echo "issue #$n already has card $id"; fi ;;
    edited)
      if [ -z "$id" ]; then create_card "$n" "$title" "$body" "$url" "$TRELLO_INBOX_LIST"
      else trello PUT "/cards/$id" --data-urlencode "name=#$n $title" --data-urlencode "desc=$(describe "$url" "$body")" >/dev/null
           echo "updated card $id (issue #$n edited)"; fi ;;
    closed)
      if [ -z "$id" ]; then create_card "$n" "$title" "$body" "$url" "$TRELLO_DONE_LIST"
      else trello PUT "/cards/$id" --data-urlencode "idList=$TRELLO_DONE_LIST" --data-urlencode "pos=top" >/dev/null
           echo "moved card $id to Done (issue #$n closed)"; fi ;;
    *) echo "ignoring action $action" ;;
  esac
}

if [ "${MODE:-event}" = backfill ]; then
  gh api --paginate "repos/$GITHUB_REPOSITORY/issues?state=open&per_page=100" \
    --jq '.[] | select(.pull_request | not) | [.number, .title, (.body // ""), .html_url] | @base64' |
  while read -r row; do
    f() { printf '%s' "$row" | base64 -d | jq -r ".[$1]"; }
    sync_one backfill "$(f 0)" "$(f 1)" "$(f 2)" "$(f 3)"
  done
else
  sync_one "$ACTION" "$ISSUE_NUMBER" "$ISSUE_TITLE" "$ISSUE_BODY" "$ISSUE_URL"
fi
