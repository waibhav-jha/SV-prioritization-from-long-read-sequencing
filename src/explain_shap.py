"""
src/explain_shap.py
===================
Explainable AI (TreeSHAP) & VUS Prioritization Index Module.

- Computes global SHAP values across test structural variants.
- Generates publication-quality SHAP beeswarm & feature importance plots.
- Applies model to score all 40,741 Variants of Uncertain Significance (VUS).
- Produces prioritized clinical ranking table with top risk attribution drivers.
"""

import json
import os
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import shap

# Configure styling
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11

def explain_and_prioritize(
    test_path="data/processed/test.csv.gz",
    vus_path="data/processed/vus_inference.csv.gz"
):
    """
    Run TreeSHAP explanations on test set and score VUS variants for clinical triage.
    """
    print("--- [Step 7.1] Loading Checkpoints & Data for SHAP Explainability ---")
    xgb_model = joblib.load("models/xgboost_model.joblib")
    df_test = pd.read_csv(test_path)
    df_vus = pd.read_csv(vus_path)
    
    with open("models/feature_names.json", "r") as f:
        feature_cols = json.load(f)
        
    X_test = df_test[feature_cols].copy()
    X_vus = df_vus[feature_cols].copy()
    
    print(f"Loaded X_test ({X_test.shape}) and X_vus ({X_vus.shape}).")
    
    # 1. TreeSHAP Computation on Test Set
    print("\n--- [Step 7.2] Computing TreeSHAP Values on Test Set ---")
    explainer = shap.TreeExplainer(xgb_model)
    shap_values = explainer(X_test)
    
    # Global SHAP Beeswarm Plot
    plt.figure(figsize=(10, 6.5))
    shap.plots.beeswarm(shap_values, max_display=12, show=False)
    plt.title("TreeSHAP Feature Attribution (Impact on SV Pathogenicity Prediction)", fontweight="bold", pad=12)
    plt.tight_layout()
    plt.savefig("results/shap_summary.png", dpi=300)
    plt.close()
    
    # Global Feature Importance Bar Plot
    plt.figure(figsize=(9, 5.5))
    shap.plots.bar(shap_values, max_display=12, show=False)
    plt.title("Global Feature Importance (Mean Absolute SHAP Value)", fontweight="bold", pad=12)
    plt.tight_layout()
    plt.savefig("results/shap_importance.png", dpi=300)
    plt.close()
    
    print("Saved SHAP Summary and Importance plots to results/.")
    
    # 2. Score All VUS Variants
    print("\n--- [Step 7.3] Scoring and Prioritizing 40,741 VUS Variants ---")
    vus_probs = xgb_model.predict_proba(X_vus)[:, 1]
    df_vus["predicted_pathogenicity_score"] = vus_probs
    
    # Assign Risk Tiers
    def assign_tier(p):
        if p >= 0.85:
            return "Tier 1: High-Confidence Pathogenic Candidate"
        elif p >= 0.50:
            return "Tier 2: Moderate-Risk Potential Deleterious"
        elif p >= 0.20:
            return "Tier 3: Low-Risk Likely Tolerated"
        else:
            return "Tier 4: High-Confidence Likely Benign Polymorphism"
            
    df_vus["prioritization_tier"] = df_vus["predicted_pathogenicity_score"].apply(assign_tier)
    
    # Sort VUS by descending pathogenicity score
    df_vus_sorted = df_vus.sort_values(by="predicted_pathogenicity_score", ascending=False).reset_index(drop=True)
    
    # Save full prioritized VUS table
    out_vus_ranking = "results/vus_prioritization_ranking.csv.gz"
    df_vus_sorted.to_csv(out_vus_ranking, index=False, compression="gzip")
    print(f"Saved full VUS ranking to {out_vus_ranking}")
    
    # Summary of VUS Tiers
    tier_summary = df_vus_sorted["prioritization_tier"].value_counts().to_dict()
    print("\nVUS Prioritization Tier Breakdown:")
    for tier, count in tier_summary.items():
        print(f"  {tier}: {count:,} ({count/len(df_vus)*100:.1f}%)")
        
    # Extract Top 50 Highest Priority VUS for Clinical Review
    top50_cols = [
        "variation_id", "chrom", "start", "stop", "log10_length", "gene_count",
        "gnomad_af", "gnomad_lof", "predicted_pathogenicity_score", "prioritization_tier"
    ]
    top50_df = df_vus_sorted[top50_cols].head(50)
    top50_df.to_json("results/top50_prioritized_vus.json", orient="records", indent=2)
    
    # Save SHAP and VUS Summary Metrics
    shap_summary_dict = {
        "total_vus_evaluated": len(df_vus),
        "tier_breakdown": tier_summary,
        "mean_vus_score": float(vus_probs.mean()),
        "median_vus_score": float(np.median(vus_probs)),
        "high_priority_candidates_count": int((vus_probs >= 0.85).sum()),
        "likely_benign_candidates_count": int((vus_probs < 0.20).sum())
    }
    
    with open("results/vus_prioritization_summary.json", "w") as f:
        json.dump(shap_summary_dict, f, indent=2)
        
    print("\n--- SHAP Explainability & VUS Prioritization Complete ---")
    return df_vus_sorted

if __name__ == "__main__":
    explain_and_prioritize()
