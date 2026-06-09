#!/bin/bash
cd / 
npx hardhat compile
echo "Deploying contracts..."
cd contracts/scripts
node deploy_with_ethers.ts
ethereum-wallet --password "" --network localhost run scripts/deploy_with_ethers.ts