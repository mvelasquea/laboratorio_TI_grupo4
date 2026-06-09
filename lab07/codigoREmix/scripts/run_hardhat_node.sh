#!/bin/bash

# Script para ejecutar el nodo Hardhat localmente

# Verificar si Hardhat está instalado
if ! command -v hardhat &> /dev/null; then
  echo "❌ Hardhat no está instalado. Por favor, instálalo antes de ejecutar este script."
  exit 1
fi

# Iniciar el nodo Hardhat
echo "🚀 Iniciando el nodo Hardhat local..."