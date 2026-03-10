# ============================================================================
# SCRIPT DE INSTALACIÓN AUTOMÁTICA - MEJORAMISO CHATBOT EN IIS
# Ejecutar como Administrador
# ============================================================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "INSTALACIÓN MEJORAMISO CHATBOT EN IIS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Variables de configuración
$siteName = "Mejoramiso-Chatbot"
$appPoolName = "Mejoramiso-AppPool"
$sitePath = "C:\inetpub\wwwroot\mejoramiso"
$port = 8080  # Puerto para el sitio (puedes cambiarlo)

# 1. Verificar permisos de administrador
Write-Host "[1/10] Verificando permisos de administrador..." -ForegroundColor Yellow
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "ERROR: Debes ejecutar este script como Administrador" -ForegroundColor Red
    Write-Host "Click derecho -> Ejecutar como administrador" -ForegroundColor Red
    pause
    exit
}
Write-Host "✓ Permisos verificados" -ForegroundColor Green

# 2. Instalar componentes de IIS
Write-Host "`n[2/10] Instalando componentes de IIS..." -ForegroundColor Yellow
try {
    Enable-WindowsOptionalFeature -Online -FeatureName IIS-WebServerRole -All -NoRestart
    Enable-WindowsOptionalFeature -Online -FeatureName IIS-WebServer -All -NoRestart
    Enable-WindowsOptionalFeature -Online -FeatureName IIS-CommonHttpFeatures -All -NoRestart
    Enable-WindowsOptionalFeature -Online -FeatureName IIS-HttpErrors -All -NoRestart
    Enable-WindowsOptionalFeature -Online -FeatureName IIS-ApplicationDevelopment -All -NoRestart
    Enable-WindowsOptionalFeature -Online -FeatureName IIS-CGI -All -NoRestart
    Enable-WindowsOptionalFeature -Online -FeatureName IIS-HealthAndDiagnostics -All -NoRestart
    Enable-WindowsOptionalFeature -Online -FeatureName IIS-HttpLogging -All -NoRestart
    Write-Host "✓ IIS instalado correctamente" -ForegroundColor Green
} catch {
    Write-Host "⚠ IIS ya está instalado o error al instalar" -ForegroundColor Yellow
}

# 3. Verificar instalación de Python
Write-Host "`n[3/10] Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python encontrado: $pythonVersion" -ForegroundColor Green
    $pythonPath = (Get-Command python).Source
    Write-Host "  Ruta: $pythonPath" -ForegroundColor Gray
} catch {
    Write-Host "ERROR: Python no está instalado" -ForegroundColor Red
    Write-Host "Descarga Python 3.11+ desde: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "IMPORTANTE: Durante la instalación marca 'Add Python to PATH'" -ForegroundColor Yellow
    pause
    exit
}

# 4. Crear directorio del sitio
Write-Host "`n[4/10] Creando directorio del sitio..." -ForegroundColor Yellow
if (Test-Path $sitePath) {
    Write-Host "⚠ El directorio $sitePath ya existe" -ForegroundColor Yellow
    $overwrite = Read-Host "¿Deseas sobrescribir? (S/N)"
    if ($overwrite -eq "S" -or $overwrite -eq "s") {
        Remove-Item -Path $sitePath -Recurse -Force
        Write-Host "✓ Directorio eliminado" -ForegroundColor Green
    } else {
        Write-Host "Instalación cancelada" -ForegroundColor Red
        pause
        exit
    }
}
New-Item -ItemType Directory -Path $sitePath -Force | Out-Null
New-Item -ItemType Directory -Path "$sitePath\logs" -Force | Out-Null
New-Item -ItemType Directory -Path "$sitePath\templates" -Force | Out-Null
Write-Host "✓ Directorio creado: $sitePath" -ForegroundColor Green

# 5. Crear entorno virtual de Python
Write-Host "`n[5/10] Creando entorno virtual de Python..." -ForegroundColor Yellow
Set-Location $sitePath
python -m venv venv
Write-Host "✓ Entorno virtual creado" -ForegroundColor Green

# 6. Activar entorno virtual e instalar dependencias
Write-Host "`n[6/10] Instalando dependencias de Python..." -ForegroundColor Yellow
& "$sitePath\venv\Scripts\Activate.ps1"
python -m pip install --upgrade pip
pip install Flask requests python-dotenv wfastcgi
Write-Host "✓ Dependencias instaladas" -ForegroundColor Green

# 7. Habilitar wfastcgi
Write-Host "`n[7/10] Configurando FastCGI..." -ForegroundColor Yellow
wfastcgi-enable
Write-Host "✓ FastCGI habilitado" -ForegroundColor Green

# 8. Configurar permisos
Write-Host "`n[8/10] Configurando permisos..." -ForegroundColor Yellow
$acl = Get-Acl $sitePath
$permission = "IIS_IUSRS", "FullControl", "ContainerInherit,ObjectInherit", "None", "Allow"
$accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule $permission
$acl.SetAccessRule($accessRule)
Set-Acl $sitePath $acl
Write-Host "✓ Permisos configurados para IIS_IUSRS" -ForegroundColor Green

# 9. Crear Application Pool
Write-Host "`n[9/10] Creando Application Pool..." -ForegroundColor Yellow
Import-Module WebAdministration
if (Test-Path "IIS:\AppPools\$appPoolName") {
    Remove-WebAppPool -Name $appPoolName
}
New-WebAppPool -Name $appPoolName
Set-ItemProperty "IIS:\AppPools\$appPoolName" -Name managedRuntimeVersion -Value ""
Set-ItemProperty "IIS:\AppPools\$appPoolName" -Name processModel.identityType -Value "ApplicationPoolIdentity"
Write-Host "✓ Application Pool creado: $appPoolName" -ForegroundColor Green

# 10. Crear sitio web en IIS
Write-Host "`n[10/10] Creando sitio web en IIS..." -ForegroundColor Yellow
if (Test-Path "IIS:\Sites\$siteName") {
    Remove-WebSite -Name $siteName
}
New-WebSite -Name $siteName -Port $port -PhysicalPath $sitePath -ApplicationPool $appPoolName
Write-Host "✓ Sitio web creado: $siteName" -ForegroundColor Green

# Resumen
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "INSTALACIÓN COMPLETADA" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📁 Directorio: $sitePath" -ForegroundColor White
Write-Host "🌐 URL: http://localhost:$port" -ForegroundColor White
Write-Host "⚙️  Application Pool: $appPoolName" -ForegroundColor White
Write-Host ""
Write-Host "PRÓXIMOS PASOS:" -ForegroundColor Yellow
Write-Host "1. Copia tus archivos a: $sitePath" -ForegroundColor White
Write-Host "   - app.py" -ForegroundColor Gray
Write-Host "   - web.config" -ForegroundColor Gray
Write-Host "   - templates/" -ForegroundColor Gray
Write-Host "   - .env (con tu GROQ_API_KEY)" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Reinicia IIS: iisreset" -ForegroundColor White
Write-Host ""
Write-Host "3. Accede a: http://localhost:$port" -ForegroundColor White
Write-Host ""
Write-Host "IMPORTANTE: Configura GROQ_API_KEY en .env" -ForegroundColor Yellow
Write-Host ""
pause