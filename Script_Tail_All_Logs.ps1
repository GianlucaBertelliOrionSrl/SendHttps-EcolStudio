Get-ChildItem -Path . -Filter *.log | ForEach-Object {
    Get-Content -Path $_.FullName -Wait
}
