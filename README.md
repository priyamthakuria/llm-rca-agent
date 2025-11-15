# LLM-Assisted RCA for Database Incidents

**Objective**: Compare LLM reasoning modes (zero-shot, chain-of-thought, RAG, tool-augmented agent) for diagnosing synthetic + real-like database incidents, measure diagnosis accuracy, time-to-diagnosis, hallucination rate, and provide practical insights for ML-for-systems research.

## Project Structure

```
llm-db-rca/
├─ README.md
├─ requirements.txt
├─ LICENSE
├─ data/
│  ├─ raw/                      # raw datasets (csv/json)
│  ├─ synthetic/                # generated synthetic incidents
│  └─ README.md
├─ notebooks/
│  ├─ EDA_synthetic_incidents.ipynb
│  └─ analysis_plots.ipynb
├─ src/
│  ├─ __init__.py
│  ├─ data/
│  │  ├─ generator.py          # generate synthetic incidents
│  │  ├─ loader.py             # load and preprocess datasets
│  ├─ models/
│  │  ├─ llm_interface.py      # generic calls to LLMs (HF/OpenAI)
│  │  ├─ rag.py                # retrieval-augmented pipeline
│  │  └─ agent_runner.py       # tool-augmented agent orchestration
│  ├─ eval/
│  │  ├─ metrics.py
│  │  └─ evaluator.py
│  ├─ prompts/
│  │  └─ templates.py
│  └─ utils/
│     ├─ viz.py
│     └─ logging_setup.py
├─ experiments/
│  ├─ run_experiment.sh
│  └─ configs/
│     ├─ exp_zero_shot.yaml
│     ├─ exp_cot.yaml
│     ├─ exp_rag.yaml
│     └─ exp_agent.yaml
├─ reports/
│  ├─ report_draft.md
│  └─ figures/
└─ tests/
   └─ test_data_gen.py
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables (if using OpenAI):
```bash
export OPENAI_API_KEY="your-api-key-here"
```

## Usage

### Generate Synthetic Incidents

```bash
python -m src.data.generator --num_incidents 300 --output_dir data/synthetic/
```

### Run Experiments

```bash
cd experiments
bash run_experiment.sh exp_zero_shot.yaml
```

## Dataset

The project uses synthetic database incidents with the following schema:
- Incident metadata (ID, timestamps)
- Metrics time series (CPU, latency, error_rate, connections)
- Log summaries
- System metadata
- Ground truth root cause labels

## Experiments

The project compares:
- **E1**: Zero-shot LLM prompts
- **E2**: Chain-of-Thought (CoT)
- **E3**: RAG (Retrieval-Augmented Generation)
- **E4**: Tool-augmented Agent
- **E5**: Heuristic baseline (rule-based)

## License

See LICENSE file for details.

