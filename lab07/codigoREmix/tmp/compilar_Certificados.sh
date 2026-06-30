#!/bin/bash

# Verificar si el archivo Certificados.sol existe
if [ -f /contracts/Certificados.sol ]; then
    echo "Archivo Certificados.sol encontrado."
    echo "Ejecutando: npx hardhat compile"
    npx hardhat compile && 
    echo "Contrato compilado con éxito."
else
    echo "Error: Archivo Certificados.sol no encontrado."
fi