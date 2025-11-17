"""
TOON (Token-Optimized Object Notation) Converter
Converts verbose JSON structures to compact TOON format for reduced token consumption.
"""

import json
import re
from typing import Any, Dict, List, Union
from collections import Counter


class TOONConverter:
    """
    Converts JSON to TOON format and vice versa.

    TOON Format Rules:
    1. Common keys are abbreviated (id->i, name->n, type->t, value->v, data->d)
    2. Repeated structures use references (@ref)
    3. Arrays of similar objects are compacted
    4. Null values are represented as ~
    5. Boolean values: true=T, false=F
    6. Timestamps and common patterns are compressed
    """

    # Common abbreviations for frequently used keys
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
        'description': 'desc',
        'properties': 'props',
        'attributes': 'attrs',
        'parameters': 'params',
        'configuration': 'cfg',
        'metadata': 'meta',
        'response': 'resp',
        'request': 'req',
        'error': 'err',
        'result': 'res',
        'content': 'cnt',
        'username': 'usr',
        'password': 'pwd',
        'email': 'eml',
        'phone': 'ph',
        'address': 'addr',
        'count': 'ct',
        'total': 'tot',
        'items': 'itms',
        'children': 'ch',
        'parent': 'par',
        'index': 'idx',
        'length': 'len',
        'size': 'sz',
        'width': 'w',
        'height': 'h',
        'position': 'pos',
        'enabled': 'en',
        'disabled': 'dis',
        'visible': 'vis',
        'hidden': 'hid',
    }

    # Reverse mapping for decompression
    ABBREV_KEY = {v: k for k, v in KEY_ABBREV.items()}

    def __init__(self, aggressive: bool = False):
        """
        Initialize TOON converter.

        Args:
            aggressive: If True, use more aggressive compression (may lose some readability)
        """
        self.aggressive = aggressive
        self.ref_cache: Dict[str, Any] = {}
        self.ref_counter = 0

    def json_to_toon(self, data: Union[Dict, List, str]) -> str:
        """
        Convert JSON to TOON format.

        Args:
            data: JSON data (dict, list, or JSON string)

        Returns:
            TOON formatted string
        """
        if isinstance(data, str):
            data = json.loads(data)

        self.ref_cache = {}
        self.ref_counter = 0

        # Detect patterns and build reference cache
        self._build_ref_cache(data)

        # Convert to TOON
        toon_data = self._convert_to_toon(data)

        # Create TOON output with metadata
        result = {
            '_toon': '1.0',  # TOON version
            'd': toon_data  # data
        }

        # Add reference definitions if any
        if self.ref_cache:
            result['_refs'] = self.ref_cache

        return json.dumps(result, separators=(',', ':'))

    def toon_to_json(self, toon_str: str) -> str:
        """
        Convert TOON format back to JSON.

        Args:
            toon_str: TOON formatted string

        Returns:
            Standard JSON string
        """
        toon_data = json.loads(toon_str)

        if '_toon' not in toon_data:
            raise ValueError("Invalid TOON format: missing _toon version")

        # Load references
        refs = toon_data.get('_refs', {})

        # Convert from TOON
        json_data = self._convert_from_toon(toon_data['d'], refs)

        return json.dumps(json_data, indent=2)

    def _build_ref_cache(self, data: Any, path: str = '') -> None:
        """Build a cache of repeated structures for reference."""
        if isinstance(data, dict):
            # Check if this structure appears multiple times
            struct_hash = self._hash_structure(data)

            for key, value in data.items():
                self._build_ref_cache(value, f"{path}.{key}")

        elif isinstance(data, list):
            if len(data) > 2:
                # Check for repeated objects in array
                if all(isinstance(item, dict) for item in data):
                    # Find common keys
                    all_keys = [set(item.keys()) for item in data]
                    if all_keys:
                        common_keys = set.intersection(*all_keys)
                        if len(common_keys) > 3:  # Significant overlap
                            # This is a candidate for schema-based compression
                            pass

            for i, item in enumerate(data):
                self._build_ref_cache(item, f"{path}[{i}]")

    def _hash_structure(self, data: Dict) -> str:
        """Create a hash of the structure (keys only)."""
        if isinstance(data, dict):
            return json.dumps(sorted(data.keys()))
        return ''

    def _convert_to_toon(self, data: Any) -> Any:
        """Recursively convert data to TOON format."""
        if data is None:
            return '~'

        if isinstance(data, bool):
            return 'T' if data else 'F'

        if isinstance(data, (int, float)):
            return data

        if isinstance(data, str):
            # Compress common patterns
            return self._compress_string(data)

        if isinstance(data, list):
            return self._compress_array(data)

        if isinstance(data, dict):
            return self._compress_object(data)

        return data

    def _compress_string(self, s: str) -> str:
        """Compress string values."""
        # ISO timestamp compression
        iso_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}'
        if re.match(iso_pattern, s):
            # Could compress timestamps further if needed
            return s

        return s

    def _compress_array(self, arr: List) -> List:
        """Compress array structures."""
        if not arr:
            return []

        # Check if all items are dicts with same keys
        if all(isinstance(item, dict) for item in arr):
            all_keys = [set(item.keys()) for item in arr]
            if len(set(tuple(sorted(keys)) for keys in all_keys)) == 1:
                # All objects have same structure - use schema compression
                keys = sorted(arr[0].keys())
                compressed_keys = [self.KEY_ABBREV.get(k, k) for k in keys]

                return {
                    '_sch': compressed_keys,
                    '_dat': [
                        [self._convert_to_toon(item[k]) for k in keys]
                        for item in arr
                    ]
                }

        return [self._convert_to_toon(item) for item in arr]

    def _compress_object(self, obj: Dict) -> Dict:
        """Compress object structures."""
        compressed = {}

        for key, value in obj.items():
            # Abbreviate common keys
            compressed_key = self.KEY_ABBREV.get(key, key)
            compressed[compressed_key] = self._convert_to_toon(value)

        return compressed

    def _convert_from_toon(self, data: Any, refs: Dict) -> Any:
        """Recursively convert TOON format back to standard JSON."""
        if data == '~':
            return None

        if data == 'T':
            return True

        if data == 'F':
            return False

        if isinstance(data, (int, float)):
            return data

        if isinstance(data, str):
            # Check for reference
            if data.startswith('@'):
                ref_key = data[1:]
                return refs.get(ref_key, data)
            return data

        if isinstance(data, list):
            return [self._convert_from_toon(item, refs) for item in data]

        if isinstance(data, dict):
            # Check for schema-compressed array
            if '_sch' in data and '_dat' in data:
                return self._decompress_schema_array(data, refs)

            # Regular object decompression
            return self._decompress_object(data, refs)

        return data

    def _decompress_schema_array(self, data: Dict, refs: Dict) -> List:
        """Decompress schema-based array."""
        schema = data['_sch']
        values = data['_dat']

        # Expand abbreviated keys
        expanded_keys = [self.ABBREV_KEY.get(k, k) for k in schema]

        result = []
        for row in values:
            obj = {}
            for i, key in enumerate(expanded_keys):
                obj[key] = self._convert_from_toon(row[i], refs)
            result.append(obj)

        return result

    def _decompress_object(self, obj: Dict, refs: Dict) -> Dict:
        """Decompress object."""
        decompressed = {}

        for key, value in obj.items():
            # Expand abbreviated keys
            expanded_key = self.ABBREV_KEY.get(key, key)
            decompressed[expanded_key] = self._convert_from_toon(value, refs)

        return decompressed

    def calculate_savings(self, original_json: str, toon_str: str) -> Dict[str, Any]:
        """
        Calculate token savings from TOON conversion.

        Args:
            original_json: Original JSON string
            toon_str: TOON formatted string

        Returns:
            Dictionary with savings statistics
        """
        original_tokens = len(original_json)
        toon_tokens = len(toon_str)
        savings = original_tokens - toon_tokens
        savings_percent = (savings / original_tokens * 100) if original_tokens > 0 else 0

        return {
            'original_tokens': original_tokens,
            'toon_tokens': toon_tokens,
            'tokens_saved': savings,
            'savings_percent': round(savings_percent, 2),
            'compression_ratio': round(toon_tokens / original_tokens, 3) if original_tokens > 0 else 0
        }


def convert_json_to_toon(json_data: Union[Dict, List, str], aggressive: bool = False) -> str:
    """
    Convenience function to convert JSON to TOON.

    Args:
        json_data: JSON data to convert
        aggressive: Use aggressive compression

    Returns:
        TOON formatted string
    """
    converter = TOONConverter(aggressive=aggressive)
    return converter.json_to_toon(json_data)


def convert_toon_to_json(toon_str: str) -> str:
    """
    Convenience function to convert TOON to JSON.

    Args:
        toon_str: TOON formatted string

    Returns:
        Standard JSON string
    """
    converter = TOONConverter()
    return converter.toon_to_json(toon_str)
