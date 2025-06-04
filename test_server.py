#!/usr/bin/env python3
"""Simple test script for the Git PR MCP server."""

def test_server():
    """Test the MCP server by importing and checking basic functionality."""
    print("Testing Git PR MCP Server...")
    print("=" * 50)
    
    # Test server import and creation
    print("\n1. Testing server import...")
    try:
        from src.git_pr_mcp.server import mcp
        print(f"✓ Server imported successfully: {mcp.name}")
    except Exception as e:
        print(f"✗ Error importing server: {e}")
        return
    
    # Test individual tool functions
    print("\n2. Testing individual tool functions...")
    
    # Mock context for testing
    class MockContext:
        def info(self, msg):
            print(f"  INFO: {msg}")
        def error(self, msg):
            print(f"  ERROR: {msg}")
    
    mock_ctx = MockContext()
    
    # Test get_git_status
    print("\n  Testing get_git_status...")
    try:
        from src.git_pr_mcp.server import get_git_status
        result = get_git_status(mock_ctx, ".")
        print(f"  ✓ Result: {result[:100]}...")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    # Test list_branches
    print("\n  Testing list_branches...")
    try:
        from src.git_pr_mcp.server import list_branches
        result = list_branches(mock_ctx, ".", False)
        print(f"  ✓ Result: {result[:100]}...")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    # Test get_commit_history
    print("\n  Testing get_commit_history...")
    try:
        from src.git_pr_mcp.server import get_commit_history
        result = get_commit_history(mock_ctx, None, 5, ".")
        print(f"  ✓ Result: {result[:100]}...")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    # Test get_git_diff
    print("\n  Testing get_git_diff...")
    try:
        from src.git_pr_mcp.server import get_git_diff
        result = get_git_diff(mock_ctx, None, ".")
        print(f"  ✓ Result: {result[:100]}...")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    print("\n" + "=" * 50)
    print("Basic test completed!")
    print("\nTo run the Git PR MCP Server:")
    print("  Default (0.0.0.0:8000):     uv run python main.py")
    print("  Custom host/port:           MCP_HOST=localhost MCP_PORT=3000 uv run python main.py")

if __name__ == "__main__":
    test_server() 