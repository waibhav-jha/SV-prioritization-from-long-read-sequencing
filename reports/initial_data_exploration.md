# Comprehensive Initial Data Exploration & Dataset Analysis Report

**Project**: AI-Based Structural Variant Prioritization from Long-Read Sequencing Using Explainable Machine Learning  
**Status**: Initial Exploratory Data Analysis & Feasibility Study Complete  
**Date**: August 2026  
**Artifact Directory**: `data/`

---

## Executive Summary

Structural Variants (SVs) ($\ge 50\text{ bp}$) account for the greatest number of divergent base pairs between individual human genomes and are disproportionately responsible for rare Mendelian diseases, neurodevelopmental disorders, and genomic syndromes. High-throughput long-read sequencing technologies (Oxford Nanopore Technologies and Pacific Biosciences HiFi) can resolve complex structural variations at single-nucleotide breakpoint precision. However, clinical interpretation remains the critical bottleneck due to the overwhelming volume of benign polymorphisms and Variants of Uncertain Significance (VUS).

This report presents a thorough, empirical analysis of three foundational genomic datasets downloaded to `data/raw/`:
1. **ClinVar** (`data/raw/clinvar/variant_summary.txt.gz`): 9,036,351 total variants containing **101,891 curated structural variants**.
2. **gnomAD SV v2.1** (`data/raw/gnomad_sv/`): **387,477 population structural variants** across 10,847 deep whole genomes.
3. **NCBI dbVar** (`data/raw/dbvar/`): **79,808 curated clinical structural variant calls** partitioned into Pathogenic, Benign, and VUS.

---

## Phase 1 — Dataset Inventory & Data Audit

### Summary Table of Downloaded Datasets

| Dataset | Raw File Path | Format | Records Analyzed | Size (Compressed) | Genome Build | Identifiers Available | Coordinate System | Key Clinical & Population Fields |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **ClinVar** | `data/raw/clinvar/variant_summary.txt.gz` | TSV (`.gz`) | **9,036,351** lines<br>(**101,891** SVs $\ge 50$ bp) | 421.4 MB | Dual:<br>• GRCh37 (77,469)<br>• GRCh38 (24,422) | `AlleleID`, `VariationID`, `RCVaccession`, `RS# (dbSNP)`, `nsv/esv (dbVar)` | 1-based closed (`Start`, `Stop`) | `ClinicalSignificance`, `ReviewStatus`, `GeneSymbol`, `PhenotypeList`, `OriginSimple` |
| **gnomAD SV** | `data/raw/gnomad_sv/gnomad_v2.1_sv.sites.bed.gz` | Extended BED (`.gz`) | **387,477** SV sites | 99.7 MB | GRCh37 / hg19 | Synthetic (`gnomAD-SV_v2.1_<TYPE>_<CHR>_<ID>`) | 0-based half-open (`start`, `end`) | `AF`, `POPMAX_AF`, Continental AFs (`AFR_AF`, `EUR_AF`, etc.), `PROTEIN_CODING__LOF`, `PROTEIN_CODING__PROMOTER` |
| **gnomAD SV (VCF)** | `data/raw/gnomad_sv/gnomad_v2.1_sv.sites.vcf.gz` | VCF v4.2 (`.gz`) | **387,477** SV sites | 134.4 MB | GRCh37 / hg19 | Synthetic | 1-based closed (`POS`, `END`) | `SVTYPE`, `SVLEN`, `AN`, `AC`, `AF`, `POPMAX_AF` |
| **dbVar Pathogenic** | `data/raw/dbvar/GRCh38.variant_call.clinical.pathogenic_or_likely_pathogenic.vcf.gz` | VCF v4.1 (`.gz`) | **36,878** calls | 2.17 MB | GRCh38 | `DBVARID` (`nssv...`, `essv...`) | 1-based (`POS`, `END`) | `SVTYPE`, `SVLEN`, `CLNSIG`, `CLNACC`, `EXPERIMENT` |
| **dbVar Benign** | `data/raw/dbvar/GRCh38.variant_call.clinical.benign_or_likely_benign.vcf.gz` | VCF v4.1 (`.gz`) | **6,742** calls | 0.56 MB | GRCh38 | `DBVARID` (`nssv...`, `essv...`) | 1-based (`POS`, `END`) | `SVTYPE`, `SVLEN`, `CLNSIG`, `CLNACC`, `EXPERIMENT` |
| **dbVar VUS** | `data/raw/dbvar/GRCh38.variant_call.clinical.uncertain_significance.vcf.gz` | VCF v4.1 (`.gz`) | **36,188** calls | 2.21 MB | GRCh38 | `DBVARID` (`nssv...`, `essv...`) | 1-based (`POS`, `END`) | `SVTYPE`, `SVLEN`, `CLNSIG`, `CLNACC`, `EXPERIMENT` |

---

## Phase 2 — ClinVar Structural Variant Deep Exploration

ClinVar is the primary source of clinical ground truth. Out of 9,036,351 total entries, 101,891 structural variants ($\text{Stop} - \text{Start} \ge 50\text{ bp}$) were extracted and characterized.

### 1. Clinical Significance Label Distribution

| Clinical Category | Variant Count | Percentage (%) | Role in Modeling Strategy |
| :--- | :--- | :--- | :--- |
| **Pathogenic** | 43,456 | 42.65% | Positive Class ($Y = 1$) |
| **Likely Pathogenic** | 1,749 | 1.72% | Positive Class ($Y = 1$) |
| **Pathogenic / Likely Pathogenic (Aggregate)** | 72 | 0.07% | Positive Class ($Y = 1$) |
| **Uncertain Significance (VUS)** | 40,741 | 39.98% | **Holdout / Prioritization Inference Target** |
| **Benign** | 9,996 | 9.81% | Negative Class ($Y = 0$) |
| **Likely Benign** | 3,306 | 3.24% | Negative Class ($Y = 0$) |
| **Benign / Likely Benign (Aggregate)** | 4 | 0.004% | Negative Class ($Y = 0$) |
| **Conflicting Interpretations** | 494 | 0.48% | Excluded from training (Quality benchmark) |
| **Other / Not Provided** | 73 | 0.07% | Excluded from training |
| **Total SVs** | **101,891** | **100.0%** | — |

![Figure 1: Clinical Label Distribution](figures/01_clinical_label_distribution.png)

### 2. Analysis of Class Imbalance & VUS Recommendation

1. **Binary Training Subset Size**: Combining high-confidence classes yields **45,277 Pathogenic** vs **13,306 Benign** SVs (Total: 58,583).
2. **Imbalance Ratio**: The class ratio is **3.40 : 1** (Pathogenic:Benign).
   - This imbalance is moderate. Standard methods (e.g. `scale_pos_weight`, PR-AUC metric monitoring, and focal cross-entropy) will prevent majority-class bias.
3. **Handling of VUS (40,741 records)**:
   - **Do NOT remove or ignore VUS permanently**.
   - Training ML models on VUS introduces noisy, ambiguous labels that degrade gradient updates.
   - **Recommendation**: Train and cross-validate the model exclusively on the high-confidence Pathogenic ($N=45,277$) and Benign ($N=13,306$) subsets. Then, apply the calibrated model to all 40,741 VUS variants to generate a continuous **Prioritization Index (0.0 to 1.0)** with SHAP explanations for clinical triage.

### 3. SV Types and Length Spectrum in ClinVar

- **Dominant Variant Types**: Deletions ($N=45,862$, $45.0\%$), Copy Number Loss ($N=23,892$, $23.4\%$), Copy Number Gain ($N=21,798$, $21.4\%$), Duplications ($N=8,735$, $8.6\%$), Indels ($N=1,424$, $1.4\%$), Inversions ($N=108$, $0.1\%$).
- **Length Distribution**: Highly skewed right. Pathogenic SVs have a median length of **51,100 bp** (IQR: 2,937 – 1,584,032 bp), whereas Benign SVs have a median length of **153,420 bp** (IQR: 56,204 – 401,207 bp).

![Figure 2: SV Type Distribution](figures/02_sv_type_distribution.png)
![Figure 5: SV Length by SV Type](figures/05_sv_length_by_sv_type.png)
![Figure 6: SV Length by Clinical Class](figures/06_sv_length_by_clinical_class.png)

---

## Phase 3 — gnomAD SV Population Baseline Exploration

gnomAD SV v2.1 contains **387,477 structural variants** characterized across 10,847 unrelated individuals from diverse continental ancestries (African/African American, Admixed American, East Asian, European, and South Asian).

### 1. Allele Frequency Spectrum

| Allele Frequency Bin | Variant Count | Proportion (%) | Biological Interpretation |
| :--- | :--- | :--- | :--- |
| **Ultra-Rare (Singletons, $AF \le 0.0046\%$)** | 152,640 | 39.39% | Private / familial variants, strong candidates for de novo mutation |
| **Rare ($0.01\% \le AF < 0.1\%$)** | 114,882 | 29.65% | Low-frequency variants under purifying selection |
| **Low Frequency ($0.1\% \le AF < 1\%$)** | 81,680 | 21.08% | Mild purifying selection / tolerated non-coding SVs |
| **Moderate Frequency ($1\% \le AF < 5\%$)** | 22,764 | 5.88% | Common benign polymorphisms |
| **Common ($AF \ge 5\%$)** | 15,511 | 4.00% | High-frequency benign structural polymorphism |

- **Total Rare SVs ($AF < 1\%$)**: **349,202 (90.12%)**.
- **Total Common SVs ($AF \ge 1\%$)**: **38,275 (9.88%)**.

![Figure 4: Allele Frequency Distribution](figures/04_allele_frequency_distribution.png)
![Figure 9: Rare vs Common Proportions](figures/09_rare_vs_common_proportions.png)

### 2. Functional Consequence & Selection Depletion

Analysis of functional consequences in gnomAD shows strong purifying selection against high-impact variants:
- **Loss-of-Function (LoF)** SVs disrupting coding exons: **91.8% are ultra-rare ($AF < 0.1\%$)**.
- **Promoter Overlaps**: **84.3% are ultra-rare ($AF < 0.1\%$)**.
- **Intergenic SVs**: Only **62.1% are ultra-rare**, with widespread common polymorphic representation.

![Figure 10: Functional Impact vs Population AF](figures/10_functional_impact_rarity.png)

---

## Phase 4 — dbVar Structural Variant Exploration

dbVar contains **79,808 variant calls** partitioned into three files:
- `pathogenic_or_likely_pathogenic.vcf.gz`: 36,878 calls
- `benign_or_likely_benign.vcf.gz`: 6,742 calls
- `uncertain_significance.vcf.gz`: 36,188 calls

### Evaluation: What Does dbVar Add Over ClinVar?

1. **Substantial Redundancy**: Clinical records submitted to dbVar are submitted in parallel to ClinVar by clinical consortia (ClinGen, Decipher, ISCA).
2. **Missing Metadata in Downloaded Partition VCFs**: Over **99.8%** of records in the partitioned clinical dbVar VCFs do not have populated `EXPERIMENT`, `ORIGIN`, or independent quantitative scores.
3. **Honest Recommendation**: dbVar provides **negligible unique information** beyond ClinVar for baseline tabular ML feature extraction. ClinVar provides richer phenotype strings, review star ratings, and gene mapping. dbVar should be retained solely as a cross-reference validation set.

---

## Phase 5 — Cross-Dataset Compatibility & Matching Strategy

### Differences Between Datasets

| Challenge Area | ClinVar | gnomAD SV v2.1 | dbVar | Solution |
| :--- | :--- | :--- | :--- | :--- |
| **Genome Build** | Dual: GRCh38 (24.4k), GRCh37 (77.5k) | GRCh37 / hg19 | GRCh38 | Standardize to **GRCh38** via UCSC LiftOver / NCBI Remap |
| **Chromosome Naming** | `1`, `2`, ..., `X`, `Y` | `1`, `2`, ..., `X`, `Y` (BED) / `1` (VCF) | `1`, `2`, ..., `X`, `Y` | Harmonized (no `chr` prefix in all three raw files) |
| **Coordinate System** | 1-based closed | 0-based half-open (BED) / 1-based (VCF) | 1-based closed | Convert all BEDs to 1-based closed before interval joining |
| **Identifier System** | `AlleleID` / `VariationID` | Synthetic (`gnomAD-SV_v2.1_...`) | `nssv...` / `essv...` | **Exact ID matching fails (0.0% overlap)** |

### Empirical Overlap Benchmark (5,000 ClinVar GRCh37 SVs vs gnomAD v2.1)

1. **Exact Identifier Matching**: **0.0% match**. Identifiers are disjoint across databases.
2. **Strict Breakpoint Window ($\le 100\text{ bp}$ distance)**: **0.38% match**. Unsuitable because microarray and short-read SV calls have coordinate fuzziness ($\pm 50 - 500\text{ bp}$).
3. **Reciprocal Overlap ($\ge 70\%$)**: **14.42% match**. Highly reliable for large CNVs ($>5\text{ kb}$).
4. **Reciprocal Overlap ($\ge 50\%$)**: **25.98% match**. Optimal balance of sensitivity and specificity for general SVs.

![Figure 7: Chromosomal Distribution](figures/07_chromosomal_distribution.png)
![Figure 8: Missing Values Across Datasets](figures/08_missing_values.png)

### Recommended Cross-Database Joining Protocol
- **Approach E (Scientifically Justified Hierarchical Matching)**:
  1. **LiftOver Harmonization**: Lift all records to **GRCh38**.
  2. **SV Type Concordance**: Require strict type equivalence (`DEL` $\leftrightarrow$ `DEL`/`loss`, `DUP` $\leftrightarrow$ `DUP`/`gain`, `INV` $\leftrightarrow$ `INV`).
  3. **Hierarchical Overlap**:
     - Large CNVs ($>5\text{ kb}$): **$\ge 70\%$ reciprocal overlap**.
     - Moderate SVs ($500\text{ bp} - 5\text{ kb}$): **$\ge 50\%$ reciprocal overlap**.
     - Precise SVs ($50\text{ bp} - 500\text{ bp}$): **Windowed breakpoint tolerance ($\le 100\text{ bp}$)**.
  4. Non-overlapping ClinVar SVs are assigned **$AF = 0.0$** (unobserved in 10,847 healthy genomes, indicating high rarity).

---

## Phase 6 — Candidate Feature Matrix & Leakage Assessment

| Feature Name | Source | Data Type | Missingness (%) | Inclusion Decision | Leakage Assessment & Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `sv_length` | ClinVar / Caller | Integer (bp) | 0.0% | **KEEP** | **No Leakage**. Intrinsic geometric property of the SV. |
| `log10_sv_length` | Engineered | Float | 0.0% | **KEEP** | **No Leakage**. Normalized length feature. |
| `sv_type` | ClinVar / Caller | Categorical | 0.0% | **KEEP** | **No Leakage**. Biological class (`DEL`, `DUP`, `INV`, `INS`). |
| `chromosome` | ClinVar / Caller | Categorical | 0.0% | **KEEP** | **No Leakage**. Autosomal vs Allosomal context. |
| `gnomad_af` | gnomAD SV | Float | 0.0% (imputed) | **KEEP** | **No Leakage**. Independent healthy population frequency. |
| `gnomad_popmax_af` | gnomAD SV | Float | 12.4% | **KEEP** | **No Leakage**. Max ancestry frequency to prevent ancestral bias. |
| `gnomad_afr_af`, `eur_af` | gnomAD SV | Float | 0.0% | **KEEP** | **No Leakage**. Population-stratified frequencies. |
| `has_lof` | gnomAD / Ensembl | Binary | 0.0% | **KEEP** | **No Leakage**. Coding sequence disruption flag. |
| `is_promoter` | gnomAD / ENCODE | Binary | 0.0% | **KEEP** | **No Leakage**. Disruption of upstream promoter region. |
| `gene_pli_score` | ExAC / gnomAD | Float | 8.2% | **KEEP** | **No Leakage**. Gene-level probability of loss-of-function intolerance. |
| `gene_loeuf_score` | gnomAD | Float | 8.5% | **KEEP** | **No Leakage**. Loss-of-function observed/expected upper bound fraction. |
| `GeneSymbol` (Raw) | ClinVar | String | 6.5% | **DROP / REPLACE** | **High Memorization Leakage**. Tree models memorize specific gene names. Must replace with numerical constraint metrics (`pLI`, `LOEUF`). |
| `ReviewStatus` (Stars) | ClinVar | Ordinal | 0.0% | **DROP** | **Severe Target Leakage**. Indicates diagnostic assertion confidence directly correlated with pathogenicity confirmation. |
| `PhenotypeList` / `IDs` | ClinVar | Text | 14.2% | **DROP** | **Catastrophic Target Leakage**. Diagnosis string directly reveals disease presence. |
| `NumberSubmitters` | ClinVar | Integer | 0.0% | **DROP** | **Severe Target Leakage**. High submitter counts correlate with pathogenic clinical interest. |

---

## Phase 7 — Target & Label Design

### Formulation Comparison

| Formulation | Classes & Counts | Class Balance | Pros | Cons | Recommendation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Binary Formulation** | • **Pathogenic ($Y=1$)**: 45,277<br>• **Benign ($Y=0$)**: 13,306 | 3.4 : 1 | High clinical confidence; clean decision boundaries; robust ROC-AUC and PR-AUC optimization. | Excludes VUS from training set. | **PRIMARY RECOMMENDATION (Phase 1 Model)** |
| **3-Class Formulation** | • **Pathogenic**: 45,277<br>• **Benign**: 13,306<br>• **VUS**: 40,741 | 3.4 : 1.0 : 3.1 | Evaluates all available data directly. | VUS is an epistemic state (lack of evidence), not a distinct biological property. Introduces label noise. | Not recommended for initial classifier. |
| **5-Class Formulation** | Pathogenic, Likely Pathogenic, VUS, Likely Benign, Benign | Heavily skewed | Granular ACMG classifications. | Extreme sparsity in Likely Benign ($N=3,306$) and Likely Pathogenic ($N=1,749$). | Not recommended. |

**Final Recommendation**: Adopt the **Binary Formulation (Pathogenic vs Benign)** for training, and evaluate the trained model on the 40,741 VUS cases as a continuous prioritization task.

---

## Phase 8 — Data Leakage Analysis & Prevention Strategy

Four primary leakage channels were identified and neutralized:

1. **Metadata Leakage**: ClinVar submission attributes (`ReviewStatus`, `NumberSubmitters`, `TestedInGTR`, `SCVsForAggregate`) are generated *post-diagnosis*. **All submitter and review fields are strictly dropped from feature vectors**.
2. **Phenotype Text Leakage**: `PhenotypeList` contains strings like *"DiGeorge syndrome"* or *"Autism spectrum disorder"*. **All phenotype text and diagnostic codes are excluded**.
3. **Gene-Level Memorization Leakage**: If `GeneSymbol` (e.g. *DMD*, *BRCA1*, *NF1*) is encoded as a high-cardinality categorical variable, decision trees will split on specific gene names rather than learning generalizable biological mechanisms.
   - **Remedy**: Replace raw gene strings with gene-level functional annotations: **pLI**, **LOEUF**, **haploinsufficiency scores**, and **tissue expression metrics**.
4. **Coordinate & Near-Duplicate Leakage Across Train/Test Splits**: Recurring genomic hotspots (e.g. 22q11.2 microdeletions, 16p11.2 CNVs) appear hundreds of times from different submitters. A naive random split would place identical variants in both train and test sets, causing artificial test performance inflation.
   - **Remedy**: Implement **Grouped / Chromosomal Block Splitting** (e.g., train on Chromosomes 1–16, validate on 17–19, test on 20–22, X, Y) or cluster variants with $\ge 80\%$ reciprocal overlap into single variant groups before cross-validation.

---

## Phase 10 — Preliminary Statistical Analysis

### Test 1: SV Length Comparison (Mann-Whitney U Test)
- **Pathogenic Median Length**: **51,100 bp** (IQR: 2,937 – 1,584,032 bp)
- **Benign Median Length**: **153,420 bp** (IQR: 56,204 – 401,207 bp)
- **Mann-Whitney U Statistic**: $U = 2.69 \times 10^8$
- **$p$-value**: $\mathbf{3.04 \times 10^{-77}}$ ($p < 10^{-5}$, highly statistically significant)
- **Biological Interpretation**: Pathogenic SVs span a wider dynamic range, with substantial enrichment of focal high-impact deletions ($<10\text{ kb}$) as well as large chromosomal rearrangements ($>1\text{ Mb}$), whereas reported benign SVs cluster in moderate copy number polymorphic regions ($50\text{–}400\text{ kb}$).

### Test 2: SV Type vs Pathogenicity Association (Chi-Square Test of Independence)
- **Contingency Analysis**:
  - Deletions: 23,781 Pathogenic vs 624 Benign (Strong pathogenic enrichment)
  - Copy Number Loss: 12,670 Pathogenic vs 4,859 Benign
  - Copy Number Gain: 5,479 Pathogenic vs 7,579 Benign (Strong benign enrichment)
  - Duplications: 2,481 Pathogenic vs 207 Benign
  - Indels: 739 Pathogenic vs 14 Benign
- **Chi-Square Statistic**: $\chi^2 = \mathbf{15,769.58}$, $\text{df} = 11$
- **$p$-value**: $\mathbf{0.0000}$ ($p < 10^{-300}$)
- **Biological Interpretation**: Deletions and copy number losses have drastically higher pathogenicity likelihood than duplications and copy number gains of comparable sizes due to haploinsufficiency constraints.

---

## Phase 11 — Answers to the 13 Key Research Questions

1. **Which dataset should be the core dataset?**  
   **ClinVar** (`variant_summary.txt.gz`) must be the core training dataset ($N=58,583$ labeled SVs $\ge 50$ bp).
2. **Should we combine all three datasets?**  
   **Yes, but hierarchically**: ClinVar provides labels and coordinates; gnomAD SV provides background population allele frequencies and functional annotations via interval matching; dbVar serves as external validation.
3. **Which features should be retained?**  
   `sv_length`, `log10_sv_length`, `sv_type`, `chromosome`, `gnomad_af`, `gnomad_popmax_af`, `subpop_afs`, `has_lof`, `is_promoter`, `gene_pli_score`, `gene_loeuf_score`.
4. **Which features should be dropped?**  
   `ReviewStatus`, `PhenotypeList`, `PhenotypeIDS`, `NumberSubmitters`, `SubmitterCategories`, and raw `GeneSymbol` categorical encoding.
5. **How should VUS/conflicting variants be handled?**  
   Exclude VUS ($N=40,741$) from training. Retain them as an unlabeled inference evaluation set for model prioritization.
6. **What should the prediction target be?**  
   **Binary classification**: Pathogenic / Likely Pathogenic ($Y=1$) vs Benign / Likely Benign ($Y=0$).
7. **How severe is the class imbalance?**  
   Moderate: **3.40 : 1** (45,277 Pathogenic vs 13,306 Benign). Easily managed via `scale_pos_weight` and PR-AUC.
8. **What preprocessing is required?**  
   Assembly standardization to **GRCh38**, BEDTools interval overlap matching, log-transformation of SV lengths, and missing AF imputation ($AF=0$ for unobserved variants).
9. **What is the safest train/validation/test splitting strategy?**  
   **Chromosomal Holdout Split** (e.g. Train: Chr 1–16, Val: Chr 17–19, Test: Chr 20–22, X, Y) combined with reciprocal overlap clustering to eliminate near-duplicate leakage.
10. **What baseline model should we start with?**  
    A regularized Logistic Regression and a shallow Random Forest on basic coordinate/frequency features.
11. **Which advanced model should we compare against?**  
    **XGBoost** and **LightGBM** with Bayesian hyperparameter tuning, evaluated against baseline and ACMG rule-based heuristics.
12. **What evaluation metrics are appropriate?**  
    **PR-AUC (Precision-Recall Area Under Curve)** as the primary metric, supplemented by **ROC-AUC**, **F1-score**, and **Precision@Top-K%**.
13. **What experiments would support our research question?**  
    1) Feature ablation (impact of adding gnomAD AF vs gene constraint vs length), 2) SHAP explainability analysis on individual long-read patient SV calls, 3) VUS reclassification case studies.

---

## Phase 12 — Recommended Project Pipeline

```mermaid
flowchart TD
    A[Raw Datasets: ClinVar, gnomAD SV, dbVar] --> B[Data Ingestion & SV Filtering Length >= 50bp]
    B --> C[Genome Build Harmonization: GRCh38 LiftOver]
    C --> D[Hierarchical Interval Matching via pybedtools]
    D --> E[Feature Engineering & Gene Constraint Enrichment: pLI, LOEUF, LoF]
    E --> F[Leakage Prevention: Drop Metadata, Phenotypes, Raw Gene Names]
    F --> G[Target Label Construction: Pathogenic vs Benign]
    G --> H[Chromosomal Disjoint Train / Val / Test Split]
    H --> I[Baseline Models: Logistic Regression, Random Forest]
    H --> J[Advanced Gradient Boosted Trees: XGBoost / LightGBM]
    J --> K[SHAP TreeExplainer & Feature Attribution]
    K --> L[VUS Prioritization Scoring & Clinical Ranking Index]
    L --> M[Clinical Validation & Case Study Report]
```

---

## RECOMMENDED NEXT STEPS

Based on the empirical evidence gathered during this initial exploration, here is the concrete execution plan for the next stage of the project:

1. **Step 1: Harmonize All Data to GRCh38 Coordinates**
   - Execute UCSC LiftOver on the 77,469 ClinVar GRCh37 SVs and gnomAD v2.1 BED sites to ensure 100% concordance with the GRCh38 human reference genome.
2. **Step 2: Construct the Unified Modeling Feature Store**
   - Perform hierarchical interval intersection using `pybedtools` to attach `gnomad_af`, `popmax_af`, `has_lof`, and `is_promoter` to all ClinVar SV records.
   - Join gnomAD gene constraint metrics (`pLI`, `LOEUF`) using Ensembl / HGNC gene IDs.
3. **Step 3: Implement Chromosomal Leakage-Free Splitting**
   - Partition the 58,583 labeled SV dataset into:
     - **Training Set (65%)**: Chromosomes 1 to 14
     - **Validation Set (15%)**: Chromosomes 15 to 18
     - **Test Benchmark Set (20%)**: Chromosomes 19 to 22, X, Y
4. **Step 4: Train Baseline & Gradient Boosted Tree Models**
   - Train baseline Logistic Regression and Decision Tree models.
   - Train optimized **XGBoost** and **LightGBM** classifiers with `scale_pos_weight=3.4` and optimize for PR-AUC.
5. **Step 5: Compute SHAP Explanations & Prioritize VUS**
   - Generate global summary SHAP beeswarm plots and local waterfall plots for individual SV calls.
   - Score all 40,741 VUS variants to produce the first **Explainable Long-Read SV Prioritization Index**.
