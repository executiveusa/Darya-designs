#!/bin/bash
set -e

echo "🚀 OpenHands Studio - Vercel Deployment Script"
echo "=============================================="

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
fi

# Check if we're in the right directory
if [ ! -f "vercel.json" ]; then
    echo "❌ Error: vercel.json not found. Run this script from the repository root."
    exit 1
fi

# Get backend host from user
echo ""
read -p "Enter your backend domain (e.g., api.yourdomain.com): " BACKEND_HOST

if [ -z "$BACKEND_HOST" ]; then
    echo "❌ Backend host is required"
    exit 1
fi

echo ""
echo "📝 Configuration:"
echo "   Backend: https://$BACKEND_HOST"
echo "   Frontend: Will be deployed to Vercel"
echo ""

# Update vercel.json with backend host
echo "📝 Updating vercel.json..."
cat > vercel.json << EOF
{
  "version": 2,
  "name": "openhands-studio",
  "buildCommand": "cd frontend && npm run build",
  "outputDirectory": "frontend/build/client",
  "installCommand": "cd frontend && npm install",
  "framework": null,
  "devCommand": "cd frontend && npm run dev",
  "env": {
    "VITE_BACKEND_HOST": "$BACKEND_HOST",
    "VITE_USE_TLS": "true"
  },
  "build": {
    "env": {
      "VITE_BACKEND_HOST": "$BACKEND_HOST",
      "VITE_USE_TLS": "true"
    }
  },
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://$BACKEND_HOST/api/:path*"
    },
    {
      "source": "/socket.io/:path*",
      "destination": "https://$BACKEND_HOST/socket.io/:path*"
    },
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ],
  "headers": [
    {
      "source": "/assets/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    },
    {
      "source": "/api/(.*)",
      "headers": [
        {
          "key": "Access-Control-Allow-Origin",
          "value": "*"
        },
        {
          "key": "Access-Control-Allow-Methods",
          "value": "GET, POST, PUT, DELETE, OPTIONS"
        },
        {
          "key": "Access-Control-Allow-Headers",
          "value": "Content-Type, Authorization"
        }
      ]
    }
  ]
}
EOF

echo "✅ Configuration updated"

# Deploy to Vercel
echo ""
echo "🚀 Deploying to Vercel..."
echo ""

vercel --prod

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📝 Important: Update your backend Nginx configuration with the Vercel URL"
echo "   1. SSH into your server"
echo "   2. Edit /etc/nginx/sites-available/openhands-studio"
echo "   3. Update: add_header Access-Control-Allow-Origin \"https://YOUR-VERCEL-URL\" always;"
echo "   4. Run: sudo systemctl reload nginx"
echo ""
