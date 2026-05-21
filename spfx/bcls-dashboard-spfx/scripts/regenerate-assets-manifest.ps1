param(
  [string]$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
)

$assetRoot = Join-Path $ProjectRoot 'sharepoint/assets/BCLS-Dashboard'
$elementsPath = Join-Path $ProjectRoot 'sharepoint/assets/elements.xml'
$packagePath = Join-Path $ProjectRoot 'config/package-solution.json'

if (-not (Test-Path $assetRoot)) {
  throw "Asset root not found: $assetRoot"
}

$files = Get-ChildItem -Path $assetRoot -Recurse -File | Sort-Object FullName
$rels = foreach ($f in $files) {
  $f.FullName.Substring($assetRoot.Length + 1) -replace '\\','/'
}

$xml = @()
$xml += '<?xml version="1.0" encoding="utf-8"?>'
$xml += '<Elements xmlns="http://schemas.microsoft.com/sharepoint/">'
$xml += '  <Module Name="BCLSDashboardAssets" Url="SiteAssets/BCLS-Dashboard">'
foreach ($rel in $rels) {
  $xml += "    <File Path=""BCLS-Dashboard/$rel"" Url=""$rel"" Type=""GhostableInLibrary"" ReplaceContent=""TRUE"" />"
}
$xml += '  </Module>'
$xml += '</Elements>'
$xml -join "`r`n" | Set-Content -Path $elementsPath -Encoding UTF8

$pkg = Get-Content $packagePath -Raw | ConvertFrom-Json
$pkg.solution.features[0].assets.elementFiles = @($rels | ForEach-Object { "BCLS-Dashboard/$_" })
$pkg | ConvertTo-Json -Depth 20 | Set-Content -Path $packagePath -Encoding UTF8

Write-Output "Updated elements.xml and package-solution.json with $($rels.Count) files."
