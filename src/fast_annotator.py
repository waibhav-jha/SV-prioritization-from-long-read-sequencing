"""
src/fast_annotator.py
=====================
High-Throughput On-the-Fly Genomic Feature Annotator for Long-Read SVs.
"""

import json
import os
import pandas as pd
import numpy as np

class FastSVAnnotator:
    def __init__(self, gnomad_path="data/processed/gnomad_sv_cleaned.csv.gz"):
        self.gnomad_path = self._resolve_path(gnomad_path)
        self.gnomad_index = {}
        self._load_gnomad_index()
        
    def _resolve_path(self, p):
        for candidate in [p, os.path.join("..", p), os.path.join("data", p), os.path.join("..", "data", p)]:
            if os.path.exists(candidate):
                return candidate
        return p
        
    def _generalize_type(self, t):
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
            
    def _load_gnomad_index(self):
        """Build in-memory indexed arrays for sub-millisecond interval intersection."""
        if not os.path.exists(self.gnomad_path):
            print(f"Warning: gnomAD baseline not found at {self.gnomad_path}. Running with fallback 0 AF.")
            return
            
        df_gn = pd.read_csv(self.gnomad_path, low_memory=False)
        df_gn["gen_type"] = df_gn["svtype"].apply(self._generalize_type)
        
        for chrom, c_group in df_gn.groupby(df_gn["chrom"].astype(str)):
            self.gnomad_index[chrom] = {}
            for g_type, t_group in c_group.groupby("gen_type"):
                self.gnomad_index[chrom][g_type] = {
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
                
    def annotate(self, df_vcf, overlap_threshold=0.50):
        """
        Annotate VCF DataFrame with population, constraint, and structural features.
        """
        annotated_rows = []
        
        for _, row in df_vcf.iterrows():
            c_chr = str(row["chrom"])
            c_raw_type = row["raw_svtype"]
            c_gen_type = self._generalize_type(c_raw_type)
            c_start = row["start"]
            c_stop = row["stop"]
            c_len = row["length"]
            
            # Intrinsic features
            log10_len = float(np.log10(max(50, c_len)))
            is_del = 1 if c_gen_type == "DEL" else 0
            is_dup = 1 if c_gen_type == "DUP" else 0
            is_allosomal = 1 if c_chr in ["X", "Y"] else 0
            
            # Simulated proxy for gene count based on genomic size (approx 1 gene per 100kb average density)
            gene_count = int(max(0, np.round(c_len / 75000))) if c_len >= 10000 else (1 if c_len >= 1000 else 0)
            constraint_max = float(np.clip(gene_count * is_del, 0, 10))
            constraint_mean = float(is_del / np.log2(gene_count + 1)) if gene_count > 0 else 0.0
            constraint_cum = float(log10_len * gene_count * is_del)
            
            # Population interval matching
            f_matched = 0
            f_af = 0.0
            f_popmax_af = 0.0
            f_afr_af = 0.0
            f_eur_af = 0.0
            f_lof = 0
            f_promoter = 0
            f_copy_gain = 0
            
            if c_chr in self.gnomad_index and c_gen_type in self.gnomad_index[c_chr]:
                idx_dict = self.gnomad_index[c_chr][c_gen_type]
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
                    valid_matches = recip_overlaps >= overlap_threshold
                    
                    if np.any(valid_matches):
                        f_matched = 1
                        f_af = float(np.max(idx_dict["afs"][cand_mask][valid_matches]))
                        f_popmax_af = float(np.max(idx_dict["popmax_afs"][cand_mask][valid_matches]))
                        f_afr_af = float(np.max(idx_dict["afr_afs"][cand_mask][valid_matches]))
                        f_eur_af = float(np.max(idx_dict["eur_afs"][cand_mask][valid_matches]))
                        f_lof = int(np.max(idx_dict["lofs"][cand_mask][valid_matches]))
                        f_promoter = int(np.max(idx_dict["promoters"][cand_mask][valid_matches]))
                        f_copy_gain = int(np.max(idx_dict["copy_gains"][cand_mask][valid_matches]))
                        
            log10_af = float(np.log10(max(1e-6, f_af))) if f_af > 0 else -5.0
            log10_popmax_af = float(np.log10(max(1e-6, f_popmax_af))) if f_popmax_af > 0 else -5.0
            is_rare = 1 if f_af < 0.01 else 0
            
            # Type dummies
            type_del = 1 if c_gen_type == "DEL" else 0
            type_dup = 1 if c_gen_type == "DUP" else 0
            type_ins = 1 if c_gen_type == "INS" else 0
            type_inv = 1 if c_gen_type == "INV" else 0
            type_other = 1 if c_gen_type not in ["DEL", "DUP", "INS", "INV"] else 0
            
            annotated_rows.append({
                "log10_length": log10_len,
                "gene_count": gene_count,
                "is_allosomal": is_allosomal,
                "is_deletion": is_del,
                "is_duplication": is_dup,
                "constraint_max_proxy": constraint_max,
                "constraint_mean_proxy": constraint_mean,
                "constraint_cumulative_proxy": constraint_cum,
                "gnomad_matched": f_matched,
                "gnomad_af": f_af,
                "log10_gnomad_af": log10_af,
                "gnomad_popmax_af": f_popmax_af,
                "log10_gnomad_popmax_af": log10_popmax_af,
                "gnomad_afr_af": f_afr_af,
                "gnomad_eur_af": f_eur_af,
                "gnomad_lof": f_lof,
                "gnomad_promoter": f_promoter,
                "gnomad_copy_gain": f_copy_gain,
                "is_rare_population_sv": is_rare,
                "type_DEL": type_del,
                "type_DUP": type_dup,
                "type_INS": type_ins,
                "type_INV": type_inv,
                "type_OTHER": type_other
            })
            
        df_feat = pd.DataFrame(annotated_rows)
        return pd.concat([df_vcf.reset_index(drop=True), df_feat.reset_index(drop=True)], axis=1)
