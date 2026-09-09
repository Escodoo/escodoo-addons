#!/usr/bin/env bash
# Copyright 2026 Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
#
# Refresh the brand images from the live site into
# static/src/binary/ir_attachment/, which is what data/ir_attachment_pre.xml
# loads. Run tools/build_attachment_xml.py afterwards to regenerate that file.
#
# Usage: tools/download_assets.sh [base_url]

set -euo pipefail

BASE_URL="${1:-https://escodoo.com.br}"
MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_DIR="${MODULE_DIR}/static/src/binary/ir_attachment"
CATALOGUE="${MODULE_DIR}/tools/assets.tsv"

mkdir -p "${TARGET_DIR}"

while IFS=$'\t' read -r stem source; do
    [[ -z "${stem}" || "${stem}" == \#* ]] && continue
    tmp="$(mktemp)"
    if ! curl -sfL -m 60 "${BASE_URL}${source}" -o "${tmp}"; then
        echo "skip ${stem}: could not download ${source}" >&2
        rm -f "${tmp}"
        continue
    fi
    mime="$(file --brief --mime-type "${tmp}")"
    case "${mime}" in
        image/png) ext="png" ;;
        image/jpeg) ext="jpg" ;;
        image/svg+xml | text/xml | text/plain) ext="svg" ;;
        image/webp) ext="webp" ;;
        *)
            echo "skip ${stem}: unexpected type ${mime}" >&2
            rm -f "${tmp}"
            continue
            ;;
    esac
    mv "${tmp}" "${TARGET_DIR}/${stem}.${ext}"
    echo "ok ${stem}.${ext}"
done < "${CATALOGUE}"

if command -v python3 >/dev/null; then
    python3 "${MODULE_DIR}/tools/optimize_asset.py" "${TARGET_DIR}"
fi

echo "Now run: python3 tools/build_attachment_xml.py"
