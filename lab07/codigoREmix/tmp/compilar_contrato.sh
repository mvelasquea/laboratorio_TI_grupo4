#!/bin/bash

# Cambiar al directorio donde se encuentra Certificados.sol
cd /contracts

# Compilar el contrato usando Hardhat
npx hardhat compile

# Verificar si el contrato Certificados.sol está en el directorio y compilarlo específicamente
if grep -q 'Certificados.sol' /contracts/Certificados.sol; then
    echo "Compilando Certificados.sol..."