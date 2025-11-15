"""
Load and preprocess incident datasets.
"""
import json
import os
from typing import Dict, List, Optional
from pathlib import Path


def load_incident(filepath: str) -> Dict:
    """
    Load a single incident from a JSON file.
    
    Args:
        filepath: Path to the incident JSON file
    
    Returns:
        Dictionary containing incident data
    """
    with open(filepath, 'r') as f:
        return json.load(f)


def load_incidents_from_dir(directory: str) -> List[Dict]:
    """
    Load all incidents from a directory.
    
    Args:
        directory: Directory containing incident JSON files
    
    Returns:
        List of incident dictionaries
    """
    incidents = []
    directory_path = Path(directory)
    
    for json_file in directory_path.glob("*.json"):
        incident = load_incident(str(json_file))
        incidents.append(incident)
    
    return incidents


def format_incident_for_prompt(incident: Dict) -> str:
    """
    Format an incident dictionary into a text prompt.
    
    Args:
        incident: Incident dictionary
    
    Returns:
        Formatted text string
    """
    lines = [
        f"Incident ID: {incident['incident_id']}",
        f"Time Range: {incident['timestamp_start']} to {incident['timestamp_end']}",
        "",
        "Metrics:",
    ]
    
    for metric_name, values in incident['metrics'].items():
        # Show summary statistics
        metric_vals = [v[1] for v in values]
        avg_val = sum(metric_vals) / len(metric_vals)
        max_val = max(metric_vals)
        min_val = min(metric_vals)
        lines.append(f"  {metric_name}: avg={avg_val:.2f}, min={min_val:.2f}, max={max_val:.2f}")
    
    lines.extend([
        "",
        f"Logs Summary: {incident['logs_summary']}",
        "",
        "System Metadata:",
        f"  Database Type: {incident['system_meta']['db_type']}",
        f"  Replication: {incident['system_meta']['replication']}",
        f"  Recent Deploy: {incident['system_meta']['recent_deploy']}",
        f"  Recent Config Change: {incident['system_meta']['recent_config_change']}",
        "",
        f"Human Notes: {incident['human_notes']}"
    ])
    
    return "\n".join(lines)


def split_incidents(
    incidents: List[Dict],
    train_ratio: float = 0.7,
    val_ratio: float = 0.1,
    test_ratio: float = 0.2,
    seed: int = 42
) -> tuple:
    """
    Split incidents into train/val/test sets.
    
    Args:
        incidents: List of incident dictionaries
        train_ratio: Proportion for training set
        val_ratio: Proportion for validation set
        test_ratio: Proportion for test set
        seed: Random seed for shuffling
    
    Returns:
        Tuple of (train_incidents, val_incidents, test_incidents)
    """
    import random
    random.seed(seed)
    
    shuffled = incidents.copy()
    random.shuffle(shuffled)
    
    n = len(shuffled)
    train_end = int(n * train_ratio)
    val_end = train_end + int(n * val_ratio)
    
    train_incidents = shuffled[:train_end]
    val_incidents = shuffled[train_end:val_end]
    test_incidents = shuffled[val_end:]
    
    return train_incidents, val_incidents, test_incidents

