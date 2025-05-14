#!/bin/bash

echo "🔧 Starting Render-friendly setup..."

# Exit on any error
set -e

echo "📦 Installing Python dependencies for parler tts..."
pip install 'transformers>=4.33.2'
pip install torch
pip install parler_tts 
pip install soundfile
pip install dotenv
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
