#!/usr/bin/env bash
# Exit on error
set -e

# Install Node.js dependencies
npm install

# Create uploads directory if it doesn't exist
mkdir -p uploads

echo "Build completed successfully!" 