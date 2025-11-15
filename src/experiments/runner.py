"""
Experiment runner for RCA experiments.
"""
import argparse
import yaml
import json
from pathlib import Path
from typing import Dict

from src.models.llm_interface import LLMInterface
from src.models.rag import RAGPipeline
from src.models.agent_runner import ToolAugmentedAgent
from src.data.loader import load_incidents_from_dir, format_incident_for_prompt, split_incidents
from src.prompts.templates import zero_shot_prompt, chain_of_thought_prompt
from src.eval.evaluator import Evaluator


def create_zero_shot_pipeline(config: Dict):
    """Create zero-shot pipeline."""
    llm = LLMInterface(
        backend=config['model']['backend'],
        model_name=config['model']['model_name'],
        temperature=config['model']['temperature'],
        max_tokens=config['model']['max_tokens']
    )
    
    def pipeline(incident):
        incident_text = format_incident_for_prompt(incident)
        prompt = zero_shot_prompt(incident_text)
        response = llm.call(prompt)
        
        # Simple extraction (in practice, use structured output)
        prediction = _extract_prediction(response['text'])
        
        return {
            'prediction': prediction,
            'explanation': response['text'],
            'latency': response['latency']
        }
    
    return pipeline


def create_cot_pipeline(config: Dict):
    """Create chain-of-thought pipeline."""
    llm = LLMInterface(
        backend=config['model']['backend'],
        model_name=config['model']['model_name'],
        temperature=config['model']['temperature'],
        max_tokens=config['model']['max_tokens']
    )
    
    def pipeline(incident):
        incident_text = format_incident_for_prompt(incident)
        prompt = chain_of_thought_prompt(incident_text)
        response = llm.call(prompt)
        
        prediction = _extract_prediction(response['text'])
        
        return {
            'prediction': prediction,
            'explanation': response['text'],
            'latency': response['latency']
        }
    
    return pipeline


def create_rag_pipeline(config: Dict):
    """Create RAG pipeline."""
    # Load knowledge base (create a simple one if it doesn't exist)
    kb_path = config.get('retrieval', {}).get('knowledge_base_path', 'data/knowledge_base.json')
    
    if Path(kb_path).exists():
        with open(kb_path, 'r') as f:
            knowledge_base = json.load(f)
    else:
        # Create a simple knowledge base
        knowledge_base = _create_default_knowledge_base()
        Path(kb_path).parent.mkdir(parents=True, exist_ok=True)
        with open(kb_path, 'w') as f:
            json.dump(knowledge_base, f, indent=2)
    
    llm = LLMInterface(
        backend=config['model']['backend'],
        model_name=config['model']['model_name'],
        temperature=config['model']['temperature'],
        max_tokens=config['model']['max_tokens']
    )
    
    rag = RAGPipeline(
        knowledge_base=knowledge_base,
        embedding_model=config.get('embedding', {}).get('model_name', 'all-MiniLM-L6-v2'),
        llm_interface=llm
    )
    
    def pipeline(incident):
        incident_text = format_incident_for_prompt(incident)
        result = rag.generate(incident_text, k=config.get('retrieval', {}).get('top_k', 5))
        return result
    
    return pipeline


def create_agent_pipeline(config: Dict):
    """Create tool-augmented agent pipeline."""
    llm = LLMInterface(
        backend=config['model']['backend'],
        model_name=config['model']['model_name'],
        temperature=config['model']['temperature'],
        max_tokens=config['model']['max_tokens']
    )
    
    agent = ToolAugmentedAgent(llm)
    
    def pipeline(incident):
        result = agent.diagnose(incident)
        return result
    
    return pipeline


def _extract_prediction(text: str) -> str:
    """Extract root cause prediction from text."""
    root_causes = [
        "connection_pool_exhaustion",
        "long_running_queries",
        "network_partition",
        "schema_migration_pause",
        "disk_full",
        "memory_leak",
        "CPU_spike_due_to_backup"
    ]
    
    text_lower = text.lower()
    for cause in root_causes:
        if cause.replace('_', ' ') in text_lower or cause in text_lower:
            return cause
    
    return "unknown"


def _create_default_knowledge_base() -> list:
    """Create a default knowledge base with runbook snippets."""
    return [
        {
            "id": "kb001",
            "text": "Connection pool exhaustion occurs when the number of concurrent database connections exceeds the configured maximum. Symptoms include high latency, connection timeouts, and errors like 'too many connections'. Remediation: increase max_connections, implement connection pooling, or optimize query patterns.",
            "metadata": {"type": "runbook", "topic": "connection_pool_exhaustion"}
        },
        {
            "id": "kb002",
            "text": "Long-running queries can block other transactions and cause deadlocks. Look for queries missing indexes, full table scans, or complex joins. Check for lock wait timeouts in logs. Remediation: add indexes, optimize queries, or break into smaller transactions.",
            "metadata": {"type": "runbook", "topic": "long_running_queries"}
        },
        {
            "id": "kb003",
            "text": "Network partition issues manifest as high latency, connection failures, and replication lag. Check network connectivity between nodes, firewall rules, and DNS resolution. Remediation: restore network connectivity, check routing tables, verify DNS.",
            "metadata": {"type": "runbook", "topic": "network_partition"}
        },
        {
            "id": "kb004",
            "text": "Schema migrations can lock tables and block operations. ALTER TABLE operations are particularly blocking. Symptoms include increased latency during migration window. Remediation: use online DDL tools, schedule during low-traffic periods, or use blue-green deployments.",
            "metadata": {"type": "runbook", "topic": "schema_migration_pause"}
        },
        {
            "id": "kb005",
            "text": "Disk full errors prevent database writes and can cause crashes. Monitor disk usage proactively. Symptoms include I/O errors, write failures, and 'no space left on device' messages. Remediation: free up disk space, expand storage, or archive old data.",
            "metadata": {"type": "runbook", "topic": "disk_full"}
        },
        {
            "id": "kb006",
            "text": "Memory leaks cause gradual increase in memory usage leading to OOM (Out of Memory) errors. Check for unclosed connections, unbounded result sets, or memory-intensive operations. Remediation: fix memory leaks, increase memory limits, or restart services.",
            "metadata": {"type": "runbook", "topic": "memory_leak"}
        },
        {
            "id": "kb007",
            "text": "CPU spikes during backups are normal but can impact query performance. Full database backups are particularly CPU-intensive. Symptoms include high CPU usage during backup windows. Remediation: schedule backups during off-peak hours, use incremental backups, or increase CPU resources.",
            "metadata": {"type": "runbook", "topic": "CPU_spike_due_to_backup"}
        }
    ]


def main():
    parser = argparse.ArgumentParser(description="Run RCA experiment")
    parser.add_argument("--config", type=str, required=True, help="Path to experiment config YAML")
    
    args = parser.parse_args()
    
    # Load config
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)
    
    experiment_id = config['experiment_id']
    mode = config['mode']
    
    print(f"Running experiment: {experiment_id} (mode: {mode})")
    
    # Load incidents
    data_path = config['data']['test_set_path']
    incidents = load_incidents_from_dir(data_path)
    
    # Split if needed (for now, use all as test)
    # train, val, test = split_incidents(incidents, seed=config.get('seed', 42))
    test_incidents = incidents  # Use all for now
    
    print(f"Loaded {len(test_incidents)} incidents")
    
    # Create pipeline based on mode
    if mode == "zero_shot":
        pipeline = create_zero_shot_pipeline(config)
    elif mode == "chain_of_thought":
        pipeline = create_cot_pipeline(config)
    elif mode == "rag":
        pipeline = create_rag_pipeline(config)
    elif mode == "agent":
        pipeline = create_agent_pipeline(config)
    else:
        raise ValueError(f"Unknown mode: {mode}")
    
    # Run evaluation
    evaluator = Evaluator(output_dir=config['output']['results_dir'])
    
    labels = [
        "connection_pool_exhaustion",
        "long_running_queries",
        "network_partition",
        "schema_migration_pause",
        "disk_full",
        "memory_leak",
        "CPU_spike_due_to_backup"
    ]
    
    results = evaluator.evaluate_pipeline(
        test_incidents,
        pipeline,
        experiment_id,
        labels
    )
    
    # Save results
    evaluator.save_results(experiment_id)
    
    # Print summary
    print("\n" + "="*50)
    print("Experiment Results Summary")
    print("="*50)
    print(f"Experiment ID: {experiment_id}")
    print(f"Mode: {mode}")
    print(f"Accuracy: {results['metrics']['accuracy']:.3f}")
    print(f"Macro F1: {results['metrics']['macro_f1']:.3f}")
    print(f"Average Latency: {results['avg_latency_sec']:.3f}s")
    print("="*50)


if __name__ == "__main__":
    main()

