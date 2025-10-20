$logDir = "C:\Percorso\Alla\Cartella"
Get-ChildItem -Path $logDir -Filter *.log | ForEach-Object {
    Get-Content -Path $_.FullName -Wait
}
