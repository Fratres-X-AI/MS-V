# MS-V fast quality gate (laptop-safe, ~10s)
$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)

Write-Host "==> ruff"
python -m ruff check sim models analysis tests

Write-Host "==> mypy"
mypy

Write-Host "==> pytest"
python -m pytest tests/ -q

Write-Host "==> reproduce validate-only"
python -m sim.reproduce --validate-only

Write-Host "OK - elite check passed"
