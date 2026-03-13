/**
 * DARYA Design Wizard - Express Server
 * Main backend API for Kupuri Agency's AI Design System
 */

import express, { Express, Request, Response } from "express";
import cors from "cors";
import dotenv from "dotenv";
import { createServer } from "http";
import { Server as SocketIOServer } from "socket.io";
import { Logger } from "./utils/logger.js";
import { DaryaAgent } from "./agent/DaryaAgent.js";

// Load environment variables
dotenv.config();

const app: Express = express();
const logger = new Logger("DaryaServer");
const daryaAgent = new DaryaAgent();

// ===== MIDDLEWARE =====

app.use(
  cors({
    origin: (process.env.ALLOWED_ORIGINS || "http://localhost:3000").split(
      ","
    ),
    credentials: true,
  })
);

app.use(express.json({ limit: "50mb" }));
app.use(express.urlencoded({ limit: "50mb", extended: true }));

// ===== HEALTH CHECK =====

app.get("/healthz", (req: Request, res: Response) => {
  res.json({
    status: "healthy",
    service: "darya-design-wizard",
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
  });
});

// ===== DESIGN ANALYSIS ENDPOINTS =====

app.post("/api/design/analyze", async (req: Request, res: Response) => {
  try {
    const { title, description, targetAudience, designType, preferences } =
      req.body;

    logger.info(`Analyzing design brief: ${title}`);

    const strategy = await daryaAgent.analyzeDesignBrief({
      title,
      description,
      targetAudience,
      designType,
      preferences,
    });

    res.json({
      success: true,
      data: strategy,
    });
  } catch (error) {
    logger.error(`Design analysis error: ${error}`);
    res.status(500).json({
      success: false,
      error: String(error),
    });
  }
});

// ===== COMPONENT GENERATION ENDPOINTS =====

app.post("/api/design/generate", async (req: Request, res: Response) => {
  try {
    const { prompt, style } = req.body;

    logger.info(`Generating component: ${prompt}`);

    const component = await daryaAgent.generateComponent(
      prompt,
      style || "both"
    );

    res.json({
      success: true,
      data: component,
    });
  } catch (error) {
    logger.error(`Component generation error: ${error}`);
    res.status(500).json({
      success: false,
      error: String(error),
    });
  }
});

// ===== TRENDS ENDPOINTS =====

app.get("/api/trends/trending", async (req: Request, res: Response) => {
  try {
    const niche = (req.query.niche as string) || "design";

    logger.info(`Getting trending insights for: ${niche}`);

    const insights = await daryaAgent.getTrendingDesignInsights(niche);

    res.json({
      success: true,
      data: insights,
    });
  } catch (error) {
    logger.error(`Trends error: ${error}`);
    res.status(500).json({
      success: false,
      error: String(error),
    });
  }
});

// ===== VIRAL CONTENT ENDPOINTS =====

app.post("/api/viral/analyze", async (req: Request, res: Response) => {
  try {
    const { content, category } = req.body;

    logger.info(`Analyzing viral potential: ${content.substring(0, 50)}`);

    const viralAnalysis = await daryaAgent.analyzeViralPotential(
      content,
      category
    );

    res.json({
      success: true,
      data: viralAnalysis,
    });
  } catch (error) {
    logger.error(`Viral analysis error: ${error}`);
    res.status(500).json({
      success: false,
      error: String(error),
    });
  }
});

// ===== VR/XR ENDPOINTS =====

app.post("/api/vr-xr/create", async (req: Request, res: Response) => {
  try {
    const { prompt } = req.body;

    logger.info(`Creating VR/XR experience: ${prompt}`);

    const vrxrSpec = await daryaAgent.createVRXRExperience(prompt);

    res.json({
      success: true,
      data: vrxrSpec,
    });
  } catch (error) {
    logger.error(`VR/XR creation error: ${error}`);
    res.status(500).json({
      success: false,
      error: String(error),
    });
  }
});

// ===== HOLOGRAM ENDPOINTS =====

app.post("/api/hologram/create", async (req: Request, res: Response) => {
  try {
    const { prompt } = req.body;

    logger.info(`Creating hologram effects: ${prompt}`);

    const hologramSpec = await daryaAgent.createHologramEffects(prompt);

    res.json({
      success: true,
      data: hologramSpec,
    });
  } catch (error) {
    logger.error(`Hologram creation error: ${error}`);
    res.status(500).json({
      success: false,
      error: String(error),
    });
  }
});

// ===== 404 HANDLER =====

app.use((req: Request, res: Response) => {
  res.status(404).json({
    success: false,
    error: "Endpoint not found",
    path: req.path,
  });
});

// ===== START SERVER =====

const PORT = process.env.SERVER_PORT || 5000;

const server = createServer(app);
const io = new SocketIOServer(server, {
  cors: {
    origin: (process.env.ALLOWED_ORIGINS || "http://localhost:3000").split(
      ","
    ),
  },
});

// WebSocket connection handling
io.on("connection", (socket) => {
  logger.info(`Client connected: ${socket.id}`);

  socket.on("disconnect", () => {
    logger.info(`Client disconnected: ${socket.id}`);
  });

  socket.on("design:analyze", async (data) => {
    try {
      const strategy = await daryaAgent.analyzeDesignBrief(data);
      socket.emit("design:analysis-complete", strategy);
    } catch (error) {
      socket.emit("error", String(error));
    }
  });

  socket.on("trends:get", async (niche) => {
    try {
      const trends = await daryaAgent.getTrendingDesignInsights(niche);
      socket.emit("trends:update", trends);
    } catch (error) {
      socket.emit("error", String(error));
    }
  });
});

server.listen(PORT, () => {
  logger.info(
    `✅ Darya Design Wizard running on port ${PORT}`
  );
  logger.info(`🎨 Frontend available at http://localhost:3000`);
  logger.info(`🔥 Backend API available at http://localhost:${PORT}`);
});

export { app, server, io };
