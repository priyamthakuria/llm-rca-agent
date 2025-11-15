# Complete Learning Guide: LLM-Assisted Root Cause Analysis

**Welcome!** This guide will teach you everything about this project from scratch. We'll assume you know Python basics (variables, functions, classes, dictionaries, lists) but nothing about machine learning, LLMs, or database systems.

---

## Table of Contents

1. [What is This Project About?](#what-is-this-project-about)
2. [Core Concepts You Need to Know](#core-concepts-you-need-to-know)
3. [Project Structure Explained](#project-structure-explained)
4. [Deep Dive: Each Component](#deep-dive-each-component)
5. [How Everything Works Together](#how-everything-works-together)
6. [Step-by-Step Walkthrough](#step-by-step-walkthrough)
7. [Common Questions & Answers](#common-questions--answers)

---

## What is This Project About?

### The Problem We're Solving

Imagine you're a database administrator (DBA) or Site Reliability Engineer (SRE). Your database suddenly becomes slow, or starts throwing errors. You need to figure out **why** - this is called **Root Cause Analysis (RCA)**.

**Example Scenario:**
- Your database is suddenly very slow
- Users are complaining
- You see error messages in logs
- CPU usage is high
- You need to find the root cause quickly!

**Traditional Approach:**
- Manually check logs
- Look at metrics (CPU, memory, disk)
- Read documentation/runbooks
- Use experience to diagnose
- **This takes time and expertise!**

**Our Approach:**
- Use AI (Large Language Models) to automatically diagnose
- Compare different AI reasoning methods
- Measure which method works best

### What We're Comparing

We test **4 different ways** to use AI for diagnosis:

1. **Zero-Shot**: Ask AI directly, no training
2. **Chain-of-Thought**: Ask AI to think step-by-step
3. **RAG**: Give AI access to a knowledge base (like a library)
4. **Agent**: Give AI tools to analyze data first, then diagnose

---

## Core Concepts You Need to Know

### 1. What is a Large Language Model (LLM)?

Think of an LLM as a **very smart autocomplete** that has read millions of books, articles, and code.

**Simple Analogy:**
- You type: "The weather today is..."
- It predicts: "...sunny and warm"
- But it's so good, it can answer questions, write code, analyze problems!

**In Our Project:**
- We use LLMs like GPT-4 (OpenAI) or open-source models
- We give them information about a database incident
- They predict what the root cause might be

### 2. What is Root Cause Analysis (RCA)?

**Root Cause** = The fundamental reason something went wrong

**Example:**
- **Symptom**: Database is slow
- **Surface Issue**: High CPU usage
- **Root Cause**: A backup process is running and consuming all CPU

**In Our Project:**
- We have 7 types of root causes (connection pool exhaustion, disk full, etc.)
- Each has specific symptoms (metrics, logs)
- AI tries to identify which root cause matches the symptoms

### 3. What is Synthetic Data?

**Real Data**: Actual incidents from production (hard to get, privacy issues)

**Synthetic Data**: We **create fake but realistic** incidents for testing

**Why?**
- We know the "ground truth" (the correct answer)
- We can create many examples quickly
- No privacy concerns
- Perfect for research and testing

**In Our Project:**
- We generate 300+ synthetic database incidents
- Each has metrics, logs, and a known root cause
- We test if AI can correctly identify the root cause

### 4. What are Metrics?

**Metrics** = Numbers that describe system health over time

**Examples:**
- **CPU Usage**: 0-100% (how busy the processor is)
- **Latency**: milliseconds (how long queries take)
- **Error Rate**: percentage (how many requests fail)
- **Connections**: count (how many database connections are active)

**In Our Project:**
- Each incident has time-series metrics (values over time)
- We show metrics like: `[[0, 10.5], [1, 12.3], [2, 15.8], ...]`
- This means: at time 0, value was 10.5; at time 1, value was 12.3, etc.

### 5. What is a Prompt?

**Prompt** = Instructions you give to an LLM

**Example:**
```
You are an expert doctor. A patient has:
- Fever: 101°F
- Cough: Yes
- Headache: Yes

What is the diagnosis?
```

**In Our Project:**
- We create prompts that describe database incidents
- We ask the LLM to diagnose the root cause
- Different prompts = different reasoning methods

### 6. What is RAG (Retrieval-Augmented Generation)?

**RAG** = Give the LLM access to a knowledge base before answering

**Simple Analogy:**
- **Without RAG**: You ask a student a question, they answer from memory
- **With RAG**: You give them a textbook, they look it up, then answer

**In Our Project:**
- We have a knowledge base (runbooks, past incidents)
- When an incident happens, we search for similar cases
- We give those cases to the LLM along with the current incident
- LLM uses both to make a better diagnosis

### 7. What is an Agent?

**Agent** = An AI that can use tools (functions) to help it think

**Simple Analogy:**
- **Regular AI**: "Here's the data, what do you think?"
- **Agent**: "Let me first calculate some statistics, then analyze logs, then answer"

**In Our Project:**
- Agent has tools like:
  - `compute_anomaly_scores()`: Find which metrics are abnormal
  - `list_top_metrics()`: Find the most problematic metrics
  - `summarize_logs()`: Extract key patterns from logs
- Agent uses these tools, then asks LLM to interpret the results

---

## Project Structure Explained

Let's understand the folder structure:

```
llm-rca-agent/
├── data/                    # All data files
│   ├── raw/                # Raw datasets (empty for now)
│   └── synthetic/          # Generated synthetic incidents (JSON files)
│
├── src/                     # All source code
│   ├── data/               # Data generation and loading
│   │   ├── generator.py    # Creates synthetic incidents
│   │   └── loader.py       # Loads incidents from files
│   │
│   ├── models/             # AI/LLM related code
│   │   ├── llm_interface.py  # Wrapper to call LLMs (OpenAI/HuggingFace)
│   │   ├── rag.py          # RAG pipeline implementation
│   │   └── agent_runner.py  # Agent with tools
│   │
│   ├── prompts/            # Prompt templates
│   │   └── templates.py   # Different prompt styles
│   │
│   ├── eval/               # Evaluation code
│   │   ├── metrics.py     # Calculate accuracy, F1, etc.
│   │   └── evaluator.py    # Run experiments and evaluate
│   │
│   ├── experiments/        # Experiment runner
│   │   └── runner.py       # Main script to run experiments
│   │
│   └── utils/              # Helper utilities
│       ├── viz.py          # Plotting/visualization
│       └── logging_setup.py # Logging configuration
│
├── experiments/            # Experiment configurations
│   ├── configs/           # YAML config files for each experiment
│   └── run_experiment.sh  # Shell script to run experiments
│
├── notebooks/             # Jupyter notebooks for analysis
│   ├── EDA_synthetic_incidents.ipynb  # Explore the data
│   └── analysis_plots.ipynb            # Create visualizations
│
├── tests/                 # Unit tests
│   └── test_data_gen.py   # Test data generation
│
└── reports/               # Final reports and figures
    └── report_draft.md    # Research report template
```

---

## Deep Dive: Each Component

### Component 1: Data Generator (`src/data/generator.py`)

**Purpose**: Create fake but realistic database incidents for testing.

#### Key Concepts:

**1. Time Series Generation**
```python
def sample_timeseries(length=60, baseline=10.0, anomaly="spike"):
    # Creates a list of [timestamp, value] pairs
    # Example: [[0, 10.5], [1, 12.3], [2, 15.8], ...]
```

**What's happening:**
- We create 60 data points (one per minute)
- Start with a baseline value (e.g., 10.0)
- Add random noise (makes it realistic)
- Optionally add an anomaly (spike, drift, or drop)

**Example Output:**
```python
[
    [0, 10.2],   # Time 0: CPU at 10.2%
    [1, 10.5],   # Time 1: CPU at 10.5%
    [2, 11.1],   # Time 2: CPU at 11.1%
    ...
    [30, 45.8],  # Time 30: CPU spikes to 45.8% (anomaly!)
    [31, 48.2],  # Time 31: CPU still high
    ...
]
```

**2. Root Cause Types**

We have 7 types of problems:

1. **connection_pool_exhaustion**: Too many connections, pool runs out
2. **long_running_queries**: Queries take too long, block others
3. **network_partition**: Network issues between database nodes
4. **schema_migration_pause**: Database schema changes block operations
5. **disk_full**: No disk space left
6. **memory_leak**: Memory usage keeps growing
7. **CPU_spike_due_to_backup**: Backup process uses all CPU

**3. How We Generate an Incident**

```python
def make_incident(incident_id, label):
    # Step 1: Generate timestamps
    start_time = datetime.now() - timedelta(hours=random.randint(1, 24))
    end_time = start_time + timedelta(minutes=random.randint(10, 60))
    
    # Step 2: Generate metrics based on root cause type
    if label == "connection_pool_exhaustion":
        metrics["cpu"] = sample_timeseries(baseline=30, anomaly="spike")
        metrics["latency"] = sample_timeseries(baseline=50, anomaly="spike")
        # ... more metrics
    
    # Step 3: Generate log messages
    log_lines = random.sample(LOG_TEMPLATES[label], k=3)
    logs_summary = " | ".join(log_lines)
    
    # Step 4: Generate system metadata
    system_meta = {
        "db_type": random.choice(["postgresql", "mysql", "mongodb", "redis"]),
        "replication": random.choice(["on", "off"]),
        ...
    }
    
    # Step 5: Create the incident dictionary
    return {
        "incident_id": "INC0001",
        "timestamp_start": "...",
        "metrics": {...},
        "logs_summary": "...",
        "root_cause": "connection_pool_exhaustion",  # Ground truth!
        ...
    }
```

**Why This Matters:**
- We know the correct answer (`root_cause`)
- We can test if AI guesses correctly
- We can measure accuracy

---

### Component 2: LLM Interface (`src/models/llm_interface.py`)

**Purpose**: A wrapper that lets us call different LLMs (OpenAI, HuggingFace) in the same way.

#### Key Concepts:

**1. What is an Interface/Wrapper?**

Think of it like a universal remote:
- Different TVs have different buttons
- Universal remote has same buttons for all TVs
- You don't need to learn each TV separately

**In Code:**
```python
# Without wrapper: Different code for each LLM
openai_response = openai.ChatCompletion.create(...)  # OpenAI way
huggingface_response = model.generate(...)            # HuggingFace way

# With wrapper: Same code for both!
llm = LLMInterface(backend="openai", model_name="gpt-4")
response = llm.call("What is the root cause?")  # Works for both!
```

**2. How It Works**

```python
class LLMInterface:
    def __init__(self, backend="openai", model_name="gpt-4"):
        self.backend = backend
        if backend == "openai":
            # Set up OpenAI client
            self.client = openai.OpenAI(api_key=api_key)
        elif backend == "huggingface":
            # Set up HuggingFace model
            self.model = AutoModelForCausalLM.from_pretrained(model_name)
    
    def call(self, prompt):
        start = time.time()  # Start timer
        
        if self.backend == "openai":
            # Call OpenAI API
            response = self.client.chat.completions.create(...)
            text = response.choices[0].message.content
        elif self.backend == "huggingface":
            # Call local model
            inputs = self.tokenizer(prompt, ...)
            outputs = self.model.generate(inputs, ...)
            text = self.tokenizer.decode(outputs)
        
        latency = time.time() - start  # Calculate time taken
        
        return {
            "text": text,           # The AI's response
            "latency": latency,     # How long it took (seconds)
            "model": self.model_name
        }
```

**3. Important Parameters**

- **temperature**: Controls randomness
  - `0.0` = Deterministic (same input → same output)
  - `1.0` = Very creative/random
  - We use `0.0` for consistent results

- **max_tokens**: Maximum length of response
  - `512` = Response can be up to 512 tokens (~400 words)
  - Prevents very long responses

**Why This Matters:**
- We can easily switch between different LLMs
- We measure how long each call takes (latency)
- Consistent interface makes code simpler

---

### Component 3: Prompt Templates (`src/prompts/templates.py`)

**Purpose**: Different ways to ask the LLM the same question.

#### The 4 Prompt Types:

**1. Zero-Shot Prompt**

**What it means**: Ask directly, no examples, no hints.

```python
def zero_shot_prompt(incident_text):
    return f"""You are an expert database reliability engineer. 
    Given the following incident data:
    
    {incident_text}
    
    Question: What is the most likely root cause? 
    Answer in one phrase and then provide a short 2-3 sentence justification."""
```

**Example Output:**
```
Root cause: connection_pool_exhaustion

The incident shows high latency, connection timeouts, and error messages 
indicating max connections reached. The connection pool was set to 20 but 
traffic increased to 120 concurrent requests, exhausting available connections.
```

**2. Chain-of-Thought (CoT) Prompt**

**What it means**: Ask the LLM to show its reasoning step-by-step.

```python
def chain_of_thought_prompt(incident_text):
    return f"""You are an expert DB SRE. Read the incident below and 
    reason step-by-step. Show your chain-of-thought, then conclude with 
    the single most likely root cause.
    
    Incident:
    {incident_text}
    
    Please analyze this step by step:
    1. What metrics show anomalies?
    2. What do the logs indicate?
    3. What system metadata is relevant?
    4. What is the most likely root cause?
    5. What remediation steps would you recommend?"""
```

**Example Output:**
```
Step 1: Metrics show anomalies:
- CPU: Spiked from 20% to 90%
- Latency: Increased from 50ms to 500ms
- Error rate: Increased from 0.1% to 5%

Step 2: Logs indicate:
- "ERROR: connection timeout after 30s"
- "WARN: connection pool exhausted"

Step 3: System metadata:
- Database: PostgreSQL
- Replication: On
- Recent deploy: No

Step 4: Most likely root cause:
connection_pool_exhaustion

Step 5: Remediation:
- Increase max_connections setting
- Implement connection pooling
- Optimize query patterns
```

**Why CoT Works Better:**
- Forces the model to think through the problem
- Similar to how humans solve problems
- Often improves accuracy

**3. RAG Prompt**

**What it means**: Give the LLM relevant information from a knowledge base.

```python
def rag_prompt(incident_text, retrieved_docs):
    return f"""You are an expert DB SRE. Use the following knowledge 
    snippets retrieved from runbooks and past incidents:
    
    {retrieved_docs}
    
    Incident:
    {incident_text}
    
    Question: Provide the top-1 root cause and brief justification 
    based on the knowledge base and incident data."""
```

**Example `retrieved_docs`:**
```
[kb001] Connection pool exhaustion occurs when the number of concurrent 
database connections exceeds the configured maximum. Symptoms include 
high latency, connection timeouts, and errors like 'too many connections'. 
Remediation: increase max_connections, implement connection pooling, or 
optimize query patterns.

[kb002] Long-running queries can block other transactions and cause 
deadlocks. Look for queries missing indexes, full table scans, or complex 
joins. Check for lock wait timeouts in logs.
```

**Why RAG Works:**
- LLM has access to expert knowledge
- Can reference similar past incidents
- More accurate than relying only on training data

**4. Agent Prompt**

**What it means**: Give the LLM results from analysis tools first.

```python
def agent_prompt(incident_text, tool_outputs):
    return f"""You are an expert DB SRE with access to diagnostic tools. 
    Analyze the following incident using the tool outputs provided.
    
    Incident:
    {incident_text}
    
    Tool Outputs:
    {tool_outputs}
    
    Based on the incident data and tool outputs, provide:
    1. The most likely root cause
    2. Supporting evidence from metrics/logs/tools
    3. Recommended remediation steps"""
```

**Example `tool_outputs`:**
```
Anomaly Scores:
  cpu: 3.45
  latency: 4.12
  error_rate: 2.89
  connections: 2.34

Top Anomalous Metrics: latency, cpu, error_rate

Log Analysis:
  Errors: 3
  Warnings: 2
  Has Errors: True
```

**Why Agents Work:**
- Tools do statistical analysis (humans are good at this)
- LLM interprets the results (LLMs are good at this)
- Best of both worlds!

---

### Component 4: RAG Pipeline (`src/models/rag.py`)

**Purpose**: Retrieve relevant knowledge base documents and use them in the prompt.

#### How RAG Works:

**Step 1: Build a Knowledge Base**

```python
knowledge_base = [
    {
        "id": "kb001",
        "text": "Connection pool exhaustion occurs when...",
        "metadata": {"type": "runbook", "topic": "connection_pool_exhaustion"}
    },
    {
        "id": "kb002",
        "text": "Long-running queries can block...",
        "metadata": {"type": "runbook", "topic": "long_running_queries"}
    },
    # ... more documents
]
```

**Step 2: Convert Text to Numbers (Embeddings)**

**What are Embeddings?**
- Text: "connection pool exhausted"
- Embedding: `[0.23, -0.45, 0.67, ..., 0.12]` (a list of numbers)
- Similar texts have similar numbers
- Allows mathematical comparison!

**In Code:**
```python
from sentence_transformers import SentenceTransformer

# Load a model that converts text → numbers
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Convert all knowledge base texts to numbers
texts = [doc['text'] for doc in knowledge_base]
embeddings = embedding_model.encode(texts)
# embeddings is now a matrix: [[0.23, -0.45, ...], [0.12, 0.67, ...], ...]
```

**Step 3: Build a Search Index (FAISS)**

**What is FAISS?**
- Fast library for similarity search
- Like a search engine for numbers
- Can find similar documents quickly

**In Code:**
```python
import faiss

# Create an index
dimension = embeddings.shape[1]  # e.g., 384 (size of embedding vector)
index = faiss.IndexFlatL2(dimension)  # L2 = Euclidean distance

# Add all embeddings to index
index.add(embeddings.astype('float32'))
```

**Step 4: Retrieve Similar Documents**

```python
def retrieve(self, query, k=5):
    # Convert query to embedding
    query_embedding = self.embedding_model.encode([query])
    
    # Search for k most similar documents
    distances, indices = self.index.search(query_embedding, k)
    
    # Return the documents
    retrieved = []
    for idx, dist in zip(indices[0], distances[0]):
        doc = self.knowledge_base[idx].copy()
        doc['similarity_score'] = 1 / (1 + dist)  # Convert distance to similarity
        retrieved.append(doc)
    
    return retrieved
```

**Step 5: Use Retrieved Docs in Prompt**

```python
def generate(self, incident_text, k=5):
    # Retrieve relevant documents
    retrieved_docs = self.retrieve(incident_text, k=k)
    
    # Format them as text
    retrieved_text = "\n\n".join([
        f"[{doc['id']}] {doc['text']}"
        for doc in retrieved_docs
    ])
    
    # Create RAG prompt
    prompt = rag_prompt(incident_text, retrieved_text)
    
    # Call LLM
    response = self.llm_interface.call(prompt)
    
    return {
        'prediction': extract_prediction(response['text']),
        'explanation': response['text'],
        'retrieved_docs_ids': [doc['id'] for doc in retrieved_docs]
    }
```

**Why RAG is Powerful:**
- LLM doesn't need to memorize everything
- Can access up-to-date knowledge
- Can reference specific past incidents
- More accurate and explainable

---

### Component 5: Tool-Augmented Agent (`src/models/agent_runner.py`)

**Purpose**: Give the LLM tools to analyze data before making a diagnosis.

#### The Tools:

**1. `compute_anomaly_scores()`**

**What it does**: Finds which metrics are abnormal.

```python
def compute_anomaly_scores(self, metrics):
    scores = {}
    for metric_name, values in metrics.items():
        # Extract just the values (ignore timestamps)
        vals = np.array([v[1] for v in values])  # v[1] is the value, v[0] is timestamp
        
        # Calculate mean and standard deviation
        mean = np.mean(vals)
        std = np.std(vals)
        
        # Calculate z-scores (how many standard deviations from mean)
        z_scores = np.abs((vals - mean) / std)
        
        # Anomaly score = maximum z-score
        scores[metric_name] = float(np.max(z_scores))
    
    return scores
```

**Example:**
```python
metrics = {
    "cpu": [[0, 10], [1, 12], [2, 15], [3, 45], [4, 50]],  # Spike at time 3-4
    "latency": [[0, 50], [1, 52], [2, 48], [3, 49], [4, 51]]  # Normal
}

scores = compute_anomaly_scores(metrics)
# Result: {"cpu": 3.2, "latency": 0.5}
# CPU has high anomaly score (3.2), latency is normal (0.5)
```

**2. `list_top_metrics()`**

**What it does**: Finds the most problematic metrics.

```python
def list_top_metrics(self, metrics, top_k=3):
    anomaly_scores = self.compute_anomaly_scores(metrics)
    # Sort by score (highest first)
    sorted_metrics = sorted(anomaly_scores.items(), key=lambda x: x[1], reverse=True)
    # Return top k metric names
    return [name for name, _ in sorted_metrics[:top_k]]
```

**Example:**
```python
top_metrics = list_top_metrics(metrics, top_k=3)
# Result: ["cpu", "error_rate", "latency"]
# These are the 3 most anomalous metrics
```

**3. `summarize_logs()`**

**What it does**: Extracts patterns from log messages.

```python
def summarize_logs(self, logs_summary):
    error_keywords = ['error', 'failed', 'timeout', 'exception']
    warn_keywords = ['warn', 'warning', 'slow']
    
    logs_lower = logs_summary.lower()
    error_count = sum(1 for kw in error_keywords if kw in logs_lower)
    warn_count = sum(1 for kw in warn_keywords if kw in logs_lower)
    
    return {
        'error_count': error_count,
        'warn_count': warn_count,
        'has_errors': error_count > 0,
        'has_warnings': warn_count > 0
    }
```

**Example:**
```python
logs = "ERROR: connection timeout | WARN: slow query detected | ERROR: failed to connect"
summary = summarize_logs(logs)
# Result: {
#     'error_count': 2,
#     'warn_count': 1,
#     'has_errors': True,
#     'has_warnings': True
# }
```

**4. `diagnose()` - Putting It All Together**

```python
def diagnose(self, incident):
    # Step 1: Run all tools
    anomaly_scores = self.compute_anomaly_scores(incident['metrics'])
    top_metrics = self.list_top_metrics(incident['metrics'])
    log_summary = self.summarize_logs(incident['logs_summary'])
    
    # Step 2: Format tool outputs as text
    tool_outputs = f"""
    Anomaly Scores:
      cpu: {anomaly_scores['cpu']:.2f}
      latency: {anomaly_scores['latency']:.2f}
      ...
    
    Top Anomalous Metrics: {', '.join(top_metrics)}
    
    Log Analysis:
      Errors: {log_summary['error_count']}
      Warnings: {log_summary['warn_count']}
    """
    
    # Step 3: Format incident as text
    incident_text = format_incident_for_prompt(incident)
    
    # Step 4: Create agent prompt (includes both incident and tool outputs)
    prompt = agent_prompt(incident_text, tool_outputs)
    
    # Step 5: Call LLM
    response = self.llm_interface.call(prompt)
    
    # Step 6: Extract prediction
    prediction = self._extract_prediction(response['text'])
    
    return {
        'prediction': prediction,
        'explanation': response['text'],
        'latency': response['latency'],
        'tool_outputs': {...}  # Store tool outputs for analysis
    }
```

**Why Agents Are Powerful:**
- Tools do what they're good at (statistics, pattern matching)
- LLM does what it's good at (interpretation, reasoning)
- More accurate than either alone!

---

### Component 6: Evaluator (`src/eval/evaluator.py`)

**Purpose**: Test how well each method works and measure performance.

#### Key Concepts:

**1. What is Evaluation?**

We need to measure:
- **Accuracy**: How often is the prediction correct?
- **Latency**: How long does it take?
- **Per-Class Performance**: Which root causes are easier/harder?

**2. How Evaluation Works**

```python
class Evaluator:
    def evaluate_pipeline(self, incidents, pipeline_func, experiment_id, labels):
        predictions = []
        ground_truths = []
        latencies = []
        
        # For each incident
        for incident in incidents:
            # Run the pipeline (zero-shot, CoT, RAG, or agent)
            result = pipeline_func(incident)
            
            # Store results
            predictions.append(result['prediction'])
            ground_truths.append(incident['root_cause'])  # True answer
            latencies.append(result['latency'])
        
        # Calculate metrics
        metrics = compute_classification_metrics(ground_truths, predictions, labels)
        # Returns: accuracy, F1 score, precision, recall, etc.
        
        return {
            'metrics': metrics,
            'avg_latency_sec': sum(latencies) / len(latencies),
            'confusion_matrix': ...
        }
```

**3. What Metrics Do We Calculate?**

**Accuracy**: Fraction of correct predictions
```
accuracy = (number of correct predictions) / (total predictions)
Example: 250 correct out of 300 = 0.833 (83.3%)
```

**F1 Score**: Balance between precision and recall
- **Precision**: Of all predictions of "connection_pool_exhaustion", how many were correct?
- **Recall**: Of all actual "connection_pool_exhaustion" incidents, how many did we catch?
- **F1**: Harmonic mean of precision and recall

**Confusion Matrix**: Shows which classes are confused with which
```
                Predicted
              A    B    C
Actual  A   50    5    2
        B    3   45    7
        C    1    4   43

Diagonal = correct predictions
Off-diagonal = mistakes
```

**4. Saving Results**

```python
def save_results(self, experiment_id):
    # Save detailed results to CSV
    results_df = pd.DataFrame(self.results)
    results_df.to_csv(f"{experiment_id}_results.csv")
    
    # Each row has:
    # - incident_id
    # - ground_truth (correct answer)
    # - prediction (what AI guessed)
    # - latency_sec (how long it took)
    # - explanation (AI's reasoning)
```

**Why Evaluation Matters:**
- We can compare different methods objectively
- We can identify which methods work best
- We can find failure cases and improve

---

### Component 7: Experiment Runner (`src/experiments/runner.py`)

**Purpose**: Orchestrate everything - load data, run experiments, evaluate.

#### How It Works:

**1. Load Configuration**

```python
# From YAML file (exp_zero_shot.yaml)
config = {
    "experiment_id": "E1_zero_shot",
    "mode": "zero_shot",
    "model": {
        "backend": "openai",
        "model_name": "gpt-4",
        "temperature": 0.0
    },
    "data": {
        "test_set_path": "data/synthetic"
    }
}
```

**2. Create Pipeline Based on Mode**

```python
if mode == "zero_shot":
    pipeline = create_zero_shot_pipeline(config)
elif mode == "chain_of_thought":
    pipeline = create_cot_pipeline(config)
elif mode == "rag":
    pipeline = create_rag_pipeline(config)
elif mode == "agent":
    pipeline = create_agent_pipeline(config)
```

**3. Load Incidents**

```python
incidents = load_incidents_from_dir("data/synthetic")
# Returns list of incident dictionaries
```

**4. Run Evaluation**

```python
evaluator = Evaluator()
results = evaluator.evaluate_pipeline(
    incidents,
    pipeline,
    experiment_id="E1_zero_shot",
    labels=["connection_pool_exhaustion", "long_running_queries", ...]
)
```

**5. Save and Print Results**

```python
evaluator.save_results(experiment_id)
print(f"Accuracy: {results['metrics']['accuracy']:.3f}")
print(f"Average Latency: {results['avg_latency_sec']:.3f}s")
```

---

## How Everything Works Together

### The Complete Flow:

```
1. Generate Synthetic Data
   └─> generator.py creates 300 incidents
   └─> Saves to data/synthetic/*.json

2. Load Data
   └─> loader.py reads JSON files
   └─> Returns list of incident dictionaries

3. Choose Experiment Mode
   └─> Zero-shot: Direct prompt
   └─> CoT: Step-by-step prompt
   └─> RAG: Retrieve knowledge + prompt
   └─> Agent: Run tools + prompt

4. Create Pipeline
   └─> Initialize LLM interface
   └─> Create prompt template
   └─> (Optional) Initialize RAG or Agent

5. Run Evaluation
   └─> For each incident:
       ├─> Format incident as text
       ├─> Create prompt (with optional RAG/agent tools)
       ├─> Call LLM
       ├─> Extract prediction
       └─> Store results

6. Calculate Metrics
   └─> Compare predictions vs ground truth
   └─> Calculate accuracy, F1, confusion matrix
   └─> Measure latency

7. Save Results
   └─> CSV with all predictions
   └─> JSON summary with metrics
   └─> Can be used for analysis/visualization
```

---

## Step-by-Step Walkthrough

### Example: Running a Zero-Shot Experiment

**Step 1: Generate Data**
```bash
python -m src.data.generator --num_incidents 300 --output_dir data/synthetic/
```

**What happens:**
- Creates 300 JSON files in `data/synthetic/`
- Each file has one incident with metrics, logs, root cause

**Step 2: Run Experiment**
```bash
cd experiments
bash run_experiment.sh configs/exp_zero_shot.yaml
```

**What happens internally:**

1. **Load Config**
   ```python
   config = {
       "experiment_id": "E1_zero_shot",
       "mode": "zero_shot",
       "model": {"backend": "openai", "model_name": "gpt-4"}
   }
   ```

2. **Create LLM Interface**
   ```python
   llm = LLMInterface(
       backend="openai",
       model_name="gpt-4",
       temperature=0.0
   )
   ```

3. **Create Pipeline Function**
   ```python
   def pipeline(incident):
       # Format incident as text
       incident_text = format_incident_for_prompt(incident)
       # Create prompt
       prompt = zero_shot_prompt(incident_text)
       # Call LLM
       response = llm.call(prompt)
       # Extract prediction
       prediction = extract_prediction(response['text'])
       return {
           'prediction': prediction,
           'explanation': response['text'],
           'latency': response['latency']
       }
   ```

4. **Load Incidents**
   ```python
   incidents = load_incidents_from_dir("data/synthetic")
   # incidents is a list of 300 dictionaries
   ```

5. **Evaluate**
   ```python
   for incident in incidents:
       result = pipeline(incident)
       # Store: prediction, ground_truth, latency, explanation
   ```

6. **Calculate Metrics**
   ```python
   accuracy = (correct_predictions) / (total_predictions)
   # Example: 250/300 = 0.833
   ```

7. **Save Results**
   - `E1_zero_shot_results.csv`: All predictions
   - `E1_zero_shot_summary.json`: Summary metrics

**Step 3: Analyze Results**

Open the CSV file:
```python
import pandas as pd
df = pd.read_csv("experiments/results/E1_zero_shot_results.csv")
print(df.head())

# Output:
#   incident_id  ground_truth              prediction  latency_sec
# 0    INC0001  connection_pool_exhaustion  connection_pool_exhaustion  2.34
# 1    INC0002  long_running_queries        long_running_queries        2.45
# 2    INC0003  network_partition          connection_pool_exhaustion  2.12  # Wrong!
```

---

## Common Questions & Answers

### Q1: Why do we need synthetic data? Can't we use real incidents?

**A:** Real incidents are:
- Hard to get (privacy, security)
- Don't have known ground truth (we don't always know the real cause)
- Expensive to label
- Limited in number

Synthetic data:
- We know the correct answer (ground truth)
- Can generate as many as we need
- No privacy concerns
- Perfect for research

### Q2: What's the difference between zero-shot and fine-tuning?

**Zero-shot:**
- Use the model as-is
- Just give it a prompt
- No training needed
- Fast to set up

**Fine-tuning:**
- Train the model on our specific data
- Model learns our domain
- More accurate (potentially)
- Requires training data and compute

**We use zero-shot** because it's simpler and we want to compare reasoning methods, not training methods.

### Q3: Why do we measure latency?

**A:** In production, you need fast diagnosis:
- **2 seconds**: Acceptable
- **10 seconds**: Too slow
- **30 seconds**: Unacceptable

We compare which method is fastest while maintaining accuracy.

### Q4: What if the LLM gives a wrong answer?

**A:** That's what we're measuring! We:
1. Record all predictions
2. Compare to ground truth
3. Calculate accuracy
4. Analyze failure cases
5. Improve prompts/methods

### Q5: Can I use a different LLM?

**A:** Yes! The `LLMInterface` supports:
- OpenAI (GPT-4, GPT-3.5)
- HuggingFace (any model)
- Just change the config file

### Q6: How do I add a new root cause type?

**A:** 
1. Add to `ROOT_CAUSES` in `generator.py`
2. Add log templates in `LOG_TEMPLATES`
3. Add metric generation logic in `make_incident()`
4. Add to knowledge base (for RAG)
5. Regenerate data

### Q7: What's the best method?

**A:** That's what the experiments determine! Generally:
- **Zero-shot**: Fastest, simplest
- **CoT**: More accurate, slightly slower
- **RAG**: Most accurate with good knowledge base
- **Agent**: Best for complex cases, but slowest

### Q8: How do embeddings work?

**A:** Think of it like this:
- "cat" and "dog" are similar → similar embeddings
- "cat" and "airplane" are different → different embeddings
- We can calculate distance between embeddings
- Closer = more similar

**In practice:**
```python
embedding_model.encode("connection pool exhausted")
# Returns: [0.23, -0.45, 0.67, ..., 0.12]  (384 numbers)

embedding_model.encode("too many connections")
# Returns: [0.25, -0.43, 0.65, ..., 0.11]  (similar numbers!)

# Calculate distance → very small → very similar!
```

### Q9: What is a confusion matrix?

**A:** A table showing prediction mistakes:

```
                Predicted
              Pool  Query  Network
Actual  Pool   45    3      2
        Query   5   42      3
        Network 2    4     44

Reading: 
- 45 pool incidents correctly predicted as pool
- 3 pool incidents incorrectly predicted as query
- 2 pool incidents incorrectly predicted as network
```

**Diagonal = correct, off-diagonal = mistakes**

### Q10: How do I interpret F1 score?

**A:** F1 is a balance between precision and recall:

- **Precision**: "Of all times I said 'pool exhaustion', how many were right?"
  - High precision = Few false positives
  
- **Recall**: "Of all actual 'pool exhaustion' cases, how many did I catch?"
  - High recall = Few false negatives

- **F1**: Harmonic mean (balance of both)
  - F1 = 1.0 = Perfect
  - F1 = 0.8 = Good
  - F1 = 0.5 = Poor

---

## Next Steps

1. **Read the code**: Start with `generator.py`, then `llm_interface.py`
2. **Run experiments**: Generate data, run a zero-shot experiment
3. **Analyze results**: Look at the CSV files, understand mistakes
4. **Modify prompts**: Try different prompt styles
5. **Add features**: New tools, new metrics, new root causes

---

## Key Takeaways

1. **This project compares 4 ways to use AI for diagnosis**
2. **We use synthetic data because we know the correct answers**
3. **Each method has trade-offs: speed vs accuracy**
4. **Evaluation measures how well each method works**
5. **The code is modular: easy to swap components**

---

**Congratulations!** You now understand the entire project. Start experimenting, and don't hesitate to modify the code to learn more!

