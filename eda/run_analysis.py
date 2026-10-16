"""
Comprehensive EDA script for SV Prioritization datasets.
Parses ClinVar, gnomAD SV, and dbVar to extract exact counts, distributions,
compatibility metrics, and statistical comparisons.
"""

import gzip
import os
import re
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Configure styling
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.titlesize'] = 14
sns.set_theme(style="whitegrid", palette="deep")

os.makedirs("reports/figures", exist_ok=True)
os.makedirs("eda/figures", exist_ok=True)

print("--- Step 1: Processing ClinVar ---")
# Stream ClinVar to capture SV statistics
# Define SV: Type in ['Deletion', 'Duplication', 'Inversion', 'Insertion', 'Indel', 'copy number gain', 'copy number loss']
# or Stop - Start >= 50 (when valid integers)

clinvar_records = []
clinvar_type_counts = {}
clinvar_clinsig_counts = {}
clinvar_assembly_counts = {}
clinvar_sv_rows = []

with gzip.open("raw/clinvar/variant_summary.txt.gz", "rt", encoding="utf-8", errors="replace") as f:
    header = f.readline().strip().split("\t")
    col_map = {col: i for i, col in enumerate(header)}
    
    line_num = 0
    for line in f:
        line_num += 1
        parts = line.strip().split("\t")
        if len(parts) < len(header):
            continue
        
        vtype = parts[col_map["Type"]]
        assembly = parts[col_map["Assembly"]]
        clinsig = parts[col_map["ClinicalSignificance"]]
        review = parts[col_map["ReviewStatus"]]
        chrom = parts[col_map["Chromosome"]]
        gene_sym = parts[col_map["GeneSymbol"]]
        pheno_list = parts[col_map["PhenotypeList"]]
        dbvar_id = parts[col_map["nsv/esv (dbVar)"]]
        
        try:
            start = int(parts[col_map["Start"]])
            stop = int(parts[col_map["Stop"]])
            length = abs(stop - start) + 1
        except (ValueError, IndexError):
            start = -1
            stop = -1
            length = -1
            
        is_sv_type = vtype in ["copy number gain", "copy number loss", "Deletion", "Duplication", "Inversion", "Insertion", "Indel"]
        is_sv_length = (length >= 50)
        
        # Track assembly
        clinvar_assembly_counts[assembly] = clinvar_assembly_counts.get(assembly, 0) + 1
        
        # If it's GRCh38 and is SV
        if assembly in ["GRCh38", "GRCh37"] and (is_sv_length or is_sv_type):
            if is_sv_length: # Strict length >= 50bp
                clinvar_sv_rows.append({
                    "allele_id": parts[col_map["#AlleleID"]],
                    "variation_id": parts[col_map["VariationID"]],
                    "type": vtype,
                    "gene_symbol": gene_sym,
                    "clinsig": clinsig,
                    "clinsig_simple": parts[col_map["ClinSigSimple"]],
                    "review_status": review,
                    "phenotypes": pheno_list,
                    "assembly": assembly,
                    "chrom": chrom,
                    "start": start,
                    "stop": stop,
                    "length": length,
                    "dbvar_id": dbvar_id
                })

print(f"Total ClinVar lines read: {line_num}")
print(f"Total SV records (length >= 50 bp across assemblies): {len(clinvar_sv_rows)}")

df_clinvar_sv = pd.DataFrame(clinvar_sv_rows)
print(f"ClinVar SV DataFrame shape: {df_clinvar_sv.shape}")
print("ClinVar Assemblies in SVs:", df_clinvar_sv["assembly"].value_counts().to_dict())

# Save parsed ClinVar SV subset for fast downstream access
df_clinvar_sv_grch38 = df_clinvar_sv[df_clinvar_sv["assembly"] == "GRCh38"].copy()
df_clinvar_sv_grch37 = df_clinvar_sv[df_clinvar_sv["assembly"] == "GRCh37"].copy()

print(f"GRCh38 SV count: {len(df_clinvar_sv_grch38)}")
print(f"GRCh37 SV count: {len(df_clinvar_sv_grch37)}")

print("\n--- Step 2: Processing gnomAD SV ---")
gnomad_rows = []
with gzip.open("raw/gnomad_sv/gnomad_v2.1_sv.sites.bed.gz", "rt", encoding="utf-8", errors="replace") as f:
    gnomad_header = f.readline().strip().split("\t")
    g_map = {col: i for i, col in enumerate(gnomad_header)}
    
    for line in f:
        parts = line.strip().split("\t")
        if len(parts) < len(gnomad_header):
            continue
        
        name = parts[g_map["name"]]
        chrom = parts[g_map["#chrom"]]
        try:
            start = int(parts[g_map["start"]])
            end = int(parts[g_map["end"]])
            svlen = int(parts[g_map["SVLEN"]]) if parts[g_map["SVLEN"]] != "NA" else abs(end - start)
        except ValueError:
            continue
            
        svtype = parts[g_map["svtype"]]
        af = float(parts[g_map["AF"]]) if parts[g_map["AF"]] not in ["NA", "."] else 0.0
        popmax_af = float(parts[g_map["POPMAX_AF"]]) if parts[g_map["POPMAX_AF"]] not in ["NA", "."] else np.nan
        lof = parts[g_map["PROTEIN_CODING__LOF"]]
        dup_partial = parts[g_map["PROTEIN_CODING__DUP_PARTIAL"]]
        copy_gain = parts[g_map["PROTEIN_CODING__COPY_GAIN"]]
        intergenic = parts[g_map["PROTEIN_CODING__INTERGENIC"]]
        intronic = parts[g_map["PROTEIN_CODING__INTRONIC"]]
        promoter = parts[g_map["PROTEIN_CODING__PROMOTER"]]
        
        # Pop AFs
        afr_af = float(parts[g_map["AFR_AF"]]) if parts[g_map["AFR_AF"]] not in ["NA", "."] else 0.0
        amr_af = float(parts[g_map["AMR_AF"]]) if parts[g_map["AMR_AF"]] not in ["NA", "."] else 0.0
        eas_af = float(parts[g_map["EAS_AF"]]) if parts[g_map["EAS_AF"]] not in ["NA", "."] else 0.0
        eur_af = float(parts[g_map["EUR_AF"]]) if parts[g_map["EUR_AF"]] not in ["NA", "."] else 0.0
        
        gnomad_rows.append({
            "name": name,
            "chrom": chrom,
            "start": start,
            "end": end,
            "svlen": svlen,
            "svtype": svtype,
            "af": af,
            "popmax_af": popmax_af,
            "afr_af": afr_af,
            "amr_af": amr_af,
            "eas_af": eas_af,
            "eur_af": eur_af,
            "lof": lof,
            "dup_partial": dup_partial,
            "copy_gain": copy_gain,
            "intergenic": intergenic,
            "intronic": intronic,
            "promoter": promoter
        })

df_gnomad = pd.DataFrame(gnomad_rows)
print(f"Total gnomAD SV records: {len(df_gnomad)}")

print("\n--- Step 3: Processing dbVar ---")
dbvar_files = {
    "Pathogenic": "raw/dbvar/GRCh38.variant_call.clinical.pathogenic_or_likely_pathogenic.vcf.gz",
    "Benign": "raw/dbvar/GRCh38.variant_call.clinical.benign_or_likely_benign.vcf.gz",
    "VUS": "raw/dbvar/GRCh38.variant_call.clinical.uncertain_significance.vcf.gz"
}

dbvar_rows = []
for label_cat, filepath in dbvar_files.items():
    with gzip.open(filepath, "rt", encoding="utf-8", errors="replace") as f:
        for line in f:
            if line.startswith("#"):
                continue
            parts = line.strip().split("\t")
            if len(parts) < 8:
                continue
            chrom = parts[0]
            pos = int(parts[1])
            var_id = parts[2]
            info = parts[7]
            
            info_dict = {}
            for item in info.split(";"):
                if "=" in item:
                    k, v = item.split("=", 1)
                    info_dict[k] = v
                else:
                    info_dict[item] = True
            
            svtype = info_dict.get("SVTYPE", "UNKNOWN")
            end = int(info_dict.get("END", pos))
            svlen_str = info_dict.get("SVLEN", None)
            if svlen_str is not None:
                try:
                    svlen = abs(int(svlen_str.split(",")[0]))
                except ValueError:
                    svlen = abs(end - pos)
            else:
                svlen = abs(end - pos)
                
            clnsig = info_dict.get("CLNSIG", label_cat)
            dbvar_id = info_dict.get("DBVARID", var_id)
            clnacc = info_dict.get("CLNACC", None)
            experiment = info_dict.get("EXPERIMENT", None)
            
            dbvar_rows.append({
                "dataset_file": label_cat,
                "chrom": chrom,
                "pos": pos,
                "end": end,
                "svtype": svtype,
                "svlen": svlen,
                "dbvar_id": dbvar_id,
                "clnsig": clnsig,
                "clnacc": clnacc,
                "experiment": experiment
            })

df_dbvar = pd.DataFrame(dbvar_rows)
print(f"Total dbVar records across 3 files: {len(df_dbvar)}")
print(df_dbvar["dataset_file"].value_counts().to_dict())

# Save metrics summary JSON
summary_stats = {
    "clinvar_total_records": line_num,
    "clinvar_sv_total": len(df_clinvar_sv),
    "clinvar_sv_grch38": len(df_clinvar_sv_grch38),
    "clinvar_sv_grch37": len(df_clinvar_sv_grch37),
    "gnomad_total_sv": len(df_gnomad),
    "dbvar_total_sv": len(df_dbvar),
    "dbvar_by_file": df_dbvar["dataset_file"].value_counts().to_dict()
}

with open("reports/summary_stats.json", "w") as f:
    json.dump(summary_stats, f, indent=2)

print("\n--- Summary saved to reports/summary_stats.json ---")
