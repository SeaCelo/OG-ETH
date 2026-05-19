# Quick install

Pre-req: **git** installed. Nothing else.

## macOS / Linux

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/SeaCelo/OG-ETH/feat/uv-migration/scripts/install.sh)" _ --repo-url https://github.com/SeaCelo/OG-ETH.git --branch feat/uv-migration
```

## Windows (PowerShell)

```powershell
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/SeaCelo/OG-ETH/feat/uv-migration/scripts/install.ps1))) -RepoUrl https://github.com/SeaCelo/OG-ETH.git -Branch feat/uv-migration
```

> **Test-phase note**: the URLs above and the `--repo-url` / `-RepoUrl` flag point at `SeaCelo/OG-ETH` on the `feat/uv-migration` branch because the uv migration hasn't merged upstream yet. See [After merge](#after-merge) for the eventual cleaner form.

## Skip the prompts

```bash
# macOS / Linux -- clones to ~/Projects/OG-ETH
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/SeaCelo/OG-ETH/feat/uv-migration/scripts/install.sh)" _ --repo-url https://github.com/SeaCelo/OG-ETH.git --branch feat/uv-migration --dest ~/Projects --yes
```

```powershell
# Windows -- clones to C:\Users\<you>\Projects\OG-ETH
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/SeaCelo/OG-ETH/feat/uv-migration/scripts/install.ps1))) -RepoUrl https://github.com/SeaCelo/OG-ETH.git -Branch feat/uv-migration -Dest C:\Users\$env:USERNAME\Projects -Yes
```

## After install

Activate the venv and you're set:

```bash
# macOS / Linux
cd <destination>
source .venv/bin/activate
python -W ignore -c "import ogeth; print(ogeth.__version__)"
```

```powershell
# Windows
cd <destination>
.\.venv\Scripts\Activate.ps1
python -W ignore -c "import ogeth; print(ogeth.__version__)"
```

## Alternatives

### Double-click installer (no terminal)

Download one file and double-click it. The wrapper downloads the install script, verifies its SHA-256 against the published `SHA256SUMS`, and runs it.

- **macOS / Linux**: [install.command](https://github.com/SeaCelo/OG-ETH/raw/feat/uv-migration/scripts/install.command)
- **Windows**: [install.bat](https://github.com/SeaCelo/OG-ETH/raw/feat/uv-migration/scripts/install.bat)

First-time gotchas:
- **macOS**: browser strips the execute bit. Either `chmod +x install.command` in Terminal, or right-click → Open → confirm Gatekeeper.
- **Windows**: SmartScreen may show "Windows protected your PC." Click **More info** → **Run anyway**.

### Manual download (inspect before running)

```bash
# macOS / Linux
curl -fsSL https://raw.githubusercontent.com/SeaCelo/OG-ETH/feat/uv-migration/scripts/install.sh -o install.sh
less install.sh   # inspect
bash install.sh --repo-url https://github.com/SeaCelo/OG-ETH.git --branch feat/uv-migration
```

```powershell
# Windows
Invoke-WebRequest -UseBasicParsing -Uri https://raw.githubusercontent.com/SeaCelo/OG-ETH/feat/uv-migration/scripts/install.ps1 -OutFile install.ps1
notepad install.ps1   # inspect
powershell -ExecutionPolicy Bypass -File .\install.ps1 -RepoUrl https://github.com/SeaCelo/OG-ETH.git -Branch feat/uv-migration
```

Optional: verify against the published checksums first.

```bash
curl -fsSL https://raw.githubusercontent.com/SeaCelo/OG-ETH/feat/uv-migration/scripts/SHA256SUMS -o SHA256SUMS
shasum -a 256 -c SHA256SUMS --ignore-missing
```

## After merge

Once the migration merges to upstream `EAPD-DRB/OG-ETH`, the URLs change to upstream main and the `--repo-url` / `-RepoUrl` flags drop. The one-liners become:

```bash
# macOS / Linux
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/EAPD-DRB/OG-ETH/main/scripts/install.sh)"
```

```powershell
# Windows
iex (irm https://raw.githubusercontent.com/EAPD-DRB/OG-ETH/main/scripts/install.ps1)
```

The `--repo og-eth` / `-Repo og-eth` menu shortcut also starts working without an explicit `--repo-url`.

## Maintainer note

If you edit any of `install.sh`, `install.ps1`, `install.bat`, or `install.command`, regenerate `SHA256SUMS` before committing:

```bash
bash scripts/update-sums.sh
```

CI (`.github/workflows/verify_checksums.yml`) fails the PR if the checked-in `SHA256SUMS` doesn't match the installer files.
