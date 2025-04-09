#!/usr/bin/env python3
"""
Emma - Interfaz de Chat para Ollama
Este script es el punto de entrada principal para la interfaz de chat Emma,
que proporciona una forma amigable de interactuar con modelos de Ollama.
"""

import os
import sys
from emma.cli import app

if __name__ == "__main__":
    sys.exit(app()) 