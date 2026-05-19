# Quick install

Pre-req: **git** installed. Nothing else.

## Easiest: double-click

Download one file and double-click it. The wrapper downloads `install.sh` or
`install.ps1` from the repo, verifies its SHA-256 against the published
`SHA256SUMS`, and runs it.

| Platform        | Download this file                                                                                                              |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| macOS / Linux   | [`install.command`](https://github.com/SeaCelo/OG-ETH/raw/feat/uv-migration/scripts/install.command)                            |
| Windows         | [`install.bat`](https://github.com/SeaCelo/OG-ETH/raw/feat/uv-migration/scripts/install.bat)                                    |

**macOS first-time gotcha:** the browser strips the execute bit. Open Terminal in
the download folder and run `chmod +x install.command` once, or right-click the
file in Finder → Open → confirm the Gatekeeper warning. After that, plain
double-click works.

**Windows first-time gotcha:** SmartScreen may show a blue "Windows protected
your PC" dialog. Click **More info** → **Run anyway**.

If the wrapper reports a checksum mismatch it will abort — do not run the
downloaded installer. That means either the file was tampered with in transit
or the `SHA256SUMS` in the repo is stale (CI guards against the latter).

## macOS / Linux (manual)

```bash
# 1. Download the installer
mkdir -p ~/og-install && cd ~/og-install
curl -fsSL https://raw.githubusercontent.com/SeaCelo/OG-ETH/feat/uv-migration/scripts/install.sh -o install.sh

# 2. (Optional) Verify the SHA-256 against the published SHA256SUMS
curl -fsSL https://raw.githubusercontent.com/SeaCelo/OG-ETH/feat/uv-migration/scripts/SHA256SUMS -o SHA256SUMS
shasum -a 256 -c SHA256SUMS --ignore-missing

# 3. Run it (will prompt for model + destination)
bash install.sh
```

To skip the prompts:

```bash
bash install.sh --repo og-eth --dest ~/Projects --yes
# clones to ~/Projects/OG-ETH
```

## Windows (PowerShell, manual)

```powershell
# 1. Download the installer
mkdir C:\og-install -ErrorAction SilentlyContinue; cd C:\og-install
Invoke-WebRequest -UseBasicParsing -Uri https://raw.githubusercontent.com/SeaCelo/OG-ETH/feat/uv-migration/scripts/install.ps1 -OutFile install.ps1

# 2. (Optional) Verify the SHA-256 against the published SHA256SUMS
Invoke-WebRequest -UseBasicParsing -Uri https://raw.githubusercontent.com/SeaCelo/OG-ETH/feat/uv-migration/scripts/SHA256SUMS -OutFile SHA256SUMS
$expected = ((Get-Content SHA256SUMS | Where-Object { $_ -match 'install\.ps1$' }) -split '\s+')[0].ToLower()
$actual   = (Get-FileHash install.ps1 -Algorithm SHA256).Hash.ToLower()
if ($expected -ne $actual) { Write-Host "CHECKSUM MISMATCH" -ForegroundColor Red } else { Write-Host "OK" -ForegroundColor Green }

# 3. Run it (will prompt for model + destination)
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

To skip the prompts:

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1 -Repo og-eth -Dest C:\Users\$env:USERNAME\Projects -Yes
# clones to C:\Users\<you>\Projects\OG-ETH
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

## Testing the migration branch (right now, before merge)

The URLs above point at the `feat/uv-migration` branch on `SeaCelo/OG-ETH` (since the migration hasn't merged yet). When picking from the menu, pick **"Other (paste Git URL)"** and use:

- URL: `https://github.com/SeaCelo/OG-ETH.git`
- Branch: `feat/uv-migration`

Or skip the menu entirely:

```bash
# macOS / Linux -- clones to ~/Projects/OG-ETH
bash install.sh --repo-url https://github.com/SeaCelo/OG-ETH.git --branch feat/uv-migration --dest ~/Projects
```

```powershell
# Windows -- clones to C:\Users\<you>\Projects\OG-ETH
powershell -ExecutionPolicy Bypass -File .\install.ps1 -RepoUrl https://github.com/SeaCelo/OG-ETH.git -Branch feat/uv-migration -Dest C:\Users\$env:USERNAME\Projects
```

After the migration merges to upstream, drop `--repo-url` / `--branch` (or `-RepoUrl` / `-Branch`) — `--repo og-eth` / `-Repo og-eth` will work directly.

## Maintainer note

If you edit any of `install.sh`, `install.ps1`, `install.bat`, or `install.command`,
regenerate `SHA256SUMS` before committing:

```bash
bash scripts/update-sums.sh
```

CI (`.github/workflows/verify_checksums.yml`) fails the PR if the checked-in
`SHA256SUMS` doesn't match the installer files.
