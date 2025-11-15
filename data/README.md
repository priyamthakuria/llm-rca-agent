# Data Directory

## Structure

- `raw/`: Raw datasets (CSV/JSON files)
- `synthetic/`: Generated synthetic incidents (JSON format)

## Incident Schema

Each incident is stored as a JSON file with the following structure:

```json
{
  "incident_id": "INC0001",
  "timestamp_start": "2025-10-10T12:34:00Z",
  "timestamp_end": "2025-10-10T12:50:00Z",
  "metrics": {
    "cpu": [[t0, v0], [t1, v1], ...],
    "latency": [[...]],
    "error_rate": [[...]],
    "connections": [[...]]
  },
  "logs_summary": "top 5 log lines / aggregated keywords",
  "system_meta": {
    "db_type": "postgresql",
    "replication": "on",
    "recent_deploy": true,
    "recent_config_change": false
  },
  "human_notes": "short human-level description",
  "root_cause": "connection_pool_exhaustion",
  "rca_explanation": "pool max connections was 20 but traffic increased to 120..."
}
```

## Root Cause Labels

- `connection_pool_exhaustion`
- `long_running_queries`
- `network_partition`
- `schema_migration_pause`
- `disk_full`
- `memory_leak`
- `CPU_spike_due_to_backup`

