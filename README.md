# Epic FHIR API Integration with FastAPI

A comprehensive FastAPI application that implements OAuth2 JWT client assertion flow for Epic FHIR API integration, supporting both Sandbox and Production environments.

## 🚀 Features

- **OAuth2 JWT Client Assertion**: Implements Epic's required authentication flow using RS256-signed JWTs
- **Dual Environment Support**: Seamlessly switch between Sandbox and Production Epic environments
- **FHIR R4 API Integration**: Access Patient and Observation resources via Epic FHIR APIs
- **Interactive Web Interface**: Clean HTML/JavaScript frontend for testing API endpoints
- **JWKS Generation**: Automatic JWKS (JSON Web Key Set) generation for Epic app registration
- **Comprehensive Configuration**: Environment-based configuration with .env support

## 📋 Requirements

- Python 3.12+
- Epic FHIR Developer Account
- RSA 2048-bit Private Key
- Registered Epic Application with Backend Service access

## 🛠️ Installation

1. **Clone and Setup**:
   ```bash
   cd c:\Users\AMANPREET\python_projects\epic-fhir
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Generate Private Key**:
   ```bash
   python generate_key.py
   ```

3. **Configure Environment**:
   ```bash
   copy .env.example .env
   # Edit .env with your Epic client credentials
   ```

4. **Configure .env file**:
   ```env
   EPIC_CLIENT_ID=your-epic-client-id-here
   PRIVATE_KEY_PATH=keys/private.key
   EPIC_ENV=sandbox
   PRODUCTION_FHIR_BASE_URL=https://your-epic-prod-url.com/api/FHIR/R4/
   PRODUCTION_TOKEN_URL=https://your-epic-prod-url.com/oauth2/token
   JWT_EXPIRY_MINUTES=5
   ```

## 🔧 Epic Application Registration

1. **Register Your App** at [Epic's Developer Portal](https://fhir.epic.com/Developer)
2. **Application Type**: Backend Service
3. **FHIR Version**: R4
4. **Grant Type**: Client Credentials
5. **Authentication Method**: Private Key JWT (client_assertion)
6. **Get JWKS**: Visit `http://localhost:8000/jwks` after starting the app
7. **Provide JWKS** during Epic registration

## 🏃‍♂️ Running the Application

```bash
# Development server with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production server
uvicorn main:app --host 0.0.0.0 --port 8000
```

Visit: `http://localhost:8000`

## 📚 API Endpoints

### Authentication
- `POST /auth/token` - Exchange JWT assertion for Epic access token
- `GET /jwks` - Get JWKS for Epic registration

### FHIR Resources
- `GET /fhir/patient/{id}` - Retrieve patient data by ID
- `GET /fhir/observation/{patient_id}` - Get observations for a patient
- `GET /fhir/patient/search` - Search patients by family/given name
- `GET /fhir/patient/search/common-names` - Find patients with common names
- `GET /fhir/patient/epic-test-patients` - Get Epic's known test patients
- `GET /fhir/patients/browse` - Browse available patients in sandbox

### System
- `GET /health` - Health check and environment info
- `GET /config/info` - Current configuration details
- `GET /` - Interactive web interface

## 🔐 Authentication Flow

The application implements Epic's OAuth2 client assertion flow:

1. **JWT Generation**: Creates a signed JWT with required claims:
   ```json
   {
     "iss": "your-client-id",
     "sub": "your-client-id", 
     "aud": "https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token",
     "exp": 1234567890,
     "jti": "unique-jwt-id",
     "iat": 1234567885
   }
   ```

2. **Token Exchange**: Sends JWT to Epic's token endpoint:
   ```http
   POST /oauth2/token
   Content-Type: application/x-www-form-urlencoded
   
   grant_type=client_credentials&
   client_assertion_type=urn:ietf:params:oauth:client-assertion-type:jwt-bearer&
   client_assertion=<signed-jwt>&
   scope=system/Patient.read system/Observation.read
   ```

3. **API Access**: Uses received access token for FHIR API calls

## 🌍 Environment Configuration

### Sandbox Environment (Default)
- **Token URL**: `https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token`
- **FHIR Base URL**: `https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/`
- **Working Test Patient IDs**: 
  - `eYg3-1aJmCMq-umIIq2Njxw3` (Abby Anesthesia)
  - `Tbt3KuCY0B5PSrJvCu2j-PlK.aiHsu2xUjUM8bWpetXoB`
  - `TUKRxL29bxE9lyAcdTIyrWC6Ln5gZ-z7CLr2r-2SY964B`

### Production Environment
- Configure via environment variables
- Set `EPIC_ENV=production` in `.env`
- Provide your production URLs

## 📖 Epic FHIR Scopes & Endpoints

### Patient Resources
**Scope**: `system/Patient.read`
```bash
# Get patient by ID
http://localhost:8000/fhir/patient/eYg3-1aJmCMq-umIIq2Njxw3

# Search patients
http://localhost:8000/fhir/patient/search?family=Anesthesia&given=Abby

# Get comprehensive patient data
http://localhost:8000/fhir/patient/eYg3-1aJmCMq-umIIq2Njxw3/comprehensive
```

### Observations (Vital Signs & Labs)
**Scope**: `system/Observation.read`  
**⚠️ Required**: Must include `category` or `code` parameter
```bash
# Get vital signs
http://localhost:8000/fhir/observation/eYg3-1aJmCMq-umIIq2Njxw3?category=vital-signs&_count=20

# Get lab results
http://localhost:8000/fhir/observation/eYg3-1aJmCMq-umIIq2Njxw3?category=laboratory&_count=20

# Get specific observation (e.g., blood pressure)
http://localhost:8000/fhir/observation/eYg3-1aJmCMq-umIIq2Njxw3?code=8480-6
```

### Conditions & Diagnoses
**Scope**: `system/Condition.read`
```bash
http://localhost:8000/fhir/conditions/eYg3-1aJmCMq-umIIq2Njxw3?clinical-status=active
```

### Encounters & Visits
**Scope**: `system/Encounter.read`
```bash
http://localhost:8000/fhir/encounters/eYg3-1aJmCMq-umIIq2Njxw3?_count=20
```


### Procedures
**Scope**: `system/Procedure.read`
```bash
http://localhost:8000/fhir/procedures/eYg3-1aJmCMq-umIIq2Njxw3?_count=20
```


### Documents
**Scope**: `system/DocumentReference.read`
```bash
http://localhost:8000/fhir/documents/eYg3-1aJmCMq-umIIq2Njxw3
```

### Appointments
**Scope**: `system/Appointment.read`
```bash
# Get appointments
http://localhost:8000/fhir/appointments/eYg3-1aJmCMq-umIIq2Njxw3?date=ge2024-01-01

# Search appointments
http://localhost:8000/fhir/appointments/search?patient=eYg3-1aJmCMq-umIIq2Njxw3&status=booked
```

### Coverage & Benefits
**Scope**: `system/Coverage.read`
```bash
# Get insurance coverage
http://localhost:8000/fhir/coverage/eYg3-1aJmCMq-umIIq2Njxw3

# Search coverage
http://localhost:8000/fhir/coverage/search?beneficiary=eYg3-1aJmCMq-umIIq2Njxw3
```

**Scope**: `system/ExplanationOfBenefit.read`
```bash
http://localhost:8000/fhir/ExplanationOfBenefit/eYg3-1aJmCMq-umIIq2Njxw3
```

### Care Plans
**Scope**: `system/CarePlan.read`
```bash
http://localhost:8000/fhir/CarePlan/eYg3-1aJmCMq-umIIq2Njxw3?status=active
```

### Provider Resources
**Scope**: `system/Organization.read`
```bash
http://localhost:8000/fhir/organizations/enRnEOTlPO134WKjGk5PnDA3
```

**Scope**: `system/Practitioner.read`
```bash
http://localhost:8000/fhir/practitioner/T3Mz3KLBDVXXgaRoQd7EbUw3
```

**Scope**: `system/PractitionerRole.read`
```bash
http://localhost:8000/fhir/PractitionerRole/T3Mz3KLBDVXXgaRoQd7EbUw3
```

### Questionnaires & Forms
**Scope**: `system/Questionnaire.read`
```bash
http://localhost:8000/fhir/questionnaires/{questionnaire_id}
```

**Scope**: `system/QuestionnaireResponse.read`
```bash
http://localhost:8000/fhir/QuestionnaireResponse/eYg3-1aJmCMq-umIIq2Njxw3
```

### Administrative Resources
**Scope**: `system/List.read`
```bash
http://localhost:8000/fhir/lists/eYg3-1aJmCMq-umIIq2Njxw3
```

**Scope**: `system/Consent.read`
```bash
http://localhost:8000/fhir/consents/eYg3-1aJmCMq-umIIq2Njxw3
```

**Scope**: `system/Provenance.read`
```bash
http://localhost:8000/fhir/provenance/{resource_id}
```

**Scope**: `system/DeviceUseStatement.read`
```bash
http://localhost:8000/fhir/DeviceUseStatement/eYg3-1aJmCMq-umIIq2Njxw3
```

## 🔍 Example Usage

### 1. Get Access Token
```bash
curl -X POST "http://localhost:8000/auth/token"
```

### 2. Find Working Test Patients
```bash
curl "http://localhost:8000/fhir/patient/epic-test-patients"
```

### 3. Retrieve Patient Data (Using Working Patient ID)
```bash
curl "http://localhost:8000/fhir/patient/eYg3-1aJmCMq-umIIq2Njxw3"
```

### 4. Search Patients by Name
```bash
curl "http://localhost:8000/fhir/patient/search?family=Anesthesia&limit=5"
```

### 5. Get Patient Observations (⚠️ Category Required!)
```bash
# Vital signs
curl "http://localhost:8000/fhir/observation/eYg3-1aJmCMq-umIIq2Njxw3?category=vital-signs&_count=20"

# Lab results  
curl "http://localhost:8000/fhir/observation/eYg3-1aJmCMq-umIIq2Njxw3?category=laboratory&_count=20"
```

### 6. Browse Available Patients
```bash
curl "http://localhost:8000/fhir/patients/browse"
```

## 🏗️ Project Structure

```
epic-fhir/
├── main.py                 # FastAPI application
├── config.py              # Configuration management
├── jwt_auth.py            # JWT authentication module
├── generate_key.py        # Private key generation utility
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
├── README.md             # This documentation
├── templates/
│   └── index.html        # Web interface
├── keys/
│   ├── private.key       # Your RSA private key (generated)
│   └── private.key.example # Example key format
└── jwks_template.json    # JWKS template for registration
```

## 🔒 Security Considerations

- **Private Key Security**: Never commit private keys to version control
- **Token Storage**: In production, use Redis/database instead of in-memory storage
- **Key Rotation**: Regularly rotate your RSA keys
- **Environment Variables**: Use secure secret management in production
- **HTTPS**: Always use HTTPS in production environments
- **Error Handling**: Implement proper error logging and monitoring

## 🚨 Troubleshooting

### Common Issues

1. **"Private key file not found"**
   - Run `python generate_key.py` to create a key
   - Verify `PRIVATE_KEY_PATH` in `.env`

2. **"Token request failed"**
   - Check your `EPIC_CLIENT_ID` in `.env`
   - Verify your app is registered with Epic
   - Ensure JWKS is properly configured in Epic

3. **"Access token expired"**
   - Call `/auth/token` to refresh
   - Check JWT expiry settings

4. **"The FHIR ID provided was not found"**
   - Patient IDs in Epic sandbox change frequently
   - Use `/fhir/patient/epic-test-patients` to find current working IDs
   - Try `/fhir/patients/browse` to discover available patients
   - Use patient search by name instead of hardcoded IDs

5. **FHIR API errors**
   - Verify your Epic app has required scopes
   - Check patient ID format
   - Ensure production URLs are correct

### Development Tips

- Use Epic's Sandbox environment for testing
- Monitor the web interface for real-time API responses
- Check `/health` endpoint for configuration verification
- Use `/config/info` to debug environment settings

## 📝 Epic FHIR Documentation

- [Epic FHIR Documentation](https://fhir.epic.com/)
- [OAuth2 Implementation Guide](https://fhir.epic.com/Documentation?docId=oauth2)
- [FHIR R4 Specification](https://www.hl7.org/fhir/R4/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is provided as-is for educational and development purposes. Please ensure compliance with Epic's terms of service and applicable healthcare regulations when using in production.

---

**⚠️ Important Security Notice**: This application handles sensitive healthcare data. Ensure proper security measures, compliance with HIPAA and other regulations, and Epic's terms of service when deploying to production environments.