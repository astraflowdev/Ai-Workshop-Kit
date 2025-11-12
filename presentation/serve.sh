#!/bin/bash

# AI Workshop Presentation - Local Server Launcher
# This script starts a simple HTTP server to serve the presentation

echo "🚀 Starting AI Workshop Presentation Server..."
echo ""
echo "📊 Server will be available at:"
echo "   http://localhost:8000"
echo ""
echo "⌨️  Press Ctrl+C to stop the server"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if Python 3 is available
if command -v python3 &> /dev/null
then
    python3 -m http.server 8000
# Check if Python 2 is available
elif command -v python &> /dev/null
then
    python -m SimpleHTTPServer 8000
else
    echo "❌ Python not found. Please install Python or use:"
    echo "   npx serve"
    exit 1
fi
