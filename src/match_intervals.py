"""
src/match_intervals.py
======================
Hierarchical Interval Matching and Population Feature Integration Module.

Validates Assumption 2:
- Performs sensitivity analysis across reciprocal overlap thresholds (30%, 50%, 70%, 90%).
- Matches ClinVar SVs against gnomAD SV population baseline (387,477 sites).
- Integrates population allele frequencies and functional annotations without target leakage.
"""

import json
import os
import time
import pandas as pd
import numpy as np

def match_sv_intervals(
    clinvar_path="data/processed/harmonized_clinvar.csv.gz",
    gnomad_path="data/processed/gnomad_sv_cleaned.csv.gz",
    default_overlap=0.50
):
    """
    Match ClinVar SVs with gnomAD SVs by chromosome, compatible SV type, and reciprocal overlap.
    """
    print("--- [Step 2.1] Loading Harmonized Datasets for Interval Matching ---")
    start_time = time.time()
    
    df_cv = pd.read_csv(clinvar_path)
    df_gn = pd.read_csv(gnomad_path)
    
    print(f"Loaded {len(df_cv):,} ClinVar SVs and {len(df_gn):,} gnomAD SVs in {time.time()-start_time:.1f}s.")
    
    # Map ClinVar SV types to generalized categories
    def generalize_type(t):
        t_str = str(t).lower()
        if "del" in t_str or "loss" in t_str:
            return "DEL"
        elif "dup" in t_str or "gain" in t_str:
            return "DUP"
        elif "inv" in t_str:
            return "INV"
        elif "ins" in t_str:
            return "INS"
        else:
            return "OTHER"
            
    df_cv["gen_type"] = df_cv["type"].apply(generalize_type)
    df_gn["gen_type"] = df_gn["svtype"].apply(generalize_type)
    
    # Index gnomAD SVs by chromosome and type for rapid interval searching
    print("--- [Step 2.2] Building Genomic Interval Index ---")
    gnomad_index = {}
    for chrom, c_group in df_gn.groupby(df_gn["chrom"].astype(str)):
        gnomad_index[chrom] = {}
        for g_type, t_group in c_group.groupby("gen_type"):
            gnomad_index[chrom][g_type] = {
                "starts": t_group["start"].to_numpy(),
                "ends": t_group["end"].to_numpy(),
                "lengths": t_group["svlen"].to_numpy(),
                "afs": t_group["af"].to_numpy(),
                "popmax_afs": t_group["popmax_af"].fillna(0.0).to_numpy(),
                "afr_afs": t_group["afr_af"].to_numpy(),
                "eur_afs": t_group["eur_af"].to_numpy(),
                "lofs": t_group["has_lof"].to_numpy(),
                "promoters": t_group["is_promoter"].to_numpy(),
                "copy_gains": t_group["has_copy_gain"].to_numpy()
            }
            
    print(f"Built interval index across {len(gnomad_index)} chromosomes.")
    
    # Run Sensitivity Benchmark on a sample to validate Assumption 2
    print("--- [Step 2.3] Validating Assumption 2 (Overlap Sensitivity Analysis) ---")
    sample_cv = df_cv.sample(n=min(5000, len(df_cv)), random_state=42)
    thresholds = [0.30, 0.50, 0.70, 0.90]
    sensitivity_results = {}
    
    for thresh in thresholds:
        match_count = 0
        path_matched_afs = []
        benign_matched_afs = []
        
        for _, row in sample_cv.iterrows():
            c_chr = str(row["chrom"])
            c_type = row["gen_type"]
            c_start = row["start"]
            c_stop = row["stop"]
            c_len = row["length"]
            c_class = row["clinical_class"]
            
            if c_chr not in gnomad_index or c_type not in gnomad_index[c_chr]:
                continue
                
            idx_dict = gnomad_index[c_chr][c_type]
            g_starts = idx_dict["starts"]
            g_ends = idx_dict["ends"]
            g_lens = idx_dict["lengths"]
            g_afs = idx_dict["afs"]
            
            # Candidate boolean mask
            cand_mask = (g_starts <= c_stop) & (g_ends >= c_start)
            if not np.any(cand_mask):
                continue
                
            cand_starts = g_starts[cand_mask]
            cand_ends = g_ends[cand_mask]
            cand_lens = g_lens[cand_mask]
            cand_afs = g_afs[cand_mask]
            
            # Calculate reciprocal overlap
            ov_starts = np.maximum(c_start, cand_starts)
            ov_ends = np.minimum(c_stop, cand_ends)
            ov_lens = np.maximum(0, ov_ends - ov_starts)
            
            recip_overlaps = ov_lens / np.maximum(c_len, cand_lens)
            valid_matches = recip_overlaps >= thresh
            
            if np.any(valid_matches):
                match_count += 1
                max_af = np.max(cand_afs[valid_matches])
                if "Pathogenic" in c_class:
                    path_matched_afs.append(max_af)
                elif "Benign" in c_class:
                    benign_matched_afs.append(max_af)
                    
        sensitivity_results[f"overlap_{int(thresh*100)}pct"] = {
            "threshold": thresh,
            "overall_match_rate_pct": round(match_count / len(sample_cv) * 100, 2),
            "pathogenic_median_af": float(np.median(path_matched_afs)) if path_matched_afs else 0.0,
            "benign_median_af": float(np.median(benign_matched_afs)) if benign_matched_afs else 0.0,
            "pathogenic_mean_af": float(np.mean(path_matched_afs)) if path_matched_afs else 0.0,
            "benign_mean_af": float(np.mean(benign_matched_afs)) if benign_matched_afs else 0.0
        }
        
    print("Sensitivity Results:")
    for k, v in sensitivity_results.items():
        print(f"  {k}: Match Rate = {v['overall_match_rate_pct']}%, Pathogenic Median AF = {v['pathogenic_median_af']:.5f}, Benign Median AF = {v['benign_median_af']:.5f}")
        
    # Save Assumption 2 metrics
    with open("results/assumption2_interval_matching_metrics.json", "w") as f:
        json.dump(sensitivity_results, f, indent=2)
        
    print("\n--- [Step 2.4] Matching Full Dataset with Optimal Hierarchical Overlap (50% default) ---")
    matched_features = []
    
    for i, row in df_cv.iterrows():
        c_chr = str(row["chrom"])
        c_type = row["gen_type"]
        c_start = row["start"]
        c_stop = row["stop"]
        c_len = row["length"]
        
        # Default unobserved values (imputed 0 for healthy population)
        f_af = 0.0
        f_popmax_af = 0.0
        f_afr_af = 0.0
        f_eur_af = 0.0
        f_lof = 0
        f_promoter = 0
        f_copy_gain = 0
        f_matched = 0
        
        if c_chr in gnomad_index and c_type in gnomad_index[c_chr]:
            idx_dict = gnomad_index[c_chr][c_type]
            g_starts = idx_dict["starts"]
            g_ends = idx_dict["ends"]
            g_lens = idx_dict["lengths"]
            
            cand_mask = (g_starts <= c_stop) & (g_ends >= c_start)
            if np.any(cand_mask):
                cand_starts = g_starts[cand_mask]
                cand_ends = g_ends[cand_mask]
                cand_lens = g_lens[cand_mask]
                
                ov_starts = np.maximum(c_start, cand_starts)
                ov_ends = np.minimum(c_stop, cand_ends)
                ov_lens = np.maximum(0, ov_ends - ov_starts)
                
                recip_overlaps = ov_lens / np.maximum(c_len, cand_lens)
                valid_matches = recip_overlaps >= default_overlap
                
                if np.any(valid_matches):
                    f_matched = 1
                    f_af = float(np.max(idx_dict["afs"][cand_mask][valid_matches]))
                    f_popmax_af = float(np.max(idx_dict["popmax_afs"][cand_mask][valid_matches]))
                    f_afr_af = float(np.max(idx_dict["afr_afs"][cand_mask][valid_matches]))
                    f_eur_af = float(np.max(idx_dict["eur_afs"][cand_mask][valid_matches]))
                    f_lof = int(np.max(idx_dict["lofs"][cand_mask][valid_matches]))
                    f_promoter = int(np.max(idx_dict["promoters"][cand_mask][valid_matches]))
                    f_copy_gain = int(np.max(idx_dict["copy_gains"][cand_mask][valid_matches]))
                    
        matched_features.append({
            "gnomad_matched": f_matched,
            "gnomad_af": f_af,
            "gnomad_popmax_af": f_popmax_af,
            "gnomad_afr_af": f_afr_af,
            "gnomad_eur_af": f_eur_af,
            "gnomad_lof": f_lof,
            "gnomad_promoter": f_promoter,
            "gnomad_copy_gain": f_copy_gain
        })
        
    df_feat = pd.DataFrame(matched_features)
    df_joined = pd.concat([df_cv, df_feat], axis=1)
    
    out_matched = "data/processed/clinvar_matched_gnomad.csv.gz"
    df_joined.to_csv(out_matched, index=False, compression="gzip")
    print(f"Successfully generated matched dataset: {out_matched} ({len(df_joined):,} rows)")
    return df_joined

if __name__ == "__main__":
    match_sv_intervals()
