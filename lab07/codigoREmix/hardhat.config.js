require('dotenv').config();
require('@nomicfoundation/hardhat-toolbox');

// Configuración básica de Hardhat
const config = {
  solidity: {
    version: "0.8.20",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200,
      },
    },
  },
  networks: {
    hardhat: {
      allowUnlimitedContractSize: true,
    },
  },
  // Configuración para ejecutar pruebas
  paths: {
    tests: "tests",
    sources: "contracts",
  },
  // Configuración para ejecutar pruebas con Hardhat
  plugins: [
    "solidity-coverage",
    "nomicfoundation-hardhat-toolbox",
  ],
  // Configuración para ejecutar pruebas desde Remix IDE
  env: {
    REMIX_HARDHAT_NETWORK: "hardhat",
  },
  // Configuración para ejecutar scripts desde Remix IDE
  scripts: {
    "run_tests": "npx hardhat test --network hardhat",
  },
};

module.exports = config;