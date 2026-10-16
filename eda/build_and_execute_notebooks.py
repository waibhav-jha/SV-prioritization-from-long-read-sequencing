"""
Build and Pre-Execute all Jupyter Notebooks so all plots, tables, and metrics
are fully rendered inside the .ipynb files.
"""

import os
import nbformat as nbf
from nbclient import NotebookClient

os.makedirs("eda", exist_ok=True)

path_helper = """import os

def resolve_path(p):
    for candidate in [p, os.path.join("..", p), os.path.join("data", p), os.path.join("..", "data", p)]:
        if os.path.exists(candidate):
            return candidate
    return p
"""

# -------------------------------------------------------------
# Notebook 07: Model Training & Evaluation
# -------------------------------------------------------------
nb7 = nbf.v4.new_notebook()
nb7.cells = [
    nbf.v4.new_markdown_cell("""# 07 - Structural Variant Machine Learning Models & Benchmark
**Project**: AI-Based Structural Variant Prioritization from Long-Read Sequencing Using Explainable Machine Learning  
**Author**: Data Science & Genomics Team  
**Date**: August 2026

## Objective
Train and evaluate 4 machine learning model architectures on leakage-free chromosomal splits:
1. **Logistic Regression** (L2-regularized baseline)
2. **Random Forest** (Ensemble baseline)
3. **LightGBM** (Gradient boosted trees with class balancing)
4. **XGBoost** (Gradient boosted trees with PR-AUC optimization)

Evaluate on holdout chromosomes (Chr 19–22, X, Y) across PR-AUC, ROC-AUC, F1-Score, Brier Calibration Score, and Precision@Top-5%.
"""),
    nbf.v4.new_code_cell(path_helper + """
import json
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    precision_recall_curve, auc, roc_curve, roc_auc_score,
    f1_score, balanced_accuracy_score, brier_score_loss
)
from sklearn.calibration import calibration_curve
import xgboost as xgb
import lightgbm as lgb

sns.set_theme(style="whitegrid")
plt.rcParams['font.size'] = 11

train_path = resolve_path("processed/train.csv.gz")
val_path = resolve_path("processed/val.csv.gz")
test_path = resolve_path("processed/test.csv.gz")

df_train = pd.read_csv(train_path)
df_val = pd.read_csv(val_path)
df_test = pd.read_csv(test_path)

exclude_cols = ["variation_id", "chrom", "start", "stop", "clinical_class", "assembly", "target"]
feature_cols = [c for c in df_train.columns if c not in exclude_cols]

X_train, y_train = df_train[feature_cols], df_train["target"].to_numpy()
X_val, y_val = df_val[feature_cols], df_val["target"].to_numpy()
X_test, y_test = df_test[feature_cols], df_test["target"].to_numpy()

print("Dataset Partitions:")
print(f"  Train (Chr 1-14):      {X_train.shape[0]:,} SVs ({y_train.mean()*100:.1f}% Pathogenic)")
print(f"  Val   (Chr 15-18):     {X_val.shape[0]:,} SVs ({y_val.mean()*100:.1f}% Pathogenic)")
print(f"  Test  (Chr 19-22,X,Y): {X_test.shape[0]:,} SVs ({y_test.mean()*100:.1f}% Pathogenic)")
print(f"  Feature Count:         {len(feature_cols)} features")
"""),
    nbf.v4.new_markdown_cell("""## 1. Train Baseline & Advanced Models"""),
    nbf.v4.new_code_cell("""# 1. Logistic Regression
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

lr = LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42)
lr.fit(X_train_scaled, y_train)

# 2. Random Forest
rf = RandomForestClassifier(n_estimators=150, max_depth=12, class_weight="balanced", n_jobs=-1, random_state=42)
rf.fit(X_train, y_train)

# 3. LightGBM
lgb_train = lgb.Dataset(X_train, label=y_train)
lgb_val = lgb.Dataset(X_val, label=y_val, reference=lgb_train)
lgb_params = {
    "objective": "binary", "metric": "binary_logloss", "is_unbalance": True,
    "learning_rate": 0.05, "num_leaves": 31, "feature_fraction": 0.85,
    "verbose": -1, "random_state": 42
}
lgb_model = lgb.train(lgb_params, lgb_train, num_boost_round=300, valid_sets=[lgb_train, lgb_val])

# 4. XGBoost
scale_pos = (y_train == 0).sum() / (y_train == 1).sum()
xgb_model = xgb.XGBClassifier(
    n_estimators=300, max_depth=6, learning_rate=0.05,
    scale_pos_weight=scale_pos, subsample=0.85, colsample_bytree=0.85,
    eval_metric="aucpr", random_state=42
)
xgb_model.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=False)

print("All 4 models trained successfully.")
"""),
    nbf.v4.new_markdown_cell("""## 2. Model Performance Evaluation Table on Holdout Test Set"""),
    nbf.v4.new_code_cell("""models = {
    "Logistic Regression": lr.predict_proba(X_test_scaled)[:, 1],
    "Random Forest": rf.predict_proba(X_test)[:, 1],
    "LightGBM": lgb_model.predict(X_test),
    "XGBoost": xgb_model.predict_proba(X_test)[:, 1]
}

eval_rows = []
for name, y_prob in models.items():
    p, r, thresh_pr = precision_recall_curve(y_test, y_prob)
    pr_auc = auc(r, p)
    roc_auc = roc_auc_score(y_test, y_prob)
    
    f1_scores = 2 * (p * r) / (p + r + 1e-9)
    best_idx = np.argmax(f1_scores)
    best_f1 = f1_scores[best_idx]
    best_thresh = thresh_pr[best_idx] if best_idx < len(thresh_pr) else 0.5
    
    y_pred_opt = (y_prob >= best_thresh).astype(int)
    bal_acc = balanced_accuracy_score(y_test, y_pred_opt)
    brier = brier_score_loss(y_test, y_prob)
    
    n_top5 = int(len(y_prob) * 0.05)
    p_at_5 = y_test[np.argsort(y_prob)[::-1][:n_top5]].mean()
    
    eval_rows.append({
        "Model": name,
        "PR-AUC": round(pr_auc, 4),
        "ROC-AUC": round(roc_auc, 4),
        "F1-Score": round(best_f1, 4),
        "Brier Score": round(brier, 4),
        "Precision@Top-5%": f"{p_at_5*100:.1f}%",
        "Balanced Accuracy": round(bal_acc, 4)
    })

df_results = pd.DataFrame(eval_rows)
df_results
"""),
    nbf.v4.new_markdown_cell("""## 3. Precision-Recall, ROC, and Calibration Curves"""),
    nbf.v4.new_code_cell("""fig, axes = plt.subplots(1, 3, figsize=(18, 5))
colors = {"Logistic Regression": "#7570b3", "Random Forest": "#1b9e77", "LightGBM": "#d95f02", "XGBoost": "#e7298a"}

# 1. PR Curves
for name, y_prob in models.items():
    p, r, _ = precision_recall_curve(y_test, y_prob)
    axes[0].plot(r, p, label=f"{name} (AUC = {auc(r, p):.3f})", color=colors[name], linewidth=2)
axes[0].axhline(y=y_test.mean(), color="gray", linestyle="--", label=f"Baseline ({y_test.mean():.2f})")
axes[0].set_title("Precision-Recall Curves", fontweight="bold")
axes[0].set_xlabel("Recall")
axes[0].set_ylabel("Precision")
axes[0].legend(loc="lower left")

# 2. ROC Curves
for name, y_prob in models.items():
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    axes[1].plot(fpr, tpr, label=f"{name} (AUC = {roc_auc_score(y_test, y_prob):.3f})", color=colors[name], linewidth=2)
axes[1].plot([0, 1], [0, 1], color="gray", linestyle="--", label="Chance")
axes[1].set_title("ROC Curves", fontweight="bold")
axes[1].set_xlabel("False Positive Rate")
axes[1].set_ylabel("True Positive Rate")
axes[1].legend(loc="lower right")

# 3. Calibration Curves
for name, y_prob in models.items():
    prob_true, prob_pred = calibration_curve(y_test, y_prob, n_bins=10)
    axes[2].plot(prob_pred, prob_true, marker="o", label=f"{name} (Brier = {brier_score_loss(y_test, y_prob):.3f})", color=colors[name], linewidth=2)
axes[2].plot([0, 1], [0, 1], color="gray", linestyle="--", label="Perfect Calibration")
axes[2].set_title("Probability Calibration Curves", fontweight="bold")
axes[2].set_xlabel("Mean Predicted Probability")
axes[2].set_ylabel("Fraction of True Positives")
axes[2].legend(loc="upper left")

plt.tight_layout()
plt.show()
""")
]

# -------------------------------------------------------------
# Notebook 08: SHAP Explainability & VUS Prioritization
# -------------------------------------------------------------
nb8 = nbf.v4.new_notebook()
nb8.cells = [
    nbf.v4.new_markdown_cell("""# 08 - Explainable AI (TreeSHAP) & VUS Prioritization Index
**Project**: AI-Based Structural Variant Prioritization from Long-Read Sequencing Using Explainable Machine Learning  
**Author**: Data Science & Genomics Team  
**Date**: August 2026

## Objective
1. Compute **TreeSHAP feature attributions** to explain model predictions globally and locally.
2. Apply the trained model to all **34,466 Variants of Uncertain Significance (VUS)**.
3. Classify VUS into clinical prioritization tiers and inspect top high-risk candidates for diagnostic follow-up.
"""),
    nbf.v4.new_code_cell(path_helper + """
import json
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import shap

test_path = resolve_path("processed/test.csv.gz")
vus_path = resolve_path("processed/vus_inference.csv.gz")
model_path = resolve_path("models/xgboost_model.joblib")
if not os.path.exists(model_path):
    model_path = resolve_path("../models/xgboost_model.joblib")

df_test = pd.read_csv(test_path)
df_vus = pd.read_csv(vus_path)
xgb_model = joblib.load(model_path)

exclude_cols = ["variation_id", "chrom", "start", "stop", "clinical_class", "assembly", "target"]
feature_cols = [c for c in df_test.columns if c not in exclude_cols]

X_test = df_test[feature_cols]
X_vus = df_vus[feature_cols]

print(f"Loaded X_test ({X_test.shape}) and X_vus ({X_vus.shape}).")
"""),
    nbf.v4.new_markdown_cell("""## 1. TreeSHAP Global Feature Attribution (Beeswarm Plot)"""),
    nbf.v4.new_code_cell("""explainer = shap.TreeExplainer(xgb_model)
shap_values = explainer(X_test)

# Plot Beeswarm Summary directly with shap.summary_plot
shap.summary_plot(shap_values.values, X_test, max_display=12, show=True)
"""),
    nbf.v4.new_markdown_cell("""### Global Feature Importance Bar Chart"""),
    nbf.v4.new_code_cell("""# Plot Feature Importance Bar Chart
shap.summary_plot(shap_values.values, X_test, plot_type="bar", max_display=12, show=True)
"""),
    nbf.v4.new_markdown_cell("""## 2. Prioritize 34,466 Variants of Uncertain Significance (VUS)"""),
    nbf.v4.new_code_cell("""vus_probs = xgb_model.predict_proba(X_vus)[:, 1]
df_vus["predicted_pathogenicity_score"] = vus_probs

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
df_vus_sorted = df_vus.sort_values(by="predicted_pathogenicity_score", ascending=False).reset_index(drop=True)

tier_counts = df_vus_sorted["prioritization_tier"].value_counts()
print("VUS Triage Breakdown:")
for tier, count in tier_counts.items():
    print(f"  {tier}: {count:,} ({count/len(df_vus)*100:.1f}%)")

plt.figure(figsize=(10, 4.5))
tier_counts.plot(kind="barh", color=["#b2182b", "#ef8a62", "#d1e5f0", "#2166ac"], edgecolor="black")
plt.title("Triage Breakdown of 34,466 Variants of Uncertain Significance (VUS)", fontweight="bold", pad=12)
plt.xlabel("Number of Variants")
plt.tight_layout()
plt.show()
"""),
    nbf.v4.new_markdown_cell("""## 3. Top 20 Highest Priority VUS Candidates for Clinical Diagnostic Review"""),
    nbf.v4.new_code_cell("""display_cols = [
    "variation_id", "chrom", "start", "stop", "log10_length", "gene_count",
    "is_deletion", "gnomad_af", "predicted_pathogenicity_score", "prioritization_tier"
]
df_vus_sorted[display_cols].head(20)
""")
]

# Write and execute both notebooks
for filename, nb in [
    ("eda/07_model_training_and_evaluation.ipynb", nb7),
    ("eda/08_shap_explainability_and_vus_prioritization.ipynb", nb8)
]:
    print(f"Executing and saving {filename}...")
    client = NotebookClient(nb, timeout=600, kernel_name="python3")
    client.execute()
    with open(filename, "w", encoding="utf-8") as f:
        nbf.write(nb, f)
    print(f"Successfully executed and saved: {filename}")

print("\nAll notebooks built and pre-rendered with executed outputs.")
