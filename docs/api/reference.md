---
layout: guide
title: API Reference
description: Complete API documentation for TOON-MCP
---

## Core API

### toon_converter.TOONConverter

Main converter class for JSON ↔ TOON conversions.

```python
class TOONConverter(aggressive: bool = False)
```

**Parameters**:
- `aggressive` (bool): Enable aggressive compression mode (default: False)

**Methods**:

#### json_to_toon

```python
def json_to_toon(data: Union[Dict, List, str]) -> str
```

Convert JSON to TOON format.

**Parameters**:
- `data`: JSON data (dict, list, or JSON string)

**Returns**:
- TOON formatted string

**Example**:
```python
converter = TOONConverter()
toon = converter.json_to_toon({"id": 123, "name": "Test"})
```

#### toon_to_json

```python
def toon_to_json(toon_str: str) -> str
```

Convert TOON format back to JSON.

**Parameters**:
- `toon_str`: TOON formatted string

**Returns**:
- Standard JSON string

#### calculate_savings

```python
def calculate_savings(original_json: str, toon_str: str) -> Dict[str, Any]
```

Calculate token savings from TOON conversion.

**Returns**:
```python
{
    'original_tokens': int,
    'toon_tokens': int,
    'tokens_saved': int,
    'savings_percent': float,
    'compression_ratio': float
}
```

### Convenience Functions

#### convert_json_to_toon

```python
def convert_json_to_toon(
    json_data: Union[Dict, List, str],
    aggressive: bool = False
) -> str
```

Quick conversion function.

#### convert_toon_to_json

```python
def convert_toon_to_json(toon_str: str) -> str
```

Quick restoration function.

## Pattern Detection API

### patterns.PatternDetector

Detects patterns in JSON data for optimization.

```python
class PatternDetector()
```

**Methods**:

#### analyze

```python
def analyze(data: Any) -> List[Pattern]
```

Analyze data and detect patterns.

**Returns**: List of detected Pattern objects

**Example**:
```python
detector = PatternDetector()
patterns = detector.analyze(data)

for pattern in patterns:
    print(f"{pattern.pattern_type}: {pattern.confidence}")
```

#### get_compression_recommendations

```python
def get_compression_recommendations() -> List[str]
```

Get recommendations for optimal compression.

**Returns**: List of recommendation strings

#### suggest_custom_abbreviations

```python
def suggest_custom_abbreviations() -> Dict[str, str]
```

Suggest custom abbreviations for frequently used keys.

**Returns**: Dictionary mapping keys to suggested abbreviations

### patterns.SmartCompressionStrategy

Determines optimal compression strategy.

```python
class SmartCompressionStrategy(detector: PatternDetector)
```

**Methods**:

#### get_strategy

```python
def get_strategy(data: Any) -> Dict[str, Any]
```

Determine optimal compression strategy.

**Returns**:
```python
{
    'use_schema_compression': bool,
    'use_reference_compression': bool,
    'custom_abbreviations': Dict[str, str],
    'expected_savings': float,
    'patterns': List[Pattern]
}
```

## Token Monitoring API

### token_monitor.TokenMonitor

Monitors conversation token usage.

```python
class TokenMonitor(
    warn_threshold: int = 50000,
    critical_threshold: int = 100000
)
```

**Parameters**:
- `warn_threshold`: Token count to trigger warning
- `critical_threshold`: Token count to trigger critical alert

**Methods**:

#### analyze_message

```python
def analyze_message(
    content: str,
    role: str = 'user',
    message_id: str = None
) -> TokenUsage
```

Analyze a message for token usage.

**Parameters**:
- `content`: Message content
- `role`: Message role ('user', 'assistant', 'tool')
- `message_id`: Optional message identifier

**Returns**: TokenUsage object

#### get_metrics

```python
def get_metrics() -> ConversationMetrics
```

Get current conversation metrics.

**Returns**:
```python
ConversationMetrics(
    total_tokens: int,
    user_tokens: int,
    assistant_tokens: int,
    tool_tokens: int,
    optimized_tokens: int,
    total_savings: int,
    savings_percent: float,
    message_count: int,
    optimization_count: int
)
```

#### check_thresholds

```python
def check_thresholds() -> Optional[str]
```

Check if token usage has crossed thresholds.

**Returns**: Warning message if threshold crossed, None otherwise

#### get_optimization_recommendations

```python
def get_optimization_recommendations() -> List[str]
```

Get recommendations for optimizing token usage.

#### export_report

```python
def export_report(file_path: Optional[Path] = None) -> str
```

Export detailed token usage report.

## Tool Output Optimization API

### tool_output_optimizer.ToolOutputOptimizer

Optimizes MCP tool outputs.

```python
class ToolOutputOptimizer(
    auto_optimize: bool = True,
    min_savings: float = 15.0
)
```

**Parameters**:
- `auto_optimize`: Automatically optimize outputs above threshold
- `min_savings`: Minimum savings percentage to trigger optimization

**Methods**:

#### optimize_tool_output

```python
def optimize_tool_output(
    tool_name: str,
    output: Any
) -> Tuple[Any, Dict[str, Any]]
```

Optimize a tool's output.

**Returns**: Tuple of (optimized_output, metadata)

#### create_optimized_response

```python
def create_optimized_response(tool_name: str, output: Any) -> str
```

Create an optimized response for tool output.

#### batch_optimize

```python
def batch_optimize(
    tool_outputs: List[Tuple[str, Any]]
) -> List[Tuple[str, Any, Dict]]
```

Batch optimize multiple tool outputs.

#### get_stats

```python
def get_stats() -> Dict[str, Any]
```

Get optimization statistics.

**Returns**:
```python
{
    'total_outputs': int,
    'optimized_outputs': int,
    'total_tokens_saved': int,
    'optimization_rate': float,
    'avg_tokens_saved': float
}
```

## MCP Integration API

### mcp_integration.MCPConfigManager

Manages MCP configuration.

```python
class MCPConfigManager(config_path: Path = None)
```

**Methods**:

#### add_toon_server

```python
def add_toon_server() -> None
```

Add TOON MCP server to configuration.

#### enable_toon_for_server

```python
def enable_toon_for_server(server_name: str) -> None
```

Enable TOON optimization for an existing server.

#### get_server_list

```python
def get_server_list() -> List[str]
```

Get list of configured MCP servers.

## Auto-Conversion API

### auto_converter.AutoTOONConverter

Automatically converts JSON to TOON in files.

```python
class AutoTOONConverter()
```

**Methods**:

#### convert_file

```python
def convert_file(file_path: Path) -> Tuple[str, int]
```

Convert JSON in a file to TOON format.

**Returns**: Tuple of (modified_content, conversion_count)

#### process_directory

```python
def process_directory(
    directory: Path,
    extensions: List[str] = None
) -> Dict[str, int]
```

Process all files in a directory.

**Returns**: Statistics dictionary

## Example Generator API

### example_generator.CodeExampleGenerator

Generates code examples with TOON.

```python
class CodeExampleGenerator()
```

**Methods**:

#### generate_python_example

```python
def generate_python_example(
    data: Dict[str, Any],
    context: str = ""
) -> str
```

Generate Python code example with TOON.

#### generate_typescript_example

```python
def generate_typescript_example(
    data: Dict[str, Any],
    context: str = ""
) -> str
```

Generate TypeScript code example with TOON.

#### generate_api_example

```python
def generate_api_example(
    endpoint: str,
    response_data: Dict[str, Any]
) -> str
```

Generate API documentation example with TOON.

## MCP Tools

The following tools are available when using TOON as an MCP server:

### convert_to_toon

Convert JSON to TOON format.

**Input Schema**:
```json
{
  "json_data": "string (required)",
  "aggressive": "boolean (optional, default: false)"
}
```

### convert_to_json

Convert TOON back to JSON.

**Input Schema**:
```json
{
  "toon_data": "string (required)"
}
```

### analyze_patterns

Analyze JSON and detect patterns.

**Input Schema**:
```json
{
  "json_data": "string (required)"
}
```

### get_compression_strategy

Get optimal compression strategy.

**Input Schema**:
```json
{
  "json_data": "string (required)"
}
```

### calculate_savings

Calculate token savings.

**Input Schema**:
```json
{
  "json_data": "string (required)"
}
```

### batch_convert

Batch convert multiple JSON objects.

**Input Schema**:
```json
{
  "json_array": "string (required)",
  "aggressive": "boolean (optional, default: false)"
}
```

## Data Structures

### Pattern

```python
@dataclass
class Pattern:
    pattern_type: str
    confidence: float
    keys: Optional[List[str]] = None
    sample: Optional[Any] = None
    count: int = 0
```

### TokenUsage

```python
@dataclass
class TokenUsage:
    timestamp: float
    message_id: str
    role: str
    content_type: str
    token_count: int
    optimized_token_count: Optional[int] = None
    savings_potential: float = 0.0
    optimization_applied: bool = False
```

### ConversationMetrics

```python
@dataclass
class ConversationMetrics:
    total_tokens: int
    user_tokens: int
    assistant_tokens: int
    tool_tokens: int
    optimized_tokens: int
    total_savings: int
    savings_percent: float
    message_count: int
    optimization_count: int
```

## Constants

### Key Abbreviations

Default key abbreviations used by TOON:

```python
KEY_ABBREV = {
    'id': 'i',
    'name': 'n',
    'type': 't',
    'value': 'v',
    'data': 'd',
    'message': 'm',
    'status': 's',
    'timestamp': 'ts',
    'created_at': 'ca',
    'updated_at': 'ua',
    # ... (50+ more)
}
```

Full list available in `src/toon_converter.py`

---

For more information, see the [User Guide](/guides/user-guide) or [Troubleshooting Guide](/guides/troubleshooting).
