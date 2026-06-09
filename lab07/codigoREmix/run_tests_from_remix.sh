#!/bin/bash

# Configuración para ejecutar pruebas de Hardhat desde Remix IDE
echo "Iniciando pruebas con Hardhat..."

# Instalar dependencias de Hardhat (si no están instaladas)
pnpm install --save-dev hardhat

# Ejecutar pruebas con Hardhat
npx hardhat test --network hardhat

echo "Pruebas completadas."