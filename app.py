"""
ASISTENTE VIRTUAL - MEJORAMISO (IMPROSOFT S.A.S)
Sistema de chatbot inteligente con IA para atencion al cliente 24/7
Plataforma de Sistemas de Gestion Empresarial basada en Mejoramiento Continuo
Desarrollado con Flask + Groq API (LLaMA 3.3)
"""

from flask import Flask, render_template, request, jsonify
from datetime import datetime
import sqlite3
import os
import requests
import json
from dotenv import load_dotenv

# Cargar variables de entorno (.env)
load_dotenv()

# Inicializar aplicacion Flask
app = Flask(__name__)

# =============================================================================
# CONFIGURACION UTF-8
# =============================================================================
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_MIMETYPE'] = 'application/json; charset=utf-8'

# =============================================================================
# CONFIGURACION DE IA (Groq API)
# =============================================================================
GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# =============================================================================
# BASE DE CONOCIMIENTO - MEJORAMISO
# =============================================================================

CONOCIMIENTO_MEJORAMISO = """
Eres un asistente virtual de Mejoramiso®, la plataforma de Sistemas de Gestión Empresarial 
desarrollada por IMPROSOFT S.A.S. Tu nombre es "Miso" 🤖

Web oficial: https://web.mejoramiso.com/
Desarrollador: IMPROSOFT S.A.S

=== INFORMACION CORPORATIVA ===
Mejoramiso® es una plataforma integral basada en Mejoramiento Continuo que permite 
gestionar eficientemente sistemas de calidad, ambiental, seguridad, riesgos y más.

ENFOQUE: Optimizar cada aspecto de las organizaciones mediante gestión de procesos 
eficiente y estructurada, aplicando técnicas de Mejoramiento Continuo.

VENTAJAS COMPETITIVAS:
- Metodología basada en Mejoramiento Continuo (Ciclo PHVA)
- Integración de múltiples sistemas de gestión en una sola plataforma
- Análisis gráfico de datos para toma de decisiones gerenciales
- Aplica a todos los niveles: estratégico, táctico y operativo
- Recursos multimedia: videos, tutoriales, capacitación

=== CONTACTO Y UBICACION ===

SEDE PRINCIPAL
Dirección: Carrera 43 A # 1 sur 31, Edificio BBVA, Medellín, Colombia
Teléfono: +57 318 6072127
WhatsApp: +57 318 6072127
Email: (usar formulario de contacto web)
Horario: Lunes a viernes 8:00 am a 5:00 pm

ACCESO CLIENTES
Portal de ingreso: https://mejoramiso.com/mejoramisosql/login.asp

=== MODULOS Y PRODUCTOS ===

MÓDULOS PRINCIPALES (19 módulos disponibles):

1. MAPA DE PROCESOS Y CONTROL DOCUMENTAL
   - Gestión de documentos (políticas, procedimientos, registros)
   - Mapeo de procesos organizacionales
   - Control de versiones y aprobaciones
   - Trazabilidad documental completa

2. MEJORAMIENTO
   - Acciones correctivas, preventivas y de mejora
   - Planes de mejoramiento
   - Seguimiento y cierre de hallazgos
   - Análisis de causas raíz (5 porqués, Ishikawa)

3. AUDITORIAS
   - Programación de auditorías internas
   - Listas de verificación personalizables
   - Generación de informes automáticos
   - Seguimiento de hallazgos

4. INDICADORES DE GESTION
   - KPIs y métricas de desempeño
   - Tableros de control (dashboards)
   - Semáforos y alertas automáticas
   - Gráficos y tendencias

5. PQRS (Peticiones, Quejas, Reclamos, Solicitudes)
   - Gestión de solicitudes de clientes
   - Tiempos de respuesta
   - Transformar PQRS en oportunidades de mejora
   - Trazabilidad completa

6. CONTEXTO ESTRATEGICO
   - Balanced Score Card (BSC)
   - Seguimiento del plan estratégico
   - Objetivos estratégicos
   - Cuadros de mando integral

7. EVALUACION DEL DESEMPEÑO / TH
   - Evaluación por competencias
   - Gestión de talento humano
   - Planes de desarrollo individual
   - Retroalimentación 360°

8. GESTION DE RIESGO
   - Identificación y valoración de riesgos
   - Matriz de riesgos según ISO 31000
   - Planes de tratamiento
   - Monitoreo y control

9. EVALUACION DE PROVEEDORES
   - Evaluación y calificación de proveedores
   - Criterios personalizables
   - Registro de proveedores aprobados
   - Reevaluación periódica

10. PROYECTOS Y PROGRAMAS
    - Gestión de proyectos
    - Cronogramas y hitos
    - Asignación de recursos
    - Seguimiento de avances

11. CONTROL DE EQUIPOS Y VEHICULOS
    - Inventario de equipos
    - Mantenimientos preventivos y correctivos
    - Calibraciones
    - Hojas de vida de equipos

12. ACTAS Y TAREAS
    - Registro de reuniones
    - Asignación de tareas
    - Seguimiento de compromisos
    - Recordatorios automáticos

13. REVISION POR LA DIRECCION
    - Datos de entrada para la revisión
    - Actas de revisión gerencial
    - Decisiones y recursos
    - Seguimiento de compromisos

14. GESTION DEL CONOCIMIENTO
    - Repositorio de conocimiento organizacional
    - Lecciones aprendidas
    - Buenas prácticas
    - Base de conocimiento

15. ENCUESTAS
    - Diseño de encuestas personalizadas
    - Clima laboral, satisfacción
    - Análisis estadístico
    - Reportes gráficos

16. ADMINISTRACION DEL RIESGO Y DISEÑO DE CONTROLES
    - Diseño de controles específicos
    - Análisis de riesgos operacionales
    - Controles preventivos y detectivos
    - Planes de contingencia

17. GESTION AMBIENTAL
    - Aspectos e impactos ambientales
    - Cumplimiento legal ambiental
    - Programas ambientales
    - ISO 14001

18. SG-SST (Sistema de Gestión de Seguridad y Salud en el Trabajo)
    - Cumplimiento normativo colombiano
    - Matriz de peligros y riesgos
    - Investigación de accidentes
    - Planes de emergencia
    - Normatividad vigente Decreto 1072

19. SEGURIDAD DE LA INFORMACION
    - Gestión de activos de información
    - Análisis de vulnerabilidades
    - ISO 27001
    - Controles de seguridad

=== SISTEMAS DE GESTION SOPORTADOS ===

✅ Sistema de Gestión de Calidad (ISO 9001)
✅ Seguridad y Salud en el Trabajo (SG-SST, Decreto 1072)
✅ MIPG - Modelo Integrado de Planeación y Gestión (Colombia)
✅ Medio Ambiente (ISO 14001)
✅ Gestión del Riesgo (ISO 31000)
✅ Seguridad de la Información (ISO 27001)

=== PLANES Y PRECIOS ===

PLAN EMPRENDEDOR
- Hasta 10 usuarios
- 8 GB de espacio en disco
- Módulos incluidos: Gestión Documental, Mejoramiento, Auditorías, 
  Indicadores de Gestión, PQRS
- Ideal para: Iniciar implementación de Sistema de Gestión con líderes de proceso
- Perfecto para: Startups, pequeñas empresas

PLAN ESTANDARPYME
- Hasta 30 usuarios
- 15 GB de espacio en disco
- Módulos incluidos: Los 5 del Emprendedor + Contexto Estratégico, 
  Evaluación del Desempeño, Gestión del Riesgo, Evaluación de Proveedores, Proyectos
- Ideal para: Empresas pequeñas o medianas
- Enfoque: Gestión integral con requisitos ISO 9001 y cultura de mejoramiento continuo

PLAN PROFESIONAL
- Usuarios ilimitados
- 50 GB de espacio en disco
- TODOS LOS 19 MÓDULOS incluidos
- Seguridad adicional: Log de transacciones, controles de autenticación
- Ideal para: Empresas medianas o grandes
- Enfoque: Implantar enfoque de procesos en toda la organización
- Máxima capacidad de Medir, Analizar y Mejorar (MAM)

COTIZACION PERSONALIZADA
- Disponible para necesidades específicas
- Configuración a medida
- Módulos personalizados
- Soporte dedicado

=== RECURSOS Y SOPORTE ===

DEMO INTERACTIVA
- Agenda una demo en: https://meetings.hubspot.com/s-acevedo
- Conoce la plataforma con expertos
- Personalización según tus necesidades

SOPORTE TECNICO
- Equipo disponible durante horario laboral
- Videos tutoriales
- Manuales de usuario
- Capacitación online

BLOG
- Artículos sobre mejoramiento continuo
- Casos de éxito
- Mejores prácticas
- Actualizaciones del sistema

=== BENEFICIOS CLAVE ===

✨ PRODUCTIVIDAD: Elimina costos de fallos y maximiza eficiencia
✨ CUMPLIMIENTO: Asegura cumplimiento normativo (ISO, decretos)
✨ MEJORA CONTINUA: Metodología sistemática y sostenible
✨ TOMA DE DECISIONES: Informes gráficos y análisis de datos en tiempo real
✨ INTEGRACION: Todos los sistemas en una sola plataforma
✨ ACCESIBILIDAD: Plataforma web, acceso desde cualquier lugar
✨ ESCALABILIDAD: Crece con tu organización

=== METODOLOGIA DE MEJORAMIENTO CONTINUO ===

Mejoramiso® implementa el ciclo PHVA (Planear, Hacer, Verificar, Actuar):
- PLANEAR: Identificación de oportunidades y planificación
- HACER: Implementación de planes y acciones
- VERIFICAR: Medición y seguimiento (indicadores, auditorías)
- ACTUAR: Mejoramiento basado en resultados

=== INDUSTRIAS Y SECTORES ===

Mejoramiso® aplica a múltiples sectores:
- Manufactura e industria
- Servicios de salud
- Educación
- Gobierno y sector público
- Servicios profesionales
- Construcción
- Logística y transporte
- Alimentos y bebidas
- Tecnología

=== INSTRUCCIONES DE RESPUESTA ===

Como "Miso" 🤖, tu asistente virtual:

1. SER PROFESIONAL PERO CERCANO
   - Usa un tono amigable y profesional
   - Puedes usar emojis ocasionalmente (no excesivo)
   - Sé empático con las necesidades del usuario

2. RESPUESTAS ESPECIFICAS
   - Si preguntan por módulos, explica beneficios concretos
   - Si preguntan por planes, compara opciones según su tamaño
   - Si preguntan por precios, orienta al formulario de cotización
   - Si preguntan técnicamente, da detalles de funcionalidades

3. GUIAR AL USUARIO
   - Sugiere el plan adecuado según su descripción
   - Recomienda agendar demo para ver la plataforma
   - Ofrece recursos adicionales (blog, tutoriales)
   - Para dudas complejas, sugiere contacto con equipo comercial

4. DATOS DE CONTACTO
   - Siempre incluye WhatsApp/teléfono cuando sea relevante
   - Menciona la opción de agendar demo
   - Proporciona enlaces web cuando aplique

5. CASOS DE USO
   - Si mencionan industria específica, personaliza respuesta
   - Si mencionan norma (ISO), enfoca en módulos relevantes
   - Si mencionan problema, sugiere módulo que lo resuelve

6. NO INVENTES
   - Si no sabes algo específico, sé honesto
   - Sugiere crear ticket o contactar al equipo
   - No des precios específicos (solo planes generales)

7. PROACTIVIDAD
   - Sugiere módulos complementarios relevantes
   - Menciona beneficios de integración
   - Destaca casos de éxito cuando aplique

8. PALABRAS CLAVE
   - Mejoramiento Continuo
   - Sistema de Gestión
   - ISO 9001, ISO 14001, ISO 31000, ISO 27001
   - SG-SST
   - Calidad
   - Eficiencia
   - Productividad
"""

# =============================================================================
# FUNCIONES DE BASE DE DATOS
# =============================================================================

def get_db():
    """Crea y retorna conexion a BD SQLite con UTF-8"""
    conn = sqlite3.connect('mejoramiso_db.db')
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA encoding = "UTF-8"')
    return conn


def init_db():
    """Inicializa la base de datos con tablas necesarias"""
    conn = get_db()
    
    # Tabla de conversaciones
    conn.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT NOT NULL,
            bot_response TEXT NOT NULL,
            intenciones TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla de solicitudes de demo
    conn.execute('''
        CREATE TABLE IF NOT EXISTS demo_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL,
            empresa TEXT,
            telefono TEXT,
            plan_interes TEXT,
            usuarios_estimados INTEGER,
            mensaje TEXT,
            estado TEXT DEFAULT 'pendiente',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla de tickets de soporte
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL,
            telefono TEXT,
            empresa TEXT,
            asunto TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            categoria TEXT DEFAULT 'consulta',
            prioridad TEXT DEFAULT 'normal',
            estado TEXT DEFAULT 'pendiente',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla de estadisticas
    conn.execute('''
        CREATE TABLE IF NOT EXISTS stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            valor TEXT NOT NULL,
            metadata TEXT,
            fecha DATE DEFAULT CURRENT_DATE
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Base de datos Mejoramiso inicializada correctamente")


# =============================================================================
# SISTEMA DE ANALISIS DE INTENCIONES
# =============================================================================

def analizar_intencion(mensaje):
    """Detecta intenciones del usuario en el mensaje"""
    mensaje_lower = mensaje.lower()
    
    intenciones_dict = {
        'info_modulos': ['modulo', 'módulo', 'funcionalidad', 'caracteristica', 'que hace', 'para que sirve'],
        'info_planes': ['plan', 'precio', 'costo', 'cuanto cuesta', 'cuanto vale', 'suscripcion'],
        'demo': ['demo', 'demostracion', 'probar', 'prueba', 'ver', 'mostrar'],
        'contacto': ['contacto', 'telefono', 'whatsapp', 'correo', 'email', 'hablar', 'comunicar'],
        'iso': ['iso', 'norma', 'certificacion', 'certificar', 'calidad'],
        'sgsst': ['sst', 'seguridad', 'salud', 'trabajo', 'decreto 1072'],
        'mejoramiento': ['mejora', 'mejorar', 'mejoramiento', 'optimizar', 'eficiencia'],
        'comparacion': ['diferencia', 'comparar', 'versus', 'vs', 'mejor que'],
        'industria': ['industria', 'sector', 'empresa', 'negocio', 'manufactura', 'salud', 'gobierno'],
        'implementacion': ['implementar', 'empezar', 'iniciar', 'comenzar', 'instalar'],
        'soporte': ['ayuda', 'soporte', 'problema', 'error', 'no funciona', 'capacitacion'],
        'login': ['login', 'ingresar', 'acceso', 'entrar', 'sesion', 'usuario']
    }
    
    detectadas = []
    for intencion, palabras_clave in intenciones_dict.items():
        if any(palabra in mensaje_lower for palabra in palabras_clave):
            detectadas.append(intencion)
    
    return detectadas


def generar_sugerencias(mensaje, intenciones):
    """Genera sugerencias proactivas contextuales"""
    sugerencias = []
    
    if 'info_modulos' in intenciones:
        sugerencias.append("Tenemos 19 módulos especializados. ¿Te gustaría ver una demo?")
    
    if 'info_planes' in intenciones:
        sugerencias.append("Ofrecemos 3 planes: Emprendedor, EstándarPyme y Profesional")
    
    if 'demo' in intenciones:
        sugerencias.append("Puedes agendar una demo personalizada en nuestro calendario")
    
    if 'iso' in intenciones:
        sugerencias.append("Mejoramiso cumple con ISO 9001, 14001, 31000 y 27001")
    
    if 'sgsst' in intenciones:
        sugerencias.append("Nuestro módulo SG-SST cumple Decreto 1072 de Colombia")
    
    if 'mejoramiento' in intenciones:
        sugerencias.append("Aplicamos el ciclo PHVA: Planear, Hacer, Verificar, Actuar")
    
    if 'implementacion' in intenciones:
        sugerencias.append("El plan Emprendedor es ideal para iniciar con 10 usuarios")
    
    if 'soporte' in intenciones:
        sugerencias.append("Ofrecemos videos tutoriales, manuales y soporte técnico")
    
    return sugerencias[:2]  # Máximo 2 sugerencias


# =============================================================================
# SISTEMA DE INTELIGENCIA ARTIFICIAL
# =============================================================================

def llamar_ia(mensaje_usuario, historial=[]):
    """
    Interactúa con Groq API para generar respuestas inteligentes
    """
    
    if not GROQ_API_KEY:
        return {
            'respuesta': "Lo siento, el servicio de IA no está configurado. ¿Te gustaría agendar una demo o crear un ticket de soporte?",
            'sugerencias': ["Agendar demo", "Crear ticket"],
            'intenciones': []
        }
    
    try:
        # Analizar intenciones
        intenciones = analizar_intencion(mensaje_usuario)
        
        # Construir prompt del sistema
        system_prompt = CONOCIMIENTO_MEJORAMISO
        if intenciones:
            system_prompt += f"\n\nINTENCIONES DETECTADAS: {', '.join(intenciones)}"
            system_prompt += "\nResponde específicamente a estas intenciones detectadas."
        
        # Preparar mensajes
        mensajes = [
            {"role": "system", "content": system_prompt}
        ]
        
        # Agregar historial (últimos 6 mensajes)
        for msg in historial[-6:]:
            mensajes.append(msg)
        
        # Agregar mensaje actual
        mensajes.append({"role": "user", "content": mensaje_usuario})
        
        # Llamar a Groq API
        response = requests.post(
            GROQ_API_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": mensajes,
                "temperature": 0.7,
                "max_tokens": 700
            },
            timeout=30
        )
        
        if response.status_code == 200:
            respuesta_texto = response.json()['choices'][0]['message']['content']
            sugerencias = generar_sugerencias(mensaje_usuario, intenciones)
            
            return {
                'respuesta': respuesta_texto,
                'sugerencias': sugerencias,
                'intenciones': intenciones
            }
        else:
            return {
                'respuesta': "Tuve un problema al procesar tu consulta. ¿Quieres que un asesor te contacte?",
                'sugerencias': ["Agendar demo", "Contactar asesor"],
                'intenciones': []
            }
            
    except Exception as e:
        print(f"❌ Error en llamada a IA: {str(e)}")
        return {
            'respuesta': "Ocurrió un error inesperado. Nuestro equipo está disponible en WhatsApp: +57 318 6072127",
            'sugerencias': [],
            'intenciones': []
        }


# =============================================================================
# CLASIFICADORES AUTOMATICOS
# =============================================================================

def clasificar_categoria_ticket(texto):
    """Clasifica automáticamente un ticket por categoría"""
    texto = texto.lower()
    
    if any(p in texto for p in ['precio', 'costo', 'plan', 'cotizacion']):
        return 'comercial'
    elif any(p in texto for p in ['modulo', 'funcionalidad', 'como usar']):
        return 'consulta_producto'
    elif any(p in texto for p in ['error', 'no funciona', 'problema', 'falla']):
        return 'soporte_tecnico'
    elif any(p in texto for p in ['demo', 'prueba', 'conocer']):
        return 'demo'
    elif any(p in texto for p in ['implementar', 'empezar', 'iniciar']):
        return 'implementacion'
    else:
        return 'consulta_general'


def clasificar_prioridad(texto):
    """Clasifica prioridad del ticket"""
    texto = texto.lower()
    
    if any(p in texto for p in ['urgente', 'critico', 'no funciona', 'error', 'bloqueado']):
        return 'urgente'
    elif any(p in texto for p in ['importante', 'pronto', 'necesito']):
        return 'alta'
    else:
        return 'normal'


def recomendar_plan(mensaje):
    """Recomienda el plan más adecuado según el contexto"""
    mensaje = mensaje.lower()
    
    if any(p in mensaje for p in ['grande', 'muchos usuarios', 'ilimitado', '50', '100']):
        return 'profesional'
    elif any(p in mensaje for p in ['mediana', 'pyme', '20', '30']):
        return 'estandarpyme'
    elif any(p in mensaje for p in ['pequeña', 'inicio', 'empezar', '10']):
        return 'emprendedor'
    else:
        return 'contactar_comercial'


# =============================================================================
# RUTAS WEB - PAGINAS
# =============================================================================

@app.route('/')
def index():
    """Página principal del chatbot"""
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    """Dashboard administrativo"""
    conn = get_db()
    
    # Métricas generales
    total_tickets = conn.execute('SELECT COUNT(*) as total FROM tickets').fetchone()['total']
    tickets_pendientes = conn.execute(
        "SELECT COUNT(*) as total FROM tickets WHERE estado = 'pendiente'"
    ).fetchone()['total']
    demos_pendientes = conn.execute(
        "SELECT COUNT(*) as total FROM demo_requests WHERE estado = 'pendiente'"
    ).fetchone()['total']
    conversaciones_hoy = conn.execute(
        'SELECT COUNT(*) as total FROM conversations WHERE DATE(created_at) = DATE("now")'
    ).fetchone()['total']
    
    # Últimos tickets
    tickets = conn.execute(
        'SELECT * FROM tickets ORDER BY created_at DESC LIMIT 10'
    ).fetchall()
    
    # Solicitudes de demo
    demos = conn.execute(
        'SELECT * FROM demo_requests ORDER BY created_at DESC LIMIT 10'
    ).fetchall()
    
    conn.close()
    
    return render_template('dashboard.html',
                         total_tickets=total_tickets,
                         tickets_pendientes=tickets_pendientes,
                         demos_pendientes=demos_pendientes,
                         conversaciones_hoy=conversaciones_hoy,
                         tickets=tickets,
                         demos=demos)


# =============================================================================
# API ENDPOINTS - CHATBOT
# =============================================================================

@app.route('/api/chat', methods=['POST'])
def chat():
    """Endpoint principal del chatbot"""
    try:
        data = request.get_json(force=True)
        mensaje_usuario = data.get('message', '').strip()
        historial = data.get('history', [])
        
        if not mensaje_usuario:
            return jsonify({'error': 'Mensaje vacío'}), 400
        
        # Obtener respuesta de IA
        resultado_ia = llamar_ia(mensaje_usuario, historial)
        
        respuesta_bot = resultado_ia['respuesta']
        sugerencias = resultado_ia['sugerencias']
        intenciones = resultado_ia['intenciones']
        
        # Guardar conversación
        conn = get_db()
        conn.execute(
            'INSERT INTO conversations (user_message, bot_response, intenciones) VALUES (?, ?, ?)',
            (mensaje_usuario, respuesta_bot, ','.join(intenciones))
        )
        conn.commit()
        conn.close()
        
        # Detectar necesidades especiales
        necesita_demo = 'demo' in intenciones or any(p in respuesta_bot.lower() 
                                                      for p in ['agendar demo', 'solicitar demo'])
        necesita_ticket = any(p in respuesta_bot.lower() 
                             for p in ['ticket', 'contactar', 'asesor'])
        
        return jsonify({
            'response': respuesta_bot,
            'needs_demo': necesita_demo,
            'needs_ticket': necesita_ticket,
            'sugerencias': sugerencias,
            'intenciones': intenciones,
            'plan_recomendado': recomendar_plan(mensaje_usuario)
        }), 200, {'Content-Type': 'application/json; charset=utf-8'}
        
    except Exception as e:
        print(f"❌ Error en /api/chat: {str(e)}")
        return jsonify({'error': 'Error al procesar mensaje'}), 500


# =============================================================================
# API ENDPOINTS - SOLICITUDES DE DEMO
# =============================================================================

@app.route('/api/demo', methods=['POST'])
def solicitar_demo():
    """Crea solicitud de demostración"""
    try:
        data = request.get_json(force=True)
        
        nombre = data.get('nombre', '').strip()
        email = data.get('email', '').strip()
        empresa = data.get('empresa', '').strip()
        telefono = data.get('telefono', '').strip()
        plan_interes = data.get('plan_interes', 'no_especificado')
        usuarios_estimados = data.get('usuarios_estimados', 0)
        mensaje = data.get('mensaje', '').strip()
        
        if not all([nombre, email]):
            return jsonify({'error': 'Nombre y email son obligatorios'}), 400
        
        conn = get_db()
        cursor = conn.execute(
            '''INSERT INTO demo_requests 
               (nombre, email, empresa, telefono, plan_interes, usuarios_estimados, mensaje) 
               VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (nombre, email, empresa, telefono, plan_interes, usuarios_estimados, mensaje)
        )
        demo_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'demo_id': demo_id,
            'message': f'¡Solicitud #{demo_id} registrada! Te contactaremos pronto para agendar tu demo personalizada 🎯'
        }), 200
        
    except Exception as e:
        print(f"❌ Error en /api/demo: {str(e)}")
        return jsonify({'error': 'Error al crear solicitud de demo'}), 500


@app.route('/api/demo', methods=['GET'])
def listar_demos():
    """Lista solicitudes de demo"""
    conn = get_db()
    demos = conn.execute(
        'SELECT * FROM demo_requests ORDER BY created_at DESC'
    ).fetchall()
    conn.close()
    
    return jsonify([dict(demo) for demo in demos])


# =============================================================================
# API ENDPOINTS - TICKETS DE SOPORTE
# =============================================================================

@app.route('/api/tickets', methods=['POST'])
def crear_ticket():
    """Crea ticket de soporte"""
    try:
        data = request.get_json(force=True)
        
        nombre = data.get('nombre', '').strip()
        email = data.get('email', '').strip()
        telefono = data.get('telefono', '').strip()
        empresa = data.get('empresa', '').strip()
        asunto = data.get('asunto', '').strip()
        descripcion = data.get('descripcion', '').strip()
        
        if not all([nombre, email, asunto, descripcion]):
            return jsonify({'error': 'Faltan campos obligatorios'}), 400
        
        categoria = clasificar_categoria_ticket(asunto + ' ' + descripcion)
        prioridad = clasificar_prioridad(asunto + ' ' + descripcion)
        
        conn = get_db()
        cursor = conn.execute(
            '''INSERT INTO tickets 
               (nombre, email, telefono, empresa, asunto, descripcion, categoria, prioridad) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            (nombre, email, telefono, empresa, asunto, descripcion, categoria, prioridad)
        )
        ticket_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'ticket_id': ticket_id,
            'categoria': categoria,
            'prioridad': prioridad,
            'message': f'Ticket #{ticket_id} creado exitosamente. Nuestro equipo te contactará pronto.'
        }), 200
        
    except Exception as e:
        print(f"❌ Error en /api/tickets POST: {str(e)}")
        return jsonify({'error': 'Error al crear ticket'}), 500


@app.route('/api/tickets', methods=['GET'])
def listar_tickets():
    """Lista todos los tickets"""
    conn = get_db()
    tickets = conn.execute(
        'SELECT * FROM tickets ORDER BY created_at DESC'
    ).fetchall()
    conn.close()
    
    return jsonify([dict(ticket) for ticket in tickets])


@app.route('/api/tickets/<int:ticket_id>', methods=['PUT'])
def actualizar_ticket(ticket_id):
    """Actualiza estado de ticket"""
    data = request.get_json()
    estado = data.get('estado', 'pendiente')
    
    conn = get_db()
    conn.execute(
        'UPDATE tickets SET estado = ? WHERE id = ?',
        (estado, ticket_id)
    )
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Ticket actualizado'})


# =============================================================================
# API ENDPOINTS - ESTADISTICAS
# =============================================================================

@app.route('/api/stats', methods=['GET'])
def obtener_estadisticas():
    """Obtiene estadísticas del sistema"""
    conn = get_db()
    
    # Tickets por categoría
    por_categoria = conn.execute('''
        SELECT categoria, COUNT(*) as total 
        FROM tickets 
        GROUP BY categoria
    ''').fetchall()
    
    # Tickets por prioridad
    por_prioridad = conn.execute('''
        SELECT prioridad, COUNT(*) as total 
        FROM tickets 
        GROUP BY prioridad
    ''').fetchall()
    
    # Intenciones más comunes
    intenciones_comunes = conn.execute('''
        SELECT intenciones, COUNT(*) as total
        FROM conversations
        WHERE intenciones IS NOT NULL AND intenciones != ''
        GROUP BY intenciones
        ORDER BY total DESC
        LIMIT 10
    ''').fetchall()
    
    # Conversaciones por día (últimos 7 días)
    conversaciones_diarias = conn.execute('''
        SELECT DATE(created_at) as fecha, COUNT(*) as total
        FROM conversations
        WHERE created_at >= DATE('now', '-7 days')
        GROUP BY DATE(created_at)
    ''').fetchall()
    
    conn.close()
    
    return jsonify({
        'por_categoria': [dict(row) for row in por_categoria],
        'por_prioridad': [dict(row) for row in por_prioridad],
        'intenciones_comunes': [dict(row) for row in intenciones_comunes],
        'conversaciones_diarias': [dict(row) for row in conversaciones_diarias]
    })


@app.route('/api/health', methods=['GET'])
def health():
    """Endpoint de salud del servicio"""
    return jsonify({
        'status': 'ok',
        'servicio': 'Mejoramiso Chatbot',
        'timestamp': datetime.now().isoformat(),
        'ia_configurada': bool(GROQ_API_KEY)
    })


# =============================================================================
# MANEJO DE ERRORES
# =============================================================================

@app.errorhandler(500)
def error_interno(e):
    return jsonify({'error': 'Error interno del servidor'}), 500


@app.errorhandler(404)
def no_encontrado(e):
    return jsonify({'error': 'Recurso no encontrado'}), 404


# =============================================================================
# INICIALIZACION Y EJECUCION
# =============================================================================

# =============================================================================
# MODIFICACIONES PARA PRODUCCIÓN EN IIS
# Agrega esto al FINAL de tu app.py (reemplaza el if __name__ == '__main__')
# =============================================================================

if __name__ == '__main__':
    # Inicializar base de datos
    init_db()
    
    # Mensajes informativos
    print("\n" + "="*70)
    print("🤖 ASISTENTE VIRTUAL MISO - MEJORAMISO® (IMPROSOFT S.A.S)")
    print("="*70)
    
    # Detectar si estamos en IIS (producción) o desarrollo
    import os
    if os.environ.get('WEBSITE_SITE_NAME'):
        # Estamos en IIS/Azure
        print("🌐 Modo: PRODUCCIÓN (IIS)")
        print(f"📊 Base de datos: {os.path.abspath('mejoramiso_db.db')}")
        print(f"🤖 Estado IA: {'✅ Configurada' if GROQ_API_KEY else '❌ NO CONFIGURADA'}")
        
        if not GROQ_API_KEY:
            print("\n⚠️  ADVERTENCIA: GROQ_API_KEY no configurada")
            print("   Configura la variable de entorno en IIS")
        
        print("="*70 + "\n")
        
        # En producción, Flask se ejecuta vía FastCGI/WSGI
        # No usar app.run()
    else:
        # Modo desarrollo local
        print(f"🌐 Servidor iniciando en: http://localhost:5000")
        print(f"📊 Dashboard disponible en: http://localhost:5000/dashboard")
        print(f"🤖 Estado IA: {'✅ Configurada' if GROQ_API_KEY else '❌ NO CONFIGURADA'}")
        print(f"📧 Contacto: WhatsApp +57 318 6072127")
        print(f"🏢 Sede: Medellín, Colombia")
        
        if not GROQ_API_KEY:
            print("\n⚠️  ADVERTENCIA: Variable GROQ_API_KEY no encontrada en .env")
            print("   El chatbot funcionará en modo limitado sin IA")
        
        print("="*70 + "\n")
        
        # Iniciar servidor Flask en desarrollo
        app.run(debug=True, host='0.0.0.0', port=5000)

# Para IIS, el objeto 'app' debe estar disponible globalmente
# IIS buscará automáticamente el objeto 'app' en este archivo
    # Inicializar BD
    init_db()
    
    # Mensajes informativos
    print("\n" + "="*70)
    print("🤖 ASISTENTE VIRTUAL MISO - MEJORAMISO® (IMPROSOFT S.A.S)")
    print("="*70)
    print(f"🌐 Servidor iniciando en: http://localhost:5000")
    print(f"📊 Dashboard disponible en: http://localhost:5000/dashboard")
    print(f"🤖 Estado IA: {'✅ Configurada' if GROQ_API_KEY else '❌ NO CONFIGURADA'}")
    print(f"📧 Contacto: WhatsApp +57 318 6072127")
    print(f"🏢 Sede: Medellín, Colombia")
    
    if not GROQ_API_KEY:
        print("\n⚠️  ADVERTENCIA: Variable GROQ_API_KEY no encontrada en .env")
        print("   El chatbot funcionará en modo limitado sin IA")
    
    print("="*70 + "\n")
    
    # Iniciar servidor
    app.run(debug=True, host='0.0.0.0', port=5000)