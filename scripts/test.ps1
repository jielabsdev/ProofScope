$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$VenvPython = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$Python = if (Test-Path $VenvPython) { $VenvPython } else { "python" }

Set-Location $ProjectRoot
& $Python -m pytest
if ($LASTEXITCODE -ne 0) {
    throw "Command failed with exit code $LASTEXITCODE"
}
