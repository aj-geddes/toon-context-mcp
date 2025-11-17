"""
TOON MCP Server
Model Context Protocol server for TOON conversions.
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional

from mcp.server import Server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)
import mcp.server.stdio

from .toon_converter import TOONConverter, convert_json_to_toon, convert_toon_to_json
from .patterns import PatternDetector, SmartCompressionStrategy

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("toon-mcp-server")


class TOONMCPServer:
    """MCP Server for TOON conversions."""

    def __init__(self):
        """Initialize the TOON MCP server."""
        self.server = Server("toon-mcp-server")
        self.converter = TOONConverter()
        self.detector = PatternDetector()
        self.strategy = SmartCompressionStrategy(self.detector)

        # Statistics
        self.conversion_count = 0
        self.total_tokens_saved = 0

        # Setup handlers
        self._setup_handlers()

    def _setup_handlers(self):
        """Set up MCP protocol handlers."""

        @self.server.list_resources()
        async def list_resources() -> List[Resource]:
            """List available resources."""
            return [
                Resource(
                    uri="toon://stats",
                    name="TOON Conversion Statistics",
                    mimeType="application/json",
                    description="Statistics about TOON conversions"
                ),
                Resource(
                    uri="toon://guide",
                    name="TOON Format Guide",
                    mimeType="text/markdown",
                    description="Guide to TOON format and best practices"
                )
            ]

        @self.server.read_resource()
        async def read_resource(uri: str) -> str:
            """Read a resource."""
            if uri == "toon://stats":
                stats = {
                    "conversion_count": self.conversion_count,
                    "total_tokens_saved": self.total_tokens_saved,
                    "average_savings": (
                        self.total_tokens_saved / self.conversion_count
                        if self.conversion_count > 0
                        else 0
                    )
                }
                return json.dumps(stats, indent=2)

            elif uri == "toon://guide":
                return """# TOON Format Guide

## What is TOON?

TOON (Token-Optimized Object Notation) is a compact representation format
for JSON data that reduces token consumption in AI-assisted development.

## Key Features

1. **Abbreviated Keys**: Common keys like 'id', 'name', 'type' are shortened
2. **Schema Compression**: Arrays of similar objects use schema-based encoding
3. **Reference System**: Repeated structures are referenced
4. **Compact Values**: Null (~), Boolean (T/F), and optimized strings

## Example

Original JSON:
```json
{
  "id": 123,
  "name": "John Doe",
  "type": "user",
  "status": "active"
}
```

TOON Format:
```json
{"_toon":"1.0","d":{"i":123,"n":"John Doe","t":"user","s":"active"}}
```

## Best Practices

- Use TOON for large API responses
- Enable aggressive mode for maximum compression
- Monitor savings with the stats resource
- Use pattern detection for optimal results
"""

            raise ValueError(f"Unknown resource: {uri}")

        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            """List available tools."""
            return [
                Tool(
                    name="convert_to_toon",
                    description="Convert JSON to TOON format",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "json_data": {
                                "type": "string",
                                "description": "JSON data to convert (as string)"
                            },
                            "aggressive": {
                                "type": "boolean",
                                "description": "Use aggressive compression",
                                "default": False
                            }
                        },
                        "required": ["json_data"]
                    }
                ),
                Tool(
                    name="convert_to_json",
                    description="Convert TOON format back to JSON",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "toon_data": {
                                "type": "string",
                                "description": "TOON formatted data to convert"
                            }
                        },
                        "required": ["toon_data"]
                    }
                ),
                Tool(
                    name="analyze_patterns",
                    description="Analyze JSON data and detect patterns for optimal compression",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "json_data": {
                                "type": "string",
                                "description": "JSON data to analyze"
                            }
                        },
                        "required": ["json_data"]
                    }
                ),
                Tool(
                    name="get_compression_strategy",
                    description="Get optimal compression strategy for JSON data",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "json_data": {
                                "type": "string",
                                "description": "JSON data to analyze"
                            }
                        },
                        "required": ["json_data"]
                    }
                ),
                Tool(
                    name="calculate_savings",
                    description="Calculate token savings from TOON conversion",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "json_data": {
                                "type": "string",
                                "description": "Original JSON data"
                            }
                        },
                        "required": ["json_data"]
                    }
                ),
                Tool(
                    name="batch_convert",
                    description="Convert multiple JSON objects to TOON format",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "json_array": {
                                "type": "string",
                                "description": "Array of JSON objects to convert"
                            },
                            "aggressive": {
                                "type": "boolean",
                                "description": "Use aggressive compression",
                                "default": False
                            }
                        },
                        "required": ["json_array"]
                    }
                )
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> List[TextContent]:
            """Handle tool calls."""
            try:
                if name == "convert_to_toon":
                    return await self._convert_to_toon(arguments)
                elif name == "convert_to_json":
                    return await self._convert_to_json(arguments)
                elif name == "analyze_patterns":
                    return await self._analyze_patterns(arguments)
                elif name == "get_compression_strategy":
                    return await self._get_compression_strategy(arguments)
                elif name == "calculate_savings":
                    return await self._calculate_savings(arguments)
                elif name == "batch_convert":
                    return await self._batch_convert(arguments)
                else:
                    raise ValueError(f"Unknown tool: {name}")

            except Exception as e:
                logger.error(f"Error in tool {name}: {str(e)}")
                return [TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
                )]

    async def _convert_to_toon(self, arguments: Dict) -> List[TextContent]:
        """Convert JSON to TOON format."""
        json_data = arguments["json_data"]
        aggressive = arguments.get("aggressive", False)

        # Parse JSON
        data = json.loads(json_data)

        # Convert to TOON
        converter = TOONConverter(aggressive=aggressive)
        toon_result = converter.json_to_toon(data)

        # Calculate savings
        savings = converter.calculate_savings(json_data, toon_result)

        # Update statistics
        self.conversion_count += 1
        self.total_tokens_saved += savings['tokens_saved']

        result = {
            "toon_format": toon_result,
            "savings": savings
        }

        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]

    async def _convert_to_json(self, arguments: Dict) -> List[TextContent]:
        """Convert TOON to JSON format."""
        toon_data = arguments["toon_data"]

        # Convert to JSON
        json_result = convert_toon_to_json(toon_data)

        return [TextContent(
            type="text",
            text=json_result
        )]

    async def _analyze_patterns(self, arguments: Dict) -> List[TextContent]:
        """Analyze patterns in JSON data."""
        json_data = arguments["json_data"]
        data = json.loads(json_data)

        # Detect patterns
        patterns = self.detector.analyze(data)

        # Get recommendations
        recommendations = self.detector.get_compression_recommendations()

        result = {
            "patterns": [
                {
                    "type": p.pattern_type,
                    "confidence": p.confidence,
                    "keys": p.keys,
                    "count": p.count
                }
                for p in patterns
            ],
            "recommendations": recommendations
        }

        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]

    async def _get_compression_strategy(self, arguments: Dict) -> List[TextContent]:
        """Get optimal compression strategy."""
        json_data = arguments["json_data"]
        data = json.loads(json_data)

        # Get strategy
        strategy = self.strategy.get_strategy(data)

        # Format for output
        result = {
            "use_schema_compression": strategy["use_schema_compression"],
            "use_reference_compression": strategy["use_reference_compression"],
            "custom_abbreviations": strategy["custom_abbreviations"],
            "expected_savings_percent": round(strategy["expected_savings"] * 100, 2),
            "detected_patterns": [
                {
                    "type": p.pattern_type,
                    "confidence": round(p.confidence, 3)
                }
                for p in strategy["patterns"][:5]  # Top 5
            ]
        }

        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]

    async def _calculate_savings(self, arguments: Dict) -> List[TextContent]:
        """Calculate token savings."""
        json_data = arguments["json_data"]

        # Convert to TOON
        toon_result = convert_json_to_toon(json_data)

        # Calculate savings
        converter = TOONConverter()
        savings = converter.calculate_savings(json_data, toon_result)

        return [TextContent(
            type="text",
            text=json.dumps(savings, indent=2)
        )]

    async def _batch_convert(self, arguments: Dict) -> List[TextContent]:
        """Batch convert multiple JSON objects."""
        json_array = arguments["json_array"]
        aggressive = arguments.get("aggressive", False)

        # Parse array
        data_array = json.loads(json_array)

        if not isinstance(data_array, list):
            raise ValueError("json_array must be an array")

        # Convert each item
        converter = TOONConverter(aggressive=aggressive)
        results = []
        total_savings = 0

        for item in data_array:
            item_json = json.dumps(item)
            toon_result = converter.json_to_toon(item)
            savings = converter.calculate_savings(item_json, toon_result)

            results.append({
                "toon": toon_result,
                "savings_percent": savings["savings_percent"]
            })
            total_savings += savings["tokens_saved"]

        # Update statistics
        self.conversion_count += len(data_array)
        self.total_tokens_saved += total_savings

        result = {
            "converted_count": len(data_array),
            "total_tokens_saved": total_savings,
            "results": results
        }

        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]

    async def run(self):
        """Run the MCP server."""
        logger.info("Starting TOON MCP Server...")

        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


def main():
    """Main entry point."""
    server = TOONMCPServer()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
