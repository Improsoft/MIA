# AsistenteCC - Chatbot Inteligente para Cámara de Comercio de Pereira

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![IA](https://img.shields.io/badge/IA-Groq%20LLaMA%203.3-orange.svg)](https://groq.com/)

---

## 📋 Índice

- [Descripción](#descripción)
- [Problema y Solución](#problema-y-solución)
- [Características](#características)
- [Arquitectura](#arquitectura)
- [Tecnologías](#tecnologías)
- [Instalación](#instalación)
- [Uso](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [API Endpoints](#api-endpoints)
- [Docker](#docker)
- [Capturas de Pantalla](#capturas-de-pantalla)
- [Roadmap](#roadmap)
- [Autor](#autor)

---

## Descripción

**AsistenteCC** es un chatbot inteligente con IA conversacional desarrollado específicamente para la **Cámara de Comercio de Pereira por Risaralda**. El sistema automatiza la atención al cliente 24/7, respondiendo consultas sobre trámites, servicios, ubicaciones y horarios, reduciendo la carga operativa en aproximadamente un 60%.

### Problema que Resuelve

La Cámara de Comercio recibe cientos de consultas diarias sobre:
- Renovación de matrículas mercantiles
- Ubicación y horarios de sedes
- Registro de nuevas empresas
- Solicitud de certificados
- Información general sobre trámites

### Solución Propuesta

Un chatbot con IA conversacional que:
- ✅ Entiende lenguaje natural (incluso con errores ortográficos)
- ✅ Responde consultas 24/7 de forma inmediata
- ✅ Proporciona información detallada de 8 sedes
- ✅ Genera sugerencias proactivas
- ✅ Crea tickets automáticos cuando requiere intervención humana
- ✅ Clasifica consultas por categoría y prioridad
- ✅ Dashboard administrativo con métricas en tiempo real

---

## Características

### Para Usuarios
- **Chat Conversacional Natural**: Entiende preguntas en lenguaje cotidiano
- **Respuestas Formateadas**: Listas, negritas, links clickeables para mejor legibilidad
- **Información Completa**: 8 sedes con direcciones, teléfonos, WhatsApp y horarios
- **Sugerencias Inteligentes**: Proactivas según el contexto de la conversación
- **Acciones Rápidas**: Botones predefinidos para consultas comunes
- **Tickets de Soporte**: Formulario para casos que requieren atención personalizada
- **Disponibilidad 24/7**: Sin limitación de horarios

### Para Administradores
- **Dashboard Administrativo**: Métricas en tiempo real
- **Sistema de Tickets**: Gestión completa con estados y prioridades
- **Clasificación Automática**: Por categoría (renovación, registro, certificados, etc.)
- **Priorización Inteligente**: Urgente, alta, normal según palabras clave
- **Historial de Conversaciones**: Registro completo para análisis
- **Estadísticas**: Tickets por día, categoría y prioridad
- **Auto-refresh**: Dashboard se actualiza automáticamente cada 30 segundos

### Capacidades de IA
- **Análisis de Intenciones**: Detecta qué busca el usuario
- **Comprensión Contextual**: Mantiene el hilo de la conversación
- **Respuestas Personalizadas**: Adaptadas al contexto específico
- **Manejo de Errores**: Comprende mensajes con errores ortográficos
- **Base de Conocimiento**: 1,200+ líneas de información institucional

---

## Arquitectura

```
┌─────────────────────────────────────────────────────┐
│         Frontend (HTML/CSS/JavaScript)              │
│  - Interfaz de Chat con renderizado Markdown       │
│  - Dashboard Administrativo                         │
│  - Diseño Responsive                                │
└────────────────────┬────────────────────────────────┘
                     │ HTTP/REST
┌────────────────────┴────────────────────────────────┐
│           Backend API (Flask/Python)                │
│  - Endpoint /api/chat (chatbot principal)          │
│  - Endpoint /api/tickets (gestión de tickets)      │
│  - Sistema de análisis de intenciones              │
│  - Clasificación automática                         │
└────┬──────────────────────┬─────────────────────────┘
     │                      │
┌────┴──────────┐   ┌───────┴──────────────────────┐
│   SQLite      │   │   Groq API (LLaMA 3.3)       │
│   Database    │   │   - Modelo: 70B parámetros   │
│   - Tickets   │   │   - Gratuito                 │
│   - Chats     │   │   - Ultra rápido (~10x GPT)  │
│   - Stats     │   └──────────────────────────────┘
└───────────────┘
```

### Flujo de una Consulta

```
Usuario escribe mensaje
         ↓
Frontend captura y envía a /api/chat
         ↓
Backend analiza intenciones (ubicación, horario, etc.)
         ↓
Construye prompt con base de conocimiento
         ↓
Llama a Groq API (LLaMA 3.3)
         ↓
IA genera respuesta personalizada
         ↓
Backend genera sugerencias proactivas
         ↓
Guarda conversación en SQLite
         ↓
Frontend renderiza respuesta con formato Markdown
         ↓
Usuario recibe respuesta estructurada y clara
```

---

## Tecnologías

### Backend
- **Python 3.11+** - Lenguaje principal
- **Flask 3.0** - Framework web minimalista y potente
- **SQLite 3** - Base de datos sin servidor (ideal para desarrollo)
- **Groq API** - IA conversacional (LLaMA 3.3 - 70B parámetros)
- **python-dotenv** - Gestión de variables de entorno
- **requests** - Cliente HTTP para APIs

### Frontend
- **HTML5** - Estructura semántica
- **CSS3** - Estilos modernos con gradientes y animaciones
- **JavaScript ES6+** - Interactividad y lógica del cliente
- **Renderizado Markdown** - Conversión de texto plano a HTML formateado

### DevOps
- **Docker** - Contenedorización
- **Docker Compose** - Orquestación (preparado para N8N)
- **Git** - Control de versiones

### IA y NLP
- **Groq LLaMA 3.3 (70B)** - Modelo de lenguaje
- **Análisis de Intenciones** - Sistema custom con palabras clave
- **Clasificación Automática** - Machine learning básico

---

## Instalación

### Opción 1: Instalación Local (Desarrollo)

#### Requisitos Previos
- Python 3.11 o superior
- pip (gestor de paquetes de Python)
- Cuenta gratuita en [Groq](https://console.groq.com)

#### Pasos

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/asistente-cc.git
cd asistente-cc
```

2. **Crear entorno virtual**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
# Windows
copy .env.example .env

# Mac/Linux
cp .env.example .env
```

Editar `.env` y agregar tu API key de Groq:
```env
GROQ_API_KEY=gsk_tu_clave_aqui
```

5. **Ejecutar la aplicación**
```bash
python app.py
```

6. **Acceder a la aplicación**
- Chatbot: http://localhost:5000
- Dashboard: http://localhost:5000/dashboard

---

### Opción 2: Docker (Recomendado para Producción)

#### Requisitos Previos
- Docker instalado
- Docker Compose (opcional)

#### Construcción de la Imagen

```bash
# Construir imagen
docker build -t assistant-cc .

# Ver imagen creada
docker images
```

#### Ejecución del Contenedor

```bash
# Ejecutar con .env
docker run -d -p 5000:5000 --name my-assistant --env-file .env assistant-cc

# Ver logs
docker logs -f my-assistant

# Detener
docker stop my-assistant

# Eliminar
docker rm my-assistant
```

#### Comandos Útiles

```bash
# Reconstruir sin caché (después de cambios)
docker build --no-cache -t assistant-cc .

# Entrar al contenedor
docker exec -it my-assistant /bin/bash

# Ver estado
docker ps

# Limpiar todo
docker stop my-assistant
docker rm my-assistant
docker rmi assistant-cc
```

---

## Uso

### Para Usuarios Finales

1. Accede a http://localhost:5000
2. Escribe tu consulta en lenguaje natural
3. Ejemplos de preguntas:
   - "¿Dónde están ubicados?"
   - "¿Cuál es el horario de atención?"
   - "¿Cómo renuevo mi matrícula mercantil?"
   - "¿Cuánto cuesta un certificado?"
   - "¿Tienen sede en La Virginia?"

### Botones de Acción Rápida

- **Renovar Matrícula**: Info sobre renovación
- **Certificados**: Costos y procedimiento
- **Ubicación**: Sedes y direcciones
- **Horarios**: Horarios de atención

### Crear un Ticket

Si el chatbot no puede resolver tu consulta:
1. El bot te ofrecerá crear un ticket
2. Completa el formulario (nombre, email, descripción)
3. El sistema clasifica automáticamente tu solicitud
4. Un funcionario te contactará pronto

---

### Para Administradores

1. Accede a http://localhost:5000/dashboard
2. Visualiza:
   - Total de tickets
   - Tickets pendientes
   - Tickets del día
   - Conversaciones del día
3. Gestiona tickets:
   - Ver detalles
   - Cambiar estado
   - Marcar como resuelto

---

## 📁 Estructura del Proyecto

```
asistente-cc/
│
├── app.py                      # Backend Flask (API + lógica)
├── database.db                 # SQLite (generado automáticamente)
├── requirements.txt            # Dependencias Python
├── Dockerfile                  # Instrucciones Docker
├── .env                        # Variables de entorno (NO subir a Git)
├── .env.example                # Plantilla de .env
├── .gitignore                  # Archivos a ignorar en Git
├── .dockerignore               # Archivos a ignorar en Docker
├── README.md                   # Documentación (este archivo)
│
├── templates/                  # HTML Templates (Jinja2)
│   ├── index.html             # Página principal (chatbot)
│   └── dashboard.html         # Dashboard administrativo
│
├── static/                     # Archivos estáticos (opcional)
│   ├── chat.js                # JavaScript del chat (si se separa)
│   ├── dashboard.css          # CSS del dashboard (si se separa)
│   └── style.css              # CSS global (si se separa)
│
└── venv/                       # Entorno virtual (NO subir a Git)
```

### Archivos Clave

| Archivo | Descripción |
|---------|-------------|
| `app.py` | Backend completo: rutas, IA, base de datos |
| `templates/index.html` | Interfaz del chatbot con JS integrado |
| `templates/dashboard.html` | Panel administrativo |
| `requirements.txt` | Dependencias: Flask, requests, python-dotenv |
| `Dockerfile` | Configuración para crear imagen Docker |
| `.env` | API keys y configuración (privado) |
| `database.db` | Base de datos SQLite (autogenerado) |

---

## 🔌 API Endpoints

### Chatbot

#### `POST /api/chat`
Procesa un mensaje del usuario y retorna respuesta del bot.

**Request:**
```json
{
  "message": "¿Dónde están ubicados?",
  "history": [
    {"role": "user", "content": "Hola"},
    {"role": "assistant", "content": "¡Hola! ¿En qué puedo ayudarte?"}
  ]
}
```

**Response:**
```json
{
  "response": "¡Con gusto! Tenemos 8 sedes en Risaralda...",
  "needs_ticket": false,
  "sugerencias": ["Pereira: 8am-4pm continuo", "Tenemos WhatsApp en todas las sedes"],
  "intenciones": ["ubicacion"]
}
```

---

### Tickets

#### `POST /api/tickets`
Crea un nuevo ticket de soporte.

**Request:**
```json
{
  "nombre": "Juan Pérez",
  "email": "juan@empresa.com",
  "telefono": "3001234567",
  "asunto": "Consulta sobre renovación",
  "descripcion": "Necesito saber si mi matrícula venció"
}
```

**Response:**
```json
{
  "success": true,
  "ticket_id": 42,
  "categoria": "renovacion",
  "prioridad": "normal",
  "message": "Ticket #42 creado exitosamente. Te contactaremos pronto."
}
```

#### `GET /api/tickets`
Lista todos los tickets.

#### `PUT /api/tickets/<id>`
Actualiza el estado de un ticket.

**Request:**
```json
{
  "estado": "resuelto"
}
```

---

### Otros

#### `GET /api/stats`
Obtiene estadísticas del sistema.

#### `GET /api/health`
Verifica que el servicio esté funcionando.

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2024-12-29T15:30:00",
  "ia_configurada": true
}
```

---

## 🐳 Docker

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Exponer puerto
EXPOSE 5000

# Comando de inicio
CMD ["python", "app.py"]
```

### Variables de Entorno Requeridas

```env
GROQ_API_KEY=gsk_...        # Obligatorio
FLASK_ENV=production        # Opcional
```

### Docker Compose (Preparado para N8N)

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
    volumes:
      - ./database.db:/app/database.db

  # N8N (Comentado - listo para activar)
  # n8n:
  #   image: n8nio/n8n
  #   ports:
  #     - "5678:5678"
  #   environment:
  #     - N8N_BASIC_AUTH_ACTIVE=true
  #     - N8N_BASIC_AUTH_USER=admin
  #     - N8N_BASIC_AUTH_PASSWORD=admin123
```

---

## 📸 Capturas de Pantalla

### Chatbot Principal
Chatbot
- Interfaz limpia y moderna
- Respuestas formateadas con Markdown
- Botones de acción rápida
- Sugerencias proactivas

### Dashboard Administrativo
Dashboard
- Métricas en tiempo real
- Gestión de tickets
- Tabla con últimos tickets
- Auto-refresh cada 30 segundos

### Respuestas Formateadas
Formato
- Listas con bullets
- Negritas en títulos
- Links clickeables
- Separación visual clara

---

## Roadmap

### Fase 1 - MVP (Completado)
- [x] Chatbot con IA conversacional
- [x] Sistema de tickets
- [x] Dashboard administrativo
- [x] Análisis de intenciones
- [x] Sugerencias proactivas
- [x] Renderizado Markdown
- [x] Dockerización
- [x] Base de conocimiento completa (8 sedes)

### Fase 2 - Mejoras (Próximas)
- [ ] Integración con N8N para automatizaciones
- [ ] Notificaciones por email cuando se crea ticket
- [ ] Exportar tickets a Excel/PDF
- [ ] Sistema de autenticación para dashboard
- [ ] Tests unitarios y de integración
- [ ] Métricas avanzadas con gráficos
- [ ] Feedback del usuario (rating de respuestas)

### Fase 3 - Escalamiento (Futuro)
- [ ] Integración con WhatsApp Business API
- [ ] Integración con sistema interno de la CCP
- [ ] Multi-idioma (inglés, portugués)
- [ ] Análisis de sentimientos
- [ ] Chatbot por voz
- [ ] App móvil nativa
- [ ] Base de datos PostgreSQL
- [ ] Redis para caché
- [ ] Despliegue en la nube (AWS/Azure)

---

## 🧪 Testing

### Pruebas Manuales

```bash
# Test básico de la API
curl http://localhost:5000/api/health

# Test del chatbot
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"¿Dónde están ubicados?"}'

# Test crear ticket
curl -X POST http://localhost:5000/api/tickets \
  -H "Content-Type: application/json" \
  -d '{
    "nombre":"Test",
    "email":"test@test.com",
    "asunto":"Prueba",
    "descripcion":"Ticket de prueba"
  }'
```

---

## Troubleshooting

### Problema: "GROQ_API_KEY no configurada"
**Solución:**
1. Verifica que existe `.env`
2. Verifica que la clave está sin comillas
3. Reinicia el servidor

### Problema: "Port 5000 already in use"
**Solución:**
```bash
# Mac/Linux
lsof -ti:5000 | xargs kill -9

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Problema: El bot no responde o es muy lento
**Causas posibles:**
- Sin internet
- API key inválida
- Límite de Groq alcanzado (esperar 1 minuto)

---


## 👨‍💻 Autor

**Felipe Mogollón**

Proyecto desarrollado como demostración técnica para la posición de **Desarrollador Profesional de Sistemas** en la **Cámara de Comercio de Pereira por Risaralda**.

### Contacto
- 📧 Email: afme-95@hotmail.com
- 💼 LinkedIn: www.linkedin.com/in/felipe-mogollon
- 🐙 GitHub: https://github.com/FelipeMogollon1


## Licencia

Este proyecto fue desarrollado con fines educativos y de demostración.

---
**¡Gracias por revisar este proyecto! 🚀**

Si tienes preguntas o sugerencias, no dudes en contactarme.