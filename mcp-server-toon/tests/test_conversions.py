"""
Tests for TOON conversions
"""

import json
import pytest
from src.toon_converter import TOONConverter, convert_json_to_toon, convert_toon_to_json
from src.patterns import PatternDetector, SmartCompressionStrategy


class TestTOONConverter:
    """Test TOON converter functionality."""

    def test_simple_object_conversion(self):
        """Test conversion of simple object."""
        data = {
            "id": 123,
            "name": "Test User",
            "type": "user"
        }

        converter = TOONConverter()
        toon = converter.json_to_toon(data)

        # Should be valid JSON
        toon_obj = json.loads(toon)
        assert '_toon' in toon_obj
        assert toon_obj['_toon'] == '1.0'

        # Should have abbreviated keys
        assert 'i' in toon_obj['d']  # id -> i
        assert 'n' in toon_obj['d']  # name -> n
        assert 't' in toon_obj['d']  # type -> t

    def test_round_trip_conversion(self):
        """Test that data survives round-trip conversion."""
        original_data = {
            "id": 456,
            "name": "Test Item",
            "type": "product",
            "status": "active",
            "metadata": {
                "created_at": "2025-01-01T00:00:00Z",
                "updated_at": "2025-01-02T00:00:00Z"
            }
        }

        converter = TOONConverter()

        # Convert to TOON
        toon = converter.json_to_toon(original_data)

        # Convert back to JSON
        json_str = converter.toon_to_json(toon)
        restored_data = json.loads(json_str)

        # Should match original
        assert restored_data == original_data

    def test_null_conversion(self):
        """Test null value conversion."""
        data = {"value": None}

        converter = TOONConverter()
        toon = converter.json_to_toon(data)
        toon_obj = json.loads(toon)

        # Null should be converted to ~
        assert toon_obj['d']['v'] == '~'

        # Should restore to None
        json_str = converter.toon_to_json(toon)
        restored = json.loads(json_str)
        assert restored['value'] is None

    def test_boolean_conversion(self):
        """Test boolean value conversion."""
        data = {
            "enabled": True,
            "disabled": False
        }

        converter = TOONConverter()
        toon = converter.json_to_toon(data)
        toon_obj = json.loads(toon)

        # Booleans should be T/F
        assert toon_obj['d']['en'] == 'T'
        assert toon_obj['d']['dis'] == 'F'

        # Should restore correctly
        json_str = converter.toon_to_json(toon)
        restored = json.loads(json_str)
        assert restored['enabled'] is True
        assert restored['disabled'] is False

    def test_array_compression(self):
        """Test array compression with consistent schema."""
        data = [
            {"id": 1, "name": "Item 1", "type": "A"},
            {"id": 2, "name": "Item 2", "type": "B"},
            {"id": 3, "name": "Item 3", "type": "C"}
        ]

        converter = TOONConverter()
        toon = converter.json_to_toon(data)
        toon_obj = json.loads(toon)

        # Should use schema-based compression
        data_content = toon_obj['d']
        if isinstance(data_content, dict):
            assert '_sch' in data_content
            assert '_dat' in data_content

        # Should restore correctly
        json_str = converter.toon_to_json(toon)
        restored = json.loads(json_str)
        assert restored == data

    def test_nested_objects(self):
        """Test nested object conversion."""
        data = {
            "id": 1,
            "user": {
                "id": 100,
                "name": "John Doe",
                "email": "john@example.com"
            },
            "metadata": {
                "created_at": "2025-01-01T00:00:00Z"
            }
        }

        converter = TOONConverter()
        toon = converter.json_to_toon(data)

        # Should restore correctly
        json_str = converter.toon_to_json(toon)
        restored = json.loads(json_str)
        assert restored == data

    def test_savings_calculation(self):
        """Test token savings calculation."""
        original_data = {
            "id": 123,
            "name": "Test User",
            "type": "user",
            "status": "active",
            "metadata": {
                "created_at": "2025-01-01T00:00:00Z",
                "updated_at": "2025-01-02T00:00:00Z"
            }
        }

        original_json = json.dumps(original_data)
        converter = TOONConverter()
        toon = converter.json_to_toon(original_data)

        savings = converter.calculate_savings(original_json, toon)

        assert 'original_tokens' in savings
        assert 'toon_tokens' in savings
        assert 'tokens_saved' in savings
        assert 'savings_percent' in savings
        assert 'compression_ratio' in savings

        # TOON should be smaller
        assert savings['toon_tokens'] < savings['original_tokens']
        assert savings['tokens_saved'] > 0
        assert savings['savings_percent'] > 0

    def test_large_array_conversion(self):
        """Test conversion of large arrays."""
        data = [
            {
                "id": i,
                "name": f"Item {i}",
                "value": i * 10,
                "status": "active" if i % 2 == 0 else "inactive"
            }
            for i in range(100)
        ]

        converter = TOONConverter()
        toon = converter.json_to_toon(data)

        # Should restore correctly
        json_str = converter.toon_to_json(toon)
        restored = json.loads(json_str)
        assert restored == data

        # Should have significant savings
        original_json = json.dumps(data)
        savings = converter.calculate_savings(original_json, toon)
        assert savings['savings_percent'] > 20  # At least 20% savings


class TestPatternDetector:
    """Test pattern detection functionality."""

    def test_api_response_detection(self):
        """Test detection of API response pattern."""
        data = {
            "status": "success",
            "data": {"id": 1},
            "message": "OK",
            "meta": {"page": 1}
        }

        detector = PatternDetector()
        patterns = detector.analyze(data)

        # Should detect API response pattern
        api_patterns = [p for p in patterns if p.pattern_type == 'api_response']
        assert len(api_patterns) > 0
        assert api_patterns[0].confidence > 0.3

    def test_database_record_detection(self):
        """Test detection of database record pattern."""
        data = {
            "id": 1,
            "created_at": "2025-01-01T00:00:00Z",
            "updated_at": "2025-01-02T00:00:00Z"
        }

        detector = PatternDetector()
        patterns = detector.analyze(data)

        # Should detect database record pattern
        db_patterns = [p for p in patterns if p.pattern_type == 'database_record']
        assert len(db_patterns) > 0

    def test_consistent_schema_array_detection(self):
        """Test detection of arrays with consistent schema."""
        data = {
            "users": [
                {"id": 1, "name": "User 1"},
                {"id": 2, "name": "User 2"},
                {"id": 3, "name": "User 3"}
            ]
        }

        detector = PatternDetector()
        patterns = detector.analyze(data)

        # Should detect consistent schema
        schema_patterns = [p for p in patterns if 'consistent_schema' in p.pattern_type]
        assert len(schema_patterns) > 0

    def test_compression_recommendations(self):
        """Test compression recommendations."""
        data = [
            {"id": i, "name": f"Item {i}", "type": "product"}
            for i in range(10)
        ]

        detector = PatternDetector()
        detector.analyze(data)
        recommendations = detector.get_compression_recommendations()

        assert len(recommendations) > 0
        assert any('schema' in r.lower() for r in recommendations)

    def test_custom_abbreviation_suggestions(self):
        """Test custom abbreviation suggestions."""
        data = {
            "product_id": 1,
            "product_name": "Test",
            "product_type": "A",
            "product_category": "B"
        }

        detector = PatternDetector()
        detector.analyze(data)
        suggestions = detector.suggest_custom_abbreviations()

        # Should suggest abbreviations for frequently used keys
        assert len(suggestions) > 0


class TestSmartCompressionStrategy:
    """Test smart compression strategy."""

    def test_strategy_for_array(self):
        """Test strategy recommendation for arrays."""
        data = [
            {"id": i, "name": f"Item {i}"}
            for i in range(10)
        ]

        detector = PatternDetector()
        strategy = SmartCompressionStrategy(detector)
        result = strategy.get_strategy(data)

        assert 'use_schema_compression' in result
        assert 'use_reference_compression' in result
        assert 'expected_savings' in result
        assert result['expected_savings'] > 0

    def test_strategy_for_complex_object(self):
        """Test strategy for complex nested object."""
        data = {
            "users": [
                {
                    "id": i,
                    "name": f"User {i}",
                    "email": f"user{i}@example.com",
                    "status": "active"
                }
                for i in range(20)
            ],
            "metadata": {
                "total": 20,
                "page": 1,
                "per_page": 20
            }
        }

        detector = PatternDetector()
        strategy = SmartCompressionStrategy(detector)
        result = strategy.get_strategy(data)

        assert result['expected_savings'] > 0
        assert len(result['patterns']) > 0


class TestConvenienceFunctions:
    """Test convenience functions."""

    def test_convert_json_to_toon_function(self):
        """Test convert_json_to_toon convenience function."""
        data = {"id": 1, "name": "Test"}
        toon = convert_json_to_toon(data)

        # Should be valid TOON
        toon_obj = json.loads(toon)
        assert '_toon' in toon_obj

    def test_convert_toon_to_json_function(self):
        """Test convert_toon_to_json convenience function."""
        data = {"id": 1, "name": "Test"}
        toon = convert_json_to_toon(data)
        json_str = convert_toon_to_json(toon)

        # Should match original
        restored = json.loads(json_str)
        assert restored == data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
