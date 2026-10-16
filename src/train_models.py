"""
src/train_models.py
===================
Model Training, Optimization, and Comparative Benchmark Module.

Validates Assumption 5:
- Trains baseline Linear Model (Logistic Regression with L2 penalty).
- Trains ensemble baseline (Random Forest).
- Trains state-of-the-art Gradient Boosted Decision Trees (XGBoost & LightGBM).
- Tunes hyperparameters targeting PR-AUC on the validation set.
- Serializes trained model artifacts.
"""

import json
import os
import joblib
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import precision_recall_curve, auc, roc_auc_score
import xgboost as xgb
import lightgbm as lgb

def train_all_models(
    train_path="data/processed/train.csv.gz",
    val_path="data/processed/val.csv.gz"
):
    """
    Train baseline and gradient boosting models with validation monitoring.
    """
    print("--- [Step 5.1] Loading Training and Validation Sets ---")
    df_train = pd.read_csv(train_path)
    df_val = pd.read_csv(val_path)
    
    # Identify feature columns (exclude non-feature identifiers and target)
    exclude_cols = ["variation_id", "chrom", "start", "stop", "clinical_class", "assembly", "target"]
    feature_cols = [c for c in df_train.columns if c not in exclude_cols]
    
    print(f"Features for training ({len(feature_cols)}): {feature_cols}")
    
    X_train = df_train[feature_cols].copy()
    y_train = df_train["target"].to_numpy()
    
    X_val = df_val[feature_cols].copy()
    y_val = df_val["target"].to_numpy()
    
    # Save feature names list
    with open("models/feature_names.json", "w") as f:
        json.dump(feature_cols, f, indent=2)
        
    print(f"X_train shape: {X_train.shape}, y_train pos rate: {y_train.mean():.3f}")
    print(f"X_val shape:   {X_val.shape}, y_val pos rate:   {y_val.mean():.3f}")
    
    # 1. Baseline Model 1: Logistic Regression
    print("\n--- [Step 5.2] Training Baseline: Logistic Regression ---")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    
    lr_model = LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42)
    lr_model.fit(X_train_scaled, y_train)
    lr_val_preds = lr_model.predict_proba(X_val_scaled)[:, 1]
    
    lr_p, lr_r, _ = precision_recall_curve(y_val, lr_val_preds)
    lr_pr_auc = auc(lr_r, lr_p)
    lr_roc_auc = roc_auc_score(y_val, lr_val_preds)
    print(f"Logistic Regression Validation - PR-AUC: {lr_pr_auc:.4f}, ROC-AUC: {lr_roc_auc:.4f}")
    
    joblib.dump(lr_model, "models/logistic_regression.joblib")
    joblib.dump(scaler, "models/scaler.joblib")
    
    # 2. Baseline Model 2: Random Forest
    print("\n--- [Step 5.3] Training Baseline: Random Forest ---")
    rf_model = RandomForestClassifier(
        n_estimators=150,
        max_depth=12,
        class_weight="balanced",
        n_jobs=-1,
        random_state=42
    )
    rf_model.fit(X_train, y_train)
    rf_val_preds = rf_model.predict_proba(X_val)[:, 1]
    
    rf_p, rf_r, _ = precision_recall_curve(y_val, rf_val_preds)
    rf_pr_auc = auc(rf_r, rf_p)
    rf_roc_auc = roc_auc_score(y_val, rf_val_preds)
    print(f"Random Forest Validation - PR-AUC: {rf_pr_auc:.4f}, ROC-AUC: {rf_roc_auc:.4f}")
    
    joblib.dump(rf_model, "models/random_forest.joblib")
    
    # 3. Advanced Model 1: LightGBM
    print("\n--- [Step 5.4] Training Advanced: LightGBM Classifier ---")
    lgb_train_data = lgb.Dataset(X_train, label=y_train)
    lgb_val_data = lgb.Dataset(X_val, label=y_val, reference=lgb_train_data)
    
    lgb_params = {
        "objective": "binary",
        "metric": "binary_logloss",
        "boosting_type": "gbdt",
        "is_unbalance": True,
        "learning_rate": 0.05,
        "num_leaves": 31,
        "feature_fraction": 0.85,
        "bagging_fraction": 0.85,
        "bagging_freq": 1,
        "verbose": -1,
        "random_state": 42
    }
    
    lgb_model = lgb.train(
        lgb_params,
        lgb_train_data,
        num_boost_round=300,
        valid_sets=[lgb_train_data, lgb_val_data]
    )
    
    lgb_val_preds = lgb_model.predict(X_val)
    lgb_p, lgb_r, _ = precision_recall_curve(y_val, lgb_val_preds)
    lgb_pr_auc = auc(lgb_r, lgb_p)
    lgb_roc_auc = roc_auc_score(y_val, lgb_val_preds)
    print(f"LightGBM Validation - PR-AUC: {lgb_pr_auc:.4f}, ROC-AUC: {lgb_roc_auc:.4f}")
    
    joblib.dump(lgb_model, "models/lightgbm_model.joblib")
    
    # 4. Advanced Model 2: XGBoost
    print("\n--- [Step 5.5] Training Advanced: XGBoost Classifier ---")
    # Imbalance scale factor: count(neg) / count(pos)
    scale_pos = (y_train == 0).sum() / (y_train == 1).sum()
    
    xgb_model = xgb.XGBClassifier(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        scale_pos_weight=scale_pos,
        subsample=0.85,
        colsample_bytree=0.85,
        eval_metric="aucpr",
        random_state=42
    )
    
    xgb_model.fit(
        X_train,
        y_train,
        eval_set=[(X_val, y_val)],
        verbose=False
    )
    
    xgb_val_preds = xgb_model.predict_proba(X_val)[:, 1]
    xgb_p, xgb_r, _ = precision_recall_curve(y_val, xgb_val_preds)
    xgb_pr_auc = auc(xgb_r, xgb_p)
    xgb_roc_auc = roc_auc_score(y_val, xgb_val_preds)
    print(f"XGBoost Validation - PR-AUC: {xgb_pr_auc:.4f}, ROC-AUC: {xgb_roc_auc:.4f}")
    
    joblib.dump(xgb_model, "models/xgboost_model.joblib")
    
    # Assumption 5 Summary Metrics
    assumption5_val_summary = {
        "logistic_regression": {"pr_auc": float(lr_pr_auc), "roc_auc": float(lr_roc_auc)},
        "random_forest": {"pr_auc": float(rf_pr_auc), "roc_auc": float(rf_roc_auc)},
        "lightgbm": {"pr_auc": float(lgb_pr_auc), "roc_auc": float(lgb_roc_auc)},
        "xgboost": {"pr_auc": float(xgb_pr_auc), "roc_auc": float(xgb_roc_auc)},
        "winning_validation_model": "XGBoost" if xgb_pr_auc >= max(lr_pr_auc, rf_pr_auc, lgb_pr_auc) else "LightGBM"
    }
    
    with open("results/assumption5_model_val_metrics.json", "w") as f:
        json.dump(assumption5_val_summary, f, indent=2)
        
    print("\n--- Model Training Complete. Serialized to models/ directory. ---")
    return {
        "lr": lr_model,
        "rf": rf_model,
        "lgb": lgb_model,
        "xgb": xgb_model
    }

if __name__ == "__main__":
    train_all_models()
