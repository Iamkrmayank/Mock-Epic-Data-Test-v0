#!/bin/bash
# Azure Container Registry Push Script
# Usage: ./push-to-acr.sh <acr-name> <resource-group> [image-tag]

set -e

ACR_NAME=${1:-""}
RESOURCE_GROUP=${2:-""}
IMAGE_TAG=${3:-"latest"}
IMAGE_NAME="gooclaim-mock-fhir"

if [ -z "$ACR_NAME" ] || [ -z "$RESOURCE_GROUP" ]; then
    echo "❌ Usage: ./push-to-acr.sh <acr-name> <resource-group> [image-tag]"
    exit 1
fi

echo "🚀 Pushing Gooclaim Mock FHIR API to Azure Container Registry..."
echo ""

# Step 1: Check Azure login
echo "📝 Checking Azure login..."
if ! az account show &>/dev/null; then
    echo "⚠️  Not logged in to Azure. Logging in..."
    az login
fi

# Step 2: Verify ACR exists
echo "🔍 Verifying ACR exists..."
if ! az acr show --name $ACR_NAME --resource-group $RESOURCE_GROUP &>/dev/null; then
    echo "❌ ACR '$ACR_NAME' not found in resource group '$RESOURCE_GROUP'"
    echo "Would you like to create it? (y/n)"
    read -r create
    if [ "$create" = "y" ] || [ "$create" = "Y" ]; then
        echo "🏗️  Creating ACR..."
        az acr create --resource-group $RESOURCE_GROUP --name $ACR_NAME --sku Basic --admin-enabled true
    else
        echo "❌ Cannot proceed without ACR"
        exit 1
    fi
fi

# Step 3: Get ACR login server
echo "🔐 Getting ACR login server..."
ACR_LOGIN_SERVER=$(az acr show --name $ACR_NAME --resource-group $RESOURCE_GROUP --query loginServer --output tsv)
if [ -z "$ACR_LOGIN_SERVER" ]; then
    echo "❌ Failed to get ACR login server"
    exit 1
fi
echo "✓ ACR Login Server: $ACR_LOGIN_SERVER"

# Step 4: Login to ACR
echo "🔑 Logging in to ACR..."
az acr login --name $ACR_NAME

# Step 5: Build image if not exists
echo "🏗️  Checking if image exists locally..."
if ! docker images "$IMAGE_NAME:$IMAGE_TAG" --format "{{.Repository}}:{{.Tag}}" | grep -q "$IMAGE_NAME:$IMAGE_TAG"; then
    echo "📦 Image not found. Building..."
    docker build -t "$IMAGE_NAME:$IMAGE_TAG" .
else
    echo "✓ Image exists locally: $IMAGE_NAME:$IMAGE_TAG"
fi

# Step 6: Tag image for ACR
echo "📦 Tagging image for ACR..."
ACR_IMAGE_TAG="$ACR_LOGIN_SERVER/$IMAGE_NAME:$IMAGE_TAG"
docker tag "$IMAGE_NAME:$IMAGE_TAG" $ACR_IMAGE_TAG
echo "✓ Tagged: $ACR_IMAGE_TAG"

# Step 7: Push to ACR
echo "⬆️  Pushing image to ACR..."
docker push $ACR_IMAGE_TAG

# Step 8: Verify
echo ""
echo "✅ Successfully pushed to ACR!"
echo ""
echo "📋 Image Details:"
echo "   ACR Login Server: $ACR_LOGIN_SERVER"
echo "   Image Name: $IMAGE_NAME"
echo "   Tag: $IMAGE_TAG"
echo "   Full Path: $ACR_IMAGE_TAG"
echo ""
echo "🔗 Pull Command:"
echo "   docker pull $ACR_IMAGE_TAG"

