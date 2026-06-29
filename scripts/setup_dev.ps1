$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$VenvPath = Join-Path $ProjectRoot ".venv"

function Invoke-ProofScopeCommand {
    param([scriptblock]$Command)
    & $Command
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed with exit code $LASTEXITCODE"
    }
}

if (-not (Test-Path $VenvPath)) {
    Invoke-ProofScopeCommand { python -m venv $VenvPath }
}

Invoke-ProofScopeCommand { & "$VenvPath\Scripts\python.exe" -m pip install --upgrade pip }
Invoke-ProofScopeCommand { & "$VenvPath\Scripts\python.exe" -m pip install -r (Join-Path $ProjectRoot "requirements-dev.txt") }

Write-Host "ProofScope development environment is ready."
