# Baixa o instalador do Python 3.11
$pythonUrl = "https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe"
$installerPath = "$env:TEMP\python311.exe"

Write-Host "Baixando Python 3.11..."
Invoke-WebRequest -Uri $pythonUrl -OutFile $installerPath

# Instala Python 3.11
Write-Host "Instalando Python 3.11..."
Start-Process -FilePath $installerPath -ArgumentList "/quiet", "InstallAllUsers=1", "PrependPath=1" -Wait

# Remove o instalador
Remove-Item $installerPath

Write-Host "Python 3.11 instalado com sucesso!"
Write-Host "Por favor, reinicie o PowerShell para que as alterações tenham efeito." 