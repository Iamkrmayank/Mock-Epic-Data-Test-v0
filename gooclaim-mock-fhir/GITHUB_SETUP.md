# GitHub Setup Guide

Complete guide for pushing Gooclaim Mock FHIR API to GitHub.

## 🚀 Quick Start

### Step 1: Initialize Git Repository

```bash
cd gooclaim-mock-fhir

# Initialize git (if not already done)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Gooclaim Mock FHIR API"
```

### Step 2: Create GitHub Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click the **+** icon → **New repository**
3. Repository name: `gooclaim-mock-fhir` (or your preferred name)
4. Description: `Mock FHIR API server using Epic-style fixtures`
5. Choose **Public** or **Private**
6. **DO NOT** initialize with README (we already have one)
7. Click **Create repository**

### Step 3: Connect and Push

```bash
# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/gooclaim-mock-fhir.git

# Or using SSH (if you have SSH keys set up)
# git remote add origin git@github.com:YOUR_USERNAME/gooclaim-mock-fhir.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

## 📝 Complete Commands

### For New Repository:

```bash
cd gooclaim-mock-fhir

# Initialize git
git init

# Add files
git add .

# Commit
git commit -m "Initial commit: Gooclaim Mock FHIR API with Docker support"

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/gooclaim-mock-fhir.git

# Push
git branch -M main
git push -u origin main
```

### For Existing Repository:

```bash
cd gooclaim-mock-fhir

# Check current status
git status

# Add all changes
git add .

# Commit
git commit -m "Add Docker support and ACR deployment"

# Push
git push origin main
```

## 🔒 What Gets Pushed?

Based on `.gitignore`, these files **will be pushed**:
- ✅ Source code (`src/`)
- ✅ Configuration files (`package.json`, `tsconfig.json`, `Dockerfile`)
- ✅ Documentation (`README.md`, `*.md`)
- ✅ Fixture files (`fhir-fixtures/`)
- ✅ Scripts (`*.sh`, `*.ps1`)

These files **will NOT be pushed**:
- ❌ `node_modules/` (dependencies)
- ❌ `dist/` (build output)
- ❌ `.env` (environment variables)
- ❌ Log files
- ❌ IDE files

## 🔐 Security Considerations

### Before Pushing:

1. **Check for secrets**: Make sure no API keys, tokens, or passwords are in code
2. **Review .gitignore**: Ensure sensitive files are excluded
3. **Environment variables**: Never commit `.env` files

### Recommended Secrets to Add to GitHub:

If using GitHub Actions for CI/CD, add these as **Repository Secrets**:
- `ACR_LOGIN_SERVER`
- `ACR_USERNAME`
- `ACR_PASSWORD`
- `AZURE_CREDENTIALS`

## 🔄 GitHub Actions CI/CD

A GitHub Actions workflow is included (`.github/workflows/docker-build.yml`) that will:
- Build TypeScript on push
- Build Docker image
- Push to Azure Container Registry

To enable:
1. Add repository secrets (Settings → Secrets → Actions)
2. Push to main branch
3. Workflow will run automatically

## 📋 Git Workflow Best Practices

### Making Changes:

```bash
# Check what changed
git status

# Add specific files
git add src/app.ts

# Or add all changes
git add .

# Commit with descriptive message
git commit -m "Add new FHIR endpoint"

# Push to GitHub
git push origin main
```

### Creating Branches:

```bash
# Create feature branch
git checkout -b feature/new-endpoint

# Make changes and commit
git add .
git commit -m "Add new endpoint"

# Push branch
git push origin feature/new-endpoint

# Create Pull Request on GitHub
```

## 🌿 Branch Strategy

Recommended branches:
- `main` - Production-ready code
- `develop` - Development branch
- `feature/*` - Feature branches
- `hotfix/*` - Urgent fixes

## 📚 Repository Structure on GitHub

Your repository will have:

```
gooclaim-mock-fhir/
├── .github/
│   └── workflows/
│       └── docker-build.yml    # CI/CD pipeline
├── src/                        # TypeScript source
├── fhir-fixtures/              # JSON fixture files
├── public/                     # Static files
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Docker Compose
├── package.json                # Dependencies
├── tsconfig.json               # TypeScript config
├── README.md                   # Documentation
├── ACR_DEPLOYMENT.md           # ACR deployment guide
├── DOCKER.md                   # Docker guide
└── .gitignore                  # Git ignore rules
```

## 🐛 Troubleshooting

### Authentication Issues

```bash
# If prompted for credentials, use Personal Access Token
# Or set up SSH keys:
ssh-keygen -t ed25519 -C "your_email@example.com"
# Add public key to GitHub Settings → SSH and GPG keys
```

### Large Files

If fixtures are too large:
```bash
# Use Git LFS for large JSON files
git lfs install
git lfs track "*.json"
git add .gitattributes
git add fhir-fixtures/
git commit -m "Track JSON files with Git LFS"
```

### Push Rejected

```bash
# If remote has changes you don't have:
git pull origin main --rebase
# Then push again
git push origin main
```

## 🔗 Useful Links

- [GitHub Documentation](https://docs.github.com)
- [Git Basics](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics)
- [GitHub Actions](https://docs.github.com/en/actions)

---

**Ready to push?** Follow the Quick Start steps above! 🚀

