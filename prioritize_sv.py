#!/usr/bin/env python
"""
prioritize_sv.py
================
End-to-End AI-Based Long-Read Structural Variant Prioritization CLI Tool.

Usage:
    python prioritize_sv.py --input sample.vcf --output-dir reports/sample_01/
"""

import argparse
import os
import sys
import time
import pandas as pd

from src.vcf_parser import LongReadVCFParser
from src.fast_annotator import FastSVAnnotator
from src.predictor import SVPredictor
from src.visualizer import SHAPVisualizer
from src.reporter import ClinicalReporter

def main():
    parser = argparse.ArgumentParser(
        description="AI-Based Structural Variant Prioritization for Long-Read Sequencing (PacBio / Oxford Nanopore)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--input", "-i", required=True, help="Input Long-Read VCF file (e.g. from Sniffles2, cuteSV, PBSV)")
    parser.add_argument("--output-dir", "-o", default="output", help="Directory to save generated reports, CSVs, and figures")
    parser.add_argument("--sample-name", "-s", default=None, help="Sample identifier (defaults to input filename stem)")
    parser.add_argument("--top-k-shap", "-k", type=int, default=4, help="Number of top candidates to render SHAP waterfall plots for")
    parser.add_argument("--overlap", type=float, default=0.50, help="Reciprocal overlap threshold for gnomAD matching")
    parser.add_argument("--min-support", type=int, default=3, help="Minimum read support threshold")
    parser.add_argument("--model-type", "-m", choices=["xgboost", "dl", "ensemble"], default="xgboost", help="Model architecture: 'xgboost' (default), 'dl' (Tabular ResNet), or 'ensemble'")
    
    args = parser.parse_args()
    
    start_total = time.time()
    
    if not os.path.exists(args.input):
        print(f"Error: Input VCF file not found at '{args.input}'", file=sys.stderr)
        sys.exit(1)
        
    sample_name = args.sample_name or os.path.splitext(os.path.basename(args.input))[0].replace(".prioritized", "")
    os.makedirs(args.output_dir, exist_ok=True)
    
    print("================================================================================")
    print("Long-Read Structural Variant Prioritizer (Explainable AI Engine)")
    print(f"Sample: {sample_name} | Input: {args.input} | Output: {args.output_dir}")
    print("================================================================================")
    
    # Step 1: Parse VCF
    print("\n[1/5] Ingesting & Parsing Long-Read VCF...")
    t0 = time.time()
    vcf_parser = LongReadVCFParser(args.input, min_support=args.min_support)
    df_raw = vcf_parser.parse()
    print(f"      Parsed {len(df_raw):,} structural variants (>= 50 bp) in {time.time()-t0:.2f}s.")
    
    if len(df_raw) == 0:
        print("Warning: No structural variants >= 50 bp found in input VCF.")
        sys.exit(0)
        
    # Step 2: Annotate Features
    print("\n[2/5] Annotating Population Frequencies & Gene Constraints...")
    t0 = time.time()
    annotator = FastSVAnnotator()
    df_annotated = annotator.annotate(df_raw, overlap_threshold=args.overlap)
    print(f"      Annotated in {time.time()-t0:.2f}s.")
    
    # Step 3: Run Model Prediction & Clinical Tiers
    print(f"\n[3/5] Running Calibrated ML Model Inference ({args.model_type.upper()}) & ACMG Risk Tiering...")
    t0 = time.time()
    predictor = SVPredictor(model_type=args.model_type)
    df_prioritized = predictor.predict(df_annotated)
    print(f"      Inference complete in {time.time()-t0:.2f}s.")
    
    tier_counts = df_prioritized["priority_tier"].value_counts().to_dict()
    for tier, cnt in tier_counts.items():
        print(f"      • {tier}: {cnt:,} variants")
        
    # Step 4: Generate Local TreeSHAP Explanations
    print(f"\n[4/5] Computing TreeSHAP Attributions for Top {min(args.top_k_shap, len(df_prioritized))} Candidates...")
    t0 = time.time()
    visualizer = SHAPVisualizer()
    shap_images_b64 = []
    
    figures_dir = os.path.join(args.output_dir, "figures")
    os.makedirs(figures_dir, exist_ok=True)
    
    for rank in range(min(args.top_k_shap, len(df_prioritized))):
        row = df_prioritized.iloc[rank]
        png_path = os.path.join(figures_dir, f"shap_candidate_{rank+1}.png")
        img_b64 = visualizer.generate_waterfall(row, out_png_path=png_path)
        shap_images_b64.append(img_b64)
    print(f"      SHAP waterfall figures generated in {time.time()-t0:.2f}s.")
    
    # Step 5: Generate Reports
    print("\n[5/5] Generating Multi-Format Clinical Reports...")
    reporter = ClinicalReporter(df_prioritized, sample_name=sample_name, top_shap_images=shap_images_b64)
    
    csv_path = os.path.join(args.output_dir, "ranked_variants.csv")
    reporter.save_csv(csv_path)
    
    vcf_path = os.path.join(args.output_dir, f"{sample_name}.prioritized.vcf")
    reporter.save_annotated_vcf(args.input, vcf_path)
    
    html_path = os.path.join(args.output_dir, "clinical_report.html")
    reporter.generate_html_report(html_path)
    
    total_time = time.time() - start_total
    print("\n================================================================================")
    print(f"Pipeline Completed Successfully in {total_time:.2f}s!")
    print(f"• Interactive HTML Report: {html_path}")
    print(f"• Ranked CSV File:         {csv_path}")
    print(f"• Annotated Patient VCF:   {vcf_path}")
    print("================================================================================")

if __name__ == "__main__":
    main()
