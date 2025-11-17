#!/usr/bin/env python3
"""
TOON Example Generator
Adds TOON examples to generated code and documentation.
"""

import json
from typing import Dict, Any, List
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "mcp-server-toon"))
from src.toon_converter import TOONConverter
from src.patterns import PatternDetector


class CodeExampleGenerator:
    """
    Generates code examples with TOON format.
    """

    def __init__(self):
        """Initialize example generator."""
        self.converter = TOONConverter()
        self.detector = PatternDetector()

    def generate_python_example(self, data: Dict[str, Any], context: str = "") -> str:
        """
        Generate Python code example with TOON.

        Args:
            data: Sample data
            context: Context for the example

        Returns:
            Python code with TOON example
        """
        json_str = json.dumps(data, indent=2)
        toon = self.converter.json_to_toon(data)
        savings = self.converter.calculate_savings(json_str, toon)

        return f'''"""
{context if context else "Example: Using TOON for efficient data representation"}

Token Savings: {savings['savings_percent']:.1f}% ({savings['tokens_saved']} tokens)
"""

from toon_converter import convert_toon_to_json, convert_json_to_toon

# Original JSON format
json_data = {json_str}

# Convert to TOON (compact format)
toon_format = convert_json_to_toon(json_data)
print(f"TOON: {{toon_format}}")

# TOON representation (use this in your code/docs to save tokens)
compact_data = '{toon}'

# Convert back when needed
original_data = convert_toon_to_json(compact_data)
assert original_data == json_data  # Data integrity verified
'''

    def generate_typescript_example(self, data: Dict[str, Any], context: str = "") -> str:
        """
        Generate TypeScript code example with TOON.

        Args:
            data: Sample data
            context: Context for the example

        Returns:
            TypeScript code with TOON example
        """
        json_str = json.dumps(data, indent=2)
        toon = self.converter.json_to_toon(data)
        savings = self.converter.calculate_savings(json_str, toon)

        return f'''/**
 * {context if context else "Example: Using TOON for efficient data representation"}
 *
 * Token Savings: {savings['savings_percent']:.1f}% ({savings['tokens_saved']} tokens)
 */

import {{ convertToonToJson, convertJsonToToon }} from 'toon-converter';

// Original JSON format
const jsonData = {json_str};

// Convert to TOON (compact format)
const toonFormat = convertJsonToToon(jsonData);
console.log('TOON:', toonFormat);

// TOON representation (use this in your code/docs to save tokens)
const compactData = '{toon}';

// Convert back when needed
const originalData = convertToonToJson(compactData);
console.assert(JSON.stringify(originalData) === JSON.stringify(jsonData));
'''

    def generate_api_example(self, endpoint: str, response_data: Dict[str, Any]) -> str:
        """
        Generate API documentation example with TOON.

        Args:
            endpoint: API endpoint
            response_data: API response data

        Returns:
            API documentation with TOON example
        """
        json_str = json.dumps(response_data, indent=2)
        toon = self.converter.json_to_toon(response_data)
        savings = self.converter.calculate_savings(json_str, toon)

        # Detect patterns
        patterns = self.detector.analyze(response_data)
        pattern_info = "\n".join([
            f"  - {p.pattern_type} (confidence: {p.confidence:.2f})"
            for p in patterns[:3]
        ])

        return f'''## {endpoint}

### Response (Standard JSON)

```json
{json_str}
```

### Response (TOON Format)

For token efficiency, you can represent this response in TOON format:

```json
{toon}
```

**Token Savings**: {savings['savings_percent']:.1f}% ({savings['tokens_saved']} tokens saved)

**Detected Patterns**:
{pattern_info}

### Usage Example

```python
from toon_converter import convert_toon_to_json

# Use TOON in your documentation/code
toon_response = '{toon}'

# Convert to usable format
response = convert_toon_to_json(toon_response)
```
'''

    def generate_schema_documentation(self, schema_name: str, example_data: Dict[str, Any]) -> str:
        """
        Generate schema documentation with TOON examples.

        Args:
            schema_name: Name of the schema
            example_data: Example data conforming to schema

        Returns:
            Schema documentation with TOON examples
        """
        json_str = json.dumps(example_data, indent=2)
        toon = self.converter.json_to_toon(example_data)
        savings = self.converter.calculate_savings(json_str, toon)

        # Extract field info
        fields = []
        for key, value in example_data.items():
            value_type = type(value).__name__
            fields.append(f"  - `{key}` ({value_type})")

        fields_str = "\n".join(fields)

        return f'''# {schema_name}

## Fields

{fields_str}

## Example (JSON)

```json
{json_str}
```

## Example (TOON Format)

For efficient context usage:

```json
{toon}
```

> 💡 **Token Optimization**: Using TOON format saves {savings['savings_percent']:.1f}% tokens ({savings['tokens_saved']} tokens)

## Converting from TOON

```python
from toon_converter import convert_toon_to_json

toon_data = '{toon}'
json_data = convert_toon_to_json(toon_data)
```
'''

    def generate_inline_example(self, data: Dict[str, Any], language: str = 'python') -> str:
        """
        Generate inline TOON example for code comments.

        Args:
            data: Data to convert
            language: Programming language

        Returns:
            Inline comment with TOON example
        """
        toon = self.converter.json_to_toon(data)

        if language == 'python':
            return f"# TOON: {toon}"
        elif language in ['javascript', 'typescript']:
            return f"// TOON: {toon}"
        elif language in ['java', 'c', 'cpp']:
            return f"// TOON: {toon}"
        else:
            return f"TOON: {toon}"

    def generate_comparison_table(self, examples: List[Dict[str, Any]]) -> str:
        """
        Generate comparison table for multiple examples.

        Args:
            examples: List of example data

        Returns:
            Markdown table comparing JSON and TOON
        """
        rows = []
        for i, data in enumerate(examples, 1):
            json_str = json.dumps(data)
            toon = self.converter.json_to_toon(data)
            savings = self.converter.calculate_savings(json_str, toon)

            rows.append(
                f"| Example {i} | {savings['original_tokens']} | "
                f"{savings['toon_tokens']} | {savings['savings_percent']:.1f}% |"
            )

        rows_str = "\n".join(rows)

        return f'''## Token Savings Comparison

| Example | JSON Tokens | TOON Tokens | Savings |
|---------|-------------|-------------|---------|
{rows_str}
'''


class ContextAwareGenerator:
    """
    Generates context-aware TOON examples based on use case.
    """

    def __init__(self):
        """Initialize context-aware generator."""
        self.generator = CodeExampleGenerator()

    def generate_for_mcp_tool(self, tool_name: str, sample_output: Dict[str, Any]) -> str:
        """
        Generate TOON example for MCP tool output.

        Args:
            tool_name: Name of the MCP tool
            sample_output: Sample tool output

        Returns:
            Documentation with TOON example
        """
        return f'''## {tool_name} Tool

### Sample Output

{self.generator.generate_api_example(f"MCP Tool: {tool_name}", sample_output)}

### Integration Tip

When using this tool in Claude Code, the output can be automatically converted to TOON format
to reduce context window usage. Enable TOON auto-conversion in your MCP settings.
'''

    def generate_for_database_query(self, query: str, results: List[Dict[str, Any]]) -> str:
        """
        Generate TOON example for database query results.

        Args:
            query: SQL query
            results: Query results

        Returns:
            Documentation with TOON example
        """
        json_str = json.dumps(results, indent=2)
        toon = self.converter.json_to_toon(results)
        savings = self.converter.calculate_savings(json_str, toon)

        return f'''### Database Query Results

**Query**:
```sql
{query}
```

**Results** (Standard JSON):
```json
{json_str}
```

**Results** (TOON Format):
```json
{toon}
```

**Token Savings**: {savings['savings_percent']:.1f}% - Especially useful when storing query results in code comments or documentation.
'''

    def generate_for_api_client(self, service_name: str, endpoints: Dict[str, Dict[str, Any]]) -> str:
        """
        Generate TOON examples for API client documentation.

        Args:
            service_name: Name of the API service
            endpoints: Dictionary of endpoint names to sample responses

        Returns:
            Complete API documentation with TOON examples
        """
        sections = [f"# {service_name} API Client\n"]

        for endpoint, response in endpoints.items():
            sections.append(self.generator.generate_api_example(endpoint, response))

        return "\n\n".join(sections)


def main():
    """Demo of example generator."""
    generator = CodeExampleGenerator()

    # Example 1: User data
    user_data = {
        "id": 12345,
        "name": "John Doe",
        "email": "john@example.com",
        "status": "active",
        "metadata": {
            "created_at": "2025-01-01T00:00:00Z",
            "last_login": "2025-01-15T10:30:00Z"
        }
    }

    print("="*60)
    print("Python Example:")
    print("="*60)
    print(generator.generate_python_example(user_data, "User data representation"))

    print("\n" + "="*60)
    print("API Documentation Example:")
    print("="*60)
    print(generator.generate_api_example("GET /api/users/{id}", user_data))

    print("\n" + "="*60)
    print("Schema Documentation:")
    print("="*60)
    print(generator.generate_schema_documentation("User", user_data))


if __name__ == "__main__":
    main()
