#!/bin/bash

# Configuración para ejecutar el despliegue y pruebas

# Desplegar contratos usando ethers
echo "Desplegando contratos con ethers...";
ts-node /contracts/scripts/deploy_with_ethers.ts

# Ejecutar pruebas con Hardhat y redirigir logs
npx hardhat test --network hardhat --show-stack-traces --report && echo "Logs guardados en el directorio /tmp/test_logs_dir"

# Copiar el contenido del archivo de Hardhat report
cp /home/udapp/hardhat-report.json /tmp/test_logs.json

# Asegurar que los logs estén accesibles para análisis
echo "Logs de las pruebas guardados en /tmp/test_logs.json."