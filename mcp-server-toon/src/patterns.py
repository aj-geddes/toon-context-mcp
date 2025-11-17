"""
Pattern Detection for TOON Converter
Identifies common patterns in JSON data for optimal compression.
"""

import re
from typing import Any, Dict, List, Optional, Tuple
from collections import Counter
from dataclasses import dataclass


@dataclass
class Pattern:
    """Represents a detected pattern in JSON data."""
    pattern_type: str
    confidence: float
    keys: Optional[List[str]] = None
    sample: Optional[Any] = None
    count: int = 0


class PatternDetector:
    """
    Detects common patterns in JSON data to optimize TOON conversion.
    """

    # Patterns for API responses
    API_RESPONSE_PATTERNS = [
        'status',
        'data',
        'message',
        'error',
        'errors',
        'meta',
        'pagination',
    ]

    # Patterns for database records
    DATABASE_PATTERNS = [
        'id',
        'created_at',
        'updated_at',
        'deleted_at',
    ]

    # Patterns for user data
    USER_PATTERNS = [
        'username',
        'email',
        'password',
        'first_name',
        'last_name',
        'profile',
    ]

    # Common nested object patterns
    NESTED_PATTERNS = {
        'address': ['street', 'city', 'state', 'zip', 'country'],
        'coordinates': ['latitude', 'longitude', 'altitude'],
        'dimensions': ['width', 'height', 'depth'],
        'date_range': ['start_date', 'end_date'],
        'time_range': ['start_time', 'end_time'],
    }

    def __init__(self):
        """Initialize pattern detector."""
        self.detected_patterns: List[Pattern] = []
        self.key_frequency: Counter = Counter()

    def analyze(self, data: Any) -> List[Pattern]:
        """
        Analyze data and detect patterns.

        Args:
            data: JSON data to analyze

        Returns:
            List of detected patterns
        """
        self.detected_patterns = []
        self.key_frequency = Counter()

        # Traverse and analyze
        self._traverse(data)

        # Detect specific patterns
        self._detect_api_response(data)
        self._detect_database_records(data)
        self._detect_user_data(data)
        self._detect_nested_structures(data)
        self._detect_array_patterns(data)
        self._detect_repeated_structures(data)

        return sorted(self.detected_patterns, key=lambda p: p.confidence, reverse=True)

    def _traverse(self, data: Any, path: str = '') -> None:
        """Traverse data and collect key statistics."""
        if isinstance(data, dict):
            for key, value in data.items():
                self.key_frequency[key] += 1
                self._traverse(value, f"{path}.{key}")

        elif isinstance(data, list):
            for i, item in enumerate(data):
                self._traverse(item, f"{path}[{i}]")

    def _detect_api_response(self, data: Any) -> None:
        """Detect API response patterns."""
        if not isinstance(data, dict):
            return

        matches = sum(1 for key in self.API_RESPONSE_PATTERNS if key in data)
        confidence = matches / len(self.API_RESPONSE_PATTERNS)

        if confidence > 0.3:
            self.detected_patterns.append(Pattern(
                pattern_type='api_response',
                confidence=confidence,
                keys=[k for k in self.API_RESPONSE_PATTERNS if k in data],
                sample=None
            ))

    def _detect_database_records(self, data: Any) -> None:
        """Detect database record patterns."""
        if isinstance(data, dict):
            matches = sum(1 for key in self.DATABASE_PATTERNS if key in data)
            confidence = matches / len(self.DATABASE_PATTERNS)

            if confidence > 0.3:
                self.detected_patterns.append(Pattern(
                    pattern_type='database_record',
                    confidence=confidence,
                    keys=[k for k in self.DATABASE_PATTERNS if k in data],
                    sample=None
                ))

        elif isinstance(data, list) and len(data) > 0:
            # Check if it's an array of database records
            if isinstance(data[0], dict):
                matches = sum(1 for key in self.DATABASE_PATTERNS if key in data[0])
                confidence = matches / len(self.DATABASE_PATTERNS)

                if confidence > 0.3:
                    self.detected_patterns.append(Pattern(
                        pattern_type='database_records_array',
                        confidence=confidence,
                        keys=[k for k in self.DATABASE_PATTERNS if k in data[0]],
                        count=len(data)
                    ))

    def _detect_user_data(self, data: Any) -> None:
        """Detect user data patterns."""
        if not isinstance(data, dict):
            return

        matches = sum(1 for key in self.USER_PATTERNS if key in data)
        confidence = matches / len(self.USER_PATTERNS)

        if confidence > 0.25:
            self.detected_patterns.append(Pattern(
                pattern_type='user_data',
                confidence=confidence,
                keys=[k for k in self.USER_PATTERNS if k in data],
                sample=None
            ))

    def _detect_nested_structures(self, data: Any) -> None:
        """Detect common nested structure patterns."""
        if not isinstance(data, dict):
            return

        for pattern_name, pattern_keys in self.NESTED_PATTERNS.items():
            for key, value in data.items():
                if isinstance(value, dict):
                    matches = sum(1 for pk in pattern_keys if pk in value)
                    confidence = matches / len(pattern_keys)

                    if confidence > 0.5:
                        self.detected_patterns.append(Pattern(
                            pattern_type=f'nested_{pattern_name}',
                            confidence=confidence,
                            keys=[pk for pk in pattern_keys if pk in value],
                            sample={key: value}
                        ))

    def _detect_array_patterns(self, data: Any) -> None:
        """Detect patterns in arrays."""
        if not isinstance(data, dict):
            return

        for key, value in data.items():
            if isinstance(value, list) and len(value) > 0:
                # Homogeneous arrays
                if self._is_homogeneous_array(value):
                    item_type = type(value[0]).__name__
                    self.detected_patterns.append(Pattern(
                        pattern_type=f'homogeneous_array_{item_type}',
                        confidence=1.0,
                        keys=[key],
                        count=len(value)
                    ))

                # Arrays of objects with same schema
                if all(isinstance(item, dict) for item in value):
                    schema_consistency = self._calculate_schema_consistency(value)
                    if schema_consistency > 0.8:
                        self.detected_patterns.append(Pattern(
                            pattern_type='consistent_schema_array',
                            confidence=schema_consistency,
                            keys=[key],
                            count=len(value),
                            sample=value[0] if value else None
                        ))

    def _detect_repeated_structures(self, data: Any) -> None:
        """Detect repeated object structures."""
        if not isinstance(data, dict):
            return

        structure_hashes: Counter = Counter()

        def hash_structure(obj: Any) -> Optional[str]:
            """Create a hash of object structure."""
            if isinstance(obj, dict):
                return '|'.join(sorted(obj.keys()))
            return None

        def collect_structures(d: Any):
            """Collect all structure hashes."""
            if isinstance(d, dict):
                h = hash_structure(d)
                if h:
                    structure_hashes[h] += 1
                for v in d.values():
                    collect_structures(v)
            elif isinstance(d, list):
                for item in d:
                    collect_structures(item)

        collect_structures(data)

        # Find repeated structures
        for structure, count in structure_hashes.items():
            if count > 2:  # Appears more than twice
                self.detected_patterns.append(Pattern(
                    pattern_type='repeated_structure',
                    confidence=min(count / 10.0, 1.0),  # Cap at 1.0
                    keys=structure.split('|'),
                    count=count
                ))

    def _is_homogeneous_array(self, arr: List) -> bool:
        """Check if array contains all same type."""
        if not arr:
            return True

        first_type = type(arr[0])
        return all(isinstance(item, first_type) for item in arr)

    def _calculate_schema_consistency(self, arr: List[Dict]) -> float:
        """Calculate how consistent the schemas are in an array of objects."""
        if not arr:
            return 0.0

        # Get all unique key sets
        key_sets = [set(item.keys()) for item in arr if isinstance(item, dict)]

        if not key_sets:
            return 0.0

        # Calculate consistency based on key overlap
        all_keys = set.union(*key_sets)
        common_keys = set.intersection(*key_sets)

        return len(common_keys) / len(all_keys) if all_keys else 0.0

    def get_compression_recommendations(self) -> List[str]:
        """
        Get recommendations for optimal compression based on detected patterns.

        Returns:
            List of recommendation strings
        """
        recommendations = []

        for pattern in self.detected_patterns:
            if pattern.pattern_type == 'consistent_schema_array' and pattern.confidence > 0.9:
                recommendations.append(
                    f"Array with {pattern.count} items has consistent schema - use schema-based compression"
                )

            elif pattern.pattern_type == 'repeated_structure' and pattern.count > 5:
                recommendations.append(
                    f"Structure with keys {pattern.keys[:3]}... appears {pattern.count} times - use reference-based compression"
                )

            elif pattern.pattern_type.startswith('nested_'):
                nested_type = pattern.pattern_type.replace('nested_', '')
                recommendations.append(
                    f"Detected {nested_type} pattern - consider using compact notation"
                )

            elif pattern.pattern_type == 'api_response':
                recommendations.append(
                    "API response pattern detected - use standard API abbreviations"
                )

        # Check for highly frequent keys
        for key, count in self.key_frequency.most_common(10):
            if count > 5:
                recommendations.append(
                    f"Key '{key}' appears {count} times - ensure it's abbreviated"
                )

        return recommendations

    def suggest_custom_abbreviations(self) -> Dict[str, str]:
        """
        Suggest custom abbreviations for frequently used keys.

        Returns:
            Dictionary mapping keys to suggested abbreviations
        """
        suggestions = {}

        for key, count in self.key_frequency.most_common():
            if count < 3:  # Only suggest for frequently used keys
                continue

            if len(key) > 4:  # Only abbreviate longer keys
                # Generate abbreviation
                # Remove vowels except first letter
                abbrev = key[0] + ''.join(c for c in key[1:] if c not in 'aeiou')

                # If still too long, use first 3 consonants
                if len(abbrev) > 4:
                    abbrev = abbrev[:4]

                suggestions[key] = abbrev.lower()

        return suggestions


class SmartCompressionStrategy:
    """
    Determines the best compression strategy based on detected patterns.
    """

    def __init__(self, detector: PatternDetector):
        """Initialize with a pattern detector."""
        self.detector = detector

    def get_strategy(self, data: Any) -> Dict[str, Any]:
        """
        Determine optimal compression strategy for given data.

        Args:
            data: Data to analyze

        Returns:
            Dictionary with strategy recommendations
        """
        patterns = self.detector.analyze(data)

        strategy = {
            'use_schema_compression': False,
            'use_reference_compression': False,
            'custom_abbreviations': {},
            'expected_savings': 0.0,
            'patterns': patterns
        }

        # Analyze patterns to determine strategy
        for pattern in patterns:
            if pattern.pattern_type == 'consistent_schema_array' and pattern.confidence > 0.8:
                strategy['use_schema_compression'] = True
                strategy['expected_savings'] += 0.20  # 20% savings

            if pattern.pattern_type == 'repeated_structure' and pattern.count > 3:
                strategy['use_reference_compression'] = True
                strategy['expected_savings'] += 0.15  # 15% savings

        # Add custom abbreviations
        custom_abbrevs = self.detector.suggest_custom_abbreviations()
        if custom_abbrevs:
            strategy['custom_abbreviations'] = custom_abbrevs
            strategy['expected_savings'] += len(custom_abbrevs) * 0.01  # 1% per abbreviation

        # Cap expected savings at 60%
        strategy['expected_savings'] = min(strategy['expected_savings'], 0.60)

        return strategy
