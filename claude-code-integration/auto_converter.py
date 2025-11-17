#!/usr/bin/env python3
"""
Auto-conversion System for TOON
Automatically converts JSON to TOON in comments, documentation, and generated code.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "mcp-server-toon"))
from src.toon_converter import TOONConverter


class AutoTOONConverter:
    """
    Automatically converts JSON to TOON in various contexts.
    """

    def __init__(self):
        """Initialize auto converter."""
        self.converter = TOONConverter()
        self.min_savings_threshold = 15  # Minimum 15% savings to convert

    def convert_file(self, file_path: Path) -> Tuple[str, int]:
        """
        Convert JSON in a file to TOON format.

        Args:
            file_path: Path to file to process

        Returns:
            Tuple of (modified content, number of conversions)
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        modified_content, count = self._convert_content(content, file_path.suffix)
        return modified_content, count

    def _convert_content(self, content: str, file_type: str) -> Tuple[str, int]:
        """
        Convert JSON in content to TOON.

        Args:
            content: File content
            file_type: File extension (.py, .js, .md, etc.)

        Returns:
            Tuple of (modified content, number of conversions)
        """
        conversions = 0
        modified = content

        # Different patterns for different file types
        if file_type in {'.py'}:
            modified, conversions = self._convert_python(modified)
        elif file_type in {'.js', '.ts', '.jsx', '.tsx'}:
            modified, conversions = self._convert_javascript(modified)
        elif file_type in {'.md', '.mdx'}:
            modified, conversions = self._convert_markdown(modified)

        return modified, conversions

    def _convert_python(self, content: str) -> Tuple[str, int]:
        """Convert JSON in Python files."""
        conversions = 0

        # Pattern for JSON in comments
        def replace_comment_json(match):
            nonlocal conversions
            indent = match.group(1)
            comment_prefix = match.group(2)
            json_str = match.group(3)

            try:
                data = json.loads(json_str)
                original_len = len(json_str)

                # Convert to TOON
                toon = self.converter.json_to_toon(data)
                savings = self.converter.calculate_savings(json_str, toon)

                if savings['savings_percent'] >= self.min_savings_threshold:
                    conversions += 1
                    return (
                        f"{indent}{comment_prefix} TOON format (saves {savings['savings_percent']:.1f}%):\n"
                        f"{indent}{comment_prefix} {toon}"
                    )
            except (json.JSONDecodeError, Exception):
                pass

            return match.group(0)

        # Match JSON in Python comments
        pattern = r'^(\s*)(#)\s*({.+}|[\[].+[\]])$'
        content = re.sub(pattern, replace_comment_json, content, flags=re.MULTILINE)

        # Pattern for JSON in docstrings
        def replace_docstring_json(match):
            nonlocal conversions
            indent = match.group(1)
            json_str = match.group(2)

            try:
                data = json.loads(json_str)
                toon = self.converter.json_to_toon(data)
                savings = self.converter.calculate_savings(json_str, toon)

                if savings['savings_percent'] >= self.min_savings_threshold:
                    conversions += 1
                    return (
                        f'{indent}"""\n'
                        f'{indent}TOON format (saves {savings["savings_percent"]:.1f}%):\n'
                        f'{indent}{toon}\n'
                        f'{indent}"""'
                    )
            except (json.JSONDecodeError, Exception):
                pass

            return match.group(0)

        docstring_pattern = r'^(\s*)"""(.+)"""$'
        content = re.sub(docstring_pattern, replace_docstring_json, content, flags=re.MULTILINE | re.DOTALL)

        return content, conversions

    def _convert_javascript(self, content: str) -> Tuple[str, int]:
        """Convert JSON in JavaScript/TypeScript files."""
        conversions = 0

        # Pattern for JSON in single-line comments
        def replace_comment_json(match):
            nonlocal conversions
            indent = match.group(1)
            json_str = match.group(2)

            try:
                data = json.loads(json_str)
                toon = self.converter.json_to_toon(data)
                savings = self.converter.calculate_savings(json_str, toon)

                if savings['savings_percent'] >= self.min_savings_threshold:
                    conversions += 1
                    return (
                        f'{indent}// TOON format (saves {savings["savings_percent"]:.1f}%):\n'
                        f'{indent}// {toon}'
                    )
            except (json.JSONDecodeError, Exception):
                pass

            return match.group(0)

        pattern = r'^(\s*)//\s*({.+}|[\[].+[\]])$'
        content = re.sub(pattern, replace_comment_json, content, flags=re.MULTILINE)

        return content, conversions

    def _convert_markdown(self, content: str) -> Tuple[str, int]:
        """Convert JSON in Markdown files."""
        conversions = 0

        # Pattern for JSON code blocks
        def replace_json_block(match):
            nonlocal conversions
            json_str = match.group(1)

            try:
                data = json.loads(json_str)
                toon = self.converter.json_to_toon(data)
                savings = self.converter.calculate_savings(json_str, toon)

                if savings['savings_percent'] >= self.min_savings_threshold:
                    conversions += 1
                    return (
                        f'```json\n'
                        f'// Original JSON\n'
                        f'{json_str}\n'
                        f'```\n\n'
                        f'```json\n'
                        f'// TOON format (saves {savings["savings_percent"]:.1f}% tokens)\n'
                        f'{toon}\n'
                        f'```'
                    )
            except (json.JSONDecodeError, Exception):
                pass

            return match.group(0)

        pattern = r'```json\s*\n(.+?)\n```'
        content = re.sub(pattern, replace_json_block, content, flags=re.DOTALL)

        return content, conversions

    def process_directory(self, directory: Path, extensions: List[str] = None) -> Dict[str, int]:
        """
        Process all files in a directory.

        Args:
            directory: Directory to process
            extensions: List of file extensions to process (default: ['.py', '.js', '.ts', '.md'])

        Returns:
            Dictionary with statistics
        """
        if extensions is None:
            extensions = ['.py', '.js', '.ts', '.jsx', '.tsx', '.md']

        stats = {
            'files_processed': 0,
            'files_modified': 0,
            'total_conversions': 0
        }

        for file_path in directory.rglob('*'):
            if file_path.suffix not in extensions:
                continue

            if file_path.is_file():
                stats['files_processed'] += 1

                try:
                    modified_content, conversions = self.convert_file(file_path)

                    if conversions > 0:
                        # Write back modified content
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(modified_content)

                        stats['files_modified'] += 1
                        stats['total_conversions'] += conversions

                        print(f"✅ {file_path}: {conversions} conversions")

                except Exception as e:
                    print(f"❌ Error processing {file_path}: {e}")

        return stats


class TOONExampleGenerator:
    """
    Generates TOON examples for documentation and code.
    """

    def __init__(self):
        """Initialize example generator."""
        self.converter = TOONConverter()

    def generate_comparison_example(self, data: Dict) -> str:
        """
        Generate a side-by-side comparison of JSON and TOON.

        Args:
            data: JSON data

        Returns:
            Formatted comparison string
        """
        json_str = json.dumps(data, indent=2)
        toon = self.converter.json_to_toon(data)
        savings = self.converter.calculate_savings(json_str, toon)

        return f"""
### JSON vs TOON Comparison

**Original JSON** ({savings['original_tokens']} tokens):
```json
{json_str}
```

**TOON Format** ({savings['toon_tokens']} tokens):
```json
{toon}
```

**Savings**: {savings['savings_percent']}% ({savings['tokens_saved']} tokens)
"""

    def generate_code_example(self, language: str, data: Dict) -> str:
        """
        Generate code example with TOON conversion.

        Args:
            language: Programming language ('python', 'javascript', etc.)
            data: JSON data

        Returns:
            Code example string
        """
        toon = self.converter.json_to_toon(data)

        if language == 'python':
            return f'''
# Example: Using TOON format to reduce token usage
from toon_converter import convert_toon_to_json

# TOON format (compact)
toon_data = '{toon}'

# Convert back to usable JSON
data = convert_toon_to_json(toon_data)
print(data)
'''
        elif language in ['javascript', 'typescript']:
            return f'''
// Example: Using TOON format to reduce token usage
import {{ convertToonToJson }} from 'toon-converter';

// TOON format (compact)
const toonData = '{toon}';

// Convert back to usable JSON
const data = convertToonToJson(toonData);
console.log(data);
'''
        else:
            return f"// TOON format: {toon}"


def main():
    """CLI for auto-conversion."""
    import argparse

    parser = argparse.ArgumentParser(description='Auto-convert JSON to TOON')
    parser.add_argument('path', type=Path, help='File or directory to process')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be converted without modifying files')
    parser.add_argument('--threshold', type=int, default=15, help='Minimum savings percentage to convert (default: 15)')

    args = parser.parse_args()

    converter = AutoTOONConverter()
    converter.min_savings_threshold = args.threshold

    if args.path.is_file():
        modified_content, conversions = converter.convert_file(args.path)
        print(f"Found {conversions} conversions in {args.path}")

        if not args.dry_run and conversions > 0:
            with open(args.path, 'w', encoding='utf-8') as f:
                f.write(modified_content)
            print(f"✅ File updated")

    elif args.path.is_dir():
        stats = converter.process_directory(args.path)
        print(f"\n📊 Statistics:")
        print(f"  Files processed: {stats['files_processed']}")
        print(f"  Files modified: {stats['files_modified']}")
        print(f"  Total conversions: {stats['total_conversions']}")


if __name__ == "__main__":
    main()
