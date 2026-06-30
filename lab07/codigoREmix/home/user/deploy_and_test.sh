#!/bin/bash

# Configuración de Hardhat para despliegue y pruebas
cd /contracts/scripts

# Compilar el contrato
./compile_contract.sh

# Ejecutar despliegue y pruebas
npx hardhat run scripts/deploy_and_test.ts --network hardhat