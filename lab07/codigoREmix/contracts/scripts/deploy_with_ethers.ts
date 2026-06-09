const { ethers } = require('ethers');

// Configure Remix IDE environment variables
const provider = new ethers.providers.JsonRpcProvider('http://localhost:8545');
const remix = new ethers.providers.Web3Provider(provider);

// Deploy Certificados contract
(async () => {
  try {
    const CertificadosFactory = await remix.getContractFactory('Certificados');
    const certificadosContract = await CertificadosFactory.deploy();
    await certificadosContract.deployed();
    console.log(`Certificados contract address: ${certificadosContract.address}`);

    const metadata = JSON.parse(await remix.call('fileManager', 'getFile', '/artifacts/Certificados_metadata.json'));
    const codigo = 'UNSA-2026-0041';
    const nombreTitular = 'Juan Pérez';

    await certificadosContract.registrar(codigo, nombreTitular, metadata);
    console.log(`Certificado ${codigo} registrado con éxito para ${nombreTitular}`);
  } catch (e) {
    console.error(e.message);
  }
})();