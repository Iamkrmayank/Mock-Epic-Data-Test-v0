/**
 * Server entry point
 */

import * as dotenv from 'dotenv';
import { createApp } from './app';

// Load environment variables
dotenv.config();

const PORT = process.env.PORT || 8080;

const app = createApp();

app.listen(PORT, () => {
  console.log(`🚀 Gooclaim Mock FHIR API server running on port ${PORT}`);
  console.log(`📚 Swagger UI available at http://localhost:${PORT}/docs`);
  console.log(`❤️  Health check at http://localhost:${PORT}/healthz`);
  console.log(`📁 Fixture directory: ${process.env.FIXTURE_DIR || './fhir-fixtures'}`);
});

