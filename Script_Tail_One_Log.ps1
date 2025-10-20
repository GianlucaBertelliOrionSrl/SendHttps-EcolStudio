$logFile = Get-ChildItem -Path . -Filter *.log | Select-Object -First 1
Get-Content -Path $logFile.FullName -Wait
