# Git PR MCP Server

A Model Context Protocol (MCP) server for Git and Pull Request operations, providing tools for repository management and PR workflows.

Built with FastMCP and runs in SSE mode by default on `0.0.0.0:8000`.

## Features

This MCP server provides the following tools and capabilities:

**Core Git Operations (on specified repository path):**
- **get_git_status**: Get the current git status of a repository.
- **list_branches**: List all branches in the repository (with optional remote branches).
- **create_pr_summary**: Create a summary for a pull request based on git diff.
- **get_commit_history**: Get commit history for a branch.
- **get_git_diff**: Get git diff between commits, branches, or working directory.

**Automated PR Workflow (operates on an internally managed "active" repository):**
- **clone_repository**: Clones a GitHub repository into a managed temporary directory, making it the "active" repository for subsequent operations. Automatically cleans up any previously active repository's temporary directory.
- **create_git_branch**: Creates a new branch in the active repository.
- **write_file_in_repo**: Creates or overwrites files within the active repository.
- **git_commit_changes**: Stages all changes (`git add .`) and commits them in the active repository.
- **git_push_branch**: Pushes a specified branch from the active repository to its remote origin.
- **create_github_pr**: Creates a pull request on GitHub for the active repository using the PyGithub library. Requires `GITHUB_TOKEN`.

**State Management:**
- The server maintains the state of the currently "active" cloned repository (path, URL, owner, name) in an `active_repo_state.json` file. This allows some persistence across server restarts, though the temporary clone directory itself might be OS-managed.

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd git-pr-mcp
```

2. Install using uv:
```bash
uv sync
```

## Usage

The server runs in SSE mode by default on `0.0.0.0:9999` and is configured via environment variables. Here's a sample .env file:

```
FASTMCP_HOST=0.0.0.0
FASTMCP_PORT=9999
GITHUB_TOKEN=your_github_token
```

### Quick Start

```bash
# Run with defaults (0.0.0.0:8000)
uv run python main.py

# Or run the server module directly
uv run python -m src.git_pr_mcp.server
```

You can then access the MCP server at `http://localhost:9999/sse`.