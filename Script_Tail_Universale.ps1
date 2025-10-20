# ───────── Determina la cartella base dello script o eseguibile Python ─────────
# Se eseguito come script PowerShell, usa la cartella dello script
$scriptDir = $PSScriptRoot

# Controlla se esiste una variabile d’ambiente personalizzata con la cartella dell’eseguibile
# Ad esempio puoi esportarla nel tuo Python con: os.environ["APP_BASE_DIR"] = base_dir
if ($env:APP_BASE_DIR) {
    $baseDir = $env:APP_BASE_DIR
} else {
    $baseDir = $scriptDir
}

# ───────── Cartella LogFiles ─────────
$logDir = Join-Path -Path $baseDir -ChildPath "LogFiles"

if (-Not (Test-Path $logDir)) {
    Write-Host "La cartella dei log non esiste: $logDir"
    exit
}

# ───────── Trova il file .log più recente ─────────
$latestLog = Get-ChildItem -Path $logDir -Filter *.log |
             Sort-Object LastWriteTime -Descending |
             Select-Object -First 1

if ($null -eq $latestLog) {
    Write-Host "Nessun file .log trovato nella cartella: $logDir"
    exit
}

Write-Host "Apro il file log più recente: $($latestLog.Name)"

# ───────── Segui il file log come 'tail -f' ─────────
Get-Content -Path $latestLog.FullName -Wait
