import { ethers } from 'ethers'

// Import Certificados metadata for registration functions
const certificadosMetadata = JSON.parse(await remix.call('fileManager', 'getFile', 'artifacts/Certificados_metadata.json'))

/**
 * Deploy the given contract
 * @param {string} contractName name of the contract to deploy
 * @param {Array<any>} args list of constructor parameters
 * @param {Number} accountIndex account index from the exposed account
 * @return {Contract} deployed contract
 */
export const deploy = async (contractName: string, args: Array<any>, accountIndex?: number): Promise<ethers.Contract> => {
  console.log(`deploying ${contractName}`)
  const artifactsPath = `browser/artifacts/${contractName}.json`
  const metadata = JSON.parse(await remix.call('fileManager', 'getFile', artifactsPath))
  const signer = (new ethers.providers.Web3Provider(web3Provider)).getSigner(accountIndex)

  const factory = new ethers.ContractFactory(metadata.abi, metadata.data.bytecode.object, signer)
  const contract = await factory.deploy(...args)
  await contract.deployed()
  return contract
}

/**
 * Register a certificate with metadata
 * @param {ethers.Contract} contract - The Certificados contract instance
 * @param {string} codigo - Certificate code
 * @param {string} nombreTitular - Full name of the certificate holder
 * @return {Promise<void>} - Promise that resolves when registration is complete
 */
export const registrarCertificado = async (contract: ethers.Contract, codigo: string, nombreTitular: string, metadata: any): Promise<void> => {
  console.log(`Registering certificate: ${codigo} for ${nombreTitular}`)
  await contract.registrarCertificado(codigo, nombreTitular)
}

/**
 * Revoke a certificate
 * @param {ethers.Contract} contract - The Certificados contract instance
 * @param {string} codigo - Certificate code to revoke
 * @return {Promise<void>} - Promise that resolves when revocation is complete
 */
export const revocarCertificado = async (contract: ethers.Contract, codigo: string): Promise<void> => {
  console.log(`Revocating certificate: ${codigo}`)
  await contract.revocarCertificado(codigo)
}

/**
 * Verify a certificate
 * @param {ethers.Contract} contract - The Certificados contract instance
 * @param {string} codigo - Certificate code to verify
 * @return {Promise<{ nombre: string, fecha: number, validez: boolean }>} - Verification result
 */
export const verificarCertificado = async (contract: ethers.Contract, codigo: string): Promise<{ nombre: string, fecha: number, validez: boolean }> => {
  const result = await contract.verificarCertificado(codigo)
  return {
    nombre: result.nombre,
    fecha: result.fecha,
    validez: result.validez
  }
}