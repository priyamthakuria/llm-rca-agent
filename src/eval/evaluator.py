"""
Evaluator for running experiments and computing metrics.
"""
import json
import csv
import os
from typing import Dict, List, Optional
from pathlib import Path
import pandas as pd

from src.eval.metrics import (
    compute_classification_metrics,
    compute_confusion_matrix,
    compute_top_k_accuracy
)
from src.data.loader import load_incidents_from_dir, format_incident_for_prompt


class Evaluator:
    """Evaluator for RCA diagnosis experiments."""
    
    def __init__(self, output_dir: str = "experiments/results"):
        """
        Initialize evaluator.
        
        Args:
            output_dir: Directory to save evaluation results
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.results = []
    
    def evaluate_pipeline(
        self,
        incidents: List[Dict],
        pipeline_func,
        experiment_id: str,
        labels: List[str]
    ) -> Dict:
        """
        Evaluate a pipeline on a set of incidents.
        
        Args:
            incidents: List of incident dictionaries
            pipeline_func: Function that takes incident dict and returns prediction
            experiment_id: Identifier for this experiment
            labels: List of all possible root cause labels
        
        Returns:
            Dictionary with evaluation results
        """
        predictions = []
        ground_truths = []
        latencies = []
        explanations = []
        
        print(f"Evaluating {len(incidents)} incidents for experiment {experiment_id}...")
        
        for i, incident in enumerate(incidents):
            if (i + 1) % 10 == 0:
                print(f"  Processed {i + 1}/{len(incidents)} incidents...")
            
            # Run pipeline
            result = pipeline_func(incident)
            
            # Extract prediction (assume pipeline returns dict with 'prediction' and 'explanation')
            prediction = result.get('prediction', 'unknown')
            explanation = result.get('explanation', '')
            latency = result.get('latency', 0.0)
            
            predictions.append(prediction)
            ground_truths.append(incident['root_cause'])
            latencies.append(latency)
            explanations.append(explanation)
            
            # Store detailed result
            self.results.append({
                'experiment_id': experiment_id,
                'incident_id': incident['incident_id'],
                'ground_truth': incident['root_cause'],
                'prediction': prediction,
                'confidence': result.get('confidence', 0.0),
                'latency_sec': latency,
                'explanation': explanation,
                'retrieved_docs_ids': result.get('retrieved_docs_ids', [])
            })
        
        # Compute metrics
        metrics = compute_classification_metrics(ground_truths, predictions, labels)
        confusion_mat = compute_confusion_matrix(ground_truths, predictions, labels)
        
        # Compute average latency
        avg_latency = sum(latencies) / len(latencies) if latencies else 0.0
        
        results_summary = {
            'experiment_id': experiment_id,
            'num_incidents': len(incidents),
            'metrics': metrics,
            'avg_latency_sec': avg_latency,
            'confusion_matrix': confusion_mat.tolist()
        }
        
        return results_summary
    
    def save_results(self, experiment_id: str):
        """
        Save evaluation results to CSV.
        
        Args:
            experiment_id: Experiment identifier
        """
        # Save detailed results
        results_df = pd.DataFrame(self.results)
        csv_path = os.path.join(self.output_dir, f"{experiment_id}_results.csv")
        results_df.to_csv(csv_path, index=False)
        print(f"Saved results to {csv_path}")
        
        # Save summary
        summary_path = os.path.join(self.output_dir, f"{experiment_id}_summary.json")
        # Group by experiment and compute summary stats
        summary = {}
        for exp_id in results_df['experiment_id'].unique():
            exp_results = results_df[results_df['experiment_id'] == exp_id]
            summary[exp_id] = {
                'num_incidents': len(exp_results),
                'avg_latency': exp_results['latency_sec'].mean(),
                'accuracy': (exp_results['ground_truth'] == exp_results['prediction']).mean()
            }
        
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        print(f"Saved summary to {summary_path}")

