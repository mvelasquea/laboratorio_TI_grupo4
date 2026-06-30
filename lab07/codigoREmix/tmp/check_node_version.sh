#!/bin/bash

# Comprobar la versión de Node.js
node_version=$(node --version 2>/dev/null)
if [ -z "$node_version" ]; then
    echo "Node.js no está instalado o no se puede acceder a él."
else
    echo "Node.js está instalado (versión: $node_version)"
fi

# Comprobar la versión de npm
npm_version=$(npm --version 2>/dev/null)
if [ -z "$npm_version" ]; then
    echo "npm no está instalado o no se puede acceder a él."
else
    echo "npm está instalado (versión: $npm_version)"
fi