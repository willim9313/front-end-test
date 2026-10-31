# Screenshot style pages into styles/<slug>/thumb.jpg (640x400) with headless Edge,
# for machines without Node/Playwright (same output as overview/tools/thumbs.js).
# Run from the repo root with a static server on :8000:
#   powershell -ExecutionPolicy Bypass -File tools/thumbs.ps1 [slug ...]
param([Parameter(ValueFromRemainingArguments = $true)][string[]]$Slugs)

$edge = "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe"
if (-not (Test-Path $edge)) { $edge = "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe" }
if (-not $Slugs) { $Slugs = Get-ChildItem styles -Directory | ForEach-Object Name }

Add-Type -AssemblyName System.Drawing
$jpeg = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object MimeType -eq 'image/jpeg'
$params = New-Object System.Drawing.Imaging.EncoderParameters 1
$params.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter ([System.Drawing.Imaging.Encoder]::Quality, [long]78)
foreach ($slug in $Slugs) {
  $png = Join-Path $env:TEMP "thumb-$slug.png"
  # a fresh profile per shot, or Edge hands off to the previous instance and writes nothing
  $profile = Join-Path $env:TEMP "thumbs-edge-$slug"
  # ?thumb hides the shared spec bar; reduced motion shows every page in its finished state
  & $edge --headless=new --disable-gpu --hide-scrollbars --user-data-dir="$profile" `
    --force-prefers-reduced-motion --force-color-profile=srgb `
    --window-size=1280,800 --force-device-scale-factor=0.5 --virtual-time-budget=6000 `
    --screenshot="$png" "http://localhost:8000/styles/$slug/?thumb" 2>$null | Out-Null
  if (-not (Test-Path $png)) { Write-Warning "no screenshot for $slug"; continue }
  $img = [System.Drawing.Image]::FromFile($png)
  $out = New-Object System.Drawing.Bitmap 640, 400
  $g = [System.Drawing.Graphics]::FromImage($out)
  $g.InterpolationMode = 'HighQualityBicubic'
  $g.DrawImage($img, 0, 0, 640, 400)
  $out.Save((Resolve-Path "styles/$slug").Path + "\thumb.jpg", $jpeg, $params)
  $g.Dispose(); $out.Dispose(); $img.Dispose(); Remove-Item $png
  Write-Host "thumb $slug"
}
