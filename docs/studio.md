# OpenHands Studio

OpenHands Studio is a visual, voice-enabled, non-CLI interface for running, observing, controlling, and approving autonomous agents operating on real repositories.

## Overview

OpenHands Studio transforms the OpenHands agent platform into a calm, high-trust, transparent environment designed for three distinct user personas:

- **Non-technical users** (Studio Mode) - Default experience focused on outcomes
- **Power users** (Builder Mode) - Advanced configuration and customization
- **Operators** (Operator Mode) - Deep debugging and intervention capabilities

## Architecture

### Feature Flag

Studio functionality is controlled by the `STUDIO_ENABLED` environment variable (default: `true`).

```bash
export STUDIO_ENABLED=true
```

### Core Components

#### Frontend Architecture
- **Framework**: React 19 with React Router v7
- **Styling**: TailwindCSS v4 + shadcn/ui components
- **State Management**: Zustand stores
- **UI Components**: Radix UI primitives for accessibility
- **Animations**: Framer Motion for subtle state transitions
- **Visualizations**: Recharts for scorecards and metrics

#### Backend Architecture
- **API**: FastAPI with WebSocket support (Socket.IO)
- **Agent Runtime**: Docker/K8s sandboxed execution
- **Event Streaming**: Real-time observability events
- **Container Streaming**: Live desktop/terminal views

## User Modes

### 1. Studio Mode (Default)

**Audience**: Non-technical users who want to run agents without touching CLI.

**Features**:
- **Fleet Dashboard**: Overview of all repositories with status, scores, and actions
- **Job Run View**: Visual progress tracking with agent timeline
- **Approval View**: One-click PR approval with preview and diff summary
- **Voice Interface**: Push-to-talk input and TTS notifications

**Philosophy**:
- Progressive disclosure - see outcomes first, internals only if requested
- Jobs over logs - logs are hidden unless expanded
- Scorecards over text - metrics, deltas, visuals
- Preview first - always show what changed

### 2. Builder Mode

**Audience**: Advanced users who want to configure and customize agents.

**Pages**:
- **Standards Profiles**: Define code quality standards and conventions
- **Scoring Rubrics**: Configure how repositories are evaluated
- **Agent Roles**: Customize agent capabilities and behaviors
- **Policies**: Set resource caps, timeouts, and limits

**Access**: Toggle in settings or via URL parameter `?mode=builder`

### 3. Operator Mode

**Audience**: Engineers who need deep debugging and intervention.

**Capabilities**:
- **Full Agent Trace**: Step-by-step reasoning stream
- **Tool Call Inspector**: Detailed view of all tool executions
- **Mid-Run Intervention**: Pause, inject context, resume
- **Container Access**: Live view of agent's execution environment

**Access**: Toggle in settings or via URL parameter `?mode=operator`

## Agent Observability

Studio provides ChatGPT-level agent observability with real-time visibility into agent execution.

### Agent Timeline

Vertical timeline showing:
- **Planning Phase**: Agent's initial approach
- **Acting Phase**: Current tool execution
- **Waiting Phase**: Blocked or awaiting approval
- **Validation Phase**: Checking results

Each step includes:
- Timestamp
- Summary (always visible)
- Expandable detail (operator mode)

### Container/Desktop Viewer

When an agent spins up a container:
- **Live Desktop Panel**: Stream of container's visual output
- **Terminal Viewer**: stdout/stderr stream (xterm.js)
- **Filesystem Tree**: Read-only view (expandable in operator mode)
- **Process List**: Running processes and resource usage

**Implementation**: WebSocket stream from container to frontend.

### Mid-Run Intervention

While an agent is running:
1. **Pause**: Freeze execution at current step
2. **Add Context**: Inject text or voice guidance
3. **Resume**: Continue with new context

Added context is:
- Appended to agent's task queue
- Visible in timeline
- Preserved in event stream

## Voice Integration

Voice is a first-class feature, not an add-on.

### Voice Input

**Push-to-Talk Button**:
- Press and hold to record
- Automatic speech-to-text transcription
- Supported actions:
  - Adding agent context during runs
  - Approving/rejecting PRs
  - Issuing commands (pause, resume, stop)

**Implementation**: Web Speech API (browser-native)

### Voice Output

**Text-to-Speech (TTS)** for:
- Job started
- Job completed
- Blocked / needs review
- PR ready for approval

**Configuration**:
- Webhook support for external TTS (Twilio, etc.)
- Configurable voice and rate
- Can be muted per-session

## Computer Use Agents

Studio integrates computer-use agents as first-class tools.

### Capabilities

Computer-use agents can:
- Open browsers
- Navigate UIs
- Click, type, scroll
- Capture screenshots
- Interact with desktop applications

### Implementation

- **Language**: Python
- **OS Support**: Linux/macOS/Windows
- **Execution**: Inside agent containers
- **Observability**: Visible in desktop viewer

### Default Agent

**Lux Computer-Use Agent** is wired in as a default available capability.

### Usage

Computer-use agents appear as:
- Agent tools in the tool palette
- Runnable actions in job runs
- Observable events in the timeline

## Deployment

### Local Development

```bash
# Using Docker Compose
docker-compose -f docker-compose.studio.yml up

# Using CLI (requires uv)
export STUDIO_ENABLED=true
uvx --python 3.12 --from openhands-ai openhands serve
```

### Production Deployment

#### Docker Deployment

```bash
# Build
docker build -f containers/app/Dockerfile -t openhands-studio:latest .

# Run
docker run -it --rm \
  -e STUDIO_ENABLED=true \
  -e LLM_API_KEY=your_key \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -p 3000:3000 \
  openhands-studio:latest
```

#### Cloud Platforms

**Railway** (Recommended):
```bash
railway up
```

**Render**:
```bash
render deploy
```

**Fly.io**:
```bash
fly deploy
```

See deployment-specific guides in `/deployment` directory.

### Environment Variables

```bash
# Studio Feature Flag
STUDIO_ENABLED=true  # Enable Studio features

# LLM Configuration
LLM_MODEL=anthropic/claude-3-5-sonnet-20241022
LLM_API_KEY=your_api_key

# Server Configuration
FRONTEND_PORT=3000
BACKEND_HOST=0.0.0.0

# Workspace
WORKSPACE_BASE=/opt/workspace_base

# Logging
LOG_ALL_EVENTS=true
```

## UI Components

### Fleet Dashboard

**Purpose**: Overview of all managed repositories.

**Components**:
- Repository cards with:
  - Name and description
  - Status pill (idle/running/blocked/complete)
  - Current score (0-10)
  - Last run timestamp
  - CTA buttons: View / Run / Resume

**Layout**: Grid or table view (user preference)

### Job Run View

**Purpose**: Real-time monitoring of agent execution.

**Components**:
- **Progress Bar**: Semantic progress (not time-based)
- **Phase Indicator**: Current execution phase
- **Agent Timeline**: Vertical step-by-step view
- **Desktop Viewer**: Live container view
- **Control Panel**: Pause / Stop / Inject Context buttons

**Updates**: Real-time via WebSocket

### Scorecard View

**Purpose**: Visualize repository quality metrics.

**Components**:
- **Radar Chart**: Multi-dimensional quality view
- **Bar Chart**: Before vs After comparison
- **Gap Analysis**: "Why not 10?" explanations
- **Trend Line**: Historical score evolution

**Data Source**: POST /api/studio/scorecard

### Approval View

**Purpose**: Review and approve agent-generated PRs.

**Components**:
- **Preview URL**: Clickable link to PR
- **Diff Summary**: File-by-file changes
- **Scorecard**: Quality improvements
- **Approve Button**: One-click approval
- **Voice Approval**: Say "approve" to accept

**Actions**: Approve / Reject / Request Changes

## API Endpoints

### Studio Routes

```
GET  /api/studio/fleet           - List all repositories
GET  /api/studio/jobs/:id        - Get job details
POST /api/studio/jobs/:id/pause  - Pause job
POST /api/studio/jobs/:id/resume - Resume job
POST /api/studio/jobs/:id/inject - Inject context
GET  /api/studio/scorecard/:repo - Get scorecard
POST /api/studio/approve/:pr     - Approve PR
```

### WebSocket Events

```
oh_studio_job_update     - Job status changed
oh_studio_agent_step     - New agent timeline step
oh_studio_container_out  - Container output stream
oh_studio_voice_command  - Voice command received
```

## Development

### Adding New Components

```bash
# Create feature component
frontend/src/components/features/studio/[feature]/

# Add route
frontend/src/routes/studio/[feature].tsx

# Add to routes.ts
route("studio/[feature]", "routes/studio/[feature].tsx")
```

### Adding New Agent Capabilities

```python
# openhands/studio/agents/[capability].py

class MyCapability:
    def execute(self, action):
        # Implementation
        pass
```

### Extending Observability

```python
# openhands/studio/events/[event_type].py

class StudioEvent(Event):
    event_type = "studio_[type]"
    # Fields
```

## Testing

### Frontend Tests

```bash
cd frontend
npm run test
npm run test:e2e
```

### Backend Tests

```bash
poetry run pytest openhands/studio/
```

### Integration Tests

```bash
# Start services
docker-compose -f docker-compose.studio.yml up -d

# Run tests
pytest tests/integration/studio/
```

## Performance Considerations

### Event Streaming

- Events are batched (100ms window)
- Only changed data is streamed
- Client-side debouncing for UI updates

### Container Streaming

- Video stream: 10 FPS (adjustable)
- Terminal: 30 FPS
- Compression: H.264 for video, gzip for terminal

### Voice Processing

- Speech-to-text: Browser-native (no server cost)
- Text-to-speech: Configurable (browser or server)
- Audio codec: Opus (low latency)

## Security

### Authentication

- All Studio endpoints require authentication
- Token-based API access
- WebSocket authentication via session token

### Authorization

- Repository access validated per request
- Agent capabilities are sandboxed
- Container isolation via Docker

### Data Privacy

- Voice data never stored
- Event streams are ephemeral
- Logs are configurable per-user

## Troubleshooting

### Studio Not Appearing

```bash
# Check feature flag
echo $STUDIO_ENABLED

# Check logs
docker logs openhands-studio

# Verify frontend build
cd frontend && npm run build
```

### Voice Not Working

- Check browser permissions (microphone)
- Verify HTTPS (required for Web Speech API)
- Check console for errors

### Container Viewer Blank

- Verify Docker socket mount
- Check container is running
- Verify WebSocket connection

## Roadmap

- [ ] Multi-agent orchestration view
- [ ] Collaborative approval workflows
- [ ] Advanced computer-use capabilities
- [ ] Mobile app (iOS/Android)
- [ ] VS Code extension integration

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for development setup and guidelines.

## License

OpenHands Studio is part of OpenHands and is licensed under the MIT License.

## Support

- Documentation: https://docs.all-hands.dev
- Community: https://all-hands.dev/joinslack
- Issues: https://github.com/OpenHands/OpenHands/issues
