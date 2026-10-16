"""
src/visualizer.py
=================
Local TreeSHAP Waterfall Visualization & Explanation Generator.
"""

import base64
import io
import json
import os
import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap

# Configure matplotlib for headless generation
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10

class SHAPVisualizer:
    def __init__(self, model_path="models/xgboost_model.joblib"):
        self.model_path = self._resolve_path(model_path)
        self.model = joblib.load(self.model_path)
        self.explainer = shap.TreeExplainer(self.model)
        
        feature_names_path = self._resolve_path("models/feature_names.json")
        with open(feature_names_path, "r") as f:
            self.feature_cols = json.load(f)
            
    def _resolve_path(self, p):
        for candidate in [p, os.path.join("..", p), os.path.join("data", p), os.path.join("..", "data", p)]:
            if os.path.exists(candidate):
                return candidate
        return p
        
    def generate_waterfall(self, df_row, out_png_path=None):
        """
        Generate a local SHAP waterfall explanation for a single variant row.
        Returns base64 encoded image string.
        """
        # Build 1-row DataFrame with explicit float dtypes
        feat_dict = {col: float(df_row.get(col, 0.0)) for col in self.feature_cols}
        X_single = pd.DataFrame([feat_dict])
        
        shap_values_single = self.explainer(X_single)[0]
        
        # Create clear plot
        fig, ax = plt.subplots(figsize=(8.5, 4.5))
        shap.plots.waterfall(shap_values_single, max_display=9, show=False)
        var_id = str(df_row.get('var_id', 'SV'))
        chrom = str(df_row.get('chrom', ''))
        start = df_row.get('start', 0)
        stop = df_row.get('stop', 0)
        plt.title(f"Variant Risk Drivers: {var_id} (Chr{chrom}:{start:,}-{stop:,})", fontweight="bold", pad=12)
        plt.tight_layout()
        
        # Save to file if path provided
        if out_png_path:
            os.makedirs(os.path.dirname(out_png_path), exist_ok=True)
            plt.savefig(out_png_path, dpi=200, bbox_inches="tight")
            
        # Generate base64 buffer for HTML embedding
        buf = io.BytesIO()
        plt.savefig(buf, format="png", dpi=180, bbox_inches="tight")
        plt.close(fig)
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode("utf-8")
        
        return img_base64
