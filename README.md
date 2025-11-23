# Emma - Interfaz de Chat Inteligente para Ollama

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-rev_250718-green.svg)](https://github.com/ozkar-co/Emma)

Emma es una interfaz de chat inteligente en Python diseñada para interactuar con modelos de Ollama. Proporciona una experiencia de conversación natural con capacidades avanzadas de análisis de prompts, búsqueda inteligente y gestión de personalidades.

## 🚀 Características Principales

### ✅ **Implementado y Funcional**
- **Chat Interactivo**: Interfaz de línea de comandos intuitiva
- **Arquitectura Modular**: Core refactorizado con adaptadores LLM y sistema de personalidades separado
- **Adapter Ollama**: Integración completa con la API de Ollama
- **Análisis de Prompts**: Sistema inteligente que determina si una pregunta requiere búsqueda externa
- **Comandos de Búsqueda**: Generación automática de comandos `<search>`, `<memory>`, `<query>`
- **Sistema de Personalidades**: Archivos YAML separados para cada personalidad
- **Configuración Flexible**: Archivo YAML para personalización completa
- **Gestión de Conversaciones**: Guardado automático de conversaciones

## 📋 Tabla de Contenidos

- [Instalación](#instalación)
- [Uso Rápido](#uso-rápido)
- [Configuración](#configuración)
- [Comandos Disponibles](#comandos-disponibles)
- [Personalidades](#personalidades)
- [Sistema de Búsqueda](#sistema-de-búsqueda)
- [Contribución](#contribución)
- [Roadmap](#roadmap)
- [Changelog](#changelog)

## 🛠️ Instalación

### Requisitos Previos
- Python 3.8 o superior
- Ollama instalado y configurado
- Modelo compatible en Ollama (ver recomendaciones abajo)

#### Modelos Recomendados

| Modelo | Tamaño | Velocidad | Instrucciones | Personalidad | Recomendación |
|--------|--------|-----------|---------------|--------------|---------------|
| llama3.2:3b | 3 GB | ⚡⚡ | ✅ Bueno | ✅ Funciona bien | ⭐ RECOMENDADO |
| qwen2.5:7b | 4.7 GB | ⚡ | ⭐ Excelente | ⭐ Excelente | ⭐ Mejor para herramientas |
| mistral:7b | 4.1 GB | ⚡⚡ | ✅ Bueno | ✅ Funciona | ✅ Buena opción |
| llama3.1:8b | 4.7 GB | ⚡ | ✅ Muy bueno | ✅ Muy bueno | ✅ Máxima calidad |
| gemma3:1b | 815 MB | ⚡⚡⚡ | ❌ Pobre | ❌ No funciona | ❌ NO recomendado |

**Nota**: Los modelos pequeños (<3B parámetros) tienen dificultades para mantener personalidades y seguir instrucciones complejas.

### Pasos de Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/ozkar-co/Emma.git
cd Emma

# 2. Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Verificar que Ollama esté ejecutándose
ollama serve
```

## 🚀 Uso Rápido

```bash
# Iniciar Emma (entra directamente en modo chat)
python emma.py

# Comandos disponibles en el chat:
# /help - Mostrar ayuda
# /personality list - Listar personalidades
# /personality set <nombre> - Cambiar personalidad
# /clear - Limpiar pantalla
# /exit - Salir
```

## ⚙️ Configuración

Emma se configura mediante el archivo `config.yaml`. Las opciones principales incluyen:

```yaml
# Configuración del modelo
model: "gemma3:1b"
temperature: 0.7
max_tokens: 800

# Configuración de la aplicación
user_name: "Oz"
use_panels: false
ollama_host: "http://localhost:11434"

# Personalidades predefinidas
personalities:
  default: "Eres Emma, una asistente virtual inteligente y amigable."
  técnica: "Eres Emma, una asistente técnica experta en programación..."
  creativa: "Eres Emma, una asistente creativa con gran imaginación..."
```

## 🎮 Comandos Disponibles

### Comandos Básicos
- `/help` - Mostrar ayuda completa
- `/clear` - Limpiar la pantalla
- `/exit` - Salir de Emma

### Comandos de Personalidad
- `/personality list` - Listar personalidades disponibles
- `/personality set <nombre>` - Cambiar a una personalidad específica
- `/personality info <nombre>` - Ver detalles de una personalidad

## 🎭 Personalidades

Emma incluye varias personalidades predefinidas:

| Personalidad | Descripción |
|--------------|-------------|
| `default` | Asistente amigable y versátil |
| `técnica` | Especializada en programación y tecnología |
| `creativa` | Enfocada en ideas innovadoras |
| `concisa` | Respuestas breves y directas |
| `educativa` | Explicaciones claras y didácticas |
| `sexy` | Conversaciones de temática adulta |

## 🔍 Sistema de Búsqueda

Emma analiza automáticamente tus preguntas y determina si requieren información externa:

### Tipos de Búsqueda
- **`<search>texto</search>`** - Búsquedas en internet/Wikipedia
- **`<memory>texto</memory>`** - Búsquedas en memoria interna
- **`<query>texto</query>`** - Búsquedas en bases de datos/APIs

### Ejemplos
```
Usuario: "¿Cuál es la capital de Francia?"
Emma: "[Searching internet for: capital de Francia]"

Usuario: "¿Cuál fue mi última conversación sobre IA?"
Emma: "[Searching memory for: última conversación IA]"
```

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Aquí están los pasos fundamentales para contribuir:

### Proceso de Contribución

1. **Fork del proyecto** y clona tu repositorio
2. **Implementa tu feature** o mejora
3. **Actualiza la documentación**:
   - Si es una nueva característica importante, muévela del Roadmap a la lista de Features
   - Actualiza el README.md según corresponda
4. **Actualiza el Changelog** con los detalles de tus cambios
5. **Si usaste una nueva librería**, añádela a la sección de Agradecimientos
6. **Crea un Pull Request** con una descripción clara

### Notas Importantes

- Mantén el código simple y legible
- Sigue las convenciones de nomenclatura existentes
- Documenta cualquier nueva funcionalidad
- Los cambios deben ser compatibles con la configuración actual

## 🗺️ Roadmap

### 🎯 **Ruta Principal** - Contribuciones al Core

#### **Arquitectura Modular** ✅ **COMPLETADO**
- **Refactorización del Core**: Arquitectura modular para mejor mantenibilidad ✅
- **Adapter LLM Base**: Interfaz base y adaptadores para Ollama ✅
- **System Prompts Separados**: Archivos individuales para cada personalidad ✅

#### **Interfaz y Memoria**
- **STT/TTS Básico**: Comandos de voz iniciales (Speech-to-Text / Text-to-Speech)
- **Memoria Contextual**: Sistema básico de memoria contextual
- **Memoria Avanzada**: Base de datos local con embeddings locales
- **Consulta por Relevancia**: Búsqueda en memoria previa por similitud

### 🔬 **Ruta Alternativa** - Experimentos e Ideas

#### **Expansión de Capacidades**
- **Motor LLM Dinámico**: Selección dinámica entre local/remoto
- **Medición de Tokens**: Estimación de tokens por interacción
- **GUI Gráfica**: Interfaz gráfica de usuario
- **Plugin de Emociones**: Avatar visual con expresiones basadas en el mood

#### **Integraciones Futuras**
- **Búsquedas en Internet**: APIs de búsqueda/Wikipedia
- **Búsquedas en Base de Datos**: Conexiones con APIs personalizadas
- **Sistema de Plugins**: Arquitectura para funcionalidades adicionales
- **API REST**: Endpoints para integración externa
- **Docker Support**: Containerización de la aplicación

## 📝 Changelog

Para ver el historial completo de cambios, consulta el archivo [CHANGELOG.md](CHANGELOG.md).

### Versión Actual: rev_250718
- **Refactorización completa del Core**: Arquitectura modular implementada
- **Adapter Ollama**: Integración completa y modular con la API de Ollama
- **Sistema de Personalidades Separado**: Archivos YAML individuales para cada personalidad
- **Mejoras en la Configuración**: Sistema de configuración más limpio y modular
- Sistema de versionado por fechas
- Documentación completamente renovada
- Roadmap detallado con ruta principal y alternativa

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🙏 Agradecimientos

- [Ollama](https://ollama.ai/) por proporcionar la infraestructura de modelos
- [Rich](https://rich.readthedocs.io/) por la interfaz de terminal
- [Typer](https://typer.tiangolo.com/) por el framework CLI
- [Pydantic](https://pydantic-docs.helpmanual.io/) por la validación de datos

---

**¿Necesitas ayuda?** Abre un [issue](https://github.com/ozkar-co/Emma/issues) o consulta la [documentación](docs/). 