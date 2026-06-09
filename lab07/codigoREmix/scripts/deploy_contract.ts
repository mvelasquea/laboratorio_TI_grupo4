// Script para desplegar y registrar el contrato Certificados en Hardhat
const { ethers } = require('ethers');

// Configuración del proveedor de Hardhat
const provider = new ethers.providers.JsonRpcProvider('http://localhost:8545');

// Configuración para obtener el contrato desde Hardhat
(async () => {
  try {
    const CertificadosFactory = await ethers.getContractFactory('Certificados');
    const certificadosContract = await CertificadosFactory.deploy();
    await certificadosContract.deployed();
    console.log(`✅ Contrato desplegado correctamente: ${certificadosContract.address}`);
    
    // Obtener metadata del archivo JSON
    const metadata = JSON.parse(await require('fs').promises.readFile('/artifacts/Certificados_metadata.json', 'utf-8'));
    
    const codigo = 'UNSA-2026-0041';
    const nombreTitular = 'Juan Pérez';
    
    // Registrar el certificado
    await certificadosContract.registrar(codigo, nombreTitular, metadata);
    console.log(`🎉 Certificado ${codigo} registrado con éxito para ${nombreTitular}`);
    
  } catch (error) {
    console.error('❌ Error:', error.message);
  }
})();