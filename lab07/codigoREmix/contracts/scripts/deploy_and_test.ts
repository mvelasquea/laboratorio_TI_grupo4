import { ethers, network } from "hardhat";
import { Certificados } from "../build/Certificados.json";

async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying contracts...")

  // Deploy Certificados
  const CertificadosFactory = await ethers.getContractFactory(Certificados);
  const certificados = await CertificadosFactory.deploy();
  await certificados.deployed();
  console.log("Certificados deployed to:", certificados.address);

  // Ejecutar pruebas
  await network.provider.send(
    "hardhat_mine",
    []
  );
  await ethers.provider.send(
    "evm_setAutomine",
    [true]
  );
  await ethers.provider.send(
    "evm_setBlockTime",
    [1]
  );
  
  await require("@nomicfoundation/hardhat-toolbox/networking").run("run", "tests/Certificados.test.js");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});