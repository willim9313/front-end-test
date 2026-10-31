#!/usr/bin/env bash
# Re-subset a Google Font to exactly the characters a style page uses.
#   tools/subset-font.sh "<Family Name>" <weight> <out.woff2> <file>...
# Collects every non-ASCII character from the given files (plus printable ASCII),
# asks the Google Fonts CSS API for a subset with text=..., and saves the woff2.
# Example (repo root):
#   tools/subset-font.sh "Shippori Mincho" 400 styles/ojisan-museum/fonts/shippori-mincho-400-subset.woff2 \
#     styles/ojisan-museum/index.html styles/ojisan-museum/main.js
set -euo pipefail
export LC_ALL=C.UTF-8
family=$1 weight=$2 out=$3; shift 3

ascii=$(printf '%s' ' !"#$%&'"'"'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~')
chars=$(cat "$@" | grep -oP '[^\x00-\x7F]' | sort -u | tr -d '\n')
text="$ascii$chars"

ua="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
css=$(curl -sG "https://fonts.googleapis.com/css2" -A "$ua" \
  --data-urlencode "family=$family:wght@$weight" --data-urlencode "text=$text")
url=$(printf '%s' "$css" | grep -oE 'https://[^)]+' | head -1)
[ -n "$url" ] || { echo "no font url in response:" >&2; echo "$css" >&2; exit 1; }
curl -s -A "$ua" -o "$out" "$url"
echo "$out: $(wc -c < "$out") bytes, $(printf '%s' "$chars" | wc -m) non-ASCII chars"
