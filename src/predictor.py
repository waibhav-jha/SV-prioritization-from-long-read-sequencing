"""
src/predictor.py
================
Inference Engine and ACMG-Inspired Clinical Priority Tier Assignment.
Supports XGBoost (Tree-based), Tabular ResNet (Deep Learning), and Ensemble modes.
"""

import json
import os
import joblib
import pandas as pd
import numpy as np

try:
    import torch
    import torch.nn as nn
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False


if TORCH_AVAILABLE:
    class ResBlock(nn.Module):
        def __init__(self, dim, dropout=0.2):
            super().__init__()
            self.block = nn.Sequential(
                nn.Linear(dim, dim),
                nn.BatchNorm1d(dim),
                nn.SiLU(),
                nn.Dropout(dropout),
                nn.Linear(dim, dim),
                nn.BatchNorm1d(dim),
            )
            self.act = nn.SiLU()
            
        def forward(self, x):
            return self.act(x + self.block(x))

    class TabularResNet(nn.Module):
        def __init__(self, in_features, hidden_dim=128, num_blocks=3, dropout=0.2):
            super().__init__()
            self.stem = nn.Sequential(
                nn.Linear(in_features, hidden_dim),
                nn.BatchNorm1d(hidden_dim),
                nn.SiLU()
            )
            self.blocks = nn.ModuleList([ResBlock(hidden_dim, dropout) for _ in range(num_blocks)])
            self.head = nn.Sequential(
                nn.Linear(hidden_dim, 64),
                nn.BatchNorm1d(64),
                nn.SiLU(),
                nn.Dropout(dropout / 2),
                nn.Linear(64, 1)
            )
            
        def forward(self, x):
            h = self.stem(x)
            for block in self.blocks:
                h = block(h)
            return self.head(h).squeeze(-1)


class SVPredictor:
    def __init__(self, model_path="models/xgboost_model.joblib", model_type="xgboost"):
        """
        model_type: 'xgboost', 'dl' (Tabular ResNet), or 'ensemble' (XGBoost + DL)
        """
        self.model_type = model_type.lower()
        self.model_path = self._resolve_path(model_path)
        
        feature_names_path = self._resolve_path("models/feature_names.json")
        with open(feature_names_path, "r") as f:
            self.feature_cols = json.load(f)

        # Load models based on selection
        self.xgb_model = None
        self.dl_model = None
        self.dl_scaler = None

        if self.model_type in ["xgboost", "ensemble"]:
            self.xgb_model = joblib.load(self.model_path)
            self.model = self.xgb_model

        if self.model_type in ["dl", "ensemble"]:
            if not TORCH_AVAILABLE:
                raise ImportError("PyTorch is required for Deep Learning inference.")
            dl_weights_path = self._resolve_path("models/tabular_resnet.pth")
            dl_scaler_path = self._resolve_path("models/dl_scaler.joblib")
            
            self.dl_scaler = joblib.load(dl_scaler_path)
            self.dl_model = TabularResNet(in_features=len(self.feature_cols), hidden_dim=128, num_blocks=3, dropout=0.2)
            self.dl_model.load_state_dict(torch.load(dl_weights_path, map_location=torch.device("cpu")))
            self.dl_model.eval()
            if self.model_type == "dl":
                self.model = self.dl_model

    def _resolve_path(self, p):
        for candidate in [p, os.path.join("..", p), os.path.join("data", p), os.path.join("..", "data", p)]:
            if os.path.exists(candidate):
                return candidate
        return p
        
    def predict(self, df_annotated):
        """
        Compute continuous pathogenicity scores and clinical triage tiers.
        """
        X = df_annotated[self.feature_cols].copy()
        
        if self.model_type == "xgboost":
            probabilities = self.xgb_model.predict_proba(X)[:, 1]
        elif self.model_type == "dl":
            X_scaled = self.dl_scaler.transform(X.values.astype(np.float32))
            with torch.no_grad():
                logits = self.dl_model(torch.from_numpy(X_scaled))
                probabilities = torch.sigmoid(logits).numpy()
        elif self.model_type == "ensemble":
            p_xgb = self.xgb_model.predict_proba(X)[:, 1]
            X_scaled = self.dl_scaler.transform(X.values.astype(np.float32))
            with torch.no_grad():
                logits = self.dl_model(torch.from_numpy(X_scaled))
                p_dl = torch.sigmoid(logits).numpy()
            probabilities = 0.5 * p_xgb + 0.5 * p_dl
        else:
            raise ValueError(f"Unknown model_type: {self.model_type}")
        
        df_out = df_annotated.copy()
        df_out["pathogenicity_score"] = np.round(probabilities, 4)
        
        # Clinical Risk Tiers
        tiers = []
        recommendations = []
        
        for p in probabilities:
            if p >= 0.85:
                tiers.append("Tier 1 (High-Confidence Pathogenic)")
                recommendations.append("Immediate clinical review; candidate for diagnostic confirmation")
            elif p >= 0.50:
                tiers.append("Tier 2 (Moderate-Risk / Uncertain)")
                recommendations.append("Secondary review; evaluate patient phenotypic match")
            elif p >= 0.20:
                tiers.append("Tier 3 (Low-Risk / Likely Tolerated)")
                recommendations.append("Likely non-causal background variation")
            else:
                tiers.append("Tier 4 (Benign Polymorphism)")
                recommendations.append("Deprioritize; consistent with common population allele")
                
        df_out["priority_tier"] = tiers
        df_out["clinical_recommendation"] = recommendations
        
        # Sort by descending pathogenicity score
        df_out = df_out.sort_values(by="pathogenicity_score", ascending=False).reset_index(drop=True)
        return df_out

