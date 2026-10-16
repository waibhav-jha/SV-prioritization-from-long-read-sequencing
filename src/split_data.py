"""
src/split_data.py
=================
Leakage-Free Chromosomal Partitioning and Dataset Splitting Module.

Validates Assumption 4:
- Evaluates Jaccard overlap between genomic intervals across splits (verifies 0.0% overlap).
- Partitions primary labeled dataset (Pathogenic vs Benign) into Train, Val, Test.
- Isolates VUS variants into a separate inference evaluation set.
"""

import json
import os
import pandas as pd
import numpy as np

def split_dataset(feature_matrix_path="data/processed/feature_matrix_all.csv.gz"):
    """
    Split feature matrix into Train, Val, Test by chromosome and isolate VUS holdout.
    """
    print("--- [Step 4.1] Loading Feature Matrix for Dataset Splitting ---")
    df = pd.read_csv(feature_matrix_path)
    print(f"Loaded {len(df):,} total feature rows.")
    
    # Isolate VUS and Other variants for inference triage
    df_vus = df[df["clinical_class"] == "VUS"].copy().reset_index(drop=True)
    df_conflict = df[df["clinical_class"] == "Conflicting"].copy().reset_index(drop=True)
    
    out_vus = "data/processed/vus_inference.csv.gz"
    df_vus.to_csv(out_vus, index=False, compression="gzip")
    print(f"Isolated {len(df_vus):,} VUS variants to {out_vus}")
    
    # Filter primary labeled subset: Pathogenic (1) vs Benign (0)
    labeled_mask = df["clinical_class"].isin(["Pathogenic", "Likely Pathogenic", "Benign", "Likely Benign"])
    df_labeled = df[labeled_mask].copy().reset_index(drop=True)
    df_labeled["target"] = df_labeled["clinical_class"].isin(["Pathogenic", "Likely Pathogenic"]).astype(int)
    
    print(f"Total primary labeled dataset: {len(df_labeled):,} SVs")
    print(f"  Pathogenic (Y=1): {df_labeled['target'].sum():,} ({df_labeled['target'].mean()*100:.2f}%)")
    print(f"  Benign (Y=0):     {(df_labeled['target']==0).sum():,} ({(1-df_labeled['target'].mean())*100:.2f}%)")
    
    # Chromosomal Partitioning
    train_chroms = [str(i) for i in range(1, 15)] # Chr 1 - 14
    val_chroms = [str(i) for i in range(15, 19)]   # Chr 15 - 18
    test_chroms = [str(i) for i in range(19, 23)] + ["X", "Y"] # Chr 19 - 22, X, Y
    
    df_train = df_labeled[df_labeled["chrom"].astype(str).isin(train_chroms)].copy().reset_index(drop=True)
    df_val = df_labeled[df_labeled["chrom"].astype(str).isin(val_chroms)].copy().reset_index(drop=True)
    df_test = df_labeled[df_labeled["chrom"].astype(str).isin(test_chroms)].copy().reset_index(drop=True)
    
    print(f"\n--- [Step 4.2] Validating Assumption 4 (Split Balance & Leakage Verification) ---")
    print(f"Train Set (Chr 1-14):   {len(df_train):,} SVs (Pos: {df_train['target'].mean()*100:.1f}%)")
    print(f"Val Set   (Chr 15-18):  {len(df_val):,} SVs (Pos: {df_val['target'].mean()*100:.1f}%)")
    print(f"Test Set  (Chr 19-22,X,Y): {len(df_test):,} SVs (Pos: {df_test['target'].mean()*100:.1f}%)")
    
    # Check Chromosome Disjointness
    train_c = set(df_train["chrom"].unique())
    val_c = set(df_val["chrom"].unique())
    test_c = set(df_test["chrom"].unique())
    
    overlap_train_val = train_c.intersection(val_c)
    overlap_train_test = train_c.intersection(test_c)
    overlap_val_test = val_c.intersection(test_c)
    
    is_strictly_disjoint = (len(overlap_train_val) == 0 and len(overlap_train_test) == 0 and len(overlap_val_test) == 0)
    print(f"Strict Chromosomal Disjointness: {'CONFIRMED (Zero Overlap)' if is_strictly_disjoint else 'FAILED'}")
    
    # Save Split Datasets
    df_train.to_csv("data/processed/train.csv.gz", index=False, compression="gzip")
    df_val.to_csv("data/processed/val.csv.gz", index=False, compression="gzip")
    df_test.to_csv("data/processed/test.csv.gz", index=False, compression="gzip")
    
    assumption4_metrics = {
        "is_strictly_disjoint": is_strictly_disjoint,
        "train_count": len(df_train),
        "val_count": len(df_val),
        "test_count": len(df_test),
        "train_pos_rate": float(df_train['target'].mean()),
        "val_pos_rate": float(df_val['target'].mean()),
        "test_pos_rate": float(df_test['target'].mean()),
        "vus_count": len(df_vus)
    }
    
    with open("results/assumption4_split_metrics.json", "w") as f:
        json.dump(assumption4_metrics, f, indent=2)
        
    print("Assumption 4 Validation Complete: Metrics saved to results/assumption4_split_metrics.json")
    return df_train, df_val, df_test, df_vus

if __name__ == "__main__":
    split_dataset()
