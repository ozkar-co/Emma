# Changelog

Todas las notables mejoras y cambios en este proyecto serán documentadas en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [rev_250505] - 2025-05-05

### Añadido
- **Análisis de prompts inteligente**: Sistema que determina automáticamente si una pregunta requiere búsqueda externa
- **Procesamiento de comandos de búsqueda**: Generación automática de comandos `<search>`, `<memory>`, `<query>`
- **Instrucciones para usuarios**: Guía sobre cómo formatear comandos de búsqueda dentro de los prompts
- **Procesamiento basado en regex**: Manejo de diferentes tipos de búsqueda (internet, memoria, base de datos)
- **Mejoras en manejo de errores**: Logging mejorado para análisis de prompts y generación de respuestas

### Cambiado
- **Simplificación del comando chat**: Eliminación de opciones avanzadas para una interacción más fluida
- **Mejoras en la experiencia de usuario**: Actualización de prompts y mensajes de ayuda para mayor claridad
- **Logging y mensajes de error**: Mejor feedback para debugging y experiencia del usuario
- **Modo chat por defecto**: Activación automática del modo chat cuando no se proporcionan argumentos

## [rev_250409] - 2025-04-09

### Añadido
- **Nueva personalidad 'sexy'**: Personalidad para conversaciones de temática adulta
- **Documentación mejorada**: Secciones detalladas sobre interfaz de chat, personalidades y comandos disponibles
- **Instrucciones de uso clarificadas**: Ejemplos de configuración mejorados

## [rev_250409] - 2025-04-09

### Añadido
- **Archivo principal de aplicación**: Implementación básica de funcionalidad
- **Estructura de proyecto organizada**: Mejor claridad y mantenibilidad de archivos

## [rev_250408] - 2025-04-08

### Añadido
- **Archivos iniciales del proyecto**: .gitignore, README.md y requirements.txt
- **Configuración de exclusión**: .gitignore para archivos y directorios innecesarios
- **Documentación base**: README.md con descripción del proyecto, características, instrucciones de instalación y guías de uso
- **Dependencias**: requirements.txt con las dependencias necesarias del proyecto
