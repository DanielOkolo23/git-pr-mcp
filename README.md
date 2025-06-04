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

The server runs in SSE mode by default on `0.0.0.0:9999` and is configured via environment variables.

**Environment Variables:**
- `MCP_HOST`: Host to bind to (default: `0.0.0.0`)
- `MCP_PORT`: Port to bind to (default: `9999`)
- `GITHUB_TOKEN` (Required for `create_github_pr`): A GitHub Personal Access Token with permissions to create pull requests and access repository information. The server will fail to start if this is not set.

### Quick Start

```bash
# Run with defaults (0.0.0.0:8000)
uv run python main.py

# Or run the server module directly
uv run python -m src.git_pr_mcp.server
```

### Configuration

Configure the server using environment variables:

- `MCP_HOST`: Host to bind to (default: `0.0.0.0`)
- `MCP_PORT`: Port to bind to (default: `8000`)

### Examples

```bash
# Default configuration
uv run python main.py

# Custom host and port
MCP_HOST=localhost MCP_PORT=3000 uv run python main.py

# Bind to all interfaces on port 9000
MCP_PORT=9000 uv run python main.py
```

## Server Endpoints

The server provides:
- **Base URL**: `http://0.0.0.0:8000/` (or your configured host:port)
- **Built-in SSE endpoints** for MCP protocol communication
- **Health check and introspection** endpoints provided by FastMCP

## MCP Tools

This section details the available tools. Some tools operate on a `repo_path` you provide, while newer tools (related to the automated PR workflow) operate on an "active" repository that is set by the `clone_repository` tool.

### Tools Operating on a Specified `repo_path`

These tools require you to specify the path to the target Git repository.

#### get_git_status

Get the current git status of the repository.

**Parameters:**
- `repo_path` (optional): Path to the git repository (defaults to current directory)

#### list_branches

List all branches in the repository.

**Parameters:**
- `repo_path` (optional): Path to the git repository (defaults to current directory)
- `remote` (optional): Include remote branches (default: false)

#### create_pr_summary

Create a summary for a pull request based on git diff.

**Parameters:**
- `base_branch` (required): Base branch to compare against
- `head_branch` (optional): Head branch (defaults to current branch)
- `repo_path` (optional): Path to the git repository (defaults to current directory)

#### get_commit_history

Get commit history for a branch.

**Parameters:**
- `branch` (optional): Branch name (defaults to current branch)
- `limit` (optional): Maximum number of commits to return (default: 10)
- `repo_path` (optional): Path to the git repository (defaults to current directory)

#### get_git_diff

Get git diff between commits, branches, or working directory.

**Parameters:**
- `target` (optional): Target to diff against (commit hash, branch name, etc.). Defaults to working directory vs HEAD
- `repo_path` (optional): Path to the git repository (defaults to current directory)

### Tools Operating on the "Active" Repository

These tools operate on a repository cloned and managed by the `clone_repository` tool. The server internally tracks this "active" repository.

#### clone_repository

Clones a GitHub repository into a new temporary local directory, cleans up any previously cloned one, and sets it as the active repository for subsequent operations. It also attempts to parse the repository owner and name from the URL for use with GitHub operations. The state of the active repository is saved to `active_repo_state.json`.

**Parameters:**
- `repo_url` (required): The URL of the GitHub repository (e.g., `https://github.com/user/repo.git`).

**Returns:**
- A message indicating success or failure, including the temporary path and parsed owner/name if successful.

#### create_git_branch

Creates a new branch in the active local git repository.

**Parameters:**
- `branch_name` (required): The name of the new branch to create.
- `base_branch` (optional): The base branch to create the new branch from (defaults to the current HEAD of the active repository).

**Returns:**
- A success or error message.

#### write_file_in_repo

Creates a new file or overwrites an existing file with specified content within the active repository. Ensures parent directories are created if they don't exist.

**Parameters:**
- `relative_file_path` (required): The path of the file relative to the active repository's root (e.g., `src/my_module.py`, `README.md`).
- `content` (required): The string content to write to the file.

**Returns:**
- A success or error message, including the full path to the written file.

#### git_commit_changes

Stages all changes (`git add .`) and commits them with a given message in the active repository.

**Parameters:**
- `commit_message` (required): The commit message.

**Returns:**
- A success or error message, or a message indicating no changes to commit.

#### git_push_branch

Pushes a local branch from the active repository to its remote `origin`.

**Parameters:**
- `branch_name` (required): The name of the local branch in the active repository to push.
- `set_upstream` (optional): If true (default), sets the upstream tracking information (`git push -u origin <branch_name>`).

**Returns:**
- A success or error message, including output from the git command.

#### create_github_pr

Creates a pull request on GitHub for the active repository using the PyGithub library.
**Requires the `GITHUB_TOKEN` environment variable to be set.** The owner and repository name are determined from the URL provided during the `clone_repository` step.

**Parameters:**
- `title` (required): The title of the pull request.
- `body` (required): The body/description of the pull request.
- `base_branch` (required): The name of the branch you want the changes pulled into (e.g., `main`, `develop`).
- `head_branch` (required): The name of the branch where your changes are implemented (this branch must have been pushed to the remote).

**Returns:**
- A success message with the URL of the created PR, or an error message.

## Development

### Project Structure

```
src/git_pr_mcp/
├── __init__.py          # Package initialization
└── server.py            # Main MCP server implementation using FastMCP
main.py                  # Entry point
```

### Adding New Tools

Adding new tools is simple with FastMCP decorators:

```python
@mcp.tool(
    name="your_new_tool",
    description="Description of your new tool",
)
def your_new_tool(
    ctx: Context,
    param: Annotated[str, "Parameter description"],
    optional_param: Annotated[Optional[str], "Optional parameter description"] = None,
) -> str:
    """Handle your new tool."""
    try:
        ctx.info(f"Executing tool with param: {param}")
        # Tool implementation here
        result = f"Tool result for: {param}"
        return result
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        ctx.error(error_msg)
        return error_msg
```

## Requirements

- Python 3.11+
- Git (for git operations)
- Dependencies listed in `pyproject.toml`

## License

This project is licensed under the MIT License - see the LICENSE file for details.
