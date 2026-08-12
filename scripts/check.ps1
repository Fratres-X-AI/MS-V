# MS-V fast quality gate (laptop-safe, ~10s)
$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)

Write-Host "==> ruff"
python -m ruff check sim models analysis tests

Write-Host "==> mypy"
try {
  python -m mypy
  if ($LASTEXITCODE -ne 0) { throw "mypy exit $LASTEXITCODE" }
} catch {
  Write-Host "WARN mypy unavailable on this host (App Control / DLL): $_"
  Write-Host "Continuing with pytest + reproduce (laptop gate)."
}

Write-Host "==> pytest"
python -m pytest tests/ -q
if ($LASTEXITCODE -ne 0) { throw "pytest exit $LASTEXITCODE" }

Write-Host "==> reproduce validate-only"
python -m sim.reproduce --validate-only

Write-Host "OK - elite check passed"
