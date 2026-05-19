# Quick install

Pre-req: **git** installed. Nothing else.

## macOS / Linux

```bash
# 1. Download the installer
mkdir -p ~/og-install && cd ~/og-install
curl -fsSL https://raw.githubusercontent.com/SeaCelo/OG-ETH/feat/uv-migration/scripts/install.sh -o install.sh

# 2. Run it (will prompt for model + destination)
bash install.sh
```

To skip the prompts:

```bash
bash install.sh --repo og-eth --dest ~/Projects --yes
# clones to ~/Projects/OG-ETH
```

## Windows (PowerShell)

```powershell
# 1. Download the installer
mkdir C:\og-install -ErrorAction SilentlyContinue; cd C:\og-install
Invoke-WebRequest -UseBasicParsing -Uri https://raw.githubusercontent.com/SeaCelo/OG-ETH/feat/uv-migration/scripts/install.ps1 -OutFile install.ps1

# 2. Run it (will prompt for model + destination)
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
python -c "import ogeth; print(ogeth.__version__)"
```

```powershell
# Windows
cd <destination>
.\.venv\Scripts\Activate.ps1
python -c "import ogeth; print(ogeth.__version__)"
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
