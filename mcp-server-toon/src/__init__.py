"""
TOON MCP Server Package
Token-Optimized Object Notation for efficient AI context management.
"""

from .toon_converter import (
    TOONConverter,
    convert_json_to_toon,
    convert_toon_to_json
)
from .patterns import PatternDetector, SmartCompressionStrategy
from .server import TOONMCPServer

__version__ = "1.0.0"
__all__ = [
    "TOONConverter",
    "convert_json_to_toon",
    "convert_toon_to_json",
    "PatternDetector",
    "SmartCompressionStrategy",
    "TOONMCPServer"
]
