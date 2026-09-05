[CmdletBinding(PositionalBinding = $false)]
param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$PytestArgs,
    [string]$DatabaseName = "lifelikegame_test",
    [string]$PostgresUser = "postgres",
    [string]$PostgresPassword = "postgres",
    [string]$HostPort = "5433"
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$BackendDir = Split-Path -Parent $ScriptDir
$ProjectRoot = Split-Path -Parent $BackendDir
$Python = Join-Path $BackendDir ".venv\Scripts\python.exe"

if (-not (Test-Path $Python)) {
    throw "Backend virtual environment not found at $Python. Create it and install requirements first."
}

Set-Location $ProjectRoot

docker compose up -d db

$dbExists = docker exec lifelikegame_db psql -U $PostgresUser -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname = '$DatabaseName'"
if (($dbExists | Out-String).Trim() -ne "1") {
    docker exec lifelikegame_db createdb -U $PostgresUser $DatabaseName
}

$env:DATABASE_URL = "postgresql://$PostgresUser`:$PostgresPassword@localhost:$HostPort/$DatabaseName"
$env:TEST_DATABASE_URL = $env:DATABASE_URL
$env:JWT_SECRET = "test-secret-key"
$env:JWT_ALG = "HS256"
$env:ACCESS_TOKEN_EXPIRE_MINUTES = "60"
Remove-Item Env:SCHEDULER_ENABLED -ErrorAction SilentlyContinue

Set-Location $BackendDir

if (-not $PytestArgs -or $PytestArgs.Count -eq 0) {
    $PytestArgs = @("-q")
}

& $Python -m pytest @PytestArgs
exit $LASTEXITCODE
