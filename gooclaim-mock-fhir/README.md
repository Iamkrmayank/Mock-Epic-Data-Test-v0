# Gooclaim Mock FHIR API

A powerful, production-ready mock FHIR API server using Epic-style fixtures. Perfect for local development, testing, and demos without needing to connect to Epic FHIR.

![Node.js](https://img.shields.io/badge/Node.js-20+-green)
![TypeScript](https://img.shields.io/badge/TypeScript-5.3+-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🎯 Features

- ✅ **Complete FHIR R4 Support** - All major resource types
- ✅ **Epic-Style Fixtures** - Uses your existing JSON fixture files
- ✅ **Auto-Detection** - Smart Bundle vs Single Resource detection
- ✅ **Typo Tolerance** - Handles filename variations automatically
- ✅ **Swagger UI** - Interactive API documentation at `/docs`
- ✅ **Beautiful Landing Page** - Professional home page at `/`
- ✅ **Rate Limiting** - Built-in protection (60 req/min)
- ✅ **CORS Enabled** - Ready for frontend integration
- ✅ **Health Checks** - `/healthz` endpoint for monitoring

## 🚀 Quick Start

### Prerequisites

- **Node.js** 20+ (check with `node --version`)
- **pnpm** (or npm/yarn) - Package manager

### Installation

```bash
# Clone or navigate to the project
cd gooclaim-mock-fhir

# Install dependencies
pnpm install

# Copy environment variables (optional)
cp .env.example .env
```

### Running the Server

```bash
# Development mode (with hot reload)
pnpm dev

# Production build
pnpm build
pnpm start
```

The server will start on `http://localhost:8080` (or port specified in `.env`)

## 📁 Project Structure

```
gooclaim-mock-fhir/
├── src/
│   ├── index.ts          # Server entry point
│   ├── app.ts            # Express app setup & middleware
│   ├── routes.ts         # FHIR API route handlers
│   ├── loader.ts         # Fixture file loader with typo handling
│   ├── fhir.ts           # FHIR helper functions
│   └── swagger.ts        # Swagger/OpenAPI configuration
├── fhir-fixtures/        # JSON fixture files (your data)
│   ├── patient.json
│   ├── appointments.json
│   ├── coverage.json
│   └── ... (all other resources)
├── public/               # Static files (optional)
│   └── index.html        # Landing page
├── dist/                 # Compiled JavaScript (after build)
├── package.json
├── tsconfig.json
├── .env.example
└── README.md
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file (or use `.env.example`):

```env
PORT=8080                    # Server port (default: 8080)
FIXTURE_DIR=./fhir-fixtures  # Directory with JSON fixtures
EHR_MODE=mock                # Mode indicator
```

### Fixture Files

Place your JSON fixture files in the `fhir-fixtures/` directory:

- `patient.json`
- `appointments.json`
- `coverage.json`
- `encounterr.json` (typo handled automatically)
- `conditionss.json` (typo handled automatically)
- `organisation.json` (typo handled automatically)
- ... and all other resource files

The loader automatically maps resource types to filenames, handling common typos.

## 📡 API Endpoints

### Resource Endpoints

All FHIR resources follow these patterns:

#### Collection Search
```
GET /{ResourceType}
GET /{ResourceType}?_count=25
GET /{ResourceType}?patient={id}
```
Returns a FHIR Bundle (searchset) with all matching resources.

#### Single Resource
```
GET /{ResourceType}/{id}
```
Returns a single FHIR resource or 404 OperationOutcome.

#### Binary Content
```
GET /Binary/{id}/$content
```
Returns raw binary content (currently returns "PDF bytes placeholder").

### Supported Resources

| Resource Type | Collection | Single | Special |
|--------------|-----------|--------|---------|
| **Patient** | ✅ | ✅ | - |
| **Coverage** | ✅ | ✅ | - |
| **Encounter** | ✅ | ✅ | - |
| **Appointment** | ✅ | ✅ | - |
| **Contract** | ✅ | ✅ | - |
| **Consent** | ✅ | ✅ | - |
| **DocumentReference** | ✅ | ✅ | - |
| **Observation** | ✅ | ✅ | - |
| **Procedure** | ✅ | ✅ | - |
| **Condition** | ✅ | ✅ | - |
| **Organization** | ✅ | ✅ | - |
| **Practitioner** | ✅ | ✅ | - |
| **PractitionerRole** | ✅ | ✅ | - |
| **ExplanationOfBenefit** | ✅ | ✅ | - |
| **Binary** | ✅ | ✅ | `/$content` endpoint |
| **Provenance** | ✅ | ✅ | - |

### System Endpoints

| Endpoint | Description | Response |
|----------|-------------|----------|
| `GET /` | Landing page with API info | HTML/JSON |
| `GET /healthz` | Health check | `{ok: true}` |
| `GET /docs` | Swagger UI documentation | HTML |
| `GET /docs.json` | OpenAPI specification | JSON |

## 📝 Usage Examples

### Using cURL

```bash
# Health check
curl http://localhost:8080/healthz

# Get all patients (Bundle)
curl http://localhost:8080/Patient

# Get specific patient by ID
curl http://localhost:8080/Patient/eYg3-1aJmCMq-umIIq2Njxw3

# Search appointments
curl "http://localhost:8080/Appointment?_count=25"

# Get DocumentReference with query params
curl "http://localhost:8080/DocumentReference?patient=123&_count=25"

# Get binary content
curl http://localhost:8080/Binary/f859KKT5DsrSxpFu8cSdkasOF3QBkgahtf5cQ5PV2ZcM4/\$content

# Get Coverage
curl http://localhost:8080/Coverage

# Get Observation
curl http://localhost:8080/Observation
```

### Using JavaScript/Fetch

```javascript
// Get Patient collection
const response = await fetch('http://localhost:8080/Patient');
const bundle = await response.json();
console.log(bundle);

// Get single Patient
const patient = await fetch('http://localhost:8080/Patient/eYg3-1aJmCMq-umIIq2Njxw3')
  .then(res => res.json());

// Search with query params
const appointments = await fetch(
  'http://localhost:8080/Appointment?patient=123&_count=10'
).then(res => res.json());
```

### Using PowerShell

```powershell
# Health check
Invoke-RestMethod -Uri "http://localhost:8080/healthz"

# Get Patient
Invoke-RestMethod -Uri "http://localhost:8080/Patient"

# Get Patient by ID
Invoke-RestMethod -Uri "http://localhost:8080/Patient/eYg3-1aJmCMq-umIIq2Njxw3"
```

## 🎯 How It Works

### 1. Fixture Loading

The server loads JSON files from `fhir-fixtures/` directory and caches them in memory for performance.

### 2. Smart Detection

The loader automatically detects different JSON structures:

- **Direct FHIR Resource**: `{"resourceType": "Patient", "id": "...", ...}`
- **Bundle**: `{"resourceType": "Bundle", "type": "searchset", "entry": [...]}`
- **Wrapped in "data"**: `{"resourceType": "Patient", "data": {...}}`
- **Special structures**: `{"appointments": [...]}` (for appointments.json)

### 3. Response Mapping

- **Collection endpoint** (`GET /Resource`) → Always returns a Bundle
  - If fixture is a Bundle → Returns as-is
  - If fixture is a single resource → Wraps in Bundle
  - If no fixture found → Returns empty Bundle

- **Single resource endpoint** (`GET /Resource/:id`) → Returns resource or 404
  - Finds resource by ID in fixture
  - Returns 404 OperationOutcome if not found

### 4. Typo Tolerance

The loader handles common filename typos:

| Expected | Actual (Handled) |
|----------|------------------|
| `encounter.json` | `encounterr.json` ✅ |
| `condition.json` | `conditionss.json` ✅ |
| `organization.json` | `organisation.json` ✅ |
| `practitionerRole.json` | `practitonerrole.json` ✅ |

## 🔒 Security & Middleware

- **CORS**: Enabled for all origins (development-friendly)
- **Rate Limiting**: 60 requests per minute per IP address
- **Logging**: Morgan HTTP logger (tiny format)
- **Content-Type**: Automatically set to `application/fhir+json`
- **Error Handling**: Proper HTTP status codes and OperationOutcome responses

## 📚 API Documentation

### Swagger UI

Visit **`http://localhost:8080/docs`** for interactive API documentation with:
- All endpoints listed
- Try-it-out functionality
- Request/response schemas
- Authentication (if needed)

### Landing Page

Visit **`http://localhost:8080/`** for a beautiful landing page with:
- API overview
- Quick links to documentation
- Example endpoints
- Resource list

## 🧪 Testing

### Test All Endpoints

```bash
# Health check
curl http://localhost:8080/healthz

# Test each resource type
curl http://localhost:8080/Patient
curl http://localhost:8080/Coverage
curl http://localhost:8080/Encounter
curl http://localhost:8080/Appointment
curl http://localhost:8080/Observation
curl http://localhost:8080/Procedure
curl http://localhost:8080/Condition
curl http://localhost:8080/Organization
curl http://localhost:8080/Practitioner
curl http://localhost:8080/ExplanationOfBenefit

# Test single resource
curl http://localhost:8080/Patient/eYg3-1aJmCMq-umIIq2Njxw3
```

### Expected Responses

**Collection Endpoint** (`GET /Patient`):
```json
{
  "resourceType": "Bundle",
  "type": "searchset",
  "total": 1,
  "entry": [
    {
      "resource": {
        "resourceType": "Patient",
        "id": "...",
        ...
      }
    }
  ]
}
```

**Single Resource** (`GET /Patient/{id}`):
```json
{
  "resourceType": "Patient",
  "id": "eYg3-1aJmCMq-umIIq2Njxw3",
  ...
}
```

**404 Not Found**:
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Patient with id 'invalid-id' not found"
      }
    }
  ]
}
```

## 🐛 Troubleshooting

### Server Won't Start

**Problem**: Port already in use
```bash
Error: listen EADDRINUSE: address already in use :::8080
```

**Solution**: Change port in `.env`:
```env
PORT=8081
```

### Fixture Files Not Found

**Problem**: 404 errors or empty Bundles

**Solutions**:
1. Check files exist in `fhir-fixtures/` directory
2. Verify `FIXTURE_DIR` in `.env` matches your directory
3. Check filename mapping in `src/loader.ts` (RESOURCE_MAP)
4. Ensure JSON files are valid JSON

### Wrong Resource Returned

**Problem**: Getting wrong resource or 404 for valid ID

**Solutions**:
1. Check JSON structure matches expected format
2. Verify resource `id` field matches what you're requesting
3. For wrapped data, ensure structure is: `{"resourceType": "...", "data": {...}}`
4. Check console logs for loading errors

### Swagger UI Not Loading

**Problem**: Blank page or errors in Swagger UI

**Solutions**:
1. Check browser console for errors
2. Verify `/docs.json` endpoint returns valid OpenAPI spec
3. Clear browser cache
4. Try accessing directly: `http://localhost:8080/docs.json`

### Rate Limiting Issues

**Problem**: Getting "Too many requests" error

**Solution**: Rate limit is 60 requests/minute. Wait a minute or adjust in `src/app.ts`:
```typescript
const limiter = rateLimit({
  windowMs: 60 * 1000,
  max: 100, // Increase limit
});
```

## 🔄 Development Workflow

### Making Changes

1. **Edit source files** in `src/`
2. **Server auto-reloads** (if using `pnpm dev`)
3. **Test endpoints** using curl or Swagger UI
4. **Build for production**: `pnpm build`

### Adding New Resources

1. Add JSON fixture file to `fhir-fixtures/`
2. Update `RESOURCE_MAP` in `src/loader.ts`:
```typescript
const RESOURCE_MAP = {
  // ... existing
  NewResource: ["newresource.json"],
};
```

### Updating Fixtures

Simply update JSON files in `fhir-fixtures/` and restart server (or let auto-reload handle it).

## 📦 Production Deployment

### Docker (Recommended)

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY dist ./dist
COPY fhir-fixtures ./fhir-fixtures
EXPOSE 8080
CMD ["node", "dist/index.js"]
```

### Environment Variables

Set in your deployment platform:
- `PORT` - Server port
- `FIXTURE_DIR` - Path to fixtures (if different)
- `EHR_MODE` - Mode identifier

### Health Check

Use `/healthz` endpoint for:
- Kubernetes liveness/readiness probes
- Load balancer health checks
- Monitoring systems

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - feel free to use in your projects!

## 🙏 Acknowledgments

- Built with [Express.js](https://expressjs.com/)
- API documentation powered by [Swagger UI](https://swagger.io/tools/swagger-ui/)
- Follows [FHIR R4](https://www.hl7.org/fhir/R4/) specification
- Inspired by Epic FHIR API patterns

---

**Need Help?** Check the Swagger docs at `/docs` or open an issue!

**Happy Coding! 🚀**
