# Emma - Interfaz de Chat para Ollama

## Descripción
Emma es una interfaz de chat en Python diseñada para interactuar con Ollama, específicamente optimizada para el modelo gemma3:1b. Esta interfaz proporciona una manera eficiente de administrar:

- Interacciones con Ollama
- Contextos de conversación
- Memoria de chat
- Configuraciones personalizadas
- Personalidades para el asistente
- Historial de conversaciones

## Características

### Interfaz de Chat
- Interfaz de línea de comandos intuitiva y amigable
- Personalización del nombre de usuario (por defecto: "Oz")
- Opción para mostrar las respuestas con o sin recuadro
- Comandos integrados para gestionar la sesión

### Modelos y Configuración
- Soporte para diferentes modelos de Ollama (optimizado para gemma3:1b)
- Configuración flexible de parámetros del modelo (temperatura, tokens, etc.)
- Gestión de contexto y memoria para conversaciones más coherentes

### Personalidades
- Múltiples personalidades predefinidas:
  - **Default**: Asistente amigable y versátil
  - **Técnica**: Especializada en programación y tecnología
  - **Creativa**: Enfocada en ideas innovadoras y pensamiento creativo
  - **Concisa**: Para respuestas breves y directas
  - **Educativa**: Para explicar conceptos con claridad y ejemplos
  - **Sexy**: Para conversaciones de temática adulta/sensual
- Capacidad para crear y gestionar nuevas personalidades

### Sistema de Memoria
- Almacenamiento de información relevante entre sesiones
- Búsqueda contextual en el historial para mejorar respuestas
- Gestión de memoria a largo plazo

### Gestión de Conversaciones
- Guardado automático de conversaciones
- Carga de conversaciones anteriores
- Exportación e importación de conversaciones

## Requisitos
- Python 3.8+
- Ollama instalado y configurado con gemma3:1b
- Dependencias especificadas en `requirements.txt`

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tuusuario/Emma.git
cd Emma

# Crear un entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

## Uso Básico

```bash
# Iniciar chat con configuración por defecto
python emma.py chat

# Iniciar chat con una personalidad específica
python emma.py chat --personality técnica

# Activar modo de depuración
python emma.py chat --debug

# Ver todas las personalidades disponibles
python emma.py personalities --list
```

## Comandos Disponibles en el Chat
- `exit`, `quit`, `salir` - Salir de Emma
- `clear`, `limpiar` - Limpiar la pantalla
- `help`, `ayuda` - Mostrar menú de ayuda

### Comandos Especiales
- `/system` - Mostrar información del sistema
- `/personality list` - Listar personalidades disponibles
- `/personality set <nombre>` - Cambiar personalidad
- `/personality info <nombre>` - Ver detalles de una personalidad
- `/memory add <clave> <valor>` - Añadir elemento a la memoria
- `/memory get <clave>` - Obtener elemento de la memoria
- `/memory search <consulta>` - Buscar en la memoria
- `/memory clear` - Limpiar la memoria
- `/conversations` - Listar conversaciones guardadas

## Configuración
El archivo `config.yaml` permite personalizar varios aspectos de la interfaz:

```yaml
# Ejemplo de configuración
model: "gemma3:1b"          # Modelo de Ollama a utilizar
temperature: 0.7            # Temperatura para la generación
max_tokens: 800             # Tokens máximos por respuesta
user_name: "Oz"             # Nombre personalizado del usuario
use_panels: false           # Mostrar mensajes sin recuadros
```

## Personalización
Para añadir nuevas personalidades mediante línea de comandos:

```bash
python emma.py personalities --add
```

O directamente en el archivo `config.yaml`:

```yaml
personalities:
  miPersonalidad: "Eres Emma, una asistente que... [descripción]"
```

## Licencia
[MIT](LICENSE) 