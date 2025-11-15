"""
Tests for data generation.
"""
import pytest
import json
import os
import tempfile
from src.data.generator import make_incident, generate_incidents, ROOT_CAUSES


def test_make_incident():
    """Test that make_incident creates a valid incident."""
    incident = make_incident("INC0001", "connection_pool_exhaustion")
    
    assert incident["incident_id"] == "INC0001"
    assert incident["root_cause"] == "connection_pool_exhaustion"
    assert "metrics" in incident
    assert "cpu" in incident["metrics"]
    assert "latency" in incident["metrics"]
    assert "logs_summary" in incident
    assert "system_meta" in incident
    assert "rca_explanation" in incident


def test_generate_incidents():
    """Test that generate_incidents creates the expected number of files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        generate_incidents(num_incidents=10, output_dir=tmpdir, seed=42)
        
        # Check that files were created
        json_files = [f for f in os.listdir(tmpdir) if f.endswith('.json')]
        assert len(json_files) == 10
        
        # Check that at least one file is valid JSON
        with open(os.path.join(tmpdir, json_files[0]), 'r') as f:
            incident = json.load(f)
            assert "incident_id" in incident


def test_incident_schema():
    """Test that generated incidents match the expected schema."""
    incident = make_incident("TEST001", "disk_full")
    
    required_fields = [
        "incident_id", "timestamp_start", "timestamp_end",
        "metrics", "logs_summary", "system_meta",
        "human_notes", "root_cause", "rca_explanation"
    ]
    
    for field in required_fields:
        assert field in incident, f"Missing required field: {field}"
    
    # Check metrics structure
    assert isinstance(incident["metrics"], dict)
    for metric_name, values in incident["metrics"].items():
        assert isinstance(values, list)
        assert len(values) > 0
        assert isinstance(values[0], list) and len(values[0]) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

