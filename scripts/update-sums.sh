#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────────────
# Regenerate scripts/SHA256SUMS for the installer scripts.
#
# Run this from anywhere after modifying any of install.sh, install.ps1,
# install.bat, or install.command. Commits the updated SHA256SUMS together
# with whichever installer file(s) changed.
#
# The double-click wrappers (install.bat, install.command) download
# SHA256SUMS at runtime and verify the SHA-256 of install.sh / install.ps1
# against it. Stale checksums break the wrappers; CI guards against this.
# ──────────────────────────────────────────────────────────────────────────────
set -euo pipefail

# Resolve scripts/ directory regardless of where this script is invoked from.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Pick a SHA-256 tool (sha256sum on Linux, shasum -a 256 on macOS default).
if command -v sha256sum >/dev/null 2>&1; then
    HASHER=(sha256sum)
else
    HASHER=(shasum -a 256)
fi

FILES=(install.sh install.ps1 install.bat install.command)
for f in "${FILES[@]}"; do
    [ -f "$f" ] || { echo "ERROR: $f not found in $SCRIPT_DIR" >&2; exit 1; }
done

"${HASHER[@]}" "${FILES[@]}" > SHA256SUMS
echo "Updated ${SCRIPT_DIR}/SHA256SUMS:"
cat SHA256SUMS
