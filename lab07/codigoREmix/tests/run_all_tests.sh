#!/bin/bash

# Set up environment variables for Hardhat and Remix
export PATH=$PATH:$HOME/.nvm/versions/node/v19.0.0/lib/node_modules/.bin

# Run specific deployment and registration-related tests
docker-compose run --rm remix-ide remix test --network localhost