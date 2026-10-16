"""
Comprehensive EDA Script & Visualizations Generator
===================================================
Project: AI-Based Structural Variant Prioritization from Long-Read Sequencing Using Explainable Machine Learning
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
sns.set_theme(style="whitegrid", palette="muted")

os.makedirs("reports/figures", exist_ok=True)
os.makedirs("eda/figures", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)

print("==================================================")
print("PHASE 1 & 2: CLINVAR STREAMING & PROFILING")
print("==================================================")

clinvar_sv_rows = []
all_clinvar_type_counts = {}
all_clinvar_clinsig_counts = {}
all_clinvar_assembly_counts = {}
total_clinvar_lines = 0

with gzip.open("raw/clinvar/variant_summary.txt.gz", "rt", encoding="utf-8", errors="replace") as f:
    header = f.readline().strip().split("\t")
    col_map = {col: i for i, col in enumerate(header)}
    
    for line in f:
        total_clinvar_lines += 1
        parts = line.strip().split("\t")
        if len(parts) < len(header):
            continue
        
        vtype = parts[col_map["Type"]]
        assembly = parts[col_map["Assembly"]]
        clinsig = parts[col_map["ClinicalSignificance"]]
        review = parts[col_map["ReviewStatus"]]
        chrom = parts[col_map["Chromosome"]]
        gene_sym = parts[col_map["GeneSymbol"]]
        gene_id = parts[col_map["GeneID"]]
        pheno_list = parts[col_map["PhenotypeList"]]
        dbvar_id = parts[col_map["nsv/esv (dbVar)"]]
        rs_id = parts[col_map["RS# (dbSNP)"]]
        num_submitters = parts[col_map["NumberSubmitters"]]
        origin = parts[col_map["OriginSimple"]]
        
        all_clinvar_type_counts[vtype] = all_clinvar_type_counts.get(vtype, 0) + 1
        all_clinvar_assembly_counts[assembly] = all_clinvar_assembly_counts.get(assembly, 0) + 1
        
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
        
        if (is_sv_length or is_sv_type) and length >= 50 and assembly in ["GRCh37", "GRCh38"]:
            clinvar_sv_rows.append({
                "allele_id": parts[col_map["#AlleleID"]],
                "variation_id": parts[col_map["VariationID"]],
                "name": parts[col_map["Name"]],
                "type": vtype,
                "gene_id": gene_id,
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
                "dbvar_id": dbvar_id if dbvar_id != "-" else None,
                "rs_id": rs_id if rs_id != "-1" else None,
                "origin": origin
            })

df_clinvar_sv = pd.DataFrame(clinvar_sv_rows)
print(f"Total ClinVar lines: {total_clinvar_lines:,}")
print(f"Total ClinVar SVs (length >= 50 bp): {len(df_clinvar_sv):,}")

# Save CSV of ClinVar SVs for notebooks
df_clinvar_sv.to_csv("data/processed/clinvar_sv_cleaned.csv.gz", index=False, compression="gzip")
print("Saved data/processed/clinvar_sv_cleaned.csv.gz")

print("\n==================================================")
print("PHASE 3: gnomAD SV STREAMING & PROFILING")
print("==================================================")

def parse_float_val(val_str):
    if val_str in ["NA", ".", "", None]:
        return np.nan
    if "," in val_str:
        # Take the maximum non-reference AF for multiallelic sites
        try:
            return max([float(x) for x in val_str.split(",") if x not in ["NA", "."]])
        except ValueError:
            return np.nan
    try:
        return float(val_str)
    except ValueError:
        return np.nan

gnomad_rows = []
gnomad_type_counts = {}

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
            svlen_raw = parts[g_map["SVLEN"]]
            if svlen_raw != "NA" and svlen_raw != "":
                svlen = abs(int(svlen_raw.split(",")[0]))
            else:
                svlen = abs(end - start)
        except (ValueError, IndexError):
            continue
            
        svtype = parts[g_map["svtype"]]
        gnomad_type_counts[svtype] = gnomad_type_counts.get(svtype, 0) + 1
        
        af = parse_float_val(parts[g_map["AF"]])
        popmax_af = parse_float_val(parts[g_map["POPMAX_AF"]])
        afr_af = parse_float_val(parts[g_map["AFR_AF"]])
        amr_af = parse_float_val(parts[g_map["AMR_AF"]])
        eas_af = parse_float_val(parts[g_map["EAS_AF"]])
        eur_af = parse_float_val(parts[g_map["EUR_AF"]])
        
        lof = parts[g_map["PROTEIN_CODING__LOF"]]
        dup_partial = parts[g_map["PROTEIN_CODING__DUP_PARTIAL"]]
        copy_gain = parts[g_map["PROTEIN_CODING__COPY_GAIN"]]
        intergenic = parts[g_map["PROTEIN_CODING__INTERGENIC"]]
        intronic = parts[g_map["PROTEIN_CODING__INTRONIC"]]
        promoter = parts[g_map["PROTEIN_CODING__PROMOTER"]]
        
        gnomad_rows.append({
            "name": name,
            "chrom": str(chrom),
            "start": start,
            "end": end,
            "svlen": svlen,
            "svtype": svtype,
            "af": af if not np.isnan(af) else 0.0,
            "popmax_af": popmax_af,
            "afr_af": afr_af if not np.isnan(afr_af) else 0.0,
            "amr_af": amr_af if not np.isnan(amr_af) else 0.0,
            "eas_af": eas_af if not np.isnan(eas_af) else 0.0,
            "eur_af": eur_af if not np.isnan(eur_af) else 0.0,
            "has_lof": 1 if lof not in ["NA", "", "False", "None"] else 0,
            "has_dup_partial": 1 if dup_partial not in ["NA", "", "False", "None"] else 0,
            "has_copy_gain": 1 if copy_gain not in ["NA", "", "False", "None"] else 0,
            "is_intergenic": 1 if intergenic not in ["NA", "", "False", "None"] else 0,
            "is_intronic": 1 if intronic not in ["NA", "", "False", "None"] else 0,
            "is_promoter": 1 if promoter not in ["NA", "", "False", "None"] else 0,
        })

df_gnomad = pd.DataFrame(gnomad_rows)
print(f"Total gnomAD SV records: {len(df_gnomad):,}")
df_gnomad.to_csv("data/processed/gnomad_sv_cleaned.csv.gz", index=False, compression="gzip")
print("Saved data/processed/gnomad_sv_cleaned.csv.gz")

print("\n==================================================")
print("PHASE 4: dbVar PROFILING")
print("==================================================")

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
            chrom = str(parts[0])
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
                "start": pos,
                "end": end,
                "svtype": svtype,
                "svlen": svlen,
                "dbvar_id": dbvar_id,
                "clnsig": clnsig,
                "clnacc": clnacc,
                "experiment": experiment
            })

df_dbvar = pd.DataFrame(dbvar_rows)
print(f"Total dbVar records: {len(df_dbvar):,}")
df_dbvar.to_csv("data/processed/dbvar_cleaned.csv.gz", index=False, compression="gzip")
print("Saved data/processed/dbvar_cleaned.csv.gz")

print("\n==================================================")
print("PHASE 5: DATASET COMPATIBILITY & OVERLAP ANALYSIS")
print("==================================================")

# Standardize ClinVar clinical labels into simplified categories
def categorize_clinsig(cln):
    c = str(cln).lower()
    if "pathogenic/likely pathogenic" in c:
        return "Pathogenic/Likely Pathogenic"
    elif "pathogenic" in c and "likely" not in c and "conflict" not in c:
        return "Pathogenic"
    elif "likely pathogenic" in c and "conflict" not in c:
        return "Likely Pathogenic"
    elif "benign/likely benign" in c:
        return "Benign/Likely Benign"
    elif "benign" in c and "likely" not in c and "conflict" not in c:
        return "Benign"
    elif "likely benign" in c and "conflict" not in c:
        return "Likely Benign"
    elif "uncertain" in c or "vus" in c:
        return "Uncertain Significance (VUS)"
    elif "conflicting" in c:
        return "Conflicting Interpretations"
    else:
        return "Other / Not Provided"

df_clinvar_sv["standard_label"] = df_clinvar_sv["clinsig"].apply(categorize_clinsig)

# Check overlap between ClinVar GRCh37 SVs and gnomAD v2.1 SVs (both GRCh37)
clinvar_37 = df_clinvar_sv[df_clinvar_sv["assembly"] == "GRCh37"].copy()
clinvar_38 = df_clinvar_sv[df_clinvar_sv["assembly"] == "GRCh38"].copy()

print(f"Testing Interval Matching: ClinVar GRCh37 ({len(clinvar_37):,}) vs gnomAD v2.1 ({len(df_gnomad):,})...")

# Group by chromosome for fast interval comparison
chrom_overlap_matches = []
gnomad_by_chr = {c: df_gnomad[df_gnomad["chrom"] == c] for c in df_gnomad["chrom"].unique()}

sample_test_37 = clinvar_37.sample(n=min(5000, len(clinvar_37)), random_state=42)
reciprocal_overlaps_70 = 0
reciprocal_overlaps_50 = 0
window_matches_100bp = 0

for _, c_row in sample_test_37.iterrows():
    c_chr = str(c_row["chrom"])
    c_start = c_row["start"]
    c_stop = c_row["stop"]
    c_len = c_row["length"]
    c_type = c_row["type"]
    
    if c_chr not in gnomad_by_chr:
        continue
    
    df_chr = gnomad_by_chr[c_chr]
    # Filter potential candidates within region
    cands = df_chr[(df_chr["start"] <= c_stop) & (df_chr["end"] >= c_start)]
    
    matched_50 = False
    matched_70 = False
    matched_win = False
    
    for _, g_row in cands.iterrows():
        g_start = g_row["start"]
        g_end = g_row["end"]
        g_len = g_row["svlen"]
        
        # Calculate overlap
        ov_start = max(c_start, g_start)
        ov_end = min(c_stop, g_end)
        ov_len = max(0, ov_end - ov_start)
        
        if ov_len > 0:
            recip = ov_len / max(c_len, g_len)
            if recip >= 0.50:
                matched_50 = True
            if recip >= 0.70:
                matched_70 = True
                
        if abs(c_start - g_start) <= 100 and abs(c_stop - g_end) <= 100:
            matched_win = True
            
    if matched_50:
        reciprocal_overlaps_50 += 1
    if matched_70:
        reciprocal_overlaps_70 += 1
    if matched_win:
        window_matches_100bp += 1

print(f"Empirical Overlap on 5,000 ClinVar SVs with gnomAD:")
print(f"  >= 50% Reciprocal Overlap: {reciprocal_overlaps_50} / {len(sample_test_37)} ({reciprocal_overlaps_50/len(sample_test_37)*100:.2f}%)")
print(f"  >= 70% Reciprocal Overlap: {reciprocal_overlaps_70} / {len(sample_test_37)} ({reciprocal_overlaps_70/len(sample_test_37)*100:.2f}%)")
print(f"  <= 100bp Window Match:     {window_matches_100bp} / {len(sample_test_37)} ({window_matches_100bp/len(sample_test_37)*100:.2f}%)")

# Check dbVar to ClinVar ID matching
clinvar_with_dbvar_id = df_clinvar_sv["dbvar_id"].dropna().unique()
dbvar_ids_in_dbvar = df_dbvar["dbvar_id"].unique()
common_dbvar_ids = set(clinvar_with_dbvar_id).intersection(set(dbvar_ids_in_dbvar))
print(f"\nClinVar records with dbVar accession: {len(clinvar_with_dbvar_id):,}")
print(f"dbVar IDs in downloaded dbVar VCFs: {len(dbvar_ids_in_dbvar):,}")
print(f"Exact ID intersection: {len(common_dbvar_ids):,}")

print("\n==================================================")
print("PHASE 6 & 10: STATISTICAL COMPARISONS")
print("==================================================")

# Filter for Binary Definition: Pathogenic vs Benign
df_pathogenic = df_clinvar_sv[df_clinvar_sv["standard_label"].isin(["Pathogenic", "Likely Pathogenic", "Pathogenic/Likely Pathogenic"])]
df_benign = df_clinvar_sv[df_clinvar_sv["standard_label"].isin(["Benign", "Likely Benign", "Benign/Likely Benign"])]
df_vus = df_clinvar_sv[df_clinvar_sv["standard_label"] == "Uncertain Significance (VUS)"]
df_conflict = df_clinvar_sv[df_clinvar_sv["standard_label"] == "Conflicting Interpretations"]

print(f"Pathogenic / Likely Pathogenic count: {len(df_pathogenic):,}")
print(f"Benign / Likely Benign count:         {len(df_benign):,}")
print(f"VUS count:                            {len(df_vus):,}")
print(f"Conflicting count:                    {len(df_conflict):,}")

# Mann-Whitney U test on SV Length (Pathogenic vs Benign)
path_lengths = df_pathogenic["length"].dropna()
benign_lengths = df_benign["length"].dropna()

mwu_stat, mwu_pval = stats.mannwhitneyu(path_lengths, benign_lengths, alternative='two-sided')
print(f"\n--- Statistical Test 1: SV Length (Mann-Whitney U) ---")
print(f"Pathogenic Median Length: {path_lengths.median():,.0f} bp (IQR: {path_lengths.quantile(0.25):,.0f} - {path_lengths.quantile(0.75):,.0f})")
print(f"Benign Median Length:     {benign_lengths.median():,.0f} bp (IQR: {benign_lengths.quantile(0.25):,.0f} - {benign_lengths.quantile(0.75):,.0f})")
print(f"MWU Statistic = {mwu_stat:.2e}, p-value = {mwu_pval:.4e}")

# Chi-Square test on SV Types
type_contingency = pd.crosstab(
    pd.concat([
        pd.Series(["Pathogenic"] * len(df_pathogenic), name="Class"),
        pd.Series(["Benign"] * len(df_benign), name="Class")
    ]),
    pd.concat([df_pathogenic["type"], df_benign["type"]])
)
chi2_stat, chi2_p, dof, ex = stats.chi2_contingency(type_contingency)
print(f"\n--- Statistical Test 2: SV Type Distribution (Chi-Square) ---")
print(type_contingency)
print(f"Chi2 = {chi2_stat:.2f}, dof = {dof}, p-value = {chi2_p:.4e}")

# gnomAD AF statistics
rare_count = (df_gnomad["af"] < 0.01).sum()
common_count = (df_gnomad["af"] >= 0.01).sum()
singleton_count = (df_gnomad["af"] <= 1.0 / (2 * 10847)).sum()

print(f"\n--- gnomAD SV Population Stats ---")
print(f"Total gnomAD SVs: {len(df_gnomad):,}")
print(f"Rare SVs (AF < 0.01): {rare_count:,} ({rare_count/len(df_gnomad)*100:.2f}%)")
print(f"Common SVs (AF >= 0.01): {common_count:,} ({common_count/len(df_gnomad)*100:.2f}%)")
print(f"Singletons (approx AF <= 1/(2*N)): {singleton_count:,} ({singleton_count/len(df_gnomad)*100:.2f}%)")

print("\n==================================================")
print("PHASE 9: GENERATING PUBLICATION-QUALITY FIGURES")
print("==================================================")

# 1. Clinical Label Distribution
plt.figure(figsize=(10, 5.5))
label_order = [
    "Pathogenic", "Likely Pathogenic", "Pathogenic/Likely Pathogenic",
    "Uncertain Significance (VUS)", "Conflicting Interpretations",
    "Likely Benign", "Benign", "Benign/Likely Benign", "Other / Not Provided"
]
clinsig_counts = df_clinvar_sv["standard_label"].value_counts().reindex(label_order).dropna()
colors = ['#d95f02', '#e78ac3', '#fc8d62', '#ffd92f', '#e5c494', '#a6d854', '#66c2a5', '#8da0cb', '#b3b3b3']
ax = clinsig_counts.plot(kind="barh", color=colors[:len(clinsig_counts)], edgecolor='black', alpha=0.85)
plt.title("ClinVar Structural Variants: Clinical Significance Label Distribution", fontweight='bold', pad=15)
plt.xlabel("Number of Structural Variants (Log Scale)", labelpad=10)
plt.xscale("log")
plt.ylabel("Clinical Significance Category", labelpad=10)
for p in ax.patches:
    val = int(p.get_width())
    ax.annotate(f" {val:,}", (p.get_width(), p.get_y() + p.get_height() / 2.),
                va='center', fontsize=9, fontweight='bold', color='#333333')
plt.tight_layout()
plt.savefig("reports/figures/01_clinical_label_distribution.png", dpi=300)
plt.savefig("eda/figures/01_clinical_label_distribution.png", dpi=300)
plt.close()

# 2. SV Type Distribution across ClinVar & gnomAD
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
cv_type_counts = df_clinvar_sv["type"].value_counts().head(8)
axes[0].barh(cv_type_counts.index[::-1], cv_type_counts.values[::-1], color='#386cb0', edgecolor='black', alpha=0.85)
axes[0].set_title("ClinVar SV Types", fontweight='bold')
axes[0].set_xlabel("Variant Count", labelpad=8)
for p in axes[0].patches:
    axes[0].annotate(f" {int(p.get_width()):,}", (p.get_width(), p.get_y() + p.get_height()/2.), va='center', fontsize=9)

gn_type_counts = df_gnomad["svtype"].value_counts().head(8)
axes[1].barh(gn_type_counts.index[::-1], gn_type_counts.values[::-1], color='#7fc97f', edgecolor='black', alpha=0.85)
axes[1].set_title("gnomAD SV Types (Population Baseline)", fontweight='bold')
axes[1].set_xlabel("Variant Count", labelpad=8)
for p in axes[1].patches:
    axes[1].annotate(f" {int(p.get_width()):,}", (p.get_width(), p.get_y() + p.get_height()/2.), va='center', fontsize=9)
plt.suptitle("Structural Variant Type Distribution in ClinVar vs gnomAD", fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig("reports/figures/02_sv_type_distribution.png", dpi=300)
plt.savefig("eda/figures/02_sv_type_distribution.png", dpi=300)
plt.close()

# 3. SV Length Distribution (ClinVar vs gnomAD)
plt.figure(figsize=(10, 5.5))
sns.kdeplot(np.log10(df_clinvar_sv["length"].clip(lower=50)), label="ClinVar SVs (Clinical)", color='#d95f02', fill=True, alpha=0.35, linewidth=2)
sns.kdeplot(np.log10(df_gnomad["svlen"].clip(lower=50)), label="gnomAD SVs (Population)", color='#2b83ba', fill=True, alpha=0.35, linewidth=2)
plt.title("SV Length Distribution (Log10 Base Pairs)", fontweight='bold', pad=15)
plt.xlabel("Log10 Length (bp) [2=100bp, 3=1kb, 4=10kb, 5=100kb, 6=1Mb, 7=10Mb]", labelpad=10)
plt.ylabel("Density", labelpad=10)
plt.legend(frameon=True)
plt.tight_layout()
plt.savefig("reports/figures/03_sv_length_distribution.png", dpi=300)
plt.savefig("eda/figures/03_sv_length_distribution.png", dpi=300)
plt.close()

# 4. Allele Frequency Distribution in gnomAD (Linear & Log-Scaled)
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].hist(df_gnomad["af"], bins=50, color='#6baed6', edgecolor='black', alpha=0.85)
axes[0].set_title("gnomAD Global Allele Frequency (Linear Scale)", fontweight='bold')
axes[0].set_xlabel("Allele Frequency (AF)", labelpad=8)
axes[0].set_ylabel("Count", labelpad=8)

non_zero_af = df_gnomad[df_gnomad["af"] > 0]["af"]
axes[1].hist(np.log10(non_zero_af), bins=50, color='#fd8d3c', edgecolor='black', alpha=0.85)
axes[1].set_title("gnomAD Global Allele Frequency (Log10 Scale)", fontweight='bold')
axes[1].set_xlabel("Log10(Allele Frequency) [-4=0.01%, -2=1%, 0=100%]", labelpad=8)
axes[1].set_ylabel("Count", labelpad=8)
plt.suptitle("gnomAD Structural Variant Allele Frequency Distribution", fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig("reports/figures/04_allele_frequency_distribution.png", dpi=300)
plt.savefig("eda/figures/04_allele_frequency_distribution.png", dpi=300)
plt.close()

# 5. SV Length by SV Type (Violin/Boxplot)
plt.figure(figsize=(11, 5.5))
top_types = df_clinvar_sv["type"].value_counts().head(5).index
df_top_cv = df_clinvar_sv[df_clinvar_sv["type"].isin(top_types)].copy()
df_top_cv["log_length"] = np.log10(df_top_cv["length"])
sns.boxplot(data=df_top_cv, x="type", y="log_length", palette="Set2", showmeans=True,
            meanprops={"marker":"o", "markerfacecolor":"red", "markeredgecolor":"black"})
plt.title("ClinVar SV Length Distribution Across Major Variant Types", fontweight='bold', pad=15)
plt.xlabel("Structural Variant Type", labelpad=10)
plt.ylabel("Log10(Length in bp)", labelpad=10)
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig("reports/figures/05_sv_length_by_sv_type.png", dpi=300)
plt.savefig("eda/figures/05_sv_length_by_sv_type.png", dpi=300)
plt.close()

# 6. SV Length by Clinical Pathogenicity Class
plt.figure(figsize=(9, 5.5))
df_class_comp = df_clinvar_sv[df_clinvar_sv["standard_label"].isin([
    "Pathogenic", "Likely Pathogenic", "Uncertain Significance (VUS)", "Likely Benign", "Benign"
])].copy()
df_class_comp["log_length"] = np.log10(df_class_comp["length"])
class_order = ["Pathogenic", "Likely Pathogenic", "Uncertain Significance (VUS)", "Likely Benign", "Benign"]
sns.boxplot(data=df_class_comp, x="standard_label", y="log_length", order=class_order, palette="Spectral",
            showmeans=True, meanprops={"marker":"D", "markerfacecolor":"black", "markeredgecolor":"white"})
plt.title("SV Length Distribution Across Clinical Significance Classes", fontweight='bold', pad=15)
plt.xlabel("Clinical Classification", labelpad=10)
plt.ylabel("Log10(Length in bp)", labelpad=10)
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig("reports/figures/06_sv_length_by_clinical_class.png", dpi=300)
plt.savefig("eda/figures/06_sv_length_by_clinical_class.png", dpi=300)
plt.close()

# 7. Chromosomal Distribution (ClinVar vs gnomAD)
plt.figure(figsize=(13, 5))
valid_chroms = [str(i) for i in range(1, 23)] + ["X", "Y"]
cv_chrom_counts = df_clinvar_sv[df_clinvar_sv["chrom"].isin(valid_chroms)]["chrom"].value_counts().reindex(valid_chroms)
gn_chrom_counts = df_gnomad[df_gnomad["chrom"].isin(valid_chroms)]["chrom"].value_counts().reindex(valid_chroms)

x = np.arange(len(valid_chroms))
width = 0.38
plt.bar(x - width/2, cv_chrom_counts, width, label="ClinVar SVs", color="#e41a1c", edgecolor='black', alpha=0.8)
plt.bar(x + width/2, gn_chrom_counts, width, label="gnomAD SVs", color="#377eb8", edgecolor='black', alpha=0.8)
plt.xticks(x, valid_chroms)
plt.title("Structural Variant Density Across Human Chromosomes", fontweight='bold', pad=15)
plt.xlabel("Chromosome", labelpad=10)
plt.ylabel("Number of SVs", labelpad=10)
plt.legend(frameon=True)
plt.tight_layout()
plt.savefig("reports/figures/07_chromosomal_distribution.png", dpi=300)
plt.savefig("eda/figures/07_chromosomal_distribution.png", dpi=300)
plt.close()

# 8. Missing Value Matrix for Key Candidate Features
plt.figure(figsize=(10, 5))
missingness = {
    "GeneSymbol": (df_clinvar_sv["gene_symbol"] == "-").mean() * 100,
    "Phenotypes": (df_clinvar_sv["phenotypes"].isin(["-", "not specified", "not provided"])).mean() * 100,
    "ReviewStatus": (df_clinvar_sv["review_status"] == "").mean() * 100,
    "dbVar Accession": df_clinvar_sv["dbvar_id"].isna().mean() * 100,
    "dbSNP RS#": df_clinvar_sv["rs_id"].isna().mean() * 100,
    "gnomAD POPMAX_AF": df_gnomad["popmax_af"].isna().mean() * 100,
    "gnomAD LoF Annotation": (df_gnomad["has_lof"] == 0).mean() * 100,
    "dbVar Clinical Source": (df_dbvar["clnacc"].isna()).mean() * 100
}
miss_df = pd.Series(missingness).sort_values(ascending=True)
ax = miss_df.plot(kind="barh", color="#bc80bd", edgecolor='black', alpha=0.85)
plt.title("Missing Value / Unannotated Percentages Across Datasets", fontweight='bold', pad=15)
plt.xlabel("Percentage Missing / Unannotated (%)", labelpad=10)
for p in ax.patches:
    ax.annotate(f" {p.get_width():.1f}%", (p.get_width(), p.get_y() + p.get_height()/2.), va='center', fontsize=9)
plt.tight_layout()
plt.savefig("reports/figures/08_missing_values.png", dpi=300)
plt.savefig("eda/figures/08_missing_values.png", dpi=300)
plt.close()

# 9. Rare vs Common SV Proportions in Population
plt.figure(figsize=(6.5, 6.5))
af_bins = [
    (df_gnomad["af"] < 0.0001).sum(),
    ((df_gnomad["af"] >= 0.0001) & (df_gnomad["af"] < 0.001)).sum(),
    ((df_gnomad["af"] >= 0.001) & (df_gnomad["af"] < 0.01)).sum(),
    ((df_gnomad["af"] >= 0.01) & (df_gnomad["af"] < 0.05)).sum(),
    (df_gnomad["af"] >= 0.05).sum()
]
af_labels = [
    "Ultra-Rare (AF < 0.01%)\nSingletons",
    "Rare (0.01% <= AF < 0.1%)",
    "Low Frequency (0.1% <= AF < 1%)",
    "Moderate (1% <= AF < 5%)",
    "Common (AF >= 5%)"
]
colors_pie = ['#b2182b', '#ef8a62', '#fddbc7', '#d1e5f0', '#2166ac']
plt.pie(af_bins, labels=af_labels, autopct='%1.1f%%', colors=colors_pie, startangle=140,
        wedgeprops=dict(edgecolor='black', linewidth=1))
plt.title("gnomAD Population SV Frequency Spectrum\n(10,847 Genomes)", fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig("reports/figures/09_rare_vs_common_proportions.png", dpi=300)
plt.savefig("eda/figures/09_rare_vs_common_proportions.png", dpi=300)
plt.close()

# 10. Functional Impact vs Population AF in gnomAD
plt.figure(figsize=(10, 5))
func_categories = {
    "Loss-of-Function (LoF)": df_gnomad[df_gnomad["has_lof"] == 1]["af"],
    "Promoter Overlap": df_gnomad[df_gnomad["is_promoter"] == 1]["af"],
    "Duplication Partial": df_gnomad[df_gnomad["has_dup_partial"] == 1]["af"],
    "Intronic": df_gnomad[df_gnomad["is_intronic"] == 1]["af"],
    "Intergenic": df_gnomad[df_gnomad["is_intergenic"] == 1]["af"]
}
func_medians = {k: np.median(v[v > 0]) for k, v in func_categories.items() if len(v[v > 0]) > 0}
func_df = pd.DataFrame([
    {"Annotation": k, "Median_AF": np.median(v), "Mean_AF": np.mean(v), "Count": len(v), "Fraction_Ultra_Rare": (v < 0.001).mean()}
    for k, v in func_categories.items()
])
ax = sns.barplot(data=func_df, x="Annotation", y="Fraction_Ultra_Rare", palette="viridis", edgecolor='black', alpha=0.85)
plt.title("Proportion of Ultra-Rare SVs (AF < 0.1%) by Genomic Functional Impact", fontweight='bold', pad=15)
plt.xlabel("Functional Annotation Category", labelpad=10)
plt.ylabel("Fraction with AF < 0.1%", labelpad=10)
plt.ylim(0, 1.05)
for p in ax.patches:
    ax.annotate(f" {p.get_height()*100:.1f}%", (p.get_x() + p.get_width()/2., p.get_height() + 0.02),
                ha='center', fontsize=9, fontweight='bold')
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig("reports/figures/10_functional_impact_rarity.png", dpi=300)
plt.savefig("eda/figures/10_functional_impact_rarity.png", dpi=300)
plt.close()

print("\nAll 10 figures generated and saved successfully to reports/figures/ and eda/figures/.")

# Save detailed metrics to JSON
detailed_metrics = {
    "clinvar": {
        "total_lines": total_clinvar_lines,
        "total_sv_ge_50bp": len(df_clinvar_sv),
        "grch38_count": len(clinvar_38),
        "grch37_count": len(clinvar_37),
        "label_counts": df_clinvar_sv["standard_label"].value_counts().to_dict(),
        "type_counts": df_clinvar_sv["type"].value_counts().to_dict(),
        "median_length_pathogenic": float(path_lengths.median()),
        "median_length_benign": float(benign_lengths.median()),
        "iqr_pathogenic": [float(path_lengths.quantile(0.25)), float(path_lengths.quantile(0.75))],
        "iqr_benign": [float(benign_lengths.quantile(0.25)), float(benign_lengths.quantile(0.75))],
        "mwu_pvalue": float(mwu_pval),
        "mwu_stat": float(mwu_stat),
        "chi2_pvalue": float(chi2_p),
        "chi2_stat": float(chi2_stat)
    },
    "gnomad": {
        "total_sv": len(df_gnomad),
        "rare_count_lt_001": int(rare_count),
        "common_count_ge_001": int(common_count),
        "singleton_count": int(singleton_count),
        "type_counts": df_gnomad["svtype"].value_counts().to_dict(),
        "af_percentiles": {
            "p25": float(df_gnomad["af"].quantile(0.25)),
            "p50": float(df_gnomad["af"].quantile(0.50)),
            "p75": float(df_gnomad["af"].quantile(0.75)),
            "p95": float(df_gnomad["af"].quantile(0.95)),
            "p99": float(df_gnomad["af"].quantile(0.99))
        }
    },
    "dbvar": {
        "total_sv": len(df_dbvar),
        "file_counts": df_dbvar["dataset_file"].value_counts().to_dict(),
        "shared_ids_with_clinvar": len(common_dbvar_ids)
    },
    "overlap_simulation": {
        "sample_size": len(sample_test_37),
        "reciprocal_70_pct": float(reciprocal_overlaps_70 / len(sample_test_37) * 100),
        "reciprocal_50_pct": float(reciprocal_overlaps_50 / len(sample_test_37) * 100),
        "window_100bp_pct": float(window_matches_100bp / len(sample_test_37) * 100)
    }
}

with open("reports/detailed_metrics.json", "w") as f:
    json.dump(detailed_metrics, f, indent=2)

print("Saved detailed metrics to reports/detailed_metrics.json")
