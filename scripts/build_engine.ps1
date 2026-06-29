$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$VenvPython = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$Python = if (Test-Path $VenvPython) { $VenvPython } else { "python" }

function Invoke-ProofScopeCommand {
    param([scriptblock]$Command)
    & $Command
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed with exit code $LASTEXITCODE"
    }
}

Invoke-ProofScopeCommand { & $Python -m pip install --upgrade pip build scikit-build-core pybind11 cmake ninja }
Invoke-ProofScopeCommand { & $Python -m pip install --no-build-isolation -e $ProjectRoot }

Write-Host "ProofScope C++ bridge build completed."
