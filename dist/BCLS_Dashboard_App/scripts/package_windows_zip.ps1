param(
  [string]$OutName = "BCLS_Dashboard_App.zip"
)

$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$dist = Join-Path $root "dist"
New-Item -ItemType Directory -Force -Path $dist | Out-Null

$stage = Join-Path $dist "BCLS_Dashboard_App"
if (Test-Path $stage) { Remove-Item -Recurse -Force $stage }
New-Item -ItemType Directory -Force -Path $stage | Out-Null

$items = @(
  "dashboards",
  "data",
  "scripts",
  "shared",
  "BC_Dashboard_App.bat",
  "INSTALLATION_INSTRUCTION.md"
)

foreach ($item in $items) {
  $src = Join-Path $root $item
  if (Test-Path $src) {
    Copy-Item -Recurse -Force $src $stage
  }
}

$zipPath = Join-Path $dist $OutName
if (Test-Path $zipPath) { Remove-Item -Force $zipPath }
Compress-Archive -Path (Join-Path $stage "*") -DestinationPath $zipPath

Write-Host "[OK] Package created: $zipPath"
