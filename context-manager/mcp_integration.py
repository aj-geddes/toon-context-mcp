#!/usr/bin/env python3
"""
MCP Server Integration
Helper for integrating TOON optimization with existing MCP servers.
"""

import json
from typing import Dict, List, Any
from pathlib import Path


class MCPConfigManager:
    """
    Manages MCP configuration with TOON integration.
    """

    def __init__(self, config_path: Path = None):
        """
        Initialize config manager.

        Args:
            config_path: Path to MCP config file
        """
        self.config_path = config_path or Path.home() / ".config" / "claude" / "mcp_settings.json"
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """Load MCP configuration."""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return {"mcpServers": {}}

    def _save_config(self) -> None:
        """Save MCP configuration."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)

    def add_toon_server(self) -> None:
        """Add TOON MCP server to configuration."""
        toon_server_config = {
            "command": "python",
            "args": ["-m", "mcp-server-toon.src.server"],
            "description": "TOON Token Optimization Server"
        }

        if "mcpServers" not in self.config:
            self.config["mcpServers"] = {}

        self.config["mcpServers"]["toon"] = toon_server_config
        self._save_config()

    def enable_toon_for_server(self, server_name: str) -> None:
        """
        Enable TOON optimization for an existing server.

        Args:
            server_name: Name of the MCP server
        """
        if "mcpServers" not in self.config:
            raise ValueError("No MCP servers configured")

        if server_name not in self.config["mcpServers"]:
            raise ValueError(f"Server '{server_name}' not found")

        # Add TOON environment variables
        server_config = self.config["mcpServers"][server_name]
        if "env" not in server_config:
            server_config["env"] = {}

        server_config["env"]["TOON_OPTIMIZE"] = "true"
        server_config["env"]["TOON_MIN_SAVINGS"] = "15"

        self._save_config()

    def get_server_list(self) -> List[str]:
        """Get list of configured MCP servers."""
        return list(self.config.get("mcpServers", {}).keys())

    def export_config(self) -> str:
        """Export configuration as JSON string."""
        return json.dumps(self.config, indent=2)


def generate_integration_example() -> str:
    """
    Generate example integration code.

    Returns:
        Example integration code
    """
    return '''
# MCP Server Integration with TOON

## Quick Start

### 1. Add TOON to your MCP configuration

```json
{
  "mcpServers": {
    "toon": {
      "command": "python",
      "args": ["-m", "mcp-server-toon.src.server"]
    }
  }
}
```

### 2. Use TOON tools in your workflow

```python
# Example: Convert large API response
api_response = {
    "users": [
        {"id": i, "name": f"User {i}", "status": "active"}
        for i in range(100)
    ]
}

# Call TOON MCP tool
result = await mcp_client.call_tool(
    "convert_to_toon",
    {"json_data": json.dumps(api_response)}
)

print(f"Saved {result['savings']['savings_percent']}% tokens!")
```

### 3. Enable automatic optimization for existing servers

```python
from context_manager.mcp_integration import MCPConfigManager

config_manager = MCPConfigManager()

# Add TOON server
config_manager.add_toon_server()

# Enable TOON for existing server
config_manager.enable_toon_for_server("my-api-server")
```

### 4. Use the proactive optimizer

```python
from context_manager.tool_output_optimizer import ToolOutputOptimizer

optimizer = ToolOutputOptimizer(auto_optimize=True, min_savings=15.0)

# Automatically optimize tool output
optimized_response = optimizer.create_optimized_response(
    "api_call",
    large_api_response
)
```
'''


def main():
    """Demo of MCP integration."""
    print("MCP Integration Helper")
    print("=" * 60)

    # Example configuration
    example_config = {
        "mcpServers": {
            "filesystem": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/files"]
            },
            "github": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-github"],
                "env": {
                    "GITHUB_TOKEN": "your-token"
                }
            }
        }
    }

    print("\nOriginal Config:")
    print(json.dumps(example_config, indent=2))

    # Add TOON
    example_config["mcpServers"]["toon"] = {
        "command": "python",
        "args": ["-m", "mcp-server-toon.src.server"]
    }

    print("\n\nWith TOON Added:")
    print(json.dumps(example_config, indent=2))

    print("\n\nIntegration Example:")
    print(generate_integration_example())


if __name__ == "__main__":
    main()
