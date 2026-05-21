Add-Type -AssemblyName System.Drawing

$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$outDir = Join-Path $PSScriptRoot "backgrounds"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

$W = 1280
$H = 720

$colors = @{
  Navy      = [System.Drawing.Color]::FromArgb(0, 51, 102)
  Navy2     = [System.Drawing.Color]::FromArgb(26, 82, 118)
  Gold      = [System.Drawing.Color]::FromArgb(252, 186, 25)
  Bg        = [System.Drawing.Color]::FromArgb(242, 245, 249)
  Card      = [System.Drawing.Color]::White
  Border    = [System.Drawing.Color]::FromArgb(214, 220, 228)
  Text      = [System.Drawing.Color]::FromArgb(26, 32, 44)
  Muted     = [System.Drawing.Color]::FromArgb(74, 85, 104)
  Subtle    = [System.Drawing.Color]::FromArgb(113, 128, 150)
  HeaderDim = [System.Drawing.Color]::FromArgb(215, 226, 238)
  Red       = [System.Drawing.Color]::FromArgb(197, 48, 48)
  Amber     = [System.Drawing.Color]::FromArgb(192, 86, 33)
  Green     = [System.Drawing.Color]::FromArgb(39, 103, 73)
  SoftBlue  = [System.Drawing.Color]::FromArgb(235, 242, 250)
}

$fontTitle = New-Object System.Drawing.Font("Segoe UI Semibold", 15)
$fontSub = New-Object System.Drawing.Font("Segoe UI", 9)
$fontNav = New-Object System.Drawing.Font("Segoe UI Semibold", 8)
$fontSection = New-Object System.Drawing.Font("Segoe UI Semibold", 9)
$fontSmall = New-Object System.Drawing.Font("Segoe UI", 8)
$fontKpi = New-Object System.Drawing.Font("Segoe UI Semibold", 10)

function New-Pen($color, $width = 1) {
  return New-Object System.Drawing.Pen($color, $width)
}

function New-Brush($color) {
  return New-Object System.Drawing.SolidBrush($color)
}

function Get-RoundedPath($x, $y, $w, $h, $r) {
  $path = New-Object System.Drawing.Drawing2D.GraphicsPath
  $d = $r * 2
  $path.AddArc($x, $y, $d, $d, 180, 90)
  $path.AddArc($x + $w - $d, $y, $d, $d, 270, 90)
  $path.AddArc($x + $w - $d, $y + $h - $d, $d, $d, 0, 90)
  $path.AddArc($x, $y + $h - $d, $d, $d, 90, 90)
  $path.CloseFigure()
  return $path
}

function Draw-RoundedRect($g, $x, $y, $w, $h, $fill, $stroke, $r = 6) {
  $path = Get-RoundedPath $x $y $w $h $r
  $g.FillPath((New-Brush $fill), $path)
  if ($stroke) { $g.DrawPath((New-Pen $stroke), $path) }
  $path.Dispose()
}

function Draw-Text($g, $text, $x, $y, $w, $h, $font, $color, $align = "Near") {
  $fmt = New-Object System.Drawing.StringFormat
  $fmt.Alignment = [System.Drawing.StringAlignment]::$align
  $fmt.LineAlignment = [System.Drawing.StringAlignment]::Near
  $fmt.Trimming = [System.Drawing.StringTrimming]::EllipsisCharacter
  $g.DrawString($text, $font, (New-Brush $color), (New-Object System.Drawing.RectangleF($x, $y, $w, $h)), $fmt)
  $fmt.Dispose()
}

function Draw-Card($g, $x, $y, $w, $h, $title = "", $accent = $null) {
  Draw-RoundedRect $g $x $y $w $h $colors.Card $colors.Border 6
  if ($accent) {
    $g.FillRectangle((New-Brush $accent), $x, $y, $w, 4)
  }
  if ($title) {
    Draw-Text $g $title ($x + 14) ($y + 11) ($w - 28) 18 $fontSection $colors.Text
  }
}

function Draw-KpiRow($g, $labels, $x, $y, $w, $h, $accent) {
  $gap = 10
  $cw = [math]::Floor(($w - ($gap * ($labels.Count - 1))) / $labels.Count)
  for ($i = 0; $i -lt $labels.Count; $i++) {
    $cx = $x + ($i * ($cw + $gap))
    Draw-Card $g $cx $y $cw $h $labels[$i] $accent
  }
}

function Draw-PlaceholderChart($g, $x, $y, $w, $h, $title, $kind = "line") {
  Draw-Card $g $x $y $w $h $title $null
}

function Draw-Table($g, $x, $y, $w, $h, $title) {
  Draw-Card $g $x $y $w $h $title $null
}

function Draw-Header($g, $title, $subtitle, $active) {
  $g.Clear($colors.Bg)
  $g.FillRectangle((New-Brush $colors.Navy), 0, 0, $W, 62)
  $g.FillRectangle((New-Brush $colors.Gold), 0, 62, $W, 4)

  $logoPath = Join-Path $root "shared\assets\logo\BCID_H_RGB_rev.png"
  if (Test-Path $logoPath) {
    $logo = [System.Drawing.Image]::FromFile($logoPath)
    $ratio = [double]$logo.Width / [double]$logo.Height
    $lh = 36
    $lw = [int]($lh * $ratio)
    $g.DrawImage($logo, 24, 13, $lw, $lh)
    $logo.Dispose()
    $textX = 24 + $lw + 28
  } else {
    $textX = 28
  }
  Draw-Text $g $title $textX 12 620 24 $fontTitle ([System.Drawing.Color]::White
  )
  Draw-Text $g $subtitle $textX 38 700 16 $fontSub $colors.HeaderDim
  Draw-Text $g "Internal working dashboard" 1070 17 180 16 $fontSmall $colors.HeaderDim "Far"
  Draw-Text $g "Power BI Visual Shell" 1070 35 180 16 $fontSmall ([System.Drawing.Color]::White) "Far"

  $nav = @("Hub", "Life Sciences", "Look West", "Macroeconomy", "Trade", "Evidence & Risks")
  $x = 24
  $y = 78
  foreach ($n in $nav) {
    $ww = if ($n -eq "Evidence & Risks") { 142 } elseif ($n -eq "Life Sciences" -or $n -eq "Macroeconomy") { 122 } else { 100 }
    $fill = if ($n -eq $active) { $colors.Navy } else { [System.Drawing.Color]::White }
    $stroke = if ($n -eq $active) { $colors.Navy } else { $colors.Border }
    $txt = if ($n -eq $active) { [System.Drawing.Color]::White } else { $colors.Muted }
    Draw-RoundedRect $g $x $y $ww 32 $fill $stroke 5
    if ($n -eq $active) { $g.FillRectangle((New-Brush $colors.Gold), $x + 10, $y + 28, $ww - 20, 3) }
    Draw-Text $g $n ($x + 8) ($y + 8) ($ww - 16) 14 $fontNav $txt "Center"
    $x += $ww + 8
  }
}

function Save-Canvas($name, $drawAction) {
  $bmp = New-Object System.Drawing.Bitmap($W, $H)
  $g = [System.Drawing.Graphics]::FromImage($bmp)
  $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
  $g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::ClearTypeGridFit
  & $drawAction $g
  $path = Join-Path $outDir $name
  $bmp.Save($path, [System.Drawing.Imaging.ImageFormat]::Png)
  $g.Dispose()
  $bmp.Dispose()
  Write-Output $path
}

Save-Canvas "01_Hub_Background.png" {
  param($g)
  Draw-Header $g "B.C. Insights Dashboard" "Executive hub and sector navigation" "Hub"
  Draw-KpiRow $g @("Total Investment", "Jobs Created", "Active Goals", "Open Risks", "Latest Refresh") 24 130 1232 82 $colors.Gold
  Draw-Card $g 24 232 600 210 "Dashboard Sections" $colors.Navy
  Draw-Card $g 648 232 608 210 "Sector Readiness" $colors.Navy2
  $cards = @("Life Sciences", "Look West Strategy", "Macroeconomy", "Trade Analysis", "Evidence and Risks", "Projects")
  for ($i = 0; $i -lt $cards.Count; $i++) {
    $cx = 48 + (($i % 3) * 184)
    $cy = 286 + ([math]::Floor($i / 3) * 70)
    Draw-RoundedRect $g $cx $cy 164 48 $colors.SoftBlue $colors.Border 5
    Draw-Text $g $cards[$i] ($cx + 12) ($cy + 15) 140 16 $fontNav $colors.Navy "Center"
  }
  Draw-Table $g 24 466 1232 220 "Dashboard Status and Ownership"
}

Save-Canvas "02_Life_Sciences_Background.png" {
  param($g)
  Draw-Header $g "B.C. Life Sciences" "Sector performance, strategy progress, evidence, and risks" "Life Sciences"
  Draw-Card $g 24 128 1232 72 "Sector Definition" $colors.Navy
  Draw-KpiRow $g @("Employment", "GDP", "Revenue", "Businesses", "Exports", "Funding") 24 216 1232 78 $colors.Navy
  Draw-PlaceholderChart $g 24 312 292 142 "Employment Trend" "line"
  Draw-PlaceholderChart $g 336 312 292 142 "GDP Contribution" "line"
  Draw-PlaceholderChart $g 648 312 292 142 "Business Count" "bar"
  Draw-PlaceholderChart $g 964 312 292 142 "Goods Exports" "bar"
  Draw-Table $g 24 474 604 220 "Strategy Goals and Initiatives"
  Draw-Table $g 648 474 608 220 "Evidence and Risks"
}

Save-Canvas "03_Look_West_Background.png" {
  param($g)
  Draw-Header $g "Look West Strategy" "Media, funding, policy, and investment tracking" "Look West"
  Draw-KpiRow $g @("Media Items", "Gov Mentions", "Funding", "Policy Items", "Investment", "Jobs") 24 130 1232 78 $colors.Gold
  Draw-PlaceholderChart $g 24 226 292 144 "Investment by Pillar" "bar"
  Draw-PlaceholderChart $g 336 226 292 144 "Funding Mix" "bar"
  Draw-PlaceholderChart $g 648 226 292 144 "Top Regions" "bar"
  Draw-PlaceholderChart $g 964 226 292 144 "Employment Impact" "bar"
  Draw-Table $g 24 392 600 140 "Media Tracker"
  Draw-Table $g 648 392 608 140 "Funding and Investments"
  Draw-Table $g 24 552 1232 142 "Policy and Regulations"
}

Save-Canvas "04_Macroeconomy_Background.png" {
  param($g)
  Draw-Header $g "B.C. Macroeconomy" "Statistics Canada economic indicator briefing" "Macroeconomy"
  Draw-KpiRow $g @("Labour", "GDP", "CPI", "Trade", "Retail", "Permits") 24 130 1232 78 $colors.Navy
  Draw-PlaceholderChart $g 24 230 396 190 "Labour Trend" "line"
  Draw-PlaceholderChart $g 442 230 396 190 "GDP Trend" "line"
  Draw-PlaceholderChart $g 860 230 396 190 "CPI Trend" "line"
  Draw-PlaceholderChart $g 24 444 396 190 "Trade Trend" "line"
  Draw-PlaceholderChart $g 442 444 396 190 "Retail Sales" "line"
  Draw-PlaceholderChart $g 860 444 396 190 "Building Permits" "line"
}

Save-Canvas "05_Trade_Analysis_Background.png" {
  param($g)
  Draw-Header $g "B.C. Trade Analysis" "Composition, partners, and interprovincial flows" "Trade"
  Draw-Card $g 24 128 1232 50 "Filters: Year, Flow, Partner Mode" $colors.Gold
  Draw-KpiRow $g @("Exports", "Imports", "Balance", "Top Category", "Top Partner") 24 194 1232 80 $colors.Navy
  Draw-PlaceholderChart $g 24 292 396 188 "Trade Composition" "bar"
  Draw-PlaceholderChart $g 442 292 396 188 "Partner Ranking" "bar"
  Draw-PlaceholderChart $g 860 292 396 188 "Export / Import Trend" "line"
  Draw-Table $g 24 502 604 192 "Composition Detail"
  Draw-Table $g 648 502 608 192 "Interprovincial Trade"
}

Save-Canvas "06_Evidence_Risks_Background.png" {
  param($g)
  Draw-Header $g "Evidence and Risks" "Source confidence, risks, gaps, and mitigation tracking" "Evidence & Risks"
  Draw-KpiRow $g @("Evidence Items", "Risks / Gaps", "Red Risks", "Amber Risks", "Latest Review") 24 130 1232 78 $colors.Amber
  Draw-Card $g 24 228 1232 46 "Filters: Subsector, Evidence Type, Risk Category, RAG Status" $colors.Navy
  Draw-Table $g 24 296 604 398 "Evidence Library"
  Draw-Table $g 648 296 608 398 "Risks and Gaps"
}
