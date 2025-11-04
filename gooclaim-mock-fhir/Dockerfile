# Gooclaim Mock FHIR API - Dockerfile
# Multi-stage build for optimized production image

# Stage 1: Build
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package.json package-lock.json* pnpm-lock.yaml* ./

# Install pnpm if using pnpm (optional, can use npm instead)
RUN npm install -g pnpm@latest || true

# Install dependencies (including dev dependencies for build)
RUN if [ -f "pnpm-lock.yaml" ]; then \
      pnpm install --frozen-lockfile; \
    else \
      npm ci --ignore-scripts; \
    fi

# Copy source files
COPY tsconfig.json ./
COPY src ./src

# Build TypeScript
RUN npm run build || (npm install typescript -g && tsc)

# Stage 2: Production
FROM node:20-alpine

WORKDIR /app

# Create non-root user for security
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# Copy package files
COPY package.json package-lock.json* pnpm-lock.yaml* ./

# Install only production dependencies
RUN if [ -f "pnpm-lock.yaml" ]; then \
      npm install -g pnpm@latest && \
      pnpm install --prod --frozen-lockfile; \
    else \
      npm ci --only=production --ignore-scripts; \
    fi

# Copy built files from builder stage
COPY --from=builder /app/dist ./dist

# Copy fixture files
COPY fhir-fixtures ./fhir-fixtures

# Copy static files (if public directory exists)
COPY public ./public

# Create .env file with defaults (can be overridden)
RUN echo "PORT=8080" > .env && \
    echo "FIXTURE_DIR=./fhir-fixtures" >> .env && \
    echo "EHR_MODE=mock" >> .env

# Change ownership to nodejs user
RUN chown -R nodejs:nodejs /app

# Switch to non-root user
USER nodejs

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:8080/healthz', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"

# Start the application
CMD ["node", "dist/index.js"]

