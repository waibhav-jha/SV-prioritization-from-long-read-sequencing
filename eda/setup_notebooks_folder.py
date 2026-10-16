"""
Build all 9 notebooks, place them in notebooks/ and notebook/ folders,
and pre-execute all 9 notebooks with complete rendered outputs.
"""

import os
import shutil
import nbformat as nbf
from nbclient import NotebookClient

# Create target directories
os.makedirs("notebooks", exist_ok=True)
os.makedirs("notebook", exist_ok=True)

path_helper = """import os
import sys

# Ensure repository root is in sys.path so 'src' can be imported regardless of execution working directory
for root_candidate in [os.path.abspath("."), os.path.abspath("..")]:
    if os.path.isdir(os.path.join(root_candidate, "src")) and root_candidate not in sys.path:
        sys.path.insert(0, root_candidate)

def resolve_path(p):
    for candidate in [p, os.path.join("..", p), os.path.join("data", p), os.path.join("..", "data", p)]:
        if os.path.exists(candidate):
            return candidate
    return p
"""

# -------------------------------------------------------------
# Notebook 09: Patient VCF Prioritization Pipeline
# -------------------------------------------------------------
nb9 = nbf.v4.new_notebook()
nb9.cells = [
    nbf.v4.new_markdown_cell("""# 09 - End-to-End Long-Read Patient VCF Prioritization Pipeline
**Project**: AI-Based Structural Variant Prioritization from Long-Read Sequencing Using Explainable Machine Learning  
**Author**: Data Science & Genomics Team  
**Date**: August 2026

## Objective
Demonstrate the end-to-end clinical prioritization of structural variants directly from a raw long-read sequencing VCF file (**Sniffles2**, **cuteSV**, **PBSV**, or **Nanomonsv**):
1. **Ingest & Parse** long-read VCF calls.
2. **On-the-fly Genomic Feature Annotation** (gnomAD population frequencies & gene constraint).
3. **Calibrated ML Scoring & 4-Tier ACMG Risk Classification**.
4. **Interactive Ranked Variant Table**.
5. **Local TreeSHAP Waterfall Decision Explanations** for top candidates.
6. **Multi-Format Clinical Export** (HTML Report, Ranked CSV, Annotated VCF).
"""),
    nbf.v4.new_code_cell(path_helper + """
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import shap

from src.vcf_parser import LongReadVCFParser
from src.fast_annotator import FastSVAnnotator
from src.predictor import SVPredictor
from src.visualizer import SHAPVisualizer
from src.reporter import ClinicalReporter

sns.set_theme(style="whitegrid")
plt.rcParams['font.size'] = 11

# Path to input patient Long-Read VCF
vcf_input_path = resolve_path("examples/sample_patient_longread.vcf")
sample_id = "Patient_HG002_LongRead"

print(f"Target Patient VCF: {vcf_input_path}")
print(f"Sample Identifier:  {sample_id}")
"""),
    nbf.v4.new_markdown_cell("""## 1. Ingest & Parse Long-Read Sequencing VCF"""),
    nbf.v4.new_code_cell("""parser = LongReadVCFParser(vcf_input_path)
df_raw = parser.parse()

print(f"Successfully ingested {len(df_raw)} structural variants (>= 50 bp):")
df_raw[["var_id", "chrom", "start", "stop", "length", "raw_svtype", "support"]]
"""),
    nbf.v4.new_markdown_cell("""## 2. On-the-Fly Population & Constraint Feature Annotation"""),
    nbf.v4.new_code_cell("""annotator = FastSVAnnotator()
df_annotated = annotator.annotate(df_raw)

print(f"Annotated {len(df_annotated)} variants with population frequencies & gene models:")
df_annotated[["var_id", "raw_svtype", "length", "gene_count", "gnomad_af", "gnomad_popmax_af", "is_deletion"]]
"""),
    nbf.v4.new_markdown_cell("""## 3. Run Calibrated ML Pathogenicity Model & Risk Tiering"""),
    nbf.v4.new_code_cell("""predictor = SVPredictor()
df_prioritized = predictor.predict(df_annotated)

print("Triage Breakdown by Clinical Priority Tier:")
print(df_prioritized["priority_tier"].value_counts())
"""),
    nbf.v4.new_markdown_cell("""## 4. Interactive Ranked Patient Variant Queue"""),
    nbf.v4.new_code_cell("""display_cols = [
    "var_id", "chrom", "start", "stop", "raw_svtype", "length",
    "gene_count", "gnomad_af", "pathogenicity_score", "priority_tier", "clinical_recommendation"
]
df_prioritized[display_cols]
"""),
    nbf.v4.new_markdown_cell("""## 5. Local TreeSHAP Waterfall Decision Plots for Top Candidates"""),
    nbf.v4.new_code_cell("""visualizer = SHAPVisualizer()

# Generate and display waterfall plots for top candidate variants
top_k = min(3, len(df_prioritized))
for rank in range(top_k):
    row = df_prioritized.iloc[rank]
    var_id = row['var_id']
    score = row['pathogenicity_score']
    tier = row['priority_tier']
    
    print(f"\\nCandidate #{rank+1}: {var_id} | Pathogenicity Score: {score:.4f} | {tier}")
    
    feat_dict = {col: float(row.get(col, 0.0)) for col in visualizer.feature_cols}
    X_single = pd.DataFrame([feat_dict])
    shap_vals = visualizer.explainer(X_single)[0]
    
    plt.figure(figsize=(9, 4.5))
    shap.plots.waterfall(shap_vals, max_display=9, show=True)
"""),
    nbf.v4.new_markdown_cell("""## 6. Generate Clinical Reports (HTML, CSV, Annotated VCF)"""),
    nbf.v4.new_code_cell("""shap_images_b64 = []
for rank in range(min(4, len(df_prioritized))):
    shap_images_b64.append(visualizer.generate_waterfall(df_prioritized.iloc[rank]))

out_dir = resolve_path("reports/sample_patient_report")
os.makedirs(out_dir, exist_ok=True)

reporter = ClinicalReporter(df_prioritized, sample_name=sample_id, top_shap_images=shap_images_b64)

html_path = os.path.join(out_dir, "clinical_report.html")
csv_path = os.path.join(out_dir, "ranked_variants.csv")
vcf_path = os.path.join(out_dir, f"{sample_id}.prioritized.vcf")

reporter.generate_html_report(html_path)
reporter.save_csv(csv_path)
reporter.save_annotated_vcf(vcf_input_path, vcf_path)

print(f"\\nAll clinical deliverables exported successfully to: {out_dir}")
""")
]

# Write nb9 to eda and execute
with open("eda/09_patient_vcf_prioritization_pipeline.ipynb", "w", encoding="utf-8") as f:
    nbf.write(nb9, f)

# Copy all notebooks 01-09 into notebooks/ and notebook/
for nb_file in os.listdir("eda"):
    if nb_file.endswith(".ipynb"):
        src = os.path.join("eda", nb_file)
        shutil.copy2(src, os.path.join("notebooks", nb_file))
        shutil.copy2(src, os.path.join("notebook", nb_file))

print("Copied all notebooks into notebooks/ and notebook/.")

# Execute all 9 notebooks in notebooks/
for i in range(1, 10):
    nb_filename = next((f for f in os.listdir("notebooks") if f.startswith(f"0{i}_") and f.endswith(".ipynb")), None)
    if nb_filename:
        nb_path = os.path.join("notebooks", nb_filename)
        print(f"Pre-executing {nb_path}...")
        with open(nb_path, "r", encoding="utf-8") as f:
            nb = nbf.read(f, as_version=4)
        client = NotebookClient(nb, timeout=600, kernel_name="python3")
        client.execute()
        with open(nb_path, "w", encoding="utf-8") as f:
            nbf.write(nb, f)
        # Mirror to notebook/ as well
        shutil.copy2(nb_path, os.path.join("notebook", nb_filename))
        print(f"Rendered: {nb_filename}")

print("\nAll 9 notebooks created, pre-rendered, and stored in notebooks/ and notebook/!")
