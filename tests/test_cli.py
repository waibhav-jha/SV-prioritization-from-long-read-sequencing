"""
tests/test_cli.py
=================
Integration and unit tests for prioritize_sv.py CLI and modules.
"""

import os
import shutil
import unittest
import pandas as pd
from src.vcf_parser import LongReadVCFParser
from src.fast_annotator import FastSVAnnotator
from src.predictor import SVPredictor
from src.visualizer import SHAPVisualizer
from src.reporter import ClinicalReporter

class TestSVCLI(unittest.TestCase):
    
    def setUp(self):
        self.sample_vcf = "examples/sample_patient_longread.vcf"
        self.test_out_dir = "results/test_cli_output"
        os.makedirs(self.test_out_dir, exist_ok=True)
        
    def test_01_vcf_parser(self):
        parser = LongReadVCFParser(self.sample_vcf)
        df_parsed = parser.parse()
        self.assertGreater(len(df_parsed), 0, "Parser returned 0 records.")
        self.assertIn("raw_svtype", df_parsed.columns)
        self.assertIn("length", df_parsed.columns)
        self.assertTrue((df_parsed["length"] >= 50).all())
        
    def test_02_fast_annotator(self):
        parser = LongReadVCFParser(self.sample_vcf)
        df_parsed = parser.parse()
        annotator = FastSVAnnotator()
        df_ann = annotator.annotate(df_parsed)
        self.assertEqual(len(df_ann), len(df_parsed))
        self.assertIn("log10_length", df_ann.columns)
        self.assertIn("gnomad_af", df_ann.columns)
        self.assertIn("is_deletion", df_ann.columns)
        
    def test_03_predictor_and_risk_tiers(self):
        parser = LongReadVCFParser(self.sample_vcf)
        df_parsed = parser.parse()
        annotator = FastSVAnnotator()
        df_ann = annotator.annotate(df_parsed)
        predictor = SVPredictor()
        df_pred = predictor.predict(df_ann)
        
        self.assertIn("pathogenicity_score", df_pred.columns)
        self.assertIn("priority_tier", df_pred.columns)
        self.assertTrue((df_pred["pathogenicity_score"] >= 0.0).all())
        self.assertTrue((df_pred["pathogenicity_score"] <= 1.0).all())
        
        # Verify that the high impact large deletion is ranked high
        top_var = df_pred.iloc[0]
        self.assertIn("Tier 1", top_var["priority_tier"])
        
    def test_04_reporting_generation(self):
        parser = LongReadVCFParser(self.sample_vcf)
        df_parsed = parser.parse()
        annotator = FastSVAnnotator()
        df_ann = annotator.annotate(df_parsed)
        predictor = SVPredictor()
        df_pred = predictor.predict(df_ann)
        visualizer = SHAPVisualizer()
        
        shap_imgs = []
        for i in range(min(2, len(df_pred))):
            shap_imgs.append(visualizer.generate_waterfall(df_pred.iloc[i]))
            
        reporter = ClinicalReporter(df_pred, sample_name="TestPatient", top_shap_images=shap_imgs)
        
        html_out = os.path.join(self.test_out_dir, "clinical_report.html")
        csv_out = os.path.join(self.test_out_dir, "ranked_variants.csv")
        vcf_out = os.path.join(self.test_out_dir, "prioritized.vcf")
        
        reporter.generate_html_report(html_out)
        reporter.save_csv(csv_out)
        reporter.save_annotated_vcf(self.sample_vcf, vcf_out)
        
        self.assertTrue(os.path.exists(html_out))
        self.assertTrue(os.path.exists(csv_out))
        self.assertTrue(os.path.exists(vcf_out))
        self.assertGreater(os.path.getsize(html_out), 1000)

if __name__ == "__main__":
    unittest.main()
