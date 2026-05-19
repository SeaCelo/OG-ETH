#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────────────
# OG-ETH double-click installer (macOS / Linux).
#
# Downloads install.sh + SHA256SUMS, verifies the SHA-256 hash, then runs
# the installer if the hash matches. Aborts loudly on mismatch.
#
# First-time use on macOS:
#   1. Browser strips the execute bit; either:
#      a) Open Terminal, cd to download folder, run: chmod +x install.command
#      b) Or right-click the file in Finder → Open → confirm Gatekeeper warning
#   2. Subsequent double-clicks just work.
# ──────────────────────────────────────────────────────────────────────────────
set -e

# Source: which fork + branch to install from. Hardcoded for this test phase;
# update when the migration merges to upstream.
BASE="https://raw.githubusercontent.com/SeaCelo/OG-ETH/feat/uv-migration/scripts"
REPO_URL="https://github.com/SeaCelo/OG-ETH.git"
BRANCH="feat/uv-migration"

TMP="$(mktemp -d -t og-install)"
trap 'rm -rf "$TMP"' EXIT
SCRIPT="$TMP/og-install.sh"
SUMS="$TMP/og-SHA256SUMS"

echo "Downloading installer + checksums..."
curl -fsSL "$BASE/install.sh" -o "$SCRIPT"
curl -fsSL "$BASE/SHA256SUMS" -o "$SUMS"

# Extract expected hash for install.sh from the SUMS file (standard
# "<hash>  <filename>" format produced by sha256sum / shasum -a 256).
EXPECTED=$(awk '/^[0-9a-f]+[[:space:]]+install\.sh$/ {print $1; exit}' "$SUMS")
if [ -z "$EXPECTED" ]; then
    echo "ERROR: install.sh not listed in SHA256SUMS" >&2
    exit 1
fi

if command -v sha256sum >/dev/null 2>&1; then
    ACTUAL=$(sha256sum "$SCRIPT" | awk '{print $1}')
else
    ACTUAL=$(shasum -a 256 "$SCRIPT" | awk '{print $1}')
fi

if [ "$EXPECTED" != "$ACTUAL" ]; then
    echo ""
    echo "CHECKSUM MISMATCH -- ABORTING" >&2
    echo "  Expected : $EXPECTED" >&2
    echo "  Actual   : $ACTUAL" >&2
    echo "" >&2
    echo "Someone may have tampered with the install script in transit, or the" >&2
    echo "SHA256SUMS file in the repo is stale. Do not run the downloaded file." >&2
    exit 1
fi
echo "Checksum verified."
echo ""

bash "$SCRIPT" --repo-url "$REPO_URL" --branch "$BRANCH"

echo ""
read -p "Press Enter to close this window..."
