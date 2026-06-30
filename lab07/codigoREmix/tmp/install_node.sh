#!/bin/bash

# Descargar la última versión estable de Node.js para Linux
wget https://nodejs.org/dist/v20.12.2/node-v20.12.2-linux-x64.tar.xz -O /tmp/nodejs.tar.xz

# Descomprimir el archivo
sudo tar -xf /tmp/nodejs.tar.xz -C /usr/local

# Agregar el directorio de Node.js al PATH
echo 'export PATH=/usr/local/node-v20.12.2-linux-x64/bin:$PATH' >> /etc/environment

# Aplicar los cambios del PATH
source /etc/environment

# Verificar la instalación
node --version && npm --version