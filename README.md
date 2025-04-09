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
- Interfaz de línea de comandos intuitiva
- Soporte para diferentes modelos de Ollama (optimizado para gemma3:1b)
- Gestión de contexto y memoria para conversaciones más coherentes
- Configuración flexible para ajustar parámetros del modelo
- Exportación e importación de conversaciones
- Personalización de comportamiento del asistente

## Requisitos
- Python 3.8+
- Ollama instalado y configurado con gemma3:1b
- Dependencias especificadas en `requirements.txt`

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/ozcodx/Emma.git
cd Emma

# Crear un entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

## Uso

```bash
# Ejecutar la interfaz de chat
python emma.py
```

## Configuración
El archivo `config.yaml` permite personalizar varios aspectos de la interfaz:

```yaml
model: "gemma3:1b"
temperature: 0.7
max_tokens: 2000
...
```

## Licencia
[MIT](LICENSE) 