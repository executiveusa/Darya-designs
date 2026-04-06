# Darya Design Wizard - Integration & Deployment Guide

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   React Frontend Dashboard                   │
│              (TypeScript/React/Tailwind/GSAP)                │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/WebSocket
┌──────────────────────v──────────────────────────────────────┐
│                  Express.js API Server                       │
│                (TypeScript/Node.js/Socket.io)                │
├──────────────────────┬──────────────────────────────────────┤
│  DaryaAgent Orchestrator (Cognitive Engine)                  │
├──────────────────────┬──────────────────────────────────────┤
│ DesignAnalyzer │ TrendsService │ AnimationService │ Bridge   │
└────────┬─────────────┬──────────────┬──────────────┬────────┘
         │             │              │              │
    ┌────v────┐    ┌──v───┐   ┌─────v──┐    ┌──────v─────┐
    │ Claude  │    │Google│   │GSAP/FM │    │SuperDesign │
    │  API    │    │Trends│   │Babylon │    │   API      │
    └────────┘    └──────┘   └────────┘    └────────────┘
         │             │              │              │
    ┌────v──────────────v──────────────v──────────────v────┐
    │           External Service Layer                      │
    └──────────────────────────────────────────────────────┘
         │                          │
    ┌────v────────┐          ┌──────v────────┐
    │  Supabase   │          │    Redis      │
    │ (Database)  │          │   (Cache)     │
    └─────────────┘          └───────────────┘
```

## Installation & Setup

### Prerequisites

- Node.js 20+
- npm or yarn
- Supabase account
- Redis instance
- Anthropic API key
- SuperDesign API key (optional)

### Installation Steps

```bash
# 1. Navigate to project directory
cd darya-agent

# 2. Install dependencies
npm install

# 3. Create environment file
cp .env.example .env

# 4. Configure environment variables
# Edit .env with your API keys and database credentials
```

## Configuration

### Environment Variables

**Critical Variables:**

```env
# Anthropic API
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx

# Server
SERVER_PORT=5000
NODE_ENV=production
LOG_LEVEL=info

# Database
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOi...

# Redis
REDIS_URL=redis://localhost:6379

# Features
ENABLE_VR_XR=true
ENABLE_HOLOGRAM=true

# CORS
ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
```

### TypeScript Configuration

`tsconfig.json` includes:
- Target: ES2020
- Module: ESNext
- Strict mode: enabled
- Source maps: enabled (development)

### ESLint Configuration

Run linting:
```bash
npm run lint
npm run lint --fix  # Auto-fix issues
```

## API Endpoints Reference

### Design Management

#### Analyze Design Brief
```
POST /api/design/analyze
Content-Type: application/json

{
  "projectName": "Mobile App Design",
  "brief": "Modern mobile banking application...",
  "targetAudience": "Tech-savvy millennials",
  "brandGuide": "Minimalist, blue color scheme",
  "constraints": ["WCAG AA compliance", "Mobile first"]
}

Response:
{
  "success": true,
  "data": {
    "projectName": "Mobile App Design",
    "briefAnalysis": "...",
    "designPrinciples": ["Clarity", "Consistency"],
    "colorPalette": ["#3B82F6", "#10B981"],
    "typography": { "primary": "Inter", "secondary": "Georgia" },
    "layoutRecommendations": "...",
    "componentSuggestions": ["Button", "Card", "Form"],
    "accessibility": "WCAG 2.1 AA",
    "performanceNotes": "...",
    "estimatedHours": 40
  },
  "timestamp": "2024-03-13T..."
}
```

#### Generate UI Design
```
POST /api/design/generate
Content-Type: application/json

{
  "projectName": "Banking Dashboard",
  "description": "Interactive financial dashboard",
  "colorPalette": ["#1F2937", "#3B82F6"],
  "typography": { "primary": "Inter", "secondary": "Playfair" },
  "componentTypes": ["Button", "Card", "Chart"]
}

Response:
{
  "success": true,
  "data": {
    "id": "design-1234567890",
    "name": "Banking Dashboard",
    "components": [...],
    "layout": "grid",
    "styling": {...},
    "responsive": true,
    "accessibilityScore": 87,
    "version": 1
  }
}
```

### Trends & Analytics

#### Get Trending Topics
```
GET /api/trends/trending?region=US&category=design

Response:
{
  "success": true,
  "data": [
    {
      "title": "AI Design Tools",
      "trend": "up",
      "changePercent": 145
    },
    ...
  ]
}
```

#### Get Trending Colors
```
GET /api/trends/colors

Response:
{
  "success": true,
  "data": [
    {
      "color": "#FF6B6B",
      "colorName": "Energetic Red",
      "trend": "Bold brand identities",
      "industry": "Tech, Health",
      "viralScore": 92
    },
    ...
  ]
}
```

#### Analyze Viral Potential
```
POST /api/trends/analyze
Content-Type: application/json

{
  "topic": "Minimalist Web Design"
}

Response:
{
  "success": true,
  "data": {
    "score": 82,
    "viralPotential": "high",
    "analysis": "Topic shows exceptional viral potential..."
  }
}
```

### Animation Generation

#### Generate Animation
```
POST /api/animations/generate
Content-Type: application/json

{
  "elementType": "button",
  "duration": 0.8,
  "intensity": "dramatic",
  "useVR": false
}

Response:
{
  "success": true,
  "data": {
    "id": "anim-1234567890-abc123",
    "name": "button-animation",
    "type": "gsap",
    "duration": 0.8,
    "delay": 0,
    "easing": "power3.inOut",
    "properties": {...},
    "description": "dramatic animation for button",
    "performanceOptimized": false
  }
}
```

#### Optimize Animation
```
POST /api/animations/optimize
Content-Type: application/json

{
  "animation": {...}
}

Response:
{
  "success": true,
  "data": {
    ...animation data,
    "performanceOptimized": true
  }
}
```

### Project Management

#### Create Project
```
POST /api/projects/create
Content-Type: application/json

{
  "userId": "user-123",
  "name": "E-commerce Redesign",
  "description": "Complete redesign of shopping experience",
  "brief": "Modern, fast-loading e-commerce platform",
  "targetAudience": "Online shoppers aged 18-45",
  "estimatedHours": 120,
  "tags": ["ecommerce", "redesign", "performance"]
}

Response:
{
  "success": true,
  "data": {
    "id": "proj-1234567890",
    "userId": "user-123",
    "name": "E-commerce Redesign",
    "status": "draft",
    "createdAt": "2024-03-13T...",
    ...
  }
}
```

#### List Projects
```
GET /api/projects/list?userId=user-123

Response:
{
  "success": true,
  "data": [
    { project object },
    ...
  ]
}
```

#### Get Dashboard Metrics
```
GET /api/dashboard/metrics?userId=user-123

Response:
{
  "success": true,
  "data": {
    "totalProjects": 5,
    "completedProjects": 2,
    "totalHours": 240,
    "averageScore": 87.5,
    "recentTrends": ["AI Design", "Minimalism", "Web3"]
  }
}
```

## Frontend Integration

### React Component Usage

```typescript
import React from 'react';
import Dashboard from './src/frontend/Dashboard';

function App() {
  return <Dashboard />;
}

export default App;
```

### Environment Setup for Frontend

```typescript
// Create .env.local
REACT_APP_API_URL=http://localhost:5000
REACT_APP_WS_URL=ws://localhost:5000
```

### API Client Example

```typescript
const fetchDesignAnalysis = async (brief: {
  projectName: string;
  brief: string;
  targetAudience: string;
}) => {
  const response = await fetch('/api/design/analyze', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(brief)
  });

  return response.json();
};
```

## Database Schema

### DesignProject Table
```sql
CREATE TABLE design_projects (
  id UUID PRIMARY KEY,
  user_id VARCHAR(255),
  name VARCHAR(255),
  description TEXT,
  brief TEXT,
  target_audience TEXT,
  status VARCHAR(50),
  color_palette JSON,
  typography JSON,
  component_count INTEGER,
  estimated_hours FLOAT,
  tags JSON,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  completed_at TIMESTAMP,
  thumbnail_url TEXT
);
```

### DesignAnalysis Table
```sql
CREATE TABLE design_analyses (
  id UUID PRIMARY KEY,
  project_id UUID,
  design_principles JSON,
  color_analysis JSON,
  typography_analysis JSON,
  layout_recommendations TEXT,
  accessibility_score INTEGER,
  performance_notes TEXT,
  component_suggestions JSON,
  estimated_implementation_hours FLOAT,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);
```

### TrendSnapshot Table
```sql
CREATE TABLE trend_snapshots (
  id UUID PRIMARY KEY,
  user_id VARCHAR(255),
  topic VARCHAR(255),
  trending_score FLOAT,
  viral_potential VARCHAR(50),
  related_topics JSON,
  color_trends JSON,
  typography_trends JSON,
  pattern_trends JSON,
  growth_rate FLOAT,
  market_insight TEXT,
  created_at TIMESTAMP,
  metadata JSON
);
```

### UserPreferences Table
```sql
CREATE TABLE user_preferences (
  id UUID PRIMARY KEY,
  user_id VARCHAR(255),
  language VARCHAR(10),
  theme VARCHAR(50),
  notifications JSON,
  default_color_palette JSON,
  default_typography JSON,
  favorite_components JSON,
  design_style VARCHAR(50),
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);
```

## Deployment Guide

### Docker Deployment

```dockerfile
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY dist ./dist

EXPOSE 5000
ENV NODE_ENV=production

CMD ["node", "dist/server.js"]
```

### Build & Deploy Commands

```bash
# Build
npm run build

# Create Docker image
docker build -t darya-design-wizard .

# Run container
docker run -p 5000:5000 \
  -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
  -e SUPABASE_URL=$SUPABASE_URL \
  darya-design-wizard
```

### Vercel Deployment

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "env": {
    "ANTHROPIC_API_KEY": "@anthropic_key",
    "SUPABASE_URL": "@supabase_url",
    "SUPABASE_KEY": "@supabase_key"
  }
}
```

## Performance Optimization

### Caching Strategy

```typescript
// Response caching (1 hour)
const trends = await cache.get('trends', () =>
  trendsService.getTrendingTopics(),
  3600000
);
```

### Database Query Optimization

```typescript
// Index frequently queried columns
CREATE INDEX idx_projects_user_id ON design_projects(user_id);
CREATE INDEX idx_analysis_project_id ON design_analyses(project_id);
CREATE INDEX idx_trends_topic ON trend_snapshots(topic);
```

### Frontend Optimization

```typescript
// Lazy load components
const Dashboard = React.lazy(() => import('./Dashboard'));

// Memoize expensive operations
const MemoizedChart = React.memo(Chart);
```

## Security Checklist

- [ ] Set strong environment variable values
- [ ] Enable HTTPS in production
- [ ] Configure CORS properly
- [ ] Implement rate limiting
- [ ] Add authentication/authorization
- [ ] Validate all inputs
- [ ] Sanitize database queries
- [ ] Use parameterized queries
- [ ] Regular security audits
- [ ] Keep dependencies updated

## Monitoring & Logging

### Winston Logger Configuration

```typescript
import winston from 'winston';

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});
```

### Health Check Endpoint

```
GET /healthz

Response:
{
  "status": "healthy",
  "service": "darya-design-wizard",
  "timestamp": "2024-03-13T...",
  "uptime": 3600.123
}
```

## Troubleshooting

### Common Issues

**Issue:** Claude API rate limit
**Solution:** Implement request queuing and backoff strategy

**Issue:** Database connection timeout
**Solution:** Check Supabase credentials and network connectivity

**Issue:** CORS errors
**Solution:** Verify ALLOWED_ORIGINS in environment

**Issue:** Animation performance
**Solution:** Enable GPU acceleration, reduce animation complexity

## Support & Documentation

- API Documentation: See this file
- Build Status: `/BUILD_COMPLETE.md`
- Type Definitions: See `.d.ts` files
- Example Usage: See test files

## Version History

- **1.0.0** (2024-03-13): Initial production release
  - Core design analysis
  - Trend integration
  - Animation generation
  - Bilingual support
  - Dashboard UI

## License

© 2024 Kupuri Agency. All rights reserved.

## Contact & Support

For integration support, contact the development team.
