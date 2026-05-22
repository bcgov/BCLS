param(
  [switch]$SkipDist,
  [switch]$SkipSpfx,
  [switch]$NoSpfxManifestRefresh
)

$ErrorActionPreference = "Stop"

$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path

function Sync-Folder {
  param(
    [Parameter(Mandatory = $true)][string]$SourcePath,
    [Parameter(Mandatory = $true)][string]$DestinationPath
  )
  if (-not (Test-Path $SourcePath)) {
    throw "Source folder not found: $SourcePath"
  }
  if (Test-Path $DestinationPath) {
    Remove-Item -LiteralPath $DestinationPath -Recurse -Force
  }
  New-Item -ItemType Directory -Force -Path (Split-Path $DestinationPath -Parent) | Out-Null
  Copy-Item -LiteralPath $SourcePath -Destination $DestinationPath -Recurse -Force
}

function Sync-File {
  param(
    [Parameter(Mandatory = $true)][string]$SourcePath,
    [Parameter(Mandatory = $true)][string]$DestinationPath
  )
  if (-not (Test-Path $SourcePath)) {
    throw "Source file not found: $SourcePath"
  }
  New-Item -ItemType Directory -Force -Path (Split-Path $DestinationPath -Parent) | Out-Null
  Copy-Item -LiteralPath $SourcePath -Destination $DestinationPath -Force
}

function Sync-FileIfExists {
  param(
    [Parameter(Mandatory = $true)][string]$SourcePath,
    [Parameter(Mandatory = $true)][string]$DestinationPath
  )
  if (-not (Test-Path $SourcePath)) {
    Write-Output "[WARN] Optional source file not found, skipping: $SourcePath"
    return
  }
  New-Item -ItemType Directory -Force -Path (Split-Path $DestinationPath -Parent) | Out-Null
  Copy-Item -LiteralPath $SourcePath -Destination $DestinationPath -Force
}

function Remove-IfExists {
  param([string]$PathToRemove)
  if (Test-Path $PathToRemove) {
    Remove-Item -LiteralPath $PathToRemove -Recurse -Force
  }
}

if (-not $SkipDist) {
  $distRoot = Join-Path $root "dist/BCLS_Dashboard_App"
  New-Item -ItemType Directory -Force -Path $distRoot | Out-Null

  Sync-Folder (Join-Path $root "dashboards") (Join-Path $distRoot "dashboards")
  Sync-Folder (Join-Path $root "data")       (Join-Path $distRoot "data")
  Sync-Folder (Join-Path $root "shared")     (Join-Path $distRoot "shared")
  Sync-Folder (Join-Path $root "scripts")    (Join-Path $distRoot "scripts")

  Sync-File (Join-Path $root "BC_Dashboard_App.bat")       (Join-Path $distRoot "BC_Dashboard_App.bat")
  Sync-File (Join-Path $root "INSTALLATION_INSTRUCTION.md") (Join-Path $distRoot "INSTALLATION_INSTRUCTION.md")

  Get-ChildItem -Path $distRoot -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue |
    ForEach-Object { Remove-IfExists $_.FullName }
  Get-ChildItem -Path $distRoot -Recurse -Filter "*.pyc" -File -ErrorAction SilentlyContinue |
    ForEach-Object { Remove-Item -LiteralPath $_.FullName -Force }

  Write-Output "[OK] Dist runtime synced from canonical source."
}

if (-not $SkipSpfx) {
  $spfxRoot = Join-Path $root "spfx/bcls-dashboard-spfx"
  $spfxAssetsRoot = Join-Path $spfxRoot "sharepoint/assets/BCLS-Dashboard"
  $spfxDashboardsRoot = Join-Path $spfxAssetsRoot "dashboards"
  $spfxDataRoot = Join-Path $spfxAssetsRoot "data"
  $spfxSharedRoot = Join-Path $spfxAssetsRoot "shared"

  Sync-Folder (Join-Path $root "dashboards") $spfxDashboardsRoot

  # Keep dashboards lean for SPFx: drop per-dashboard data folders.
  Get-ChildItem -Path $spfxDashboardsRoot -Recurse -Directory -Filter "data" -ErrorAction SilentlyContinue |
    ForEach-Object { Remove-IfExists $_.FullName }

  # Keep only Logo.png in docs folders.
  Get-ChildItem -Path $spfxDashboardsRoot -Recurse -Directory -Filter "docs" -ErrorAction SilentlyContinue |
    ForEach-Object {
      Get-ChildItem -Path $_.FullName -File -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -ne "Logo.png" } |
        ForEach-Object { Remove-Item -LiteralPath $_.FullName -Force }
      if (-not (Get-ChildItem -Path $_.FullName -Force -ErrorAction SilentlyContinue)) {
        Remove-IfExists $_.FullName
      }
    }

  # Rebuild SPFx data folder with only runtime files currently used by dashboards.
  Remove-IfExists $spfxDataRoot
  New-Item -ItemType Directory -Force -Path $spfxDataRoot | Out-Null
  Sync-FileIfExists (Join-Path $root "data/bc_trade_analysis/trade_composition_sample.json") (Join-Path $spfxDataRoot "bc_trade_analysis/trade_composition_sample.json")
  Sync-File (Join-Path $root "data/ourlook_annual_forecast.csv") (Join-Path $spfxDataRoot "bc_economy_outlook/ourlook_annual_forecast.csv")
  Sync-File (Join-Path $root "data/ourlook_quarterly_conditions_2025.csv") (Join-Path $spfxDataRoot "bc_economy_outlook/ourlook_quarterly_conditions_2025.csv")
  Sync-FileIfExists (Join-Path $root "data/bc_economy_outlook/outlook_metadata.json") (Join-Path $spfxDataRoot "bc_economy_outlook/outlook_metadata.json")
  Sync-File (Join-Path $root "data/tourism_lookwest_goals_mock.csv") (Join-Path $spfxDataRoot "tourism_lookwest_goals_mock.csv")
  Sync-File (Join-Path $root "data/life_sciences_lookwest_goals_mock.csv") (Join-Path $spfxDataRoot "life_sciences_lookwest_goals_mock.csv")
  Sync-File (Join-Path $root "data/Action Plans Commitments.csv") (Join-Path $spfxDataRoot "Action Plans Commitments.csv")
  Sync-File (Join-Path $root "data/LW Announcements.csv") (Join-Path $spfxDataRoot "LW Announcements.csv")
  Sync-FileIfExists (Join-Path $root "data/Action Plans.csv") (Join-Path $spfxDataRoot "Action Plans.csv")
  Sync-FileIfExists (Join-Path $root "data/Funding Programs.csv") (Join-Path $spfxDataRoot "Funding Programs.csv")
  Sync-FileIfExists (Join-Path $root "data/Infrastructures.csv") (Join-Path $spfxDataRoot "Infrastructures.csv")
  Sync-FileIfExists (Join-Path $root "data/Investment Promotion.csv") (Join-Path $spfxDataRoot "Investment Promotion.csv")
  Sync-FileIfExists (Join-Path $root "data/LW News.csv") (Join-Path $spfxDataRoot "LW News.csv")
  Sync-FileIfExists (Join-Path $root "data/Major Projects.csv") (Join-Path $spfxDataRoot "Major Projects.csv")
  Sync-FileIfExists (Join-Path $root "data/Major Project Tracker.csv") (Join-Path $spfxDataRoot "Major Project Tracker.csv")
  Sync-FileIfExists (Join-Path $root "data/Policy & Regulations.csv") (Join-Path $spfxDataRoot "Policy & Regulations.csv")
  Sync-FileIfExists (Join-Path $root "data/Targets.csv") (Join-Path $spfxDataRoot "Targets.csv")

  # Rebuild shared folder with only vendor runtime libraries.
  Remove-IfExists $spfxSharedRoot
  New-Item -ItemType Directory -Force -Path $spfxSharedRoot | Out-Null
  Sync-Folder (Join-Path $root "shared/vendor") (Join-Path $spfxSharedRoot "vendor")

  if (-not $NoSpfxManifestRefresh) {
    $manifestScript = Join-Path $spfxRoot "scripts/regenerate-assets-manifest.ps1"
    if (-not (Test-Path $manifestScript)) {
      throw "SPFx manifest script not found: $manifestScript"
    }
    & $manifestScript -ProjectRoot $spfxRoot
  }

  Write-Output "[OK] SPFx assets synced from canonical source."
}

Write-Output "[DONE] Runtime targets sync completed."
