# 🚀 Guía de Despliegue - Mejoramiso Chatbot en IIS (Windows Server)

## 📋 Tabla de Contenidos
1. [Requisitos Previos](#requisitos-previos)
2. [Método Rápido (Recomendado)](#método-rápido-recomendado)
3. [Método Manual](#método-manual)
4. [Configuración de Variables de Entorno](#configuración-de-variables-de-entorno)
5. [Pruebas y Verificación](#pruebas-y-verificación)
6. [Solución de Problemas](#solución-de-problemas)
7. [Producción y Seguridad](#producción-y-seguridad)

---

## 📦 Requisitos Previos

### Software Necesario
- ✅ **Windows Server 2016/2019/2022** o Windows 10/11 Pro
- ✅ **IIS (Internet Information Services)** instalado
- ✅ **Python 3.8 o superior** ([Descargar aquí](https://www.python.org/downloads/))
- ✅ **Permisos de Administrador**

### Verificar Instalaciones

```powershell
# Verificar Python
python --version

# Verificar IIS
Get-WindowsFeature -Name Web-Server
```

---

## 🎯 Método Rápido (Recomendado)

### Paso 1: Descargar el Proyecto

Copia tu proyecto completo al servidor en: `C:\Proyectos\Mejoramiso-Chatbot\`

**Estructura de archivos:**
```
C:\Proyectos\Mejoramiso-Chatbot\
├── app.py                    # Backend Flask
├── web.config               # Configuración IIS
├── requirements.txt         # Dependencias Python
├── .env                     # Variables de entorno (CREAR)
├── install.ps1             # Script de instalación (EJECUTAR)
├── templates/
│   ├── index.html          # Chat de usuario
│   └── dashboard.html      # Dashboard admin
└── README.md
```

### Paso 2: Ejecutar Script de Instalación

1. **Abrir PowerShell como Administrador:**
   - Click derecho en el botón de Windows
   - "Windows PowerShell (Administrador)"

2. **Navegar al proyecto:**
   ```powershell
   cd C:\Proyectos\Mejoramiso-Chatbot
   ```

3. **Permitir ejecución de scripts:**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
   ```

4. **Ejecutar instalación:**
   ```powershell
   .\install.ps1
   ```

5. **Seguir las instrucciones en pantalla**

### Paso 3: Copiar Archivos

El script creará el directorio: `C:\inetpub\wwwroot\mejoramiso\`

**Copia estos archivos:**
```powershell
# Copiar archivos principales
Copy-Item "C:\Proyectos\Mejoramiso-Chatbot\app.py" "C:\inetpub\wwwroot\mejoramiso\"
Copy-Item "C:\Proyectos\Mejoramiso-Chatbot\web.config" "C:\inetpub\wwwroot\mejoramiso\"
Copy-Item "C:\Proyectos\Mejoramiso-Chatbot\.env" "C:\inetpub\wwwroot\mejoramiso\"

# Copiar templates
Copy-Item "C:\Proyectos\Mejoramiso-Chatbot\templates\*" "C:\inetpub\wwwroot\mejoramiso\templates\" -Recurse
```

### Paso 4: Configurar Variables de Entorno

**Crear archivo `.env` en `C:\inetpub\wwwroot\mejoramiso\.env`:**
```env
GROQ_API_KEY=gsk_tu_clave_api_aqui
```

### Paso 5: Reiniciar IIS

```powershell
iisreset
```

### Paso 6: Probar

Abre tu navegador y ve a: **http://localhost:8080**

---

## 🔧 Método Manual

### 1. Instalar IIS

```powershell
# Ejecutar como Administrador
Enable-WindowsOptionalFeature -Online -FeatureName IIS-WebServerRole
Enable-WindowsOptionalFeature -Online -FeatureName IIS-CGI
```

O desde Panel de Control:
1. **Panel de Control** → **Programas** → **Activar o desactivar características de Windows**
2. Marcar: **Internet Information Services**
3. Expandir y marcar: **CGI** (bajo Características de desarrollo de aplicaciones)

### 2. Instalar Python

1. Descargar Python 3.11+ desde [python.org](https://www.python.org/downloads/)
2. **IMPORTANTE:** Durante instalación marcar "Add Python to PATH"
3. Instalar en: `C:\Python311\` (recomendado)

### 3. Crear Directorio del Sitio

```powershell
# Crear directorio
New-Item -ItemType Directory -Path "C:\inetpub\wwwroot\mejoramiso" -Force
New-Item -ItemType Directory -Path "C:\inetpub\wwwroot\mejoramiso\logs" -Force
New-Item -ItemType Directory -Path "C:\inetpub\wwwroot\mejoramiso\templates" -Force
```

### 4. Crear Entorno Virtual e Instalar Dependencias

```powershell
cd C:\inetpub\wwwroot\mejoramiso

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
.\venv\Scripts\Activate

# Actualizar pip
python -m pip install --upgrade pip

# Instalar dependencias
pip install Flask requests python-dotenv wfastcgi

# Habilitar wfastcgi
wfastcgi-enable
```

**Copiar la ruta que devuelve** `wfastcgi-enable`. Ejemplo:
```
C:\inetpub\wwwroot\mejoramiso\venv\Scripts\python.exe|C:\inetpub\wwwroot\mejoramiso\venv\Lib\site-packages\wfastcgi.py
```

### 5. Configurar Permisos

```powershell
# Dar permisos a IIS_IUSRS
$path = "C:\inetpub\wwwroot\mejoramiso"
$acl = Get-Acl $path
$permission = "IIS_IUSRS", "FullControl", "ContainerInherit,ObjectInherit", "None", "Allow"
$accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule $permission
$acl.SetAccessRule($accessRule)
Set-Acl $path $acl
```

### 6. Crear Application Pool en IIS

```powershell
Import-Module WebAdministration

# Crear Application Pool
New-WebAppPool -Name "Mejoramiso-AppPool"

# Configurar para .NET Core / No Managed Code
Set-ItemProperty "IIS:\AppPools\Mejoramiso-AppPool" -Name managedRuntimeVersion -Value ""
```

O desde IIS Manager:
1. Abrir **IIS Manager** (Win + R → `inetmgr`)
2. Click derecho en **Application Pools** → **Add Application Pool**
3. Nombre: `Mejoramiso-AppPool`
4. **.NET CLR version:** No Managed Code
5. Click **OK**

### 7. Crear Sitio Web

```powershell
# Crear sitio
New-WebSite -Name "Mejoramiso-Chatbot" `
            -Port 8080 `
            -PhysicalPath "C:\inetpub\wwwroot\mejoramiso" `
            -ApplicationPool "Mejoramiso-AppPool"
```

O desde IIS Manager:
1. Click derecho en **Sites** → **Add Website**
2. **Site name:** Mejoramiso-Chatbot
3. **Application pool:** Mejoramiso-AppPool
4. **Physical path:** C:\inetpub\wwwroot\mejoramiso
5. **Port:** 8080
6. Click **OK**

### 8. Configurar web.config

**Editar `C:\inetpub\wwwroot\mejoramiso\web.config`** y actualizar las rutas:

```xml
scriptProcessor="C:\inetpub\wwwroot\mejoramiso\venv\Scripts\python.exe|C:\inetpub\wwwroot\mejoramiso\venv\Lib\site-packages\wfastcgi.py"
```

Usa la ruta que obtuviste de `wfastcgi-enable`.

### 9. Copiar Archivos del Proyecto

```
C:\inetpub\wwwroot\mejoramiso\
├── app.py
├── web.config
├── .env
├── templates\
│   ├── index.html
│   └── dashboard.html
└── venv\
```

### 10. Reiniciar IIS

```powershell
iisreset
```

---

## 🔐 Configuración de Variables de Entorno

### Opción 1: Archivo .env (Recomendado para Desarrollo)

**Crear `C:\inetpub\wwwroot\mejoramiso\.env`:**
```env
GROQ_API_KEY=gsk_tu_clave_api_aqui
```

### Opción 2: Variables de Entorno de Windows (Recomendado para Producción)

**PowerShell:**
```powershell
# Variable de sistema
[System.Environment]::SetEnvironmentVariable('GROQ_API_KEY', 'gsk_tu_clave_api_aqui', 'Machine')

# Reiniciar IIS
iisreset
```

**O desde IIS Manager:**
1. Seleccionar tu sitio: **Mejoramiso-Chatbot**
2. Doble click en **Configuration Editor**
3. Sección: `system.webServer/fastCgi`
4. Agregar variable de entorno:
   - Name: `GROQ_API_KEY`
   - Value: `gsk_tu_clave_api_aqui`

---

## ✅ Pruebas y Verificación

### 1. Verificar que el Sitio está Activo

```powershell
# Ver sitios en IIS
Get-Website

# Ver estado del Application Pool
Get-WebAppPoolState -Name "Mejoramiso-AppPool"
```

### 2. Acceder a la Aplicación

**Chat de Usuario:**
- http://localhost:8080
- http://TU_IP_SERVIDOR:8080
- http://tu-dominio.com:8080

**Dashboard Administrativo:**
- http://localhost:8080/dashboard

### 3. Verificar Logs

**Logs de IIS:**
```
C:\inetpub\logs\LogFiles\
```

**Logs de FastCGI:**
```
C:\inetpub\wwwroot\mejoramiso\logs\wfastcgi.log
```

**Logs de aplicación:**
```powershell
# Ver eventos de Windows
Get-EventLog -LogName Application -Source "IIS*" -Newest 10
```

---

## 🔍 Solución de Problemas

### Error: "500 Internal Server Error"

**Solución 1: Habilitar errores detallados**

Editar `web.config`:
```xml
<httpErrors errorMode="Detailed" />
```

**Solución 2: Verificar permisos**
```powershell
icacls "C:\inetpub\wwwroot\mejoramiso" /grant "IIS_IUSRS:(OI)(CI)F" /T
```

**Solución 3: Verificar ruta de Python en web.config**

### Error: "FastCGI handler not found"

```powershell
# Re-habilitar FastCGI
cd C:\inetpub\wwwroot\mejoramiso
.\venv\Scripts\Activate
wfastcgi-enable

# Copiar la nueva ruta al web.config
```

### Error: "Module not found" (Flask, requests, etc.)

```powershell
# Reinstalar en el entorno virtual correcto
cd C:\inetpub\wwwroot\mejoramiso
.\venv\Scripts\Activate
pip install -r requirements.txt
```

### La base de datos no se crea

```powershell
# Verificar permisos de escritura
icacls "C:\inetpub\wwwroot\mejoramiso" /grant "IIS_IUSRS:(OI)(CI)F" /T

# Crear BD manualmente
cd C:\inetpub\wwwroot\mejoramiso
.\venv\Scripts\Activate
python
>>> from app import init_db
>>> init_db()
>>> exit()
```

### ChatBot no responde (IA no funciona)

**Verificar API Key:**
```powershell
# Ver variables de entorno
Get-ChildItem Env:GROQ_API_KEY
```

**Si no aparece:**
1. Verifica que `.env` existe en `C:\inetpub\wwwroot\mejoramiso\.env`
2. Verifica que contiene: `GROQ_API_KEY=gsk_...`
3. Reinicia IIS: `iisreset`

---

## 🔒 Producción y Seguridad

### 1. Configurar HTTPS (SSL/TLS)

**Obtener Certificado SSL:**
- Comprar certificado SSL
- Usar Let's Encrypt (gratis)
- Certificado autofirmado (solo para pruebas internas)

**Instalar certificado en IIS:**
1. IIS Manager → Seleccionar servidor
2. **Server Certificates** → **Import**
3. Seleccionar tu sitio → **Bindings**
4. Add: **Type: https, Port: 443, SSL Certificate: tu-certificado**

### 2. Configurar Firewall

```powershell
# Abrir puerto 80 (HTTP)
New-NetFirewallRule -DisplayName "HTTP Mejoramiso" -Direction Inbound -LocalPort 80 -Protocol TCP -Action Allow

# Abrir puerto 443 (HTTPS)
New-NetFirewallRule -DisplayName "HTTPS Mejoramiso" -Direction Inbound -LocalPort 443 -Protocol TCP -Action Allow
```

### 3. Configurar Dominio

**En tu proveedor de DNS:**
1. Crear registro A: `chatbot.mejoramiso.com` → `TU_IP_PUBLICA`
2. Esperar propagación DNS (puede tardar hasta 48h)

**En IIS:**
1. Seleccionar sitio → **Bindings**
2. Edit binding:
   - **Host name:** chatbot.mejoramiso.com
   - **Port:** 443
   - **SSL certificate:** tu-certificado

### 4. Seguridad Adicional

**Deshabilitar debug en producción:**

En `app.py`, asegurar:
```python
if __name__ == '__main__':
    # NO usar debug=True en producción
    app.run(debug=False, host='0.0.0.0', port=5000)
```

**Headers de seguridad (ya incluidos en web.config):**
- X-Content-Type-Options: nosniff
- X-Frame-Options: SAMEORIGIN
- X-XSS-Protection: 1; mode=block

**Rate Limiting (Opcional):**
Implementar en `app.py` usando Flask-Limiter:
```python
from flask_limiter import Limiter
limiter = Limiter(app, key_func=get_remote_address)

@app.route('/api/chat', methods=['POST'])
@limiter.limit("10 per minute")
def chat():
    # ...
```

### 5. Backup y Monitoreo

**Backup de Base de Datos:**
```powershell
# Script de backup diario
$fecha = Get-Date -Format "yyyyMMdd"
Copy-Item "C:\inetpub\wwwroot\mejoramiso\mejoramiso_db.db" `
          "C:\Backups\mejoramiso_db_$fecha.db"
```

**Monitoreo:**
- Habilitar logs de IIS
- Configurar alertas en Event Viewer
- Usar herramientas como New Relic, Datadog, etc.

---

## 📞 Soporte

**¿Problemas durante la instalación?**

1. Revisa la sección [Solución de Problemas](#solución-de-problemas)
2. Verifica los logs en `C:\inetpub\wwwroot\mejoramiso\logs\`
3. Contacta al equipo de Mejoramiso: +57 318 6072127

---

## 📝 Checklist Final

Antes de mostrar a tu jefe, verifica:

- [ ] IIS instalado y funcionando
- [ ] Python instalado y en PATH
- [ ] Sitio web creado en IIS
- [ ] Archivos copiados correctamente
- [ ] `GROQ_API_KEY` configurada
- [ ] Base de datos se crea automáticamente
- [ ] Acceso a http://localhost:8080 ✅
- [ ] Chat funciona y responde ✅
- [ ] Dashboard muestra estadísticas ✅
- [ ] Se pueden crear tickets ✅
- [ ] Se pueden agendar demos ✅

---

**¡Listo para mostrar a tu jefe! 🎉**