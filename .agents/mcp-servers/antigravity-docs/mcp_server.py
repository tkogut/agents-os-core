import os
import json
from mcp.server.fastmcp import FastMCP

# Create the MCP server instance
mcp = FastMCP("Antigravity_Docs")

KB_DIR = "knowledge_base"

@mcp.resource("docs://index")
def list_docs() -> str:
    """Returns an index of all available Antigravity documentation pages."""
    if not os.path.exists(KB_DIR):
        return "Knowledge base directory not found."
    
    files = sorted(os.listdir(KB_DIR))
    index = "# Antigravity Documentation Index\n\n"
    for f in files:
        if f.endswith(".md"):
            index += f"- {f}\n"
    return index

@mcp.tool()
def search_docs(query: str) -> str:
    """Searches the Antigravity documentation for a specific keyword or phrase."""
    if not os.path.exists(KB_DIR):
        return "Knowledge base directory not found."
        
    results = []
    for filename in sorted(os.listdir(KB_DIR)):
        if filename.endswith(".md"):
            path = os.path.join(KB_DIR, filename)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                if query.lower() in content.lower():
                    results.append(filename)
                    
    if not results:
        return f"No results found for '{query}'."
        
    response = f"Found '{query}' in the following documents:\n"
    for r in results:
        response += f"- {r}\n"
    response += "\nUse read_doc(filename) to read the full content of a specific page."
    return response

@mcp.tool()
def read_doc(filename: str) -> str:
    """Reads the full content of a specific documentation file. 
    Provide the exact filename, e.g., '01_Home.md'."""
    path = os.path.join(KB_DIR, filename)
    if not os.path.exists(path):
        return f"Error: File '{filename}' not found."
        
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    # This runs the MCP server via standard input/output (stdio)
    print("Starting Antigravity Docs MCP Server...")
    mcp.run()
