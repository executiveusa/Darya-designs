#!/bin/bash
set -e

echo "🚀 OpenHands Studio - Hostinger Deployment Script"
echo "=================================================="

# Configuration
DEPLOY_USER="${DEPLOY_USER:-openhands}"
DEPLOY_HOST="${DEPLOY_HOST:-your-hostinger-server.com}"
DEPLOY_PATH="${DEPLOY_PATH:-/home/openhands/openhands-studio}"
DOMAIN="${DOMAIN:-your-domain.com}"

echo "📦 Building Docker image..."
docker build -f containers/app/Dockerfile -t openhands-studio:latest .

echo "💾 Saving Docker image..."
docker save openhands-studio:latest | gzip > openhands-studio.tar.gz

echo "📤 Uploading to Hostinger..."
scp openhands-studio.tar.gz ${DEPLOY_USER}@${DEPLOY_HOST}:${DEPLOY_PATH}/

echo "🔧 Deploying on server..."
ssh ${DEPLOY_USER}@${DEPLOY_HOST} << 'ENDSSH'
cd $DEPLOY_PATH

# Load Docker image
echo "Loading Docker image..."
docker load < openhands-studio.tar.gz
rm openhands-studio.tar.gz

# Stop old container
echo "Stopping old container..."
docker stop openhands-studio 2>/dev/null || true
docker rm openhands-studio 2>/dev/null || true

# Start new container
echo "Starting new container..."
docker run -d \
  --name openhands-studio \
  --restart unless-stopped \
  -p 3000:3000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v $(pwd)/workspace:/opt/workspace_base \
  -v $(pwd)/data:/.openhands \
  -e STUDIO_ENABLED=true \
  -e LLM_API_KEY=${LLM_API_KEY} \
  -e LLM_MODEL=${LLM_MODEL:-anthropic/claude-3-5-sonnet-20241022} \
  -e SANDBOX_RUNTIME_CONTAINER_IMAGE=docker.all-hands.dev/openhands/runtime:0.59-nikolaik \
  --add-host host.docker.internal:host-gateway \
  openhands-studio:latest

echo "✅ Container started successfully!"

# Show logs
docker logs --tail 50 openhands-studio
ENDSSH

echo ""
echo "✅ Deployment complete!"
echo "🌐 Backend should be accessible at: https://${DOMAIN}"
echo "📝 Next steps:"
echo "   1. Configure Nginx/Apache reverse proxy"
echo "   2. Set up SSL certificate"
echo "   3. Update Vercel environment variables"
