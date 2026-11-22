# Builds the WebAssembly firmware simulator into sim/web/pip.js + sim/web/pip.wasm.
# Activates Emscripten and CMake/Ninja strictly inside this script process (no global PATH edits).
# Usage: .\sim\build-web.ps1
param(
    [string]$EmsdkDir = "D:\emsdk",
    [string]$IdfProfile = "C:\Espressif\tools\Microsoft.v5.5.6.PowerShell_profile.ps1",
    [string]$BuildDir = "build-web"
)
$ErrorActionPreference = "Stop"
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$EmsdkEnv = Join-Path $EmsdkDir "emsdk_env.bat"
if (-not (Test-Path $EmsdkEnv)) {
    throw "Emscripten SDK not found at $EmsdkDir. See sim/README.md for setup."
}

# Ensure cmake and ninja are available locally (reuse ESP-IDF tools if not in PATH)
if (-not (Get-Command cmake -ErrorAction SilentlyContinue) -or -not (Get-Command ninja -ErrorAction SilentlyContinue)) {
    if (Test-Path $IdfProfile) { . $IdfProfile | Out-Null }
}
if (-not (Get-Command cmake -ErrorAction SilentlyContinue)) {
    throw "cmake not found. Install CMake or set -IdfProfile to your ESP-IDF PowerShell profile."
}

$Gen = if (Get-Command ninja -ErrorAction SilentlyContinue) { "-G Ninja" } else { "" }
$BuildPath = Join-Path $RepoRoot $BuildDir
$SimPath = Join-Path $RepoRoot "sim"

$Cmd = "call `"$EmsdkEnv`" && emcmake cmake $Gen -S `"$SimPath`" -B `"$BuildPath`" && cmake --build `"$BuildPath`""
cmd.exe /c $Cmd
if ($LASTEXITCODE -ne 0) { throw "WebAssembly simulator build failed with exit code $LASTEXITCODE" }

$Js = Join-Path $RepoRoot "sim\web\pip.js"
$Wasm = Join-Path $RepoRoot "sim\web\pip.wasm"
Write-Host ("Built: pip.js ({0} KB), pip.wasm ({1} KB)" -f [int]((Get-Item $Js).Length / 1KB), [int]((Get-Item $Wasm).Length / 1KB))
Write-Host "Run:   python sim/serve.py   ->   http://localhost:8466"
