# Antigravity Docs MCP
A Model Context Protocol (MCP) server that provides AI agents with up-to-date documentation for the Antigravity IDE. It includes a built-in scraper to automatically fetch and update the latest docs directly into a local knowledge base.

## Features
- **Server:** Provides `docs://index` to list pages, and tools `list_document_names` and `search_docs` to find relevant information.
- **Scraper & Extractor:** Python scripts powered by Playwright to crawl the Antigravity Docs site and extract readable Markdown.
- **Auto-Updater:** A single bash script `update.sh` to fully automate the parsing of the site and injecting the content into the `knowledge_base/` folder.

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/imgt511/Antigravity_Docs_MCP.git
cd Antigravity_Docs_MCP
```

### 2. Setup the Python Environment (For the Scraper)
The scraper uses Python and Playwright. Build a local virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install playwright
playwright install
```

### 3. Setup the Node Environment (For the Server)
The MCP server itself is served using the official MCP Node SDK.
```bash
npm install
```

## Usage

### Connecting the MCP Server to Antigravity IDE
Point your Antigravity IDE settings (or any other MCP-compatible client) to execute the Node.js server:
```json
{
  "mcpServers": {
    "antigravity-docs": {
      "command": "node",
      "args": ["/absolute/path/to/Antigravity_Docs_MCP/mcp_server.js"]
    }
  }
}
```

## How to Refresh the Knowledge Base
When new updates are released for the Antigravity IDE, you can easily pull the latest documentation yourself!

### The Easy Way
Simply run the included update script from inside the project directory:
```bash
./update.sh
```

### What it does:
1. Runs `scraper.py` to find any new pages on the website.
2. Runs `extractor.py` to overwrite your `knowledge_base/` folder with the newest text.
3. Your MCP server instantly starts using the new files. There is no need to restart anything!

## Daily Catchup Log
- **Update:** 2026-03-13 21:03:50 - Automated Catchup push.
- **Update:** 2026-03-17 20:29:47 - Automated Catchup push.
