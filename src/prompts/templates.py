"""
Prompt templates for different reasoning modes.
"""


def zero_shot_prompt(incident_text: str) -> str:
    """
    Zero-shot prompt template.
    
    Args:
        incident_text: Formatted incident description
    
    Returns:
        Complete prompt string
    """
    return f"""You are an expert database reliability engineer. Given the following incident data:

{incident_text}

Question: What is the most likely root cause? Answer in one phrase and then provide a short 2-3 sentence justification."""


def chain_of_thought_prompt(incident_text: str) -> str:
    """
    Chain-of-Thought prompt template.
    
    Args:
        incident_text: Formatted incident description
    
    Returns:
        Complete prompt string
    """
    return f"""You are an expert DB SRE. Read the incident below and reason step-by-step. Show your chain-of-thought, then conclude with the single most likely root cause and a short remediation suggestion.

Incident:
{incident_text}

Please analyze this step by step:
1. What metrics show anomalies?
2. What do the logs indicate?
3. What system metadata is relevant?
4. What is the most likely root cause?
5. What remediation steps would you recommend?"""


def rag_prompt(incident_text: str, retrieved_docs: str) -> str:
    """
    RAG (Retrieval-Augmented Generation) prompt template.
    
    Args:
        incident_text: Formatted incident description
        retrieved_docs: Retrieved knowledge base snippets
    
    Returns:
        Complete prompt string
    """
    return f"""You are an expert DB SRE. Use the following knowledge snippets retrieved from runbooks and past incidents:

{retrieved_docs}

Incident:
{incident_text}

Question: Provide the top-1 root cause and brief justification based on the knowledge base and incident data."""


def agent_prompt(incident_text: str, tool_outputs: str = "") -> str:
    """
    Tool-augmented agent prompt template.
    
    Args:
        incident_text: Formatted incident description
        tool_outputs: Outputs from tools (anomaly scores, metric summaries, etc.)
    
    Returns:
        Complete prompt string
    """
    base_prompt = f"""You are an expert DB SRE with access to diagnostic tools. Analyze the following incident using the tool outputs provided.

Incident:
{incident_text}
"""
    
    if tool_outputs:
        base_prompt += f"""
Tool Outputs:
{tool_outputs}
"""
    
    base_prompt += """
You can use the following tools:
- compute_anomaly_scores(): Analyze metric time series for anomalies
- list_top_metrics(): Identify metrics with highest deviation
- summarize_logs(): Extract key patterns from logs

Based on the incident data and tool outputs, provide:
1. The most likely root cause
2. Supporting evidence from metrics/logs/tools
3. Recommended remediation steps"""
    
    return base_prompt


# Root cause labels for reference
ROOT_CAUSE_LABELS = [
    "connection_pool_exhaustion",
    "long_running_queries",
    "network_partition",
    "schema_migration_pause",
    "disk_full",
    "memory_leak",
    "CPU_spike_due_to_backup"
]

