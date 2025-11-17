#!/usr/bin/env python3
"""
Tool Output Optimizer
Proactively converts tool outputs to TOON format for context efficiency.
"""

import json
import re
from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "mcp-server-toon"))
from src.toon_converter import TOONConverter
from src.patterns import PatternDetector


class ToolOutputOptimizer:
    """
    Optimizes MCP tool outputs for reduced token consumption.
    """

    def __init__(self, auto_optimize: bool = True, min_savings: float = 15.0):
        """
        Initialize tool output optimizer.

        Args:
            auto_optimize: Automatically optimize outputs above threshold
            min_savings: Minimum savings percentage to trigger optimization
        """
        self.auto_optimize = auto_optimize
        self.min_savings = min_savings
        self.converter = TOONConverter()
        self.detector = PatternDetector()

        # Track optimizations
        self.optimization_stats = {
            'total_outputs': 0,
            'optimized_outputs': 0,
            'total_tokens_saved': 0
        }

    def optimize_tool_output(self, tool_name: str, output: Any) -> Tuple[Any, Dict[str, Any]]:
        """
        Optimize a tool's output.

        Args:
            tool_name: Name of the tool
            output: Tool output (any JSON-serializable data)

        Returns:
            Tuple of (optimized_output, optimization_metadata)
        """
        self.optimization_stats['total_outputs'] += 1

        # Convert to JSON string for analysis
        if isinstance(output, str):
            try:
                output = json.loads(output)
            except json.JSONDecodeError:
                # Not JSON, return as-is
                return output, {'optimized': False, 'reason': 'not_json'}

        output_json = json.dumps(output, indent=2)

        # Detect patterns
        patterns = self.detector.analyze(output)

        # Convert to TOON
        toon_output = self.converter.json_to_toon(output)

        # Calculate savings
        savings = self.converter.calculate_savings(output_json, toon_output)

        metadata = {
            'tool_name': tool_name,
            'original_tokens': savings['original_tokens'],
            'toon_tokens': savings['toon_tokens'],
            'tokens_saved': savings['tokens_saved'],
            'savings_percent': savings['savings_percent'],
            'patterns_detected': [p.pattern_type for p in patterns[:3]],
            'optimized': False
        }

        # Decide whether to optimize
        if self.auto_optimize and savings['savings_percent'] >= self.min_savings:
            self.optimization_stats['optimized_outputs'] += 1
            self.optimization_stats['total_tokens_saved'] += savings['tokens_saved']

            metadata['optimized'] = True
            metadata['optimization_note'] = (
                f"Optimized with TOON format. Saved {savings['savings_percent']:.1f}% tokens. "
                f"Use convert_toon_to_json to restore original format if needed."
            )

            return toon_output, metadata

        return output, metadata

    def create_optimized_response(self, tool_name: str, output: Any) -> str:
        """
        Create an optimized response for tool output.

        Args:
            tool_name: Name of the tool
            output: Tool output

        Returns:
            Formatted response string
        """
        optimized_output, metadata = self.optimize_tool_output(tool_name, output)

        if metadata['optimized']:
            response = f"""Tool: {tool_name}

Output (TOON format):
{optimized_output}

💡 Optimization: Saved {metadata['savings_percent']:.1f}% tokens ({metadata['tokens_saved']} tokens)

To restore original format:
```python
from toon_converter import convert_toon_to_json
original = convert_toon_to_json('''{optimized_output}''')
```
"""
        else:
            response = f"""Tool: {tool_name}

Output:
{json.dumps(optimized_output, indent=2) if not isinstance(optimized_output, str) else optimized_output}
"""

        return response

    def batch_optimize(self, tool_outputs: List[Tuple[str, Any]]) -> List[Tuple[str, Any, Dict]]:
        """
        Batch optimize multiple tool outputs.

        Args:
            tool_outputs: List of (tool_name, output) tuples

        Returns:
            List of (tool_name, optimized_output, metadata) tuples
        """
        results = []

        for tool_name, output in tool_outputs:
            optimized, metadata = self.optimize_tool_output(tool_name, output)
            results.append((tool_name, optimized, metadata))

        return results

    def get_stats(self) -> Dict[str, Any]:
        """
        Get optimization statistics.

        Returns:
            Statistics dictionary
        """
        stats = self.optimization_stats.copy()
        stats['optimization_rate'] = (
            stats['optimized_outputs'] / stats['total_outputs'] * 100
            if stats['total_outputs'] > 0
            else 0
        )
        stats['avg_tokens_saved'] = (
            stats['total_tokens_saved'] / stats['optimized_outputs']
            if stats['optimized_outputs'] > 0
            else 0
        )

        return stats


class MCPIntegrationMiddleware:
    """
    Middleware for integrating TOON optimization with MCP servers.
    """

    def __init__(self, optimizer: Optional[ToolOutputOptimizer] = None):
        """
        Initialize MCP integration middleware.

        Args:
            optimizer: Optional ToolOutputOptimizer instance
        """
        self.optimizer = optimizer or ToolOutputOptimizer()
        self.tool_configs: Dict[str, Dict] = {}

    def register_tool(self, tool_name: str, config: Dict[str, Any]) -> None:
        """
        Register a tool for optimization.

        Args:
            tool_name: Name of the tool
            config: Configuration dictionary
                - auto_optimize: bool
                - min_savings: float
                - exclude_fields: List[str]
        """
        self.tool_configs[tool_name] = config

    def intercept_tool_output(self, tool_name: str, output: Any) -> Tuple[Any, Dict]:
        """
        Intercept and potentially optimize tool output.

        Args:
            tool_name: Name of the tool
            output: Tool output

        Returns:
            Tuple of (potentially_optimized_output, metadata)
        """
        # Check if tool has custom config
        if tool_name in self.tool_configs:
            config = self.tool_configs[tool_name]

            # Check if optimization is enabled for this tool
            if not config.get('auto_optimize', True):
                return output, {'optimized': False, 'reason': 'disabled'}

            # Apply exclusions if any
            if config.get('exclude_fields'):
                output = self._exclude_fields(output, config['exclude_fields'])

        return self.optimizer.optimize_tool_output(tool_name, output)

    def _exclude_fields(self, data: Any, exclude_fields: List[str]) -> Any:
        """Remove specified fields from data before optimization."""
        if isinstance(data, dict):
            return {k: v for k, v in data.items() if k not in exclude_fields}
        elif isinstance(data, list):
            return [self._exclude_fields(item, exclude_fields) for item in data]
        return data

    def create_proxy_server_config(self) -> Dict[str, Any]:
        """
        Create configuration for proxy MCP server with TOON optimization.

        Returns:
            Configuration dictionary
        """
        return {
            "name": "toon-optimizer-proxy",
            "description": "Proxy MCP server that optimizes tool outputs with TOON",
            "version": "1.0.0",
            "features": [
                "automatic_toon_conversion",
                "token_usage_monitoring",
                "pattern_detection"
            ],
            "settings": {
                "auto_optimize": self.optimizer.auto_optimize,
                "min_savings_percent": self.optimizer.min_savings,
                "registered_tools": list(self.tool_configs.keys())
            }
        }


class SmartToolWrapper:
    """
    Wraps existing MCP tools with TOON optimization.
    """

    def __init__(self, tool_function, tool_name: str, optimizer: ToolOutputOptimizer):
        """
        Initialize wrapper.

        Args:
            tool_function: Original tool function
            tool_name: Name of the tool
            optimizer: ToolOutputOptimizer instance
        """
        self.tool_function = tool_function
        self.tool_name = tool_name
        self.optimizer = optimizer

    async def __call__(self, *args, **kwargs):
        """
        Call the tool and optimize output.
        """
        # Call original tool
        result = await self.tool_function(*args, **kwargs)

        # Optimize output
        optimized_result, metadata = self.optimizer.optimize_tool_output(
            self.tool_name,
            result
        )

        # Add metadata to result
        if isinstance(optimized_result, dict):
            optimized_result['_toon_metadata'] = metadata
        elif isinstance(optimized_result, str):
            try:
                result_obj = json.loads(optimized_result)
                result_obj['_toon_metadata'] = metadata
                optimized_result = json.dumps(result_obj)
            except:
                pass

        return optimized_result


def create_optimizing_mcp_config(base_servers: Dict[str, Dict]) -> Dict[str, Dict]:
    """
    Create MCP configuration with TOON optimization enabled.

    Args:
        base_servers: Original MCP server configurations

    Returns:
        Modified configuration with TOON optimization
    """
    optimized_config = base_servers.copy()

    # Add TOON server
    optimized_config['toon'] = {
        "command": "python",
        "args": ["-m", "mcp-server-toon.src.server"],
        "description": "TOON optimization server"
    }

    # Add optimizer proxy for each server
    for server_name, server_config in base_servers.items():
        proxy_name = f"{server_name}_toon_proxy"
        optimized_config[proxy_name] = {
            **server_config,
            "description": f"TOON-optimized {server_name}",
            "env": {
                **server_config.get("env", {}),
                "TOON_OPTIMIZE": "true",
                "TOON_MIN_SAVINGS": "15"
            }
        }

    return optimized_config


def main():
    """Demo of tool output optimizer."""
    optimizer = ToolOutputOptimizer(auto_optimize=True, min_savings=15.0)

    # Simulate tool outputs
    sample_outputs = [
        ("file_search", {
            "results": [
                {
                    "file_path": f"/path/to/file{i}.py",
                    "line_number": i * 10,
                    "content": f"def function_{i}():",
                    "match_type": "exact"
                }
                for i in range(15)
            ],
            "total_matches": 15,
            "search_time_ms": 42
        }),
        ("api_call", {
            "status": "success",
            "data": {
                "users": [
                    {"id": i, "name": f"User {i}", "email": f"user{i}@test.com"}
                    for i in range(10)
                ]
            },
            "metadata": {"timestamp": "2025-01-01T00:00:00Z"}
        })
    ]

    print("="*60)
    print("Tool Output Optimization Demo")
    print("="*60)

    for tool_name, output in sample_outputs:
        print(f"\n{tool_name}:")
        print("-" * 60)

        response = optimizer.create_optimized_response(tool_name, output)
        print(response)

    # Show stats
    stats = optimizer.get_stats()
    print("\n" + "="*60)
    print("Optimization Statistics")
    print("="*60)
    print(f"Total Outputs: {stats['total_outputs']}")
    print(f"Optimized: {stats['optimized_outputs']} ({stats['optimization_rate']:.1f}%)")
    print(f"Total Tokens Saved: {stats['total_tokens_saved']}")
    print(f"Avg Tokens Saved: {stats['avg_tokens_saved']:.1f}")


if __name__ == "__main__":
    main()
