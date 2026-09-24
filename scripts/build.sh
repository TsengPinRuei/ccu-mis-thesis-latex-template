#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
target="${1:-main}"
case "$target" in main|proposal|spine) ;; *) echo 'Usage: bash scripts/build.sh [main|proposal|spine]' >&2; exit 2;; esac
command -v xelatex >/dev/null || { echo 'XeLaTeX is required.' >&2; exit 1; }
mkdir -p output/pdf
options=(-no-shell-escape -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=output/pdf)
xelatex "${options[@]}" "$target.tex"
if [ "$target" != spine ]; then
  command -v biber >/dev/null || { echo 'Biber is required.' >&2; exit 1; }
  biber --input-directory output/pdf --output-directory output/pdf "$target"
fi
xelatex "${options[@]}" "$target.tex"
xelatex "${options[@]}" "$target.tex"
if grep -E '(^!|Missing character:|Overfull|undefined references|undefined citations|Please.*rerun|Please.*Biber|Rerun to get|Label.*multiply defined)' "output/pdf/$target.log"; then
  echo 'Unresolved layout/reference issues; inspect the log.' >&2
  exit 1
fi
echo "Built: output/pdf/$target.pdf"
