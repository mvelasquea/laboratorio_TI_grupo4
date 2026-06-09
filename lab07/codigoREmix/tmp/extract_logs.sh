#!/bin/bash

# Extraer logs de Hardhat y guardarlos en un archivo
npx hardhat test --network hardhat --show-stack-traces --report &&
cp /home/udapp/hardhat-report.json /tmp/test_logs.json

# Verificar si se generó el archivo
if [ -f /tmp/test_logs.json ]; then
    echo "Logs guardados en /tmp/test_logs.json"
else
    echo "Error: No se pudo generar el archivo de logs"
    exit 1
fi