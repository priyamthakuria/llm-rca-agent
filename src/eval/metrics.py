"""
Evaluation metrics for RCA diagnosis.
"""
from sklearn.metrics import accuracy_score, f1_score, precision_recall_fscore_support, confusion_matrix
from typing import Dict, List, Tuple
import numpy as np


def compute_classification_metrics(
    y_true: List[str],
    y_pred: List[str],
    labels: List[str]
) -> Dict:
    """
    Compute classification metrics.
    
    Args:
        y_true: Ground truth labels
        y_pred: Predicted labels
        labels: List of all possible labels
    
    Returns:
        Dictionary with accuracy, macro F1, and per-class metrics
    """
    acc = accuracy_score(y_true, y_pred)
    precision, recall, f1, support = precision_recall_fscore_support(
        y_true, y_pred, labels=labels, average=None, zero_division=0
    )
    macro_f1 = f1_score(y_true, y_pred, labels=labels, average='macro', zero_division=0)
    weighted_f1 = f1_score(y_true, y_pred, labels=labels, average='weighted', zero_division=0)
    
    per_class = [
        {
            "label": label,
            "precision": float(p),
            "recall": float(r),
            "f1": float(f),
            "support": int(s)
        }
        for label, p, r, f, s in zip(labels, precision, recall, f1, support)
    ]
    
    return {
        "accuracy": float(acc),
        "macro_f1": float(macro_f1),
        "weighted_f1": float(weighted_f1),
        "per_class": per_class
    }


def compute_confusion_matrix(
    y_true: List[str],
    y_pred: List[str],
    labels: List[str]
) -> np.ndarray:
    """
    Compute confusion matrix.
    
    Args:
        y_true: Ground truth labels
        y_pred: Predicted labels
        labels: List of all possible labels
    
    Returns:
        Confusion matrix as numpy array
    """
    return confusion_matrix(y_true, y_pred, labels=labels)


def compute_top_k_accuracy(
    y_true: List[str],
    y_pred_ranked: List[List[str]],
    k: int = 3
) -> float:
    """
    Compute top-k accuracy.
    
    Args:
        y_true: Ground truth labels
        y_pred_ranked: List of ranked predictions (each element is a list of labels)
        k: Top k predictions to consider
    
    Returns:
        Top-k accuracy score
    """
    correct = 0
    for true_label, ranked_preds in zip(y_true, y_pred_ranked):
        if true_label in ranked_preds[:k]:
            correct += 1
    return correct / len(y_true) if len(y_true) > 0 else 0.0


def compute_hallucination_score(
    explanations: List[str],
    incident_data: List[Dict],
    threshold: float = 0.3
) -> Dict:
    """
    Compute a proxy for hallucination by checking if explanations reference
    metrics/events that don't exist in the incident data.
    
    This is a simple heuristic - a proper hallucination check would require
    more sophisticated NLP or human evaluation.
    
    Args:
        explanations: List of explanation strings
        incident_data: List of incident dictionaries
        threshold: Threshold for considering something a hallucination
    
    Returns:
        Dictionary with hallucination statistics
    """
    # This is a placeholder - implement more sophisticated checking
    # For now, just return basic stats
    return {
        "mean_explanation_length": np.mean([len(exp) for exp in explanations]),
        "note": "Proper hallucination detection requires more sophisticated methods"
    }


def compute_explainability_score(
    explanations: List[str],
    ground_truth_labels: List[str],
    metric_keywords: Dict[str, List[str]]
) -> float:
    """
    Compute explainability score based on keyword overlap.
    
    Args:
        explanations: List of explanation strings
        ground_truth_labels: Ground truth root cause labels
        metric_keywords: Dictionary mapping labels to expected keywords
    
    Returns:
        Average explainability score (0-1)
    """
    scores = []
    for exp, label in zip(explanations, ground_truth_labels):
        expected_keywords = metric_keywords.get(label, [])
        if not expected_keywords:
            scores.append(0.5)  # Neutral score if no keywords defined
            continue
        
        exp_lower = exp.lower()
        matches = sum(1 for kw in expected_keywords if kw.lower() in exp_lower)
        score = matches / len(expected_keywords) if expected_keywords else 0.0
        scores.append(score)
    
    return float(np.mean(scores)) if scores else 0.0

