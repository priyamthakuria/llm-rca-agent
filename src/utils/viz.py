"""
Visualization utilities for analysis.
"""
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import List, Dict, Optional
from sklearn.metrics import confusion_matrix


def plot_confusion_matrix(
    y_true: List[str],
    y_pred: List[str],
    labels: List[str],
    title: str = "Confusion Matrix",
    save_path: Optional[str] = None
):
    """
    Plot confusion matrix.
    
    Args:
        y_true: Ground truth labels
        y_pred: Predicted labels
        labels: List of all labels
        title: Plot title
        save_path: Path to save figure (optional)
    """
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        cm,
        annot=True,
        fmt='d',
        cmap='Blues',
        xticklabels=labels,
        yticklabels=labels
    )
    plt.title(title)
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return plt.gcf()


def plot_per_class_f1(
    metrics: Dict,
    title: str = "Per-Class F1 Scores",
    save_path: Optional[str] = None
):
    """
    Plot per-class F1 scores.
    
    Args:
        metrics: Metrics dictionary from compute_classification_metrics
        title: Plot title
        save_path: Path to save figure (optional)
    """
    per_class = metrics['per_class']
    labels = [item['label'] for item in per_class]
    f1_scores = [item['f1'] for item in per_class]
    
    plt.figure(figsize=(12, 6))
    plt.bar(labels, f1_scores)
    plt.title(title)
    plt.ylabel('F1 Score')
    plt.xlabel('Root Cause Class')
    plt.xticks(rotation=45, ha='right')
    plt.ylim(0, 1)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return plt.gcf()


def plot_latency_comparison(
    latency_data: Dict[str, List[float]],
    title: str = "Latency Comparison by Mode",
    save_path: Optional[str] = None
):
    """
    Plot latency boxplots for different modes.
    
    Args:
        latency_data: Dictionary mapping mode names to lists of latencies
        title: Plot title
        save_path: Path to save figure (optional)
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    data = [latency_data[mode] for mode in latency_data.keys()]
    labels = list(latency_data.keys())
    
    bp = ax.boxplot(data, labels=labels, patch_artist=True)
    
    # Color the boxes
    colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightyellow', 'lightpink']
    for patch, color in zip(bp['boxes'], colors[:len(bp['boxes'])]):
        patch.set_facecolor(color)
    
    ax.set_title(title)
    ax.set_ylabel('Latency (seconds)')
    ax.set_xlabel('Mode')
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig

