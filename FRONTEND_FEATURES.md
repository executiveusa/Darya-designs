# OpenHands Jarvis - Frontend Features & User Guide

## 🎨 Frontend Overview

The OpenHands frontend is a sophisticated React-based IDE that provides a complete development environment for AI-powered code execution and agent management.

**Tech Stack:**
- React 19.1.1
- React Router v7 (SPA mode)
- Vite (build tool)
- TypeScript
- Tailwind CSS v4
- Zustand (state management)
- TanStack Query (React Query)
- HeroUI (component library)
- Monaco Editor (code editor)
- Jupyter Terminal

---

## 📑 Main Pages & Features

### 1. **Home Page** (`/`)
**Purpose:** Welcome and quick start

**Features:**
- ✅ Quick start guide
- ✅ Feature overview
- ✅ Getting started tips
- ✅ Link to documentation
- ✅ Integration setup options

**What You'll See:**
- OpenHands logo and branding
- Main call-to-action buttons
- Quick links to key features
- Documentation links

---

### 2. **Conversation/Chat** (`/conversation`)
**Purpose:** Main AI agent interaction interface

**Features:**
- 💬 Chat interface with AI agent
- 📝 Multi-tab support (Conversation, Code, Terminal, Browser, Jupyter)
- 🔄 Real-time message streaming
- 📎 File attachment support
- 🎯 Task execution with feedback
- 📊 Token usage tracking

**Tabs:**
1. **Conversation** - Chat with AI agents
2. **Code Editor** - Monaco editor for code viewing/editing
3. **Changes** - Track file modifications
4. **Terminal** - Execute commands
5. **Browser** - Web browsing capability
6. **Jupyter Notebook** - Interactive Python/notebook support

**What You'll See:**
```
┌─────────────────────────────────────┐
│ OpenHands IDE                       │
├─────────────────────────────────────┤
│ [Conversation] [Code] [Changes]     │
│ [Terminal] [Browser] [Jupyter]      │
├─────────────────────────────────────┤
│                                     │
│ Agent: What would you like me to do?│
│                                     │
│ [Text input for chat...........] [Send]
│                                     │
└─────────────────────────────────────┘
```

---

### 3. **Settings** (`/settings`)
**Purpose:** Configure application and agent behavior

**Subpages:**

#### **User Settings** (`/settings/user`)
- Profile management
- Authentication settings
- User preferences
- Avatar upload

#### **App Settings** (`/settings/app`)
- Language selection
- Theme (light/dark)
- Default agent model
- Execution settings
- Memory/history settings

#### **LLM Settings** (`/settings/llm`)
**Most Important Setting!**
- ✅ Model selection (Claude, GPT-4, Gemini, etc.)
- ✅ API key configuration
- ✅ Temperature & sampling
- ✅ Max tokens
- ✅ System prompts
- ✅ Model routing/fallbacks

**What You Configure:**
```yaml
Model: Claude Opus 4.5 (Recommended)
API Provider: Anthropic
API Key: [Enter your key]
Temperature: 0.7
Max Output: 4096 tokens
```

#### **Git Settings** (`/settings/git`)
- GitHub authentication
- Repository access
- SSH key configuration
- Git credentials

#### **API Keys** (`/settings/api-keys`)
- Manage API keys for integrations
- GitHub token
- External service credentials
- Stripe (if using paid features)

#### **Secrets Settings** (`/settings/secrets`)
- Secure credential storage
- Environment variables
- Encrypted secrets
- Key rotation

#### **MCP Settings** (`/settings/mcp`)
- Model Context Protocol configuration
- Tool connections
- External service integration
- Custom tool setup

#### **Microagent Management** (`/settings/microagent-management`)
- Specialized agent configuration
- Skill management
- Agent parameters
- Team orchestration

---

## 🎯 Key User Workflows

### Workflow 1: Code Review

```
User: "Review this code"
    ↓
Select Code in Editor
    ↓
Agent: Analyzes code
    ↓
Results: Quality report, issues found, improvements
    ↓
Action: Create PR with suggestions
```

**Steps:**
1. Open Conversation tab
2. Copy or paste code to review
3. Ask agent: "Review this code for quality"
4. View analysis in chat
5. Accept improvements

---

### Workflow 2: Generate Tests

```
User: "Add tests for this function"
    ↓
Select Function in Code Editor
    ↓
Agent: Generates test cases
    ↓
Results: Unit tests in chat
    ↓
Action: Copy to test file
```

**Steps:**
1. Go to Code tab
2. Show function to test
3. Chat: "Generate comprehensive unit tests"
4. Copy generated tests
5. Run in Terminal tab

---

### Workflow 3: Fix Issues

```
Error/Issue Found
    ↓
Chat: "Fix this error"
    ↓
Agent: Analyzes and generates fix
    ↓
Code: Updated in editor
    ↓
Test: Run tests in Terminal
```

**Steps:**
1. Paste error message in chat
2. Agent analyzes root cause
3. Get suggested fix
4. Apply fix to code
5. Test with Terminal tab

---

### Workflow 4: Web Browsing

```
Research Needed
    ↓
Browser Tab
    ↓
Agent: Navigates and extracts info
    ↓
Results: Summary in chat
```

**Steps:**
1. Click Browser tab
2. Type URL or search query
3. Agent navigates and extracts info
4. View results and AI analysis

---

### Workflow 5: Run Jupyter Notebooks

```
Data Analysis/ML Work
    ↓
Jupyter Tab
    ↓
Agent: Writes and runs code
    ↓
Results: Visualizations and outputs
```

**Steps:**
1. Go to Jupyter tab
2. Ask agent to create notebook
3. Agent executes Python code
4. View plots and results

---

## 🎨 UI Components & Controls

### Top Navigation Bar
```
┌────────────────────────────────────────┐
│  [OpenHands Logo] [Settings] [Profile] │
└────────────────────────────────────────┘
```

### Left Sidebar (Chat History)
```
Conversation History
├─ Today
│  ├─ Code Review Session
│  ├─ Bug Fix Discussion
│  └─ Feature Brainstorm
└─ Yesterday
   ├─ Security Audit
   └─ Performance Analysis
```

Click any item to resume conversation.

### Main Content Area

**Tab Navigation:**
```
[Conversation][Code][Changes][Terminal][Browser][Jupyter]
```

**Chat Area (Conversation Tab):**
- Message history scrollable
- Agent responses with streaming
- User input field at bottom
- Markdown formatting support
- Code syntax highlighting

**Code Editor (Code Tab):**
- Full Monaco editor
- Syntax highlighting for 100+ languages
- Code completion (when enabled)
- Theme switching
- Line numbers
- Minimap

**Terminal (Terminal Tab):**
- Full xterm.js terminal
- Command execution
- Output streaming
- Copy/paste support
- Scrollback buffer

---

## 🔧 Settings Guide

### Recommended Settings for Jarvis Platform

```yaml
LLM Settings:
  Model: Claude Opus 4.5 ✅
  Provider: Anthropic
  Temperature: 0.7
  Max Tokens: 4096

App Settings:
  Language: English (or your preference)
  Theme: Dark (recommended)
  Auto-save: Enabled

Git Settings:
  GitHub Authenticated: Yes
  Default Branch: main

API Keys:
  GitHub Token: [Your token]
  LLM API Key: [Your Anthropic key]
```

### First-Time Setup Checklist

- [ ] Click Settings
- [ ] Go to LLM Settings
- [ ] Enter API key for Claude/OpenAI
- [ ] Test connection
- [ ] Go to Git Settings
- [ ] Authenticate with GitHub (if using)
- [ ] Check API Keys section
- [ ] Save all settings
- [ ] Return to Conversation tab
- [ ] Start chatting with agent!

---

## 🌐 Multi-Language Support

The frontend supports 8+ languages:

**Available Languages:**
- 🇺🇸 English
- 🇪🇸 Spanish
- 🇫🇷 French
- 🇩🇪 German
- 🇨🇳 Chinese (Simplified)
- 🇯🇵 Japanese
- 🇰🇷 Korean
- 🇮🇹 Italian

**Change Language:**
1. Go to Settings
2. Find "Language" dropdown
3. Select preferred language
4. App restarts with new language

---

## 🔐 Authentication & Security

### Login Options
- GitHub OAuth (recommended)
- Email/Password (if available)
- API Key (for headless use)

### Security Features
- ✅ HTTPS/TLS encryption
- ✅ Secure API key storage
- ✅ CSRF protection
- ✅ Rate limiting
- ✅ Session management
- ✅ Audit logging

### First-Time Users
1. Visit application
2. Sign up or log in
3. Configure LLM API keys
4. Authorize GitHub (optional)
5. Start using!

---

## 📊 Performance Indicators

### What to Expect

**First Load:**
- Time: 3-5 seconds
- Reason: Download React bundles, Monaco editor
- Improvement: Cached after first load

**Page Navigation:**
- Time: <500ms
- Reason: Client-side routing
- Improvement: Very fast

**Code Execution:**
- Time: Varies (task dependent)
- Provides: Real-time streaming updates
- Shows: Progress indicators

**Editor Load:**
- Time: 1-2 seconds
- Reason: Monaco initialization
- Note: One-time per session

---

## 💡 Tips & Tricks

### Keyboard Shortcuts
- `Ctrl+/` - Comment code
- `Ctrl+D` - Duplicate line
- `Ctrl+K` - Clear chat
- `Ctrl+L` - Focus input
- `Shift+Enter` - New line in chat

### Pro Tips
1. **Use specific prompts** - "Review this code for security issues" is better than "Review this"
2. **Provide context** - Include error messages, requirements, constraints
3. **Use code blocks** - Format code with \`\`\` for better parsing
4. **Check multiple tabs** - Errors might show in Terminal or Changes tabs
5. **Save frequently** - Auto-save is enabled but manual save is safe
6. **Use browser tab** - For research and external documentation

### Common Tasks

**"Write a React component"**
```
Chat: "Create a React component for a user profile card with name, avatar, and bio"
→ Agent generates code in Code tab
→ Copy to your project
```

**"Test this function"**
```
Chat: "Generate unit tests for this function: [paste code]"
→ Agent creates test file
→ Copy tests to test directory
→ Run in Terminal
```

**"Explain this code"**
```
Chat: "Explain how this code works: [paste code]"
→ Agent provides detailed explanation
→ Suggests improvements
```

**"Fix this error"**
```
Chat: "Fix this error: [error message and code]"
→ Agent identifies root cause
→ Provides fix
→ Test in Terminal
```

---

## 🐛 Troubleshooting Common Issues

### Chat Not Responding

**Problem:** Agent not replying to messages

**Solution:**
1. Check LLM Settings - verify API key is set
2. Verify API key is valid
3. Check rate limits (if using free tier)
4. Refresh page and try again
5. Check browser console (F12) for errors

### Code Not Executing

**Problem:** Terminal not running commands

**Solution:**
1. Ensure backend is running (or mocked API enabled)
2. Check Terminal tab for output
3. Verify permissions for operations
4. Try simpler command first

### Editor Slow or Unresponsive

**Problem:** Code editor lagging

**Solution:**
1. Close large files (>10MB)
2. Reduce number of open tabs
3. Refresh page
4. Use lighter editor if available
5. Check browser memory usage (DevTools)

### Settings Not Saving

**Problem:** Configuration changes not persisted

**Solution:**
1. Check browser has localStorage enabled
2. Clear browser cache
3. Verify you clicked Save
4. Check browser console for errors
5. Try different browser

---

## 🚀 Advanced Features

### Multi-Agent Coordination
- Configure multiple agents
- Set specializations
- Route tasks to appropriate agents
- Agent team collaboration

### Custom Prompts
- Save frequently used prompts
- Create templates
- Customize agent behavior
- Fine-tune responses

### Integration Plugins
- MCP (Model Context Protocol) tools
- Custom API integrations
- External service connections
- Tool creation

### Workspace Management
- Multiple conversations
- Organization by project
- Sharing with team
- Collaboration features

---

## 📱 Responsive Design

Works on multiple screen sizes:

**Desktop (1920x1080+):**
- Full layout with all panels
- Optimal for development

**Laptop (1366x768):**
- Optimized sidebar
- Responsive tabs
- Good for travel

**Tablet (768x1024):**
- Vertical layout option
- Touch-friendly buttons
- Scrollable panels

**Mobile (375x667):**
- Single column layout
- Collapsed navigation
- Touch optimized

---

## 📞 Getting Help

### In-App Help
- Click "?" icon or Help menu
- Browse documentation
- View keyboard shortcuts
- Contact support

### Documentation
- Full docs: https://docs.openhands.dev
- GitHub: https://github.com/openhands/openhands
- Community: Slack/Forums

### Report Issues
- GitHub Issues
- Error reporting in app
- Debug logs available

---

## 🎓 Learning Resources

### Getting Started
1. Read Home page guide
2. Try example prompts
3. Explore Settings
4. Watch tutorial (if available)
5. Join community

### Advanced Usage
1. Read full documentation
2. Explore settings in depth
3. Configure custom prompts
4. Integrate external tools
5. Build workflows

---

## ✨ What's Next

With Jarvis Platform integration, the frontend will include:

✅ **Voice Commands** - Talk to your AI agent
✅ **Slash Commands** - `/audit`, `/review`, `/deploy`, etc.
✅ **Decision Dashboard** - See autonomous decisions
✅ **Agent Monitoring** - Track multi-agent teams
✅ **Analytics** - Insights on agent performance
✅ **Skill Management** - Configure 50+ skills
✅ **Voice Chat** - Full conversational AI

---

## 📊 Frontend Architecture

```
src/
├── components/       # React components
├── routes/          # Page components
├── hooks/           # Custom React hooks
├── stores/          # Zustand state stores
├── services/        # API services
├── utils/           # Utility functions
├── types/           # TypeScript types
├── context/         # React context
├── i18n/            # Translations
├── mocks/           # Mock API handlers
└── styles/          # Global styles
```

---

*Last Updated: January 22, 2026*
*OpenHands Version: 0.59.0*
*Jarvis Integration: Ready for v1.0*
