# Docker Guide - Gooclaim Mock FHIR API

Complete guide for building and running the application with Docker.

## 🐳 Quick Start

### Build Image

```bash
docker build -t gooclaim-mock-fhir:latest .
```

### Run Container

```bash
docker run -d \
  --name gooclaim-mock-fhir \
  -p 8080:8080 \
  gooclaim-mock-fhir:latest
```

### Using Docker Compose

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## 📋 Dockerfile Details

The Dockerfile uses a **multi-stage build** for optimization:

### Stage 1: Builder
- Installs all dependencies (including dev dependencies)
- Compiles TypeScript to JavaScript
- Produces optimized production build

### Stage 2: Production
- Only includes production dependencies
- Copies built files and fixtures
- Runs as non-root user for security
- Includes health check

## 🔧 Configuration

### Environment Variables

Override environment variables when running:

```bash
docker run -d \
  --name gooclaim-mock-fhir \
  -p 8080:8080 \
  -e PORT=8081 \
  -e FIXTURE_DIR=./custom-fixtures \
  gooclaim-mock-fhir:latest
```

### Volume Mounts

Mount fixture files for easy updates:

```bash
docker run -d \
  --name gooclaim-mock-fhir \
  -p 8080:8080 \
  -v $(pwd)/fhir-fixtures:/app/fhir-fixtures:ro \
  gooclaim-mock-fhir:latest
```

## 🚀 Docker Compose

### Basic Usage

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f gooclaim-mock-fhir

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

### Custom Configuration

Edit `docker-compose.yml`:

```yaml
services:
  gooclaim-mock-fhir:
    ports:
      - "8081:8080"  # Change host port
    environment:
      - PORT=8080
      - FIXTURE_DIR=./fhir-fixtures
    volumes:
      - ./fhir-fixtures:/app/fhir-fixtures:ro
```

## 🏥 Health Checks

The container includes built-in health checks:

```bash
# Check container health
docker ps

# Manual health check
curl http://localhost:8080/healthz
```

Health check runs every 30 seconds automatically.

## 📦 Image Optimization

### Image Size

- **Alpine-based**: Uses `node:20-alpine` for smaller image size
- **Multi-stage build**: Excludes dev dependencies in final image
- **Production only**: Only necessary files included

### Build Cache

Layers are optimized for Docker build cache:
1. Dependencies (cached if package.json unchanged)
2. Source files (cached if unchanged)
3. Build output (rebuilt if source changes)

## 🔒 Security

### Non-Root User

The container runs as `nodejs` user (UID 1001) instead of root for better security.

### Read-Only Fixtures

When mounting fixtures, use `:ro` flag for read-only access:

```bash
-v $(pwd)/fhir-fixtures:/app/fhir-fixtures:ro
```

## 🧪 Testing

### Build and Test Locally

```bash
# Build image
docker build -t gooclaim-mock-fhir:test .

# Run container
docker run -d -p 8080:8080 --name test gooclaim-mock-fhir:test

# Test endpoints
curl http://localhost:8080/healthz
curl http://localhost:8080/Patient

# Stop and remove
docker stop test && docker rm test
```

## 📤 Publishing to Registry

### Tag for Registry

```bash
docker tag gooclaim-mock-fhir:latest \
  your-registry.com/gooclaim-mock-fhir:v1.0.0
```

### Push to Docker Hub

```bash
docker tag gooclaim-mock-fhir:latest \
  yourusername/gooclaim-mock-fhir:latest

docker push yourusername/gooclaim-mock-fhir:latest
```

### Push to Azure Container Registry

```bash
# Login
az acr login --name <your-acr-name>

# Tag
docker tag gooclaim-mock-fhir:latest \
  <your-acr-name>.azurecr.io/gooclaim-mock-fhir:latest

# Push
docker push <your-acr-name>.azurecr.io/gooclaim-mock-fhir:latest
```

## 🐛 Troubleshooting

### Container Won't Start

```bash
# Check logs
docker logs gooclaim-mock-fhir

# Check if port is available
netstat -an | grep 8080
```

### Fixtures Not Loading

```bash
# Verify fixtures are in image
docker exec gooclaim-mock-fhir ls -la /app/fhir-fixtures

# Check environment variable
docker exec gooclaim-mock-fhir env | grep FIXTURE_DIR
```

### Build Failures

```bash
# Build without cache
docker build --no-cache -t gooclaim-mock-fhir:latest .

# Check Dockerfile syntax
docker build --dry-run .
```

## 🔄 Updates

### Update Fixtures

If using volume mounts:
```bash
# Just update files, container auto-reloads (if watching)
cp new-patient.json fhir-fixtures/patient.json
```

If fixtures are baked in:
```bash
# Rebuild image
docker build -t gooclaim-mock-fhir:latest .
docker-compose up -d --build
```

### Update Application

```bash
# Rebuild image
docker build -t gooclaim-mock-fhir:latest .

# Restart container
docker-compose restart gooclaim-mock-fhir
# OR
docker restart gooclaim-mock-fhir
```

## 📊 Monitoring

### Container Stats

```bash
docker stats gooclaim-mock-fhir
```

### Logs

```bash
# Follow logs
docker-compose logs -f

# Last 100 lines
docker logs --tail 100 gooclaim-mock-fhir
```

## 🎯 Production Recommendations

1. **Use specific tags** instead of `latest`
2. **Set resource limits** in docker-compose.yml:
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '1'
         memory: 512M
   ```
3. **Enable health checks** (already included)
4. **Use read-only root filesystem** where possible
5. **Set up log aggregation**
6. **Use secrets management** for sensitive data
7. **Enable HTTPS** via reverse proxy (nginx/traefik)

## 📝 Example Production Setup

```bash
# Build for production
docker build -t gooclaim-mock-fhir:v1.0.0 .

# Tag for registry
docker tag gooclaim-mock-fhir:v1.0.0 \
  registry.example.com/gooclaim-mock-fhir:v1.0.0

# Push
docker push registry.example.com/gooclaim-mock-fhir:v1.0.0

# Deploy
docker-compose -f docker-compose.prod.yml up -d
```

---

For more information, see the main [README.md](./README.md).

