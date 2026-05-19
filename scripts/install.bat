@echo off
REM ─────────────────────────────────────────────────────────────────────────────
REM OG-ETH double-click installer (Windows).
REM
REM Downloads install.ps1 + SHA256SUMS, verifies the SHA-256 hash, then runs
REM the installer if the hash matches. Aborts loudly on mismatch.
REM
REM First-time use:
REM   - Windows SmartScreen may warn that the file is from the internet.
REM     Click "More info" -> "Run anyway".
REM ─────────────────────────────────────────────────────────────────────────────
setlocal

REM Source: which fork + branch to install from. Hardcoded for this test phase;
REM update when the migration merges to upstream.
set "BASE=https://raw.githubusercontent.com/SeaCelo/OG-ETH/feat/uv-migration/scripts"
set "REPO_URL=https://github.com/SeaCelo/OG-ETH.git"
set "BRANCH=feat/uv-migration"

echo Downloading OG-ETH installer + verifying checksum...
echo.

REM The PowerShell -Command runs on a single logical line. It:
REM   1. Downloads install.ps1 and SHA256SUMS to %TEMP%.
REM   2. Extracts the expected hash for install.ps1 from SHA256SUMS.
REM   3. Computes the actual SHA-256 of the downloaded install.ps1.
REM   4. Aborts with a loud error if the hashes differ.
REM   5. Otherwise invokes install.ps1 with the test-branch arguments.
powershell -ExecutionPolicy Bypass -NoProfile -Command "$ErrorActionPreference='Stop'; $base='%BASE%'; $tmp=$env:TEMP; $script=Join-Path $tmp 'og-install.ps1'; $sums=Join-Path $tmp 'og-SHA256SUMS'; Write-Host 'Downloading install.ps1...'; Invoke-RestMethod -Uri ($base + '/install.ps1') -OutFile $script; Write-Host 'Downloading SHA256SUMS...'; Invoke-RestMethod -Uri ($base + '/SHA256SUMS') -OutFile $sums; $line=(Get-Content $sums | Where-Object { $_ -match 'install\.ps1$' } | Select-Object -First 1); if (-not $line) { Write-Host 'ERROR: install.ps1 not listed in SHA256SUMS' -ForegroundColor Red; exit 1 }; $expected=($line -split '\s+')[0].ToLower(); $actual=(Get-FileHash $script -Algorithm SHA256).Hash.ToLower(); if ($expected -ne $actual) { Write-Host ''; Write-Host 'CHECKSUM MISMATCH -- ABORTING' -ForegroundColor Red; Write-Host ('  Expected : ' + $expected); Write-Host ('  Actual   : ' + $actual); Write-Host ''; Write-Host 'Someone may have tampered with the install script in transit, or the'; Write-Host 'SHA256SUMS file in the repo is stale. Do not run the downloaded file.'; exit 1 }; Write-Host 'Checksum verified.' -ForegroundColor Green; Write-Host ''; & $script -RepoUrl '%REPO_URL%' -Branch '%BRANCH%'"

echo.
pause
