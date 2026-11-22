# Builds the firmware and packs it for the web panel (docs/firmware/firmware.js).
# Windows PowerShell counterpart to tools/release.sh (exact same output format).
# Usage: pwsh -File tools/release.ps1   (or: .\tools\release.ps1)
param(
    [string]$IdfProfile = "C:\Espressif\tools\Microsoft.v5.5.6.PowerShell_profile.ps1",
    [string]$BuildDir = "build-release"
)
$ErrorActionPreference = "Stop"
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path

if (-not (Get-Command idf.py -ErrorAction SilentlyContinue)) {
    if (Test-Path $IdfProfile) { . $IdfProfile }
    else { throw "ESP-IDF profile not found: $IdfProfile" }
}

$env:KEYPET_PUBLIC = "1"
Push-Location (Join-Path $RepoRoot "firmware")
try {
    idf.py -B $BuildDir build
    if ($LASTEXITCODE -ne 0) { throw "idf.py build failed with exit code $LASTEXITCODE" }
} finally {
    Pop-Location
}

$BuildPath = Join-Path $RepoRoot "firmware\$BuildDir"
$OutFile = Join-Path $RepoRoot "docs\firmware\firmware.js"
$CmakeFile = Join-Path $RepoRoot "firmware\CMakeLists.txt"

$Py = @'
import base64, json, os, re, sys, time
build, out_file, cmake_file = sys.argv[1], sys.argv[2], sys.argv[3]
args = open(os.path.join(build, 'flash_args'), encoding='utf-8').read().split()
parts = [{'address': int(a, 16), 'file': f} for a, f in zip(args[6::2], args[7::2])]
for p in parts:
    p['data'] = base64.b64encode(open(os.path.join(build, p.pop('file')), 'rb').read()).decode()
m = re.search(r'PROJECT_VER "([^"]+)"', open(cmake_file, encoding='utf-8').read())
ver = m.group(1) if m else 'dev'
info = {'version': ver, 'built': time.strftime('%Y-%m-%d'), 'parts': parts}
os.makedirs(os.path.dirname(out_file), exist_ok=True)
with open(out_file, 'w', encoding='utf-8', newline='\n') as f:
    f.write("/* Pip's firmware for the panel: made by tools/release.ps1, do not edit */\nwindow.PIP_FIRMWARE = ")
    json.dump(info, f)
    f.write(';\n')
size = sum(len(base64.b64decode(p['data'])) for p in parts)
print(f'docs/firmware/firmware.js: {ver}, {len(parts)} parts, {size // 1024} KB')
'@
$Py | python - $BuildPath $OutFile $CmakeFile
if ($LASTEXITCODE -ne 0) { throw "Packing firmware.js failed" }
