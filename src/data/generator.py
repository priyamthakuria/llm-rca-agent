"""
Generate synthetic database incidents for RCA evaluation.
"""
import json
import random
import numpy as np
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple


# Root cause labels
ROOT_CAUSES = [
    "connection_pool_exhaustion",
    "long_running_queries",
    "network_partition",
    "schema_migration_pause",
    "disk_full",
    "memory_leak",
    "CPU_spike_due_to_backup"
]

# Log templates for each root cause
LOG_TEMPLATES = {
    "connection_pool_exhaustion": [
        "ERROR: connection timeout after 30s",
        "WARN: connection pool exhausted, waiting for available connection",
        "ERROR: failed to acquire connection from pool",
        "WARN: max connections (20) reached",
        "ERROR: too many connections"
    ],
    "long_running_queries": [
        "WARN: query execution time exceeded 60s",
        "ERROR: deadlock detected, transaction rolled back",
        "WARN: lock wait timeout",
        "ERROR: query blocked by long-running transaction",
        "WARN: slow query detected (>10s)"
    ],
    "network_partition": [
        "ERROR: network unreachable",
        "WARN: connection lost to replica",
        "ERROR: timeout waiting for network response",
        "WARN: high network latency detected (>500ms)",
        "ERROR: failed to connect to database server"
    ],
    "schema_migration_pause": [
        "INFO: schema migration in progress",
        "WARN: table locked for migration",
        "INFO: ALTER TABLE operation started",
        "WARN: migration blocking queries",
        "INFO: schema version update"
    ],
    "disk_full": [
        "ERROR: disk full, cannot write",
        "WARN: disk usage at 95%",
        "ERROR: insufficient disk space",
        "WARN: I/O error writing to disk",
        "ERROR: no space left on device"
    ],
    "memory_leak": [
        "WARN: memory usage steadily increasing",
        "ERROR: out of memory (OOM)",
        "WARN: memory usage at 90%",
        "ERROR: failed to allocate memory",
        "WARN: memory leak suspected"
    ],
    "CPU_spike_due_to_backup": [
        "INFO: backup process started",
        "WARN: CPU usage spike detected",
        "INFO: full database backup in progress",
        "WARN: high CPU utilization (>90%)",
        "INFO: backup completed"
    ]
}

DB_TYPES = ["postgresql", "mysql", "mongodb", "redis"]

def sample_timeseries(
    length: int = 60,
    baseline: float = 10.0,
    freq: float = 1.0,
    anomaly: Optional[str] = None,
    anomaly_magnitude: float = 1.0
) -> List[List[float]]:
    """
    Generate a time series with optional anomalies.
    
    Args:
        length: Number of time points
        baseline: Baseline value
        freq: Frequency for sinusoidal component
        anomaly: Type of anomaly ('spike', 'drift', 'drop')
        anomaly_magnitude: Magnitude of anomaly
    
    Returns:
        List of [timestamp, value] pairs
    """
    t = list(range(length))
    # Base signal with noise
    vals = baseline + np.random.normal(0, 0.5, length)
    
    # Add sinusoidal component
    vals += 2 * np.sin(2 * np.pi * freq * np.array(t) / length)
    
    if anomaly == "spike":
        pos = random.randint(length // 3, 2 * length // 3)
        spike_height = np.random.uniform(5, 20) * anomaly_magnitude
        vals[pos:pos+3] += spike_height
    elif anomaly == "drift":
        pos = random.randint(length // 3, 2 * length // 3)
        drift = np.linspace(0, 10 * anomaly_magnitude, length - pos)
        vals[pos:] += drift
    elif anomaly == "drop":
        pos = random.randint(length // 3, 2 * length // 3)
        vals[pos:pos+5] -= np.random.uniform(5, 15) * anomaly_magnitude
    
    return [[float(i), float(v)] for i, v in enumerate(vals)]


def make_incident(incident_id: str, label: str) -> Dict:
    """
    Generate a single synthetic incident.
    
    Args:
        incident_id: Unique identifier for the incident
        label: Root cause label
    
    Returns:
        Dictionary representing the incident
    """
    # Generate timestamps
    start_time = datetime.now() - timedelta(hours=random.randint(1, 24))
    duration_minutes = random.randint(10, 60)
    end_time = start_time + timedelta(minutes=duration_minutes)
    
    # Generate metrics based on root cause
    metrics = {}
    
    if label == "connection_pool_exhaustion":
        metrics["cpu"] = sample_timeseries(baseline=30, anomaly="spike", anomaly_magnitude=1.5)
        metrics["latency"] = sample_timeseries(baseline=50, anomaly="spike", anomaly_magnitude=2.0)
        metrics["error_rate"] = sample_timeseries(baseline=0.1, anomaly="spike", anomaly_magnitude=3.0)
        metrics["connections"] = sample_timeseries(baseline=15, anomaly="spike", anomaly_magnitude=1.2)
    elif label == "long_running_queries":
        metrics["cpu"] = sample_timeseries(baseline=40, anomaly="spike", anomaly_magnitude=1.3)
        metrics["latency"] = sample_timeseries(baseline=100, anomaly="spike", anomaly_magnitude=2.5)
        metrics["error_rate"] = sample_timeseries(baseline=0.5, anomaly="spike", anomaly_magnitude=1.5)
        metrics["connections"] = sample_timeseries(baseline=10, anomaly=None)
    elif label == "network_partition":
        metrics["cpu"] = sample_timeseries(baseline=20, anomaly="spike", anomaly_magnitude=1.2)
        metrics["latency"] = sample_timeseries(baseline=200, anomaly="spike", anomaly_magnitude=3.0)
        metrics["error_rate"] = sample_timeseries(baseline=1.0, anomaly="spike", anomaly_magnitude=2.0)
        metrics["connections"] = sample_timeseries(baseline=8, anomaly="drop", anomaly_magnitude=1.5)
    elif label == "schema_migration_pause":
        metrics["cpu"] = sample_timeseries(baseline=25, anomaly="spike", anomaly_magnitude=1.1)
        metrics["latency"] = sample_timeseries(baseline=80, anomaly="spike", anomaly_magnitude=2.0)
        metrics["error_rate"] = sample_timeseries(baseline=0.2, anomaly="spike", anomaly_magnitude=1.3)
        metrics["connections"] = sample_timeseries(baseline=12, anomaly="drop", anomaly_magnitude=1.2)
    elif label == "disk_full":
        metrics["cpu"] = sample_timeseries(baseline=35, anomaly="spike", anomaly_magnitude=1.4)
        metrics["latency"] = sample_timeseries(baseline=150, anomaly="spike", anomaly_magnitude=2.2)
        metrics["error_rate"] = sample_timeseries(baseline=2.0, anomaly="spike", anomaly_magnitude=2.5)
        metrics["connections"] = sample_timeseries(baseline=10, anomaly=None)
    elif label == "memory_leak":
        metrics["cpu"] = sample_timeseries(baseline=30, anomaly="drift", anomaly_magnitude=1.2)
        metrics["latency"] = sample_timeseries(baseline=60, anomaly="drift", anomaly_magnitude=1.3)
        metrics["error_rate"] = sample_timeseries(baseline=0.3, anomaly="drift", anomaly_magnitude=1.4)
        metrics["connections"] = sample_timeseries(baseline=12, anomaly="drift", anomaly_magnitude=1.1)
    elif label == "CPU_spike_due_to_backup":
        metrics["cpu"] = sample_timeseries(baseline=20, anomaly="spike", anomaly_magnitude=2.0)
        metrics["latency"] = sample_timeseries(baseline=40, anomaly="spike", anomaly_magnitude=1.5)
        metrics["error_rate"] = sample_timeseries(baseline=0.1, anomaly=None)
        metrics["connections"] = sample_timeseries(baseline=10, anomaly=None)
    else:
        # Default metrics
        metrics["cpu"] = sample_timeseries(baseline=25, anomaly="spike")
        metrics["latency"] = sample_timeseries(baseline=50, anomaly="spike")
        metrics["error_rate"] = sample_timeseries(baseline=0.5, anomaly="spike")
        metrics["connections"] = sample_timeseries(baseline=10, anomaly="spike")
    
    # Generate log summary
    log_lines = random.sample(LOG_TEMPLATES[label], k=min(3, len(LOG_TEMPLATES[label])))
    logs_summary = " | ".join(log_lines)
    
    # Generate system metadata
    system_meta = {
        "db_type": random.choice(DB_TYPES),
        "replication": random.choice(["on", "off"]),
        "recent_deploy": random.choice([True, False]),
        "recent_config_change": random.choice([True, False])
    }
    
    # Generate human notes
    human_notes = f"Incident detected at {start_time.strftime('%Y-%m-%d %H:%M:%S')}. " \
                  f"Observed {label.replace('_', ' ')} symptoms. " \
                  f"System: {system_meta['db_type']} with replication {system_meta['replication']}."
    
    # Generate RCA explanation
    rca_explanations = {
        "connection_pool_exhaustion": "Connection pool max connections was set to 20, but traffic increased to 120 concurrent requests, exhausting available connections.",
        "long_running_queries": "Several queries with missing indexes were blocking other transactions, causing deadlocks and timeouts.",
        "network_partition": "Network connectivity issues between primary and replica nodes caused high latency and connection failures.",
        "schema_migration_pause": "A schema migration operation locked critical tables, blocking read/write operations for 15 minutes.",
        "disk_full": "Disk usage reached 100% capacity, preventing database writes and causing I/O errors.",
        "memory_leak": "Memory usage steadily increased over 2 hours due to unclosed connections, eventually causing OOM.",
        "CPU_spike_due_to_backup": "Scheduled full database backup process consumed 90%+ CPU resources, impacting query performance."
    }
    
    incident = {
        "incident_id": incident_id,
        "timestamp_start": start_time.isoformat() + "Z",
        "timestamp_end": end_time.isoformat() + "Z",
        "metrics": metrics,
        "logs_summary": logs_summary,
        "system_meta": system_meta,
        "human_notes": human_notes,
        "root_cause": label,
        "rca_explanation": rca_explanations.get(label, "Root cause analysis pending.")
    }
    
    return incident


def generate_incidents(
    num_incidents: int = 300,
    output_dir: str = "data/synthetic",
    seed: int = 42
) -> List[str]:
    """
    Generate multiple synthetic incidents.
    
    Args:
        num_incidents: Total number of incidents to generate
        output_dir: Directory to save incident JSON files
        seed: Random seed for reproducibility
    
    Returns:
        List of generated incident file paths
    """
    random.seed(seed)
    np.random.seed(seed)
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Balance classes
    incidents_per_class = num_incidents // len(ROOT_CAUSES)
    remainder = num_incidents % len(ROOT_CAUSES)
    
    generated_files = []
    incident_counter = 1
    
    for label in ROOT_CAUSES:
        count = incidents_per_class + (1 if remainder > 0 else 0)
        remainder -= 1
        
        for i in range(count):
            incident_id = f"INC{incident_counter:04d}"
            incident = make_incident(incident_id, label)
            
            filename = os.path.join(output_dir, f"{incident_id}.json")
            with open(filename, 'w') as f:
                json.dump(incident, f, indent=2)
            
            generated_files.append(filename)
            incident_counter += 1
    
    print(f"Generated {len(generated_files)} incidents in {output_dir}")
    return generated_files


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate synthetic database incidents")
    parser.add_argument("--num_incidents", type=int, default=300, help="Number of incidents to generate")
    parser.add_argument("--output_dir", type=str, default="data/synthetic", help="Output directory")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    
    args = parser.parse_args()
    generate_incidents(args.num_incidents, args.output_dir, args.seed)

