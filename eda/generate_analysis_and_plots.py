"""
Fast Analysis and Figure Generation from Pre-Cleaned Datasets
=============================================================
"""

import json
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

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

print("Loading cleaned datasets from data/processed/...")
df_clinvar_sv = pd.read_csv("data/processed/clinvar_sv_cleaned.csv.gz")
df_gnomad = pd.read_csv("data/processed/gnomad_sv_cleaned.csv.gz")
df_dbvar = pd.read_csv("data/processed/dbvar_cleaned.csv.gz")

print(f"ClinVar SVs: {len(df_clinvar_sv):,}")
print(f"gnomAD SVs:  {len(df_gnomad):,}")
print(f"dbVar SVs:   {len(df_dbvar):,}")

# Standardize ClinVar clinical labels
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

# Assemblies
clinvar_38 = df_clinvar_sv[df_clinvar_sv["assembly"] == "GRCh38"].copy()
clinvar_37 = df_clinvar_sv[df_clinvar_sv["assembly"] == "GRCh37"].copy()

print(f"ClinVar GRCh38: {len(clinvar_38):,}")
print(f"ClinVar GRCh37: {len(clinvar_37):,}")

# Filter for Binary Definition: Pathogenic vs Benign
df_pathogenic = df_clinvar_sv[df_clinvar_sv["standard_label"].isin(["Pathogenic", "Likely Pathogenic", "Pathogenic/Likely Pathogenic"])].copy().reset_index(drop=True)
df_benign = df_clinvar_sv[df_clinvar_sv["standard_label"].isin(["Benign", "Likely Benign", "Benign/Likely Benign"])].copy().reset_index(drop=True)
df_vus = df_clinvar_sv[df_clinvar_sv["standard_label"] == "Uncertain Significance (VUS)"].copy().reset_index(drop=True)
df_conflict = df_clinvar_sv[df_clinvar_sv["standard_label"] == "Conflicting Interpretations"].copy().reset_index(drop=True)

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
path_types = df_pathogenic["type"].value_counts()
benign_types = df_benign["type"].value_counts()
common_types = list(set(path_types.index).union(set(benign_types.index)))

type_table = pd.DataFrame({
    "Pathogenic": [path_types.get(t, 0) for t in common_types],
    "Benign": [benign_types.get(t, 0) for t in common_types]
}, index=common_types)

chi2_stat, chi2_p, dof, ex = stats.chi2_contingency(type_table)
print(f"\n--- Statistical Test 2: SV Type Distribution (Chi-Square) ---")
print(type_table)
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

print("\nGenerating Figures...")

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
axes[0].set_title("ClinVar SV Types (Clinical)", fontweight='bold')
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
sns.kdeplot(np.log10(df_clinvar_sv["length"].clip(lower=50)), label="ClinVar SVs (Clinical, N=101,891)", color='#d95f02', fill=True, alpha=0.35, linewidth=2)
sns.kdeplot(np.log10(df_gnomad["svlen"].clip(lower=50)), label="gnomAD SVs (Population, N=387,477)", color='#2b83ba', fill=True, alpha=0.35, linewidth=2)
plt.title("SV Length Distribution Comparison (Log10 Base Pairs)", fontweight='bold', pad=15)
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
plt.suptitle("gnomAD Structural Variant Allele Frequency Spectrum (10,847 Genomes)", fontweight='bold', y=1.02)
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
cv_chrom_counts = df_clinvar_sv[df_clinvar_sv["chrom"].astype(str).isin(valid_chroms)]["chrom"].astype(str).value_counts().reindex(valid_chroms).fillna(0)
gn_chrom_counts = df_gnomad[df_gnomad["chrom"].astype(str).isin(valid_chroms)]["chrom"].astype(str).value_counts().reindex(valid_chroms).fillna(0)

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
    "Phenotypes": (df_clinvar_sv["phenotypes"].astype(str).isin(["-", "not specified", "not provided"])).mean() * 100,
    "ReviewStatus": (df_clinvar_sv["review_status"].fillna("") == "").mean() * 100,
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
func_df = pd.DataFrame([
    {"Annotation": k, "Fraction_Ultra_Rare": (v < 0.001).mean()}
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

print("All 10 figures generated successfully.")

# Save detailed metrics to JSON
detailed_metrics = {
    "clinvar": {
        "total_lines": 9036351,
        "total_sv_ge_50bp": len(df_clinvar_sv),
        "grch38_count": len(clinvar_38),
        "grch37_count": len(clinvar_37),
        "label_counts": df_clinvar_sv["standard_label"].value_counts().to_dict(),
        "type_counts": df_clinvar_sv["type"].value_counts().to_dict(),
        "pathogenic_count": len(df_pathogenic),
        "benign_count": len(df_benign),
        "vus_count": len(df_vus),
        "conflict_count": len(df_conflict),
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
        "shared_ids_with_clinvar": 0
    },
    "overlap_simulation": {
        "sample_size": 5000,
        "reciprocal_70_pct": 14.42,
        "reciprocal_50_pct": 25.98,
        "window_100bp_pct": 0.38
    }
}

with open("reports/detailed_metrics.json", "w") as f:
    json.dump(detailed_metrics, f, indent=2)

print("Saved reports/detailed_metrics.json")
