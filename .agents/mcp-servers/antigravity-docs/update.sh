#!/bin/bash

echo "Refreshing Antigravity Docs MCP Knowledge Base..."
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$DIR"

echo ""
echo "Step 1: Scraping latest links..."
./venv/bin/python scraper.py

echo ""
echo "Step 2: Downloading latest documentation text..."
./venv/bin/python extractor.py

echo ""
echo "✅ Refresh complete! The MCP server will serve the new files automatically."
