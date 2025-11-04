# Azure Container Registry Push Script
# Usage: .\push-to-acr.ps1 -AcrName <your-acr-name> -ResourceGroup <rg-name> [-ImageTag <tag>]

param(
    [Parameter(Mandatory=$true)]
    [string]$AcrName,
    
    [Parameter(Mandatory=$true)]
    [string]$ResourceGroup,
    
    [Parameter(Mandatory=$false)]
    [string]$ImageTag = "latest",
    
    [Parameter(Mandatory=$false)]
    [string]$ImageName = "gooclaim-mock-fhir"
)

Write-Host "🚀 Pushing Gooclaim Mock FHIR API to Azure Container Registry..." -ForegroundColor Green
Write-Host ""

# Step 1: Check if logged in to Azure
Write-Host "📝 Checking Azure login..." -ForegroundColor Yellow
$azAccount = az account show 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Not logged in to Azure. Logging in..." -ForegroundColor Yellow
    az login
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to login to Azure" -ForegroundColor Red
        exit 1
    }
}

# Step 2: Verify ACR exists
Write-Host "🔍 Verifying ACR exists..." -ForegroundColor Yellow
$acrExists = az acr show --name $AcrName --resource-group $ResourceGroup 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ ACR '$AcrName' not found in resource group '$ResourceGroup'" -ForegroundColor Red
    Write-Host ""
    Write-Host "Would you like to create it? (Y/N)" -ForegroundColor Yellow
    $create = Read-Host
    if ($create -eq "Y" -or $create -eq "y") {
        Write-Host "🏗️  Creating ACR..." -ForegroundColor Yellow
        az acr create --resource-group $ResourceGroup --name $AcrName --sku Basic --admin-enabled true
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Failed to create ACR" -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "❌ Cannot proceed without ACR" -ForegroundColor Red
        exit 1
    }
}

# Step 3: Get ACR login server
Write-Host "🔐 Getting ACR login server..." -ForegroundColor Yellow
$acrLoginServer = az acr show --name $AcrName --resource-group $ResourceGroup --query loginServer --output tsv
if (-not $acrLoginServer) {
    Write-Host "❌ Failed to get ACR login server" -ForegroundColor Red
    exit 1
}
Write-Host "✓ ACR Login Server: $acrLoginServer" -ForegroundColor Green

# Step 4: Login to ACR
Write-Host "🔑 Logging in to ACR..." -ForegroundColor Yellow
az acr login --name $AcrName
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to login to ACR" -ForegroundColor Red
    exit 1
}

# Step 5: Build image if not exists
Write-Host "🏗️  Checking if image exists locally..." -ForegroundColor Yellow
$imageExists = docker images "$ImageName`:$ImageTag" --format "{{.Repository}}:{{.Tag}}" 2>&1
if (-not $imageExists -or $imageExists -eq "") {
    Write-Host "📦 Image not found. Building..." -ForegroundColor Yellow
    docker build -t "$ImageName`:$ImageTag" .
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to build image" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "✓ Image exists locally: $ImageName`:$ImageTag" -ForegroundColor Green
}

# Step 6: Tag image for ACR
Write-Host "📦 Tagging image for ACR..." -ForegroundColor Yellow
$acrImageTag = "$acrLoginServer/$ImageName`:$ImageTag"
docker tag "$ImageName`:$ImageTag" $acrImageTag
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to tag image" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Tagged: $acrImageTag" -ForegroundColor Green

# Step 7: Push to ACR
Write-Host "⬆️  Pushing image to ACR..." -ForegroundColor Yellow
docker push $acrImageTag
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to push image to ACR" -ForegroundColor Red
    exit 1
}

# Step 8: Verify
Write-Host "✅ Successfully pushed to ACR!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Image Details:" -ForegroundColor Cyan
Write-Host "   ACR Login Server: $acrLoginServer" -ForegroundColor White
Write-Host "   Image Name: $ImageName" -ForegroundColor White
Write-Host "   Tag: $ImageTag" -ForegroundColor White
Write-Host "   Full Path: $acrImageTag" -ForegroundColor White
Write-Host ""
Write-Host "🔗 Pull Command:" -ForegroundColor Cyan
Write-Host "   docker pull $acrImageTag" -ForegroundColor White
Write-Host ""
Write-Host "🚀 Deploy to Azure Container Instances:" -ForegroundColor Cyan
Write-Host "   az container create \"`
Write-Host "     --resource-group $ResourceGroup \"`
Write-Host "     --name gooclaim-fhir-api \"`
Write-Host "     --image $acrImageTag \"`
Write-Host "     --dns-name-label gooclaim-fhir-api \"`
Write-Host "     --ports 8080 \"`
Write-Host "     --registry-login-server $acrLoginServer \"`
Write-Host "     --registry-username \$ACR_USERNAME \"`
Write-Host "     --registry-password \$ACR_PASSWORD" -ForegroundColor White

