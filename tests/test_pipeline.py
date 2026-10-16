"""
tests/test_pipeline.py
======================
Unit tests for data integrity, coordinate validity, and strict target leakage prevention.
"""

import json
import os
import unittest
import pandas as pd
import numpy as np

class TestSVPipeline(unittest.TestCase):
    
    def test_01_feature_matrix_integrity(self):
        """Test feature matrix exists, has valid shape and no NaN coordinates."""
        feat_path = "data/processed/feature_matrix_all.csv.gz"
        self.assertTrue(os.path.exists(feat_path), f"File {feat_path} does not exist.")
        
        df = pd.read_csv(feat_path)
        self.assertGreater(len(df), 50000, "Dataset contains fewer records than expected.")
        self.assertTrue((df["start"] > 0).all(), "Found invalid non-positive start coordinates.")
        self.assertTrue((df["stop"] >= df["start"]).all(), "Found stop coordinate smaller than start coordinate.")
        self.assertTrue((df["log10_length"] >= np.log10(50)).all(), "Found SVs smaller than 50 bp minimum cutoff.")
        
    def test_02_strict_leakage_prevention(self):
        """Verify that forbidden metadata and phenotype fields are not present in features."""
        with open("models/feature_names.json", "r") as f:
            features = json.load(f)
            
        forbidden_substrings = ["review", "phenotype", "submitter", "clnsig", "target", "otherid", "tested"]
        for feat in features:
            for forbidden in forbidden_substrings:
                self.assertNotIn(forbidden, feat.lower(), f"Potential leakage column found in features: {feat}")
                
    def test_03_split_disjointness(self):
        """Verify that chromosomal splits have zero chromosome overlap."""
        df_train = pd.read_csv("data/processed/train.csv.gz")
        df_val = pd.read_csv("data/processed/val.csv.gz")
        df_test = pd.read_csv("data/processed/test.csv.gz")
        
        train_c = set(df_train["chrom"].astype(str).unique())
        val_c = set(df_val["chrom"].astype(str).unique())
        test_c = set(df_test["chrom"].astype(str).unique())
        
        self.assertEqual(len(train_c.intersection(val_c)), 0, "Train and Val share chromosomes.")
        self.assertEqual(len(train_c.intersection(test_c)), 0, "Train and Test share chromosomes.")
        self.assertEqual(len(val_c.intersection(test_c)), 0, "Val and Test share chromosomes.")

if __name__ == "__main__":
    unittest.main()
