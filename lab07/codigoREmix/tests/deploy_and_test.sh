#!/bin/bash

# Deploy contracts using Remix scripts
export PATH=$PATH:$HOME/.nvm/versions/node/v19.0.0/lib/node_modules/.bin

# Deploy Certificados contract via Remix IDE
./deploy_with_ethers.ts

# Run deployment and registration tests
docker-compose run --rm remix-ide remix test --network localhost