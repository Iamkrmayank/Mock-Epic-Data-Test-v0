#!/bin/bash
# Simple ACR Push Script for Git Bash
# Usage: ./push-acr-simple.sh

set -e

ACR_NAME="gooclaimehracr"
RESOURCE_GROUP="gooclaim-rg"
IMAGE_NAME="gooclaim-mock-fhir"
IMAGE_TAG="latest"

echo "🚀 Pushing to ACR: $ACR_NAME"
echo ""

# Get ACR login server
echo "🔍 Getting ACR login server..."
ACR_SERVER=$(az acr show --name $ACR_NAME --resource-group $RESOURCE_GROUP --query loginServer --output tsv 2>/dev/null)

if [ -z "$ACR_SERVER" ]; then
    echo "❌ Failed to get ACR server. Please check ACR name and resource group."
    exit 1
fi

echo "✓ ACR Server: $ACR_SERVER"
echo ""

# Login to ACR
echo "🔑 Logging in to ACR..."
az acr login --name $ACR_NAME
echo ""

# Tag image (using quotes to handle any special characters)
echo "📦 Tagging image..."
docker tag "${IMAGE_NAME}:${IMAGE_TAG}" "${ACR_SERVER}/${IMAGE_NAME}:${IMAGE_TAG}"
echo "✓ Tagged: ${ACR_SERVER}/${IMAGE_NAME}:${IMAGE_TAG}"
echo ""

# Push to ACR
echo "⬆️  Pushing image to ACR..."
docker push "${ACR_SERVER}/${IMAGE_NAME}:${IMAGE_TAG}"

echo ""
echo "✅ Successfully pushed to ACR!"
echo ""
echo "📋 Image Location:"
echo "   ${ACR_SERVER}/${IMAGE_NAME}:${IMAGE_TAG}"
echo ""

