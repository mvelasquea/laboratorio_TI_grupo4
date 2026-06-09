// Script para iniciar el nodo Hardhat localmente

// Configuración de Hardhat para ejecutar el nodo
const hre = require('hardhat');

(async () => {
  try {
    console.log('🚀 Iniciando el nodo Hardhat local...
    ');
    
    // Iniciar el nodo Hardhat
    await hre.network.provider.request({
      method: 'hardhat_ignorePermissions',
      params: [],
    });
    
    // Iniciar el nodo
    await hre.network.provider.request({
      method: 'hardhat_startNetwork',
      params: [],
    });
    
    console.log('✅ Nodo Hardhat iniciado correctamente en localhost:8545.
    Puedes proceder con el despliegue del contrato.
    ');
  }
  catch (error) {
    console.error('❌ Error al iniciar el nodo Hardhat:', error.message);
  }
})();