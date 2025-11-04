/**
 * Express application setup
 */

import express, { Express, Request, Response } from 'express';
import cors from 'cors';
import morgan from 'morgan';
import rateLimit from 'express-rate-limit';
import swaggerUi from 'swagger-ui-express';
import { swaggerSpec } from './swagger';
import { createRoutes } from './routes';
import { FixtureLoader } from './loader';
import * as path from 'path';
import * as fs from 'fs';

export function createApp(): Express {
  const app = express();

  // Environment variables
  const PORT = process.env.PORT || 8080;
  const FIXTURE_DIR = process.env.FIXTURE_DIR || path.join(process.cwd(), 'fhir-fixtures');

  // Initialize fixture loader
  const loader = new FixtureLoader(FIXTURE_DIR);

  // Middleware
  app.use(cors());
  app.use(morgan('tiny'));

  // Serve static files if public directory exists
  const publicDir = path.join(process.cwd(), 'public');
  if (fs.existsSync(publicDir)) {
    app.use(express.static(publicDir));
  }
  
  // Rate limiting: 60 requests per minute
  const limiter = rateLimit({
    windowMs: 60 * 1000, // 1 minute
    max: 60,
    message: 'Too many requests from this IP, please try again later.',
  });
  app.use(limiter);

  // Body parser
  app.use(express.json());

  // Health check (before content-type middleware)
  app.get('/healthz', (req: Request, res: Response) => {
    res.setHeader('Content-Type', 'application/json');
    res.json({ ok: true });
  });

  // Swagger UI (before content-type middleware to avoid interference)
  app.use('/docs', swaggerUi.serve);
  app.get('/docs', swaggerUi.setup(swaggerSpec, {
    customCss: '.swagger-ui .topbar { display: none }',
    customSiteTitle: 'Gooclaim Mock FHIR API Docs',
    swaggerOptions: {
      persistAuthorization: true,
      displayRequestDuration: true,
      filter: true,
      showExtensions: true,
      showCommonExtensions: true,
    },
  }));

  // Swagger JSON endpoint
  app.get('/docs.json', (req: Request, res: Response) => {
    res.setHeader('Content-Type', 'application/json');
    res.json(swaggerSpec);
  });

  // FHIR content type middleware (skip for Binary/$content and docs)
  app.use((req: Request, res: Response, next) => {
    // Don't override Content-Type for Binary/$content or docs endpoints
    if (req.path.startsWith('/docs') || (req.path.includes('/Binary/') && req.path.includes('$content'))) {
      return next();
    }
    res.setHeader('Content-Type', 'application/fhir+json');
    next();
  });

  // FHIR API routes
  app.use('/', createRoutes(loader));

  // Root endpoint
  app.get('/', (req: Request, res: Response) => {
    res.setHeader('Content-Type', 'application/json');
    res.json({
      service: 'Gooclaim Mock FHIR API',
      version: '1.0.0',
      mode: process.env.EHR_MODE || 'mock',
      docs: '/docs',
      health: '/healthz',
      endpoints: {
        collection: 'GET /{resourceType}',
        single: 'GET /{resourceType}/{id}',
        binary: 'GET /Binary/{id}/$content',
      },
    });
  });

  return app;
}

