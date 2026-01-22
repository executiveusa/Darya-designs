# 🚀 OpenHands Studio - Complete Deployment Guide

## Architecture Overview

```
┌──────────────────────┐          ┌─────────────────────────┐
│   Vercel             │  HTTPS   │   Hostinger VPS         │
│   (Frontend)         │ ───────▶ │   (Backend)             │
│                      │          │                         │
│  • React + Vite      │          │  • Docker Container     │
│  • Static assets     │          │  • FastAPI + Python     │
│  • Edge CDN          │          │  • Nginx Reverse Proxy  │
│  • Auto-scaling      │          │  • SSL via Let's Encrypt│
└──────────────────────┘          └─────────────────────────┘
         ↓                                    ↓
    Users access                         Agent execution
    openhands.vercel.app                 on secure backend
```

---

## 📋 Prerequisites

### For Hostinger Backend:
- [ ] VPS with Docker installed
- [ ] Domain name (e.g., api.yourdomain.com)
- [ ] SSH access to server
- [ ] LLM API key (Anthropic/OpenAI)

### For Vercel Frontend:
- [ ] Vercel account (free tier works)
- [ ] GitHub repository access
- [ ] Vercel CLI installed: `npm i -g vercel`

---

## Part 1️⃣: Deploy Backend to Hostinger

### Step 1: Prepare Hostinger VPS

```bash
# SSH into your Hostinger VPS
ssh root@your-hostinger-ip

# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
apt install docker-compose -y

# Install Nginx
apt install nginx certbot python3-certbot-nginx -y

# Create deployment directory
mkdir -p /home/openhands/openhands-studio
cd /home/openhands/openhands-studio
```

### Step 2: Clone Repository on Server

```bash
# On your Hostinger VPS
cd /home/openhands/openhands-studio

# Clone your repo
git clone https://github.com/executiveusa/Darya-designs.git .
git checkout claude/openhands-studio-ux-gcRoA
```

### Step 3: Configure Environment

```bash
# Create .env file
cat > .env << 'EOF'
# Studio Configuration
STUDIO_ENABLED=true

# LLM Configuration
LLM_MODEL=anthropic/claude-3-5-sonnet-20241022
LLM_API_KEY=your_anthropic_api_key_here

# OpenHands Configuration
SANDBOX_RUNTIME_CONTAINER_IMAGE=docker.all-hands.dev/openhands/runtime:0.59-nikolaik
LOG_ALL_EVENTS=true
WORKSPACE_BASE=/opt/workspace_base

# Server Configuration
FRONTEND_PORT=3000
EOF

# Secure the .env file
chmod 600 .env
```

### Step 4: Build and Run Docker Container

```bash
# Build the Docker image
docker build -f containers/app/Dockerfile -t openhands-studio:latest .

# Or use Docker Compose (recommended)
docker-compose -f docker-compose.studio.yml up -d

# Check logs
docker logs -f openhands-studio

# Verify it's running
curl http://localhost:3000/api/options/models
```

### Step 5: Configure Nginx Reverse Proxy

```bash
# Copy Nginx configuration
cp hostinger-nginx.conf /etc/nginx/sites-available/openhands-studio

# Edit the configuration with your domain
nano /etc/nginx/sites-available/openhands-studio

# Update these lines:
# - server_name api.your-domain.com backend.your-domain.com;
# - add_header Access-Control-Allow-Origin "https://your-frontend.vercel.app" always;

# Enable the site
ln -s /etc/nginx/sites-available/openhands-studio /etc/nginx/sites-enabled/

# Test configuration
nginx -t

# Reload Nginx
systemctl reload nginx
```

### Step 6: Set Up SSL Certificate

```bash
# Install SSL certificate with Let's Encrypt
certbot --nginx -d api.yourdomain.com

# Auto-renewal is configured automatically
# Test renewal with:
certbot renew --dry-run
```

### Step 7: Configure DNS

In your domain registrar (Namecheap, GoDaddy, etc.):

```
Type: A Record
Name: api (or backend)
Value: YOUR_HOSTINGER_VPS_IP
TTL: 300
```

Wait 5-10 minutes for DNS propagation.

### Step 8: Verify Backend

```bash
# Test from your local machine
curl https://api.yourdomain.com/api/options/models

# Should return a JSON response with available models
```

✅ **Backend deployment complete!**

---

## Part 2️⃣: Deploy Frontend to Vercel

### Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

### Step 2: Login to Vercel

```bash
vercel login
# Follow the browser authentication flow
```

### Step 3: Configure Project

```bash
# In your local repository
cd /home/user/Darya-designs
git checkout claude/openhands-studio-ux-gcRoA

# Initialize Vercel project
vercel
```

When prompted:
- **Set up and deploy?** → Yes
- **Which scope?** → Your account/team
- **Link to existing project?** → No
- **Project name?** → openhands-studio (or your choice)
- **Directory?** → `./` (root)
- **Override settings?** → Yes
  - **Build Command:** `cd frontend && npm run build`
  - **Output Directory:** `frontend/build/client`
  - **Install Command:** `cd frontend && npm install`

### Step 4: Set Environment Variables

```bash
# Set backend host
vercel env add VITE_BACKEND_HOST

# When prompted, enter: api.yourdomain.com (without https://)
# Select: Production, Preview, Development

# Set TLS flag
vercel env add VITE_USE_TLS

# When prompted, enter: true
# Select: Production, Preview, Development
```

Or via Vercel Dashboard:
1. Go to https://vercel.com/dashboard
2. Select your project → Settings → Environment Variables
3. Add:
   - `VITE_BACKEND_HOST` = `api.yourdomain.com`
   - `VITE_USE_TLS` = `true`

### Step 5: Update Vercel Configuration

Edit `vercel.json` to use your domain:

```json
{
  "version": 2,
  "name": "openhands-studio",
  "env": {
    "VITE_BACKEND_HOST": "api.yourdomain.com",
    "VITE_USE_TLS": "true"
  },
  "build": {
    "env": {
      "VITE_BACKEND_HOST": "api.yourdomain.com",
      "VITE_USE_TLS": "true"
    }
  }
}
```

### Step 6: Deploy to Production

```bash
# Deploy to production
vercel --prod

# You'll get a URL like: https://openhands-studio.vercel.app
```

### Step 7: Update Backend CORS

Update your Nginx configuration to allow your Vercel domain:

```bash
# SSH into Hostinger
ssh root@your-hostinger-ip

# Edit Nginx config
nano /etc/nginx/sites-available/openhands-studio

# Update CORS origin:
add_header Access-Control-Allow-Origin "https://openhands-studio.vercel.app" always;

# Reload Nginx
systemctl reload nginx
```

### Step 8: Test the Full Stack

1. Visit your Vercel URL: `https://openhands-studio.vercel.app`
2. The frontend should load
3. Check browser console for errors
4. Try creating a conversation - it should connect to your backend

✅ **Frontend deployment complete!**

---

## 🔧 Configuration Summary

### Frontend (Vercel)
```
URL: https://openhands-studio.vercel.app
Env: VITE_BACKEND_HOST=api.yourdomain.com
     VITE_USE_TLS=true
```

### Backend (Hostinger)
```
URL: https://api.yourdomain.com
Port: 3000 (internal)
SSL: Let's Encrypt
Reverse Proxy: Nginx
```

---

## 🧪 Testing Checklist

- [ ] Frontend loads at Vercel URL
- [ ] Backend health check: `https://api.yourdomain.com/health`
- [ ] WebSocket connection works (check browser console)
- [ ] Can create a new conversation
- [ ] Agent can execute commands
- [ ] File operations work
- [ ] Terminal output streams correctly

---

## 🐛 Troubleshooting

### Frontend can't connect to backend

**Check CORS headers:**
```bash
curl -I https://api.yourdomain.com/api/options/models \
  -H "Origin: https://openhands-studio.vercel.app"
```

Should include:
```
Access-Control-Allow-Origin: https://openhands-studio.vercel.app
```

**Fix:** Update Nginx configuration with correct Vercel domain.

### WebSocket connection failing

**Check Nginx WebSocket config:**
```bash
# In /etc/nginx/sites-available/openhands-studio
location /socket.io/ {
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    ...
}
```

**Test WebSocket:**
```javascript
// In browser console at your Vercel URL
const socket = io('https://api.yourdomain.com');
socket.on('connect', () => console.log('Connected!'));
```

### SSL certificate issues

**Renew certificate:**
```bash
certbot renew
systemctl reload nginx
```

### Backend not responding

**Check Docker container:**
```bash
docker ps  # Is container running?
docker logs openhands-studio  # Check logs
docker restart openhands-studio  # Restart if needed
```

**Check Nginx:**
```bash
systemctl status nginx
nginx -t  # Test configuration
```

### High memory usage

**Limit Docker resources:**
```bash
# Add to docker-compose.studio.yml
services:
  openhands-studio:
    deploy:
      resources:
        limits:
          memory: 4G
          cpus: '2'
```

---

## 🔒 Security Checklist

- [ ] SSL/TLS enabled on backend
- [ ] Firewall configured (allow 80, 443, 22 only)
- [ ] Strong SSH key authentication
- [ ] Docker socket properly secured
- [ ] Environment variables not committed to Git
- [ ] CORS restricted to your Vercel domain
- [ ] Rate limiting configured in Nginx
- [ ] Regular security updates scheduled

---

## 📊 Monitoring

### Backend Monitoring

```bash
# Check container stats
docker stats openhands-studio

# Check logs
docker logs -f --tail 100 openhands-studio

# Check Nginx logs
tail -f /var/log/nginx/openhands-access.log
tail -f /var/log/nginx/openhands-error.log
```

### Frontend Monitoring

- Vercel Dashboard: https://vercel.com/dashboard
- Analytics: Automatically included
- Error tracking: Check Vercel logs

---

## 🔄 Continuous Deployment

### Auto-deploy frontend on Git push

```bash
# In your repository
vercel --prod

# Or connect GitHub repo in Vercel Dashboard:
# Settings → Git → Connect Repository
# Enable: Auto-deploy on push
```

### Update backend

```bash
# SSH into Hostinger
cd /home/openhands/openhands-studio
git pull
docker-compose -f docker-compose.studio.yml down
docker-compose -f docker-compose.studio.yml up -d --build
```

Or use the deploy script:
```bash
./hostinger-deploy.sh
```

---

## 💰 Cost Estimate

### Hostinger VPS
- **Recommended**: VPS 2 ($5.99/mo)
  - 2 vCPU cores
  - 4 GB RAM
  - 100 GB SSD
  - 2 TB bandwidth

### Vercel
- **Free tier**: Unlimited deployments
- **Pro**: $20/mo (if needed for team features)

### Domain
- **Cost**: $10-15/year (any registrar)

### LLM API
- **Anthropic**: Pay-as-you-go
- **OpenAI**: Pay-as-you-go

**Total**: ~$6-10/month + LLM usage

---

## 🎯 Next Steps

1. **Deploy backend** following Part 1
2. **Deploy frontend** following Part 2
3. **Test thoroughly** using checklist
4. **Set up monitoring** for production
5. **Configure backups** for workspace data
6. **Document custom settings** for your team

---

## 📞 Support

- **Documentation**: See `docs/studio.md`
- **Issues**: GitHub Issues
- **OpenHands Docs**: https://docs.all-hands.dev

---

**Status**: 🚀 Ready to deploy!
