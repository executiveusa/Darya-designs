"""
FastAPI app entry point for Vercel deployment.
This is a simple wrapper that imports the actual app from openhands.server.listen
"""

from openhands.server.listen import app

# Export app for Vercel serverless functions
__all__ = ["app"]
