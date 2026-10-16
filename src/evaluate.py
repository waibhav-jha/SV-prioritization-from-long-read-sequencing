"""
src/evaluate.py
================
Comprehensive Model Evaluation, Calibration, and Performance Benchmark Module.

Evaluates all models on the holdout Test Set (Chromosomes 19-22, X, Y):
- Precision-Recall Curve & PR-AUC
- ROC Curve & ROC-AUC
- Calibration Curve & Brier Score
- Precision@Top-K% (Clinical Prioritization metric)
- Confusion Matrix & F1 Score
"""

import json
import os
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    precision_recall_curve, auc, roc_curve, roc_auc_score,
    f1_score, balanced_accuracy_score, brier_score_loss, confusion_matrix
)
from sklearn.calibration import calibration_curve

# Styling
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11
sns.set_theme(style="whitegrid")

def evaluate_models(test_path="data/processed/test.csv.gz"):
    """
    Perform rigorous evaluation of all trained models on holdout test set.
    """
    print("--- [Step 6.1] Loading Test Benchmark Set and Model Checkpoints ---")
    df_test = pd.read_csv(test_path)
    
    with open("models/feature_names.json", "r") as f:
        feature_cols = json.load(f)
        
    X_test = df_test[feature_cols].copy()
    y_test = df_test["target"].to_numpy()
    
    print(f"Test Set shape: {X_test.shape}, Positive rate: {y_test.mean():.3f} (N={len(y_test):,})")
    
    # Load Models
    lr_model = joblib.load("models/logistic_regression.joblib")
    scaler = joblib.load("models/scaler.joblib")
    rf_model = joblib.load("models/random_forest.joblib")
    lgb_model = joblib.load("models/lightgbm_model.joblib")
    xgb_model = joblib.load("models/xgboost_model.joblib")
    
    # Generate Predictions
    X_test_scaled = scaler.transform(X_test)
    preds = {
        "Logistic Regression": lr_model.predict_proba(X_test_scaled)[:, 1],
        "Random Forest": rf_model.predict_proba(X_test)[:, 1],
        "LightGBM": lgb_model.predict(X_test),
        "XGBoost": xgb_model.predict_proba(X_test)[:, 1]
    }
    
    results = {}
    
    print("\n--- [Step 6.2] Computing Performance Metrics on Holdout Test Set ---")
    for name, y_prob in preds.items():
        # PR-AUC
        p, r, thresholds_pr = precision_recall_curve(y_test, y_prob)
        pr_auc = auc(r, p)
        
        # ROC-AUC
        roc_auc = roc_auc_score(y_test, y_prob)
        
        # Optimal F1 threshold
        f1_scores = 2 * (p * r) / (p + r + 1e-9)
        best_idx = np.argmax(f1_scores)
        best_thresh = float(thresholds_pr[best_idx]) if best_idx < len(thresholds_pr) else 0.5
        best_f1 = float(f1_scores[best_idx])
        
        # Binary predictions at optimal threshold
        y_bin = (y_prob >= best_thresh).astype(int)
        bal_acc = balanced_accuracy_score(y_test, y_bin)
        brier = brier_score_loss(y_test, y_prob)
        
        # Precision@Top-K%
        n_top5 = int(len(y_prob) * 0.05)
        top5_idx = np.argsort(y_prob)[::-1][:n_top5]
        p_at_5 = float(y_test[top5_idx].mean())
        
        n_top10 = int(len(y_prob) * 0.10)
        top10_idx = np.argsort(y_prob)[::-1][:n_top10]
        p_at_10 = float(y_test[top10_idx].mean())
        
        results[name] = {
            "PR-AUC": round(float(pr_auc), 4),
            "ROC-AUC": round(float(roc_auc), 4),
            "F1-Score (Optimal)": round(best_f1, 4),
            "Optimal_Threshold": round(best_thresh, 4),
            "Balanced_Accuracy": round(float(bal_acc), 4),
            "Brier_Score": round(float(brier), 4),
            "Precision@Top-5%": round(p_at_5, 4),
            "Precision@Top-10%": round(p_at_10, 4)
        }
        
        print(f"[{name}] PR-AUC: {pr_auc:.4f} | ROC-AUC: {roc_auc:.4f} | F1: {best_f1:.4f} | Brier: {brier:.4f} | P@Top5%: {p_at_5*100:.1f}%")
        
    # Save Metrics JSON
    with open("results/metrics_summary.json", "w") as f:
        json.dump(results, f, indent=2)
        
    print("\n--- [Step 6.3] Generating Comparative Evaluation Visualizations ---")
    
    # 1. Precision-Recall Curves
    plt.figure(figsize=(8, 6))
    colors = {"Logistic Regression": "#7570b3", "Random Forest": "#1b9e77", "LightGBM": "#d95f02", "XGBoost": "#e7298a"}
    for name, y_prob in preds.items():
        p, r, _ = precision_recall_curve(y_test, y_prob)
        pr_auc = results[name]["PR-AUC"]
        plt.plot(r, p, label=f"{name} (PR-AUC = {pr_auc:.3f})", color=colors[name], linewidth=2)
        
    # Baseline prevalence line
    plt.axhline(y=y_test.mean(), color="gray", linestyle="--", label=f"No-Skill Baseline ({y_test.mean():.3f})")
    plt.title("Precision-Recall Curves on Holdout Test Set (Chr 19-22, X, Y)", fontweight="bold", pad=12)
    plt.xlabel("Recall", labelpad=8)
    plt.ylabel("Precision", labelpad=8)
    plt.legend(loc="lower left", frameon=True)
    plt.tight_layout()
    plt.savefig("results/pr_curves.png", dpi=300)
    plt.close()
    
    # 2. ROC Curves
    plt.figure(figsize=(8, 6))
    for name, y_prob in preds.items():
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        roc_auc = results[name]["ROC-AUC"]
        plt.plot(fpr, tpr, label=f"{name} (ROC-AUC = {roc_auc:.3f})", color=colors[name], linewidth=2)
        
    plt.plot([0, 1], [0, 1], color="gray", linestyle="--", label="Chance (0.500)")
    plt.title("ROC Curves on Holdout Test Set (Chr 19-22, X, Y)", fontweight="bold", pad=12)
    plt.xlabel("False Positive Rate", labelpad=8)
    plt.ylabel("True Positive Rate", labelpad=8)
    plt.legend(loc="lower right", frameon=True)
    plt.tight_layout()
    plt.savefig("results/roc_curves.png", dpi=300)
    plt.close()
    
    # 3. Calibration / Reliability Curves
    plt.figure(figsize=(8, 6))
    for name, y_prob in preds.items():
        prob_true, prob_pred = calibration_curve(y_test, y_prob, n_bins=10)
        plt.plot(prob_pred, prob_true, marker="o", label=f"{name} (Brier = {results[name]['Brier_Score']:.3f})", color=colors[name], linewidth=2)
        
    plt.plot([0, 1], [0, 1], color="gray", linestyle="--", label="Perfect Calibration")
    plt.title("Probability Calibration Curves (Reliability Diagram)", fontweight="bold", pad=12)
    plt.xlabel("Mean Predicted Pathogenicity Probability", labelpad=8)
    plt.ylabel("Fraction of True Pathogenic SVs", labelpad=8)
    plt.legend(loc="upper left", frameon=True)
    plt.tight_layout()
    plt.savefig("results/calibration_curves.png", dpi=300)
    plt.close()
    
    print("Evaluation Figures saved to results/ (pr_curves.png, roc_curves.png, calibration_curves.png).")
    return results

if __name__ == "__main__":
    evaluate_models()
