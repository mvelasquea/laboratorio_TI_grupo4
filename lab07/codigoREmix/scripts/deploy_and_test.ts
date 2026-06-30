import { ethers, run } from 'hardhat';

async function main() {
  // Obtener el contrato factory y el contrato desplegado
  const CertificadosFactory = await ethers.getContractFactory('Certificados');
  const certificadosContract = await CertificadosFactory.deploy();
  await certificadosContract.deployed();
  console.log(`Certificados contract address: ${certificadosContract.address}`);

  // Registrar el certificado
  const codigo = 'UNSA-2026-0041';
  const nombreTitular = 'Juan Pérez';
  const metadata = '{}'; // Usar un JSON vacío o el contenido correcto desde un archivo
  await certificadosContract.registrar(codigo, nombreTitular, metadata);
  console.log(`Certificado ${codigo} registrado con éxito para ${nombreTitular}`);

  // Ejecutar pruebas unitarias
  await run('test', { blockInterval: 0 });
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});