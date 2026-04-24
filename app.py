# Vercel serverless entry point - re-exports the FastAPI app
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from api.main import app
