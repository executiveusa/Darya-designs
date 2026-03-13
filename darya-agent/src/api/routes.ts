/**
 * Darya Design Wizard - API Routes
 * Main backend endpoints for design analysis, generation, trends, and analytics
 */

import { Router, Request, Response } from 'express';
import { Logger } from '../utils/logger.js';
import { DesignAnalyzer } from '../services/Design.js';
import { TrendsService } from '../services/Trends.js';
import { AnimationsService } from '../services/Animations.js';
import { SuperDesignBridge } from '../services/SuperDesignBridge.js';
import { DatabaseService } from '../database/models.js';
import winston from 'winston';

const router = Router();
const logger = new Logger('APIRoutes');

// Initialize services
const winstonLogger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
});

const designAnalyzer = new DesignAnalyzer(winstonLogger);
const trendsService = new TrendsService(winstonLogger);
const animationsService = new AnimationsService(winstonLogger);
const superDesignBridge = new SuperDesignBridge(winstonLogger);
const dbService = new DatabaseService();

/**
 * POST /api/design/analyze
 * Analyze a design brief and return comprehensive strategy
 */
router.post('/design/analyze', async (req: Request, res: Response) => {
  try {
    const { projectName, brief, targetAudience, brandGuide, constraints } = req.body;

    logger.info(`Analyzing design brief: ${projectName}`);

    const strategy = await designAnalyzer.analyzeBrief({
      projectName,
      brief,
      targetAudience,
      brandGuide,
      constraints,
    });

    res.json({
      success: true,
      data: strategy,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    logger.error(`Design analysis error: ${error}`);
    res.status(500).json({
      success: false,
      error: String(error),
      timestamp: new Date().toISOString(),
    });
  }
});

/**
 * POST /api/design/generate
 * Generate UI components from design specifications
 */
router.post('/design/generate', async (req: Request, res: Response) => {
  try {
    const { projectName, description, colorPalette, typography, componentTypes } = req.body;

    logger.info(`Generating design: ${projectName}`);

    const design = await superDesignBridge.generateUIDesign({
      projectName,
      description,
      colorPalette,
      typography,
      componentTypes,
    });

    res.json({
      success: true,
      data: design,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    logger.error(`Design generation error: ${error}`);
    res.status(500).json({
      success: false,
      error: String(error),
      timestamp: new Date().toISOString(),
    });
  }
});

/**
 * GET /api/trends/trending
 * Get trending design topics and insights
 */
router.get('/trends/trending', async (req: Request, res: Response) => {
  try {
    const regionCode = (req.query.region as string) || 'US';
    const category = (req.query.category as string) || 'all';

    logger.info(`Fetching trending topics for region: ${regionCode}`);

    const topics = await trendsService.getTrendingTopics(regionCode, category);

    res.json({
      success: true,
      data: topics,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    logger.error(`Trends error: ${error}`);
    res.status(500).json({
      success: false,
      error: String(error),
      timestamp: new Date().toISOString(),
    });
  }
});

/**
 * GET /api/trends/colors
 * Get trending color palettes
 */
router.get('/trends/colors', async (req: Request, res: Response) => {
  try {
    logger.info('Fetching trending colors');

    const colors = await trendsService.getTrendingColors();

    res.json({
      success: true,
      data: colors,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    logger.error(`Trending colors error: ${error}`);
    res.status(500).json({
      success: false,
      error: String(error),
      timestamp: new Date().toISOString(),
    });
  }
});

/**
 * GET /api/trends/typography
 * Get trending typography styles
 */
router.get('/trends/typography', async (req: Request, res: Response) => {
  try {
    logger.info('Fetching trending typography');

    const typography = await trendsService.getTrendingTypography();

    res.json({
      success: true,
      data: typography,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    logger.error(`Trending typography error: ${error}`);
    res.status(500).json({
      success: false,
      error: String(error),
      timestamp: new Date().toISOString(),
    });
  }
});

/**
 * POST /api/trends/analyze
 * Analyze a topic for viral potential
 */
router.post('/trends/analyze', async (req: Request, res: Response) => {
  try {
    const { topic } = req.body;

    logger.info(`Analyzing viral potential for: ${topic}`);

    const analysis = await trendsService.analyzeViralPotential(topic);

    res.json({
      success: true,
      data: analysis,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    logger.error(`Viral analysis error: ${error}`);
    res.status(500).json({
      success: false,
      error: String(error),
      timestamp: new Date().toISOString(),
    });
  }
});

/**
 * POST /api/animations/generate
 * Generate animation configurations
 */
router.post('/animations/generate', async (req: Request, res: Response) => {
  try {
    const { elementType, duration, intensity, useVR } = req.body;

    logger.info(`Generating animation for element: ${elementType}`);

    const animation = animationsService.generateAnimation({
      elementType,
      duration,
      intensity,
      useVR,
    });

    res.json({
      success: true,
      data: animation,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    logger.error(`Animation generation error: ${error}`);
    res.status(500).json({
      success: false,
      error: String(error),
      timestamp: new Date().toISOString(),
    });
  }
});

/**
 * POST /api/animations/optimize
 * Optimize animation for performance
 */
router.post('/animations/optimize', async (req: Request, res: Response) => {
  try {
    const { animation } = req.body;

    logger.info(`Optimizing animation: ${animation.id}`);

    const optimized = animationsService.optimizeForPerformance(animation);

    res.json({
      success: true,
      data: optimized,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    logger.error(`Animation optimization error: ${error}`);
    res.status(500).json({
      success: false,
      error: String(error),
      timestamp: new Date().toISOString(),
    });
  }
});

/**
 * POST /api/projects/create
 * Create a new design project
 */
router.post('/projects/create', async (req: Request, res: Response) => {
  try {
    const { userId, name, description, brief, targetAudience, estimatedHours, tags } = req.body;

    logger.info(`Creating design project: ${name}`);

    const project = await dbService.createDesignProject({
      userId,
      name,
      description,
      brief,
      targetAudience,
      status: 'draft',
      colorPalette: [],
      typography: {},
      componentCount: 0,
      estimatedHours,
      tags,
    });

    res.json({
      success: true,
      data: project,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    logger.error(`Project creation error: ${error}`);
    res.status(500).json({
      success: false,
      error: String(error),
      timestamp: new Date().toISOString(),
    });
  }
});

/**
 * GET /api/projects/list
 * List user's design projects
 */
router.get('/projects/list', async (req: Request, res: Response) => {
  try {
    const userId = req.query.userId as string;

    if (!userId) {
      return res.status(400).json({
        success: false,
        error: 'userId is required',
        timestamp: new Date().toISOString(),
      });
    }

    logger.info(`Listing projects for user: ${userId}`);

    const projects = await dbService.listDesignProjects(userId);

    res.json({
      success: true,
      data: projects,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    logger.error(`Projects list error: ${error}`);
    res.status(500).json({
      success: false,
      error: String(error),
      timestamp: new Date().toISOString(),
    });
  }
});

/**
 * GET /api/dashboard/metrics
 * Get analytics and dashboard metrics
 */
router.get('/dashboard/metrics', async (req: Request, res: Response) => {
  try {
    const userId = req.query.userId as string;

    if (!userId) {
      return res.status(400).json({
        success: false,
        error: 'userId is required',
        timestamp: new Date().toISOString(),
      });
    }

    logger.info(`Fetching metrics for user: ${userId}`);

    const metrics = await dbService.getAnalyticsMetrics(userId);

    res.json({
      success: true,
      data: metrics,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    logger.error(`Metrics error: ${error}`);
    res.status(500).json({
      success: false,
      error: String(error),
      timestamp: new Date().toISOString(),
    });
  }
});

/**
 * POST /api/components/generate
 * Generate specific component types
 */
router.post('/components/generate', async (req: Request, res: Response) => {
  try {
    const { types, config } = req.body;

    logger.info(`Generating components: ${types.join(', ')}`);

    const components = await superDesignBridge.generateComponents(types, config);

    res.json({
      success: true,
      data: components,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    logger.error(`Component generation error: ${error}`);
    res.status(500).json({
      success: false,
      error: String(error),
      timestamp: new Date().toISOString(),
    });
  }
});

/**
 * POST /api/design/iterate
 * Iterate on a design with feedback
 */
router.post('/design/iterate', async (req: Request, res: Response) => {
  try {
    const { designId, changes } = req.body;

    logger.info(`Iterating on design: ${designId}`);

    const result = await superDesignBridge.iterateDesign(designId, changes);

    res.json({
      success: true,
      data: result,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    logger.error(`Design iteration error: ${error}`);
    res.status(500).json({
      success: false,
      error: String(error),
      timestamp: new Date().toISOString(),
    });
  }
});

/**
 * POST /api/design/export
 * Export design to code
 */
router.post('/design/export', async (req: Request, res: Response) => {
  try {
    const { design, format } = req.body;

    logger.info(`Exporting design to ${format}`);

    const exported = await superDesignBridge.exportToCode(design, format);

    res.json({
      success: true,
      data: exported,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    logger.error(`Design export error: ${error}`);
    res.status(500).json({
      success: false,
      error: String(error),
      timestamp: new Date().toISOString(),
    });
  }
});

export { router as apiRoutes };
