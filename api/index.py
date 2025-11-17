"""
Vercel serverless function entry point
This file imports and exports the Flask app for Vercel
"""
import sys
import os

# Add parent directory to path so we can import from src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import the Flask app
from main import app

# Export for Vercel
# Vercel looks for 'app' or 'application' variable
application = app

