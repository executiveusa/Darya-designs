# 🚀 Quick Start - Deploy OpenHands Studio

## ⚡ TL;DR - 5 Minute Deployment

### Frontend to Vercel (2 minutes)

```bash
# 1. Run the deployment script
./deploy-vercel.sh

# Follow prompts:
# - Enter your backend domain (e.g., api.yourdomain.com)
# - Authenticate with Vercel
# - Confirm deployment

# Done! You'll get a URL like: https://openhands-studio.vercel.app
```

### Backend to Hostinger (3 minutes)

```bash
# 1. SSH into your Hostinger VPS
ssh root@your-hostinger-ip

# 2. Clone and deploy
git clone https://github.com/executiveusa/Darya-designs.git /opt/openhands
cd /opt/openhands
git checkout claude/openhands-studio-ux-gcRoA

# 3. Configure
cp .env.studio.example .env
nano .env  # Add your LLM_API_KEY

# 4. Deploy
docker-compose -f docker-compose.studio.yml up -d

# 5. Set up Nginx reverse proxy
cp hostinger-nginx.conf /etc/nginx/sites-available/openhands-studio
nano /etc/nginx/sites-available/openhands-studio  # Update domain
ln -s /etc/nginx/sites-available/openhands-studio /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx

# 6. Get SSL certificate
certbot --nginx -d api.yourdomain.com

# Done! Backend is live at: https://api.yourdomain.com
```

---

## 📝 What You Need

### Before Starting:
- ✅ Hostinger VPS with Docker
- ✅ Domain name (e.g., yourdomain.com)
- ✅ Vercel account (free)
- ✅ LLM API key (Anthropic or OpenAI)

### DNS Setup:
```
Type: A Record
Name: api
Value: YOUR_HOSTINGER_IP
```

---

## 🎯 Deployment Flow

```
You → ./deploy-vercel.sh → Vercel (Frontend)
                              ↓
                         https://openhands-studio.vercel.app
                              ↓
                         Calls Backend API
                              ↓
You → Hostinger VPS → Docker + Nginx (Backend)
                              ↓
                         https://api.yourdomain.com
```

---

## ✅ Verification

### Check Backend:
```bash
curl https://api.yourdomain.com/health
# Should return: {"status": "healthy"}
```

### Check Frontend:
1. Visit https://your-vercel-url.vercel.app
2. Open browser console (F12)
3. Should see "Connected" in console
4. Try creating a conversation

---

## 🔧 Update Backend CORS

After Vercel deployment, update backend to allow your Vercel domain:

```bash
# SSH into Hostinger
nano /etc/nginx/sites-available/openhands-studio

# Update line:
add_header Access-Control-Allow-Origin "https://your-actual-vercel-url.vercel.app" always;

# Reload
systemctl reload nginx
```

---

## 📚 Need More Details?

See `DEPLOYMENT_GUIDE.md` for:
- Complete step-by-step instructions
- Troubleshooting guide
- Security configuration
- Monitoring setup
- Cost breakdown

---

## 🆘 Quick Troubleshooting

**Frontend can't connect to backend?**
→ Check CORS headers in Nginx config

**WebSocket not working?**
→ Verify Nginx WebSocket configuration (location /socket.io/)

**Backend not responding?**
→ Check: `docker logs openhands-studio`

**SSL certificate issues?**
→ Run: `certbot renew && systemctl reload nginx`

---

**Questions?** See DEPLOYMENT_GUIDE.md or open an issue!
