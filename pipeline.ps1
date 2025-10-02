# Simple pipeline script for Windows PowerShell

# Check requirements
Write-Host "Checking requirements..."
if (-not (Get-Command python -ErrorAction SilentlyContinue)) { Write-Host "Python not found"; exit 1 }
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) { Write-Host "Docker not found"; exit 1 }
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { Write-Host "Git not found"; exit 1 }
if (-not (Test-Path .env)) { Write-Host ".env file missing"; exit 1 }
if (Test-Path requirements.txt) {
    & python -m pip install -q -r requirements.txt
    if ($LASTEXITCODE -ne 0) { Write-Host "Failed to install requirements"; exit 1 }
}
New-Item -ItemType Directory -Force -Path logs | Out-Null
Write-Host "Requirements check passed."

# Run tests
Write-Host "Running tests..."
& python -m unittest discover > logs/test.log 2>&1
$LASTEXITCODE | Out-File -FilePath logs/test.exit -Encoding ascii

# Build Docker image
Write-Host "Building Docker image..."
& docker build -t myapp . > logs/build_docker.log 2>&1
$LASTEXITCODE | Out-File -FilePath logs/build_docker.exit -Encoding ascii

# Smoke test
Write-Host "Running smoke tests..."
& python smoke_test.py > logs/smoke.log 2>&1
$LASTEXITCODE | Out-File -FilePath logs/smoke.exit -Encoding ascii

# Capture logs
& python capture_logs.py

# Post pipeline
& python post_pipeline.py

Write-Host "Pipeline completed."
