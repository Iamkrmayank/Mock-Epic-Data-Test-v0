/**
 * FHIR API routes
 */

import { Router, Request, Response } from 'express';
import { FixtureLoader } from './loader';
import { isBundle, wrapToBundle, emptyBundle, operationOutcome404 } from './fhir';

export function createRoutes(loader: FixtureLoader): Router {
  const router = Router();

  /**
   * Handle Binary/:id/$content pattern (must be before generic routes)
   */
  router.get('/Binary/:id/\\$content', (req: Request, res: Response) => {
    res.setHeader('Content-Type', 'application/octet-stream');
    res.status(200).send('PDF bytes placeholder');
  });

  /**
   * Generic route handler for single resource (GET /Resource/:id)
   * Must come before collection route
   */
  router.get('/:resourceType/:id', (req: Request, res: Response) => {
    const { resourceType, id } = req.params;

    const data = loader.getResource(resourceType, id);

    if (!data || isBundle(data)) {
      res.status(404).json(operationOutcome404(resourceType, id));
      return;
    }

    res.status(200).json(data);
  });

  /**
   * Generic route handler for collection endpoints (GET /Resource)
   */
  router.get('/:resourceType', (req: Request, res: Response) => {
    const { resourceType } = req.params;

    const data = loader.getResource(resourceType);
    
    if (!data) {
      res.status(200).json(emptyBundle());
      return;
    }

    if (isBundle(data)) {
      res.status(200).json(data);
    } else {
      // Single resource - wrap in bundle
      res.status(200).json(wrapToBundle(data));
    }
  });

  return router;
}

