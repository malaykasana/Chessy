# Build a Windows desktop EXE for Chess Analyser using PyInstaller
# Usage: Run from project root in PowerShell

$ErrorActionPreference = 'Stop'

# Paths
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
# Prefer Windows venv Python; fallback to bin for mixed setups
$pyWin = Join-Path $root '.venv/Scripts/python.exe'
$pyBin = Join-Path $root '.venv/bin/python.exe'
if (Test-Path $pyWin) { $python = $pyWin }
elseif (Test-Path $pyBin) { $python = $pyBin }
else { $python = $null }
$pyinstaller = "$root/.venv/Lib/site-packages/PyInstaller/__main__.py"

if (-not $python -or -not (Test-Path $python)) {
    Write-Error "Python venv not found at $python. Activate your venv or update the path in this script."
}

# Ensure PyInstaller is installed
& $python -m pip install --upgrade pip | Out-Host
& $python -m pip install pyinstaller | Out-Host

# Sanitize environment to avoid MSYS Python DLL conflicts
$originalPath = $env:PATH
try {
    $env:PYTHONHOME = ''
    $env:PYTHONPATH = ''
    $filtered = ($originalPath -split ';') | Where-Object { $_ -and ($_ -notlike 'C:\msys64*') }
    $env:PATH = ($filtered -join ';')
} catch {}

# Output dir
$outDir = Join-Path $root 'dist'
if (!(Test-Path $outDir)) { New-Item -ItemType Directory -Path $outDir | Out-Null }

# Copy Stockfish binary into a bundled folder so the app can find it when frozen
$stockfishSrc = Join-Path $root 'stockfish/stockfish-windows-x86-64-avx2.exe'
$stockfishDst = Join-Path $root 'stockfish'
if (Test-Path $stockfishSrc) {
    if (!(Test-Path $stockfishDst)) { New-Item -ItemType Directory -Path $stockfishDst | Out-Null }
    $stockfishDstFile = Join-Path $stockfishDst (Split-Path -Leaf $stockfishSrc)
    if (!(Test-Path $stockfishDstFile)) {
        Copy-Item -Force $stockfishSrc $stockfishDstFile
    }
}

# Build
$icon = '' # Optional: set to an .ico path
$addData = "stockfish;stockfish" # folder;dest

$pyiArgs = @(
    '-m','PyInstaller',
    '--noconfirm',
    '--windowed',
    '--clean',
    "--add-data=$addData"
)
if ($icon) { $pyiArgs += "--icon=$icon" }
$pyiArgs += @('chess_gui.py','--name','Chessy')

    # Prevent user site from affecting PyInstaller
    $env:PYTHONNOUSERSITE = '1'
& $python $pyiArgs | Out-Host
if ($LASTEXITCODE -ne 0) { Write-Error "PyInstaller failed with exit code $LASTEXITCODE" }

# Restore PATH
if ($originalPath) { $env:PATH = $originalPath }

Write-Host "Build complete. Find the EXE under $root\dist\\Chessy\\Chessy.exe"

