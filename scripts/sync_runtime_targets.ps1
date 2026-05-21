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

  # Keep dashboards lean for SPFx: drop per-dashboard data folders except life sciences CSVs.
  Get-ChildItem -Path $spfxDashboardsRoot -Recurse -Directory -Filter "data" -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notlike "*dashboards\\sectors\\life_sciences\\data" } |
    ForEach-Object { Remove-IfExists $_.FullName }

  # In life sciences dashboard data, keep only the two CSVs used by Sector Snapshot.
  $lsData = Join-Path $spfxDashboardsRoot "sectors/life_sciences/data"
  New-Item -ItemType Directory -Force -Path $lsData | Out-Null
  Sync-File (Join-Path $root "dashboards/sectors/life_sciences/data/LS GDP.csv") (Join-Path $lsData "LS GDP.csv")
  Sync-File (Join-Path $root "dashboards/sectors/life_sciences/data/LS Business Count.csv") (Join-Path $lsData "LS Business Count.csv")

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
  Sync-File (Join-Path $root "data/bc_trade_analysis/trade_composition_sample.json") (Join-Path $spfxDataRoot "bc_trade_analysis/trade_composition_sample.json")
  Sync-File (Join-Path $root "data/bc_economy_outlook/annual_forecast.csv") (Join-Path $spfxDataRoot "bc_economy_outlook/annual_forecast.csv")
  Sync-File (Join-Path $root "data/bc_economy_outlook/quarterly_conditions_2025.csv") (Join-Path $spfxDataRoot "bc_economy_outlook/quarterly_conditions_2025.csv")
  Sync-File (Join-Path $root "data/bc_economy_outlook/outlook_metadata.json") (Join-Path $spfxDataRoot "bc_economy_outlook/outlook_metadata.json")
  Sync-File (Join-Path $root "data/look_west_strategy/look_west_media_coverage_mock.xlsx") (Join-Path $spfxDataRoot "look_west_strategy/look_west_media_coverage_mock.xlsx")
  Sync-File (Join-Path $root "data/look_west_strategy/lw_related_funding_investments_mock.xlsx") (Join-Path $spfxDataRoot "look_west_strategy/lw_related_funding_investments_mock.xlsx")
  Sync-File (Join-Path $root "data/sectors/life_sciences/Life_Sciences_light.xlsx") (Join-Path $spfxDataRoot "sectors/life_sciences/Life_Sciences_light.xlsx")
  Sync-File (Join-Path $root "data/sectors/tourism/tourism_lookwest_goals_mock.csv") (Join-Path $spfxDataRoot "sectors/tourism/tourism_lookwest_goals_mock.csv")
  Sync-File (Join-Path $root "data/sectors/tourism/tourism_initiatives_mock.csv") (Join-Path $spfxDataRoot "sectors/tourism/tourism_initiatives_mock.csv")

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
