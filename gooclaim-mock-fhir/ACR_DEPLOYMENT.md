# Azure Container Registry (ACR) Deployment Guide

Complete guide for pushing and deploying Gooclaim Mock FHIR API to Azure Container Registry.

## 🚀 Quick Start

### Option 1: PowerShell Script (Windows)

```powershell
.\push-to-acr.ps1 -AcrName <your-acr-name> -ResourceGroup <your-rg-name>
```

### Option 2: Bash Script (Linux/Mac)

```bash
chmod +x push-to-acr.sh
./push-to-acr.sh <acr-name> <resource-group> [tag]
```

### Option 3: Manual Steps

Follow the manual steps below.

## 📋 Prerequisites

1. **Azure CLI** installed and configured
2. **Docker** installed and running
3. **Azure Subscription** with permissions to create ACR
4. **Docker image** built locally (`gooclaim-mock-fhir:latest`)

## 🔧 Step-by-Step Guide

### Step 1: Azure Login

```powershell
# Login to Azure
az login

# Set subscription (if you have multiple)
az account set --subscription "<subscription-id>"
```

### Step 2: Create Resource Group (if not exists)

```powershell
az group create --name gooclaim-rg --location eastus
```

### Step 3: Create ACR (if not exists)

```powershell
az acr create \
  --resource-group gooclaim-rg \
  --name <your-acr-name> \
  --sku Basic \
  --admin-enabled true
```

**Note**: ACR name must be globally unique and 5-50 characters (lowercase letters and numbers only).

### Step 4: Build Docker Image (if not already built)

```powershell
cd gooclaim-mock-fhir
docker build -t gooclaim-mock-fhir:latest .
```

### Step 5: Login to ACR

```powershell
az acr login --name <your-acr-name>
```

### Step 6: Get ACR Login Server

```powershell
$acrLoginServer = az acr show --name <your-acr-name> --resource-group gooclaim-rg --query loginServer --output tsv
Write-Host $acrLoginServer
```

### Step 7: Tag Image for ACR

```powershell
docker tag gooclaim-mock-fhir:latest <acr-login-server>/gooclaim-mock-fhir:latest
```

### Step 8: Push to ACR

```powershell
docker push <acr-login-server>/gooclaim-mock-fhir:latest
```

## 🎯 Complete Example

```powershell
# Variables
$ACR_NAME = "gooclaimacr"  # Must be globally unique
$RESOURCE_GROUP = "gooclaim-rg"
$IMAGE_NAME = "gooclaim-mock-fhir"
$IMAGE_TAG = "latest"

# Create resource group
az group create --name $RESOURCE_GROUP --location eastus

# Create ACR
az acr create --resource-group $RESOURCE_GROUP --name $ACR_NAME --sku Basic --admin-enabled true

# Login to ACR
az acr login --name $ACR_NAME

# Get login server
$ACR_LOGIN_SERVER = az acr show --name $ACR_NAME --resource-group $RESOURCE_GROUP --query loginServer --output tsv

# Build image (if not already built)
docker build -t "$IMAGE_NAME`:$IMAGE_TAG" .

# Tag for ACR
docker tag "$IMAGE_NAME`:$IMAGE_TAG" "$ACR_LOGIN_SERVER/$IMAGE_NAME`:$IMAGE_TAG"

# Push to ACR
docker push "$ACR_LOGIN_SERVER/$IMAGE_NAME`:$IMAGE_TAG"
```

## 📦 Push Different Tags

### Version Tags

```powershell
# Tag with version
docker tag gooclaim-mock-fhir:latest <acr-server>/gooclaim-mock-fhir:v1.0.0
docker push <acr-server>/gooclaim-mock-fhir:v1.0.0

# Tag with date
$DATE = Get-Date -Format "yyyyMMdd"
docker tag gooclaim-mock-fhir:latest <acr-server>/gooclaim-mock-fhir:$DATE
docker push <acr-server>/gooclaim-mock-fhir:$DATE
```

## 🚀 Deploy to Azure

### Option 1: Azure Container Instances (ACI)

```powershell
# Get ACR credentials
$ACR_USERNAME = az acr credential show --name <acr-name> --query username --output tsv
$ACR_PASSWORD = az acr credential show --name <acr-name> --query passwords[0].value --output tsv

# Deploy to ACI
az container create `
  --resource-group gooclaim-rg `
  --name gooclaim-fhir-api `
  --image <acr-server>/gooclaim-mock-fhir:latest `
  --dns-name-label gooclaim-fhir-api `
  --ports 8080 `
  --registry-login-server <acr-server> `
  --registry-username $ACR_USERNAME `
  --registry-password $ACR_PASSWORD `
  --environment-variables PORT=8080 FIXTURE_DIR=./fhir-fixtures EHR_MODE=mock
```

### Option 2: Azure Container Apps

```powershell
# Create Container App Environment
az containerapp env create `
  --name gooclaim-env `
  --resource-group gooclaim-rg `
  --location eastus

# Create Container App
az containerapp create `
  --name gooclaim-fhir-api `
  --resource-group gooclaim-rg `
  --environment gooclaim-env `
  --image <acr-server>/gooclaim-mock-fhir:latest `
  --target-port 8080 `
  --ingress external `
  --registry-server <acr-server> `
  --registry-username $ACR_USERNAME `
  --registry-password $ACR_PASSWORD `
  --env-vars PORT=8080 FIXTURE_DIR=./fhir-fixtures EHR_MODE=mock
```

### Option 3: Azure Kubernetes Service (AKS)

See `deployment.yaml` in the project root for Kubernetes deployment.

## 🔍 Verify Deployment

```powershell
# List images in ACR
az acr repository list --name <acr-name> --output table

# Show image tags
az acr repository show-tags --name <acr-name> --repository gooclaim-mock-fhir --output table

# Get image details
az acr repository show --name <acr-name> --image gooclaim-mock-fhir:latest
```

## 🔐 Security Best Practices

1. **Use Managed Identity** instead of admin credentials when possible
2. **Enable ACR firewall** to restrict access
3. **Use private endpoints** for production
4. **Enable image scanning** for vulnerabilities
5. **Use Azure Key Vault** for secrets

### Managed Identity Example

```powershell
# Assign AcrPull role to managed identity
az role assignment create `
  --assignee <managed-identity-id> `
  --role AcrPull `
  --scope /subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.ContainerRegistry/registries/<acr-name>
```

## 📊 Monitoring

### View ACR Logs

```powershell
az acr repository show-manifests --name <acr-name> --repository gooclaim-mock-fhir
```

### Metrics

Monitor in Azure Portal:
- Image push/pull operations
- Storage usage
- Network traffic

## 🔄 Update Workflow

```powershell
# 1. Make changes to code
# 2. Rebuild image
docker build -t gooclaim-mock-fhir:latest .

# 3. Tag with new version
docker tag gooclaim-mock-fhir:latest <acr-server>/gooclaim-mock-fhir:v1.0.1

# 4. Push to ACR
docker push <acr-server>/gooclaim-mock-fhir:v1.0.1

# 5. Update deployment (example for ACI)
az container create `
  --resource-group gooclaim-rg `
  --name gooclaim-fhir-api `
  --image <acr-server>/gooclaim-mock-fhir:v1.0.1 `
  --restart-policy Always `
  # ... other parameters
```

## 🐛 Troubleshooting

### Authentication Failed

```powershell
# Re-login to ACR
az acr login --name <acr-name>

# Verify credentials
az acr credential show --name <acr-name>
```

### Image Push Failed

```powershell
# Check ACR quota
az acr show-usage --name <acr-name>

# Verify network connectivity
az acr check-health --name <acr-name>
```

### Pull Failed from Container

- Ensure ACR credentials are correct
- Check firewall rules
- Verify image exists: `az acr repository show-tags --name <acr-name> --repository gooclaim-mock-fhir`

## 📝 Notes

- **ACR Name**: Must be globally unique across all Azure
- **Storage**: Basic SKU includes 10GB storage
- **Pricing**: Pay per storage and operations
- **Geo-replication**: Available in Premium SKU

## 🔗 Useful Commands

```powershell
# List all ACRs
az acr list --output table

# Delete ACR (careful!)
az acr delete --name <acr-name> --resource-group <rg-name>

# Export/Import images
az acr import --name <acr-name> --source <source-registry>/<image>:<tag>

# Repository management
az acr repository list --name <acr-name>
az acr repository delete --name <acr-name> --repository gooclaim-mock-fhir --tag <tag>
```

---

For more information, see [Azure Container Registry Documentation](https://docs.microsoft.com/azure/container-registry/).

