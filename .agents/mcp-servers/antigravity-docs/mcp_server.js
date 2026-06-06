import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

// Emulate __dirname
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const KB_DIR = path.join(__dirname, "knowledge_base");

// Create MCP server instance
const server = new Server(
  {
    name: "Antigravity_Docs",
    version: "1.0.0",
  },
  {
    capabilities: {
      resources: {},
      tools: {},
    },
  }
);

/**
 * Handle listing available documentation pages as Resources
 */
server.setRequestHandler(ListResourcesRequestSchema, async () => {
  if (!fs.existsSync(KB_DIR)) {
    return { resources: [] };
  }

  const files = fs.readdirSync(KB_DIR).filter((file) => file.endsWith(".md"));
  const resources = files.map((file) => ({
    uri: `docs://index/${file}`,
    name: `Antigravity Docs: ${file}`,
    mimeType: "text/markdown",
    description: `Full documentation content for ${file}`,
  }));

  return { resources };
});

/**
 * Handle reading a specific documentation page
 */
server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const uri = request.params.uri;
  const match = uri.match(/^docs:\/\/index\/(.+)$/);

  if (!match) {
    throw new Error(`Invalid URI format. Expected docs://index/<filename>`);
  }

  const filename = match[1];
  const filePath = path.join(KB_DIR, filename);

  if (!fs.existsSync(filePath)) {
    throw new Error(`File ${filename} not found.`);
  }

  const content = fs.readFileSync(filePath, "utf-8");

  return {
    contents: [
      {
        uri,
        mimeType: "text/markdown",
        text: content,
      },
    ],
  };
});

/**
 * Handle listing tools (Search keyword)
 */
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "search_docs",
        description:
          "Searches the Antigravity documentation for a specific keyword or phrase.",
        inputSchema: {
          type: "object",
          properties: {
            query: {
              type: "string",
              description: "The keyword or phrase to search for.",
            },
          },
          required: ["query"],
        },
      },
      {
        name: "list_document_names",
        description:
          "Returns the exact filenames of all available Antigravity documentation pages located in the knowledge base.",
        inputSchema: {
          type: "object",
          properties: {},
        },
      },
    ],
  };
});

/**
 * Handle execution of tools
 */
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "list_document_names") {
    if (!fs.existsSync(KB_DIR)) {
      return {
        content: [{ type: "text", text: "Knowledge base directory not found." }],
      };
    }
    const files = fs.readdirSync(KB_DIR).filter((file) => file.endsWith(".md"));
    return {
      content: [
        {
          type: "text",
          text: `Available documents:\n${files.join("\n")}`,
        },
      ],
    };
  }

  if (request.params.name === "search_docs") {
    const query = String(request.params.arguments?.query || "").toLowerCase();

    if (!fs.existsSync(KB_DIR)) {
      return {
        content: [{ type: "text", text: "Knowledge base directory not found." }],
      };
    }

    const files = fs.readdirSync(KB_DIR).filter((file) => file.endsWith(".md"));
    const matches = [];

    for (const filename of files) {
      const filePath = path.join(KB_DIR, filename);
      const content = fs.readFileSync(filePath, "utf-8").toLowerCase();
      if (content.includes(query)) {
        matches.push(filename);
      }
    }

    if (matches.length === 0) {
      return {
        content: [{ type: "text", text: `No results found for '${query}'.` }],
      };
    }

    let resultText = `Found '${query}' in the following documents:\n`;
    for (const match of matches) {
      resultText += `- ${match}\n`;
    }
    resultText += `\nUse read_resource(docs://index/<filename>) to read the full content.`;

    return {
      content: [{ type: "text", text: resultText }],
    };
  }

  throw new Error("Tool not found");
});

// Run server using standard I/O transport
async function startServer() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Antigravity Docs MCP Server running on stdio");
}

startServer().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
