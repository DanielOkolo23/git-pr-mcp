from dotenv import load_dotenv
load_dotenv()

from src.git_pr_mcp.server import mcp

if __name__ == "__main__":
    print("Starting Git PR MCP Server")
    mcp.run(transport="sse")
