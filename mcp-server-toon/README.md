# TOON MCP Server

**Token-Optimized Object Notation** for efficient AI context management.

## Overview

TOON-MCP is a Model Context Protocol server that automatically converts verbose JSON structures into Token-Optimized Object Notation (TOON), reducing token consumption in AI-assisted development workflows by up to 60%.

## Features

- **Smart Compression**: Automatic detection of patterns in JSON data
- **Schema-Based Encoding**: Efficient representation of arrays with consistent schemas
- **Key Abbreviation**: Common keys are automatically abbreviated
- **Reference System**: Repeated structures are referenced to avoid duplication
- **MCP Integration**: Seamless integration with Claude and other MCP clients
- **Round-Trip Conversion**: Lossless conversion between JSON and TOON

## Installation

```bash
pip install -e .
```

## Usage

### As MCP Server

Add to your MCP settings:

```json
{
  "mcpServers": {
    "toon": {
      "command": "python",
      "args": ["-m", "src.server"]
    }
  }
}
```

### Programmatic Usage

```python
from src.toon_converter import convert_json_to_toon, convert_toon_to_json

# Convert JSON to TOON
json_data = {"id": 123, "name": "Test", "type": "user"}
toon_format = convert_json_to_toon(json_data)

# Convert back to JSON
original_json = convert_toon_to_json(toon_format)
```

## TOON Format

TOON uses several techniques to reduce token consumption:

1. **Key Abbreviation**: Common keys like `id`, `name`, `type` are shortened
2. **Schema Compression**: Arrays of similar objects use schema-based encoding
3. **Value Optimization**: `null` → `~`, `true` → `T`, `false` → `F`
4. **Reference System**: Repeated structures are referenced

### Example

**Original JSON** (98 characters):
```json
{
  "id": 123,
  "name": "John Doe",
  "type": "user",
  "status": "active"
}
```

**TOON Format** (62 characters, 37% reduction):
```json
{"_toon":"1.0","d":{"i":123,"n":"John Doe","t":"user","s":"active"}}
```

## MCP Tools

The server provides several tools:

- `convert_to_toon`: Convert JSON to TOON format
- `convert_to_json`: Convert TOON back to JSON
- `analyze_patterns`: Analyze JSON and detect optimization patterns
- `get_compression_strategy`: Get optimal compression strategy
- `calculate_savings`: Calculate token savings
- `batch_convert`: Batch convert multiple JSON objects

## Testing

```bash
pytest tests/ -v
```

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests with coverage
pytest tests/ --cov=src

# Format code
black src/ tests/

# Lint
ruff src/ tests/
```

## License

MIT

## Documentation

Full documentation available at `/docs`
