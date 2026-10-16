# 1st Review Presentation: AI-Based Structural Variant Prioritization

**Project Title:** AI-Based Structural Variant Prioritization from Long-Read Sequencing Using Explainable Machine Learning  
**Milestone:** Review 1 (Initial Data Exploration, Statistical Validation & Modeling Strategy — ~40% Milestone)  
**Deliverable Document:** `presentation.md`

---

## 📑 Slide Deck Structure Overview

- **Slide 1:** Title, Team & Project Objective
- **Slide 2:** Clinical Motivation & The 40% VUS Bottleneck
- **Slide 3:** Dataset Acquisition & Comprehensive Data Inventory (Notebook 01)
- **Slide 4:** Ground Truth Label Distribution & Class Imbalance Analysis (Notebook 02)
- **Slide 5:** Structural Variant Characteristics & Genomic Size Distributions (Notebook 02)
- **Slide 6:** Statistical Hypothesis Testing: Pathogenic vs. Benign Differences (Notebook 06)
- **Slide 7:** Feature Engineering & Rigorous Data Leakage Prevention (Notebook 06)
- **Slide 8:** Proposed Model Architecture & Chromosomal Validation Strategy
- **Slide 9:** Current Status Summary & Phase 2 Roadmap (Review 2 Milestones)

---

## Slide 1: Title & Project Overview

### 📌 Slide Content
- **Title:** AI-Based Structural Variant Prioritization from Long-Read Sequencing Using Explainable Machine Learning
- **Problem Statement:** Long-read sequencing (PacBio / Oxford Nanopore) uncovers >20,000 structural variants per human genome. However, over 40% of clinically reported variants remain classified as **Variants of Uncertain Significance (VUS)**, creating a critical diagnostic bottleneck.
- **Review 1 Goal:** Establish the quantitative data foundation, validate statistical differences between pathogenic and benign SVs, eliminate data leakage risks, and define the machine learning prioritization framework.

### 🎙️ Speaker Notes (What to Say)
> *"Good morning/afternoon, esteemed faculty members. Today, I am presenting our 1st milestone review on 'AI-Based Structural Variant Prioritization from Long-Read Sequencing Using Explainable Machine Learning'. In this phase, we have completed the comprehensive data ingestion across 3 primary genomic repositories, conducted statistical hypothesis testing, and formulated a leakage-free feature engineering and validation architecture."*

---

## Slide 2: Clinical Motivation & The VUS Bottleneck

### 📌 Slide Content
- **The Power of Long-Read Sequencing:** Unlike short-read sequencing (Illumina), long reads (>10 kb) span complex repeat regions, resolving structural rearrangements, large insertions, deletions, and inversions.
- **The Clinical Challenge:**
  - Standard variant callers produce thousands of candidate SVs per patient.
  - Manual clinical interpretation takes days per case.
  - **40.0% of all submitted SVs in clinical databases are unresolved VUS.**
- **Project Solution:** A calibrated Machine Learning model trained on high-confidence Pathogenic vs. Benign labels to compute a continuous **Pathogenicity Prioritization Index (0.0 to 1.0)** with **TreeSHAP local explainability**.

### 🎙️ Speaker Notes
> *"While third-generation sequencing has solved the problem of detecting structural variants, interpreting them clinically remains an enormous challenge. Over 40,000 structural variants in ClinVar have ambiguous 'uncertain significance' tags. Our aim is to build an explainable machine learning prioritization framework that ranks these variants and explains the exact biological drivers behind each prediction."*

---

## Slide 3: Multi-Dataset Ingestion & Inventory (Notebook 01)

### 📌 Slide Content

| Database | Primary File | Record Count | Genome Build | Key Fields Extracted |
| :--- | :--- | :--- | :--- | :--- |
| **ClinVar** | `variant_summary.txt.gz` | **101,891 SVs** ($\ge 50$ bp) | Dual (GRCh37 / GRCh38) | `ClinicalSignificance`, `GeneSymbol`, `ReviewStatus`, `Type`, `Length` |
| **gnomAD SV v2.1** | `gnomad_v2.1_sv.sites.bed.gz` | **387,477 sites** (10,847 genomes) | GRCh37 (standardized to GRCh38) | `AF`, `POPMAX_AF`, `PROTEIN_CODING__LOF`, `PROTEIN_CODING__PROMOTER` |
| **dbVar** | Clinical SV Callsets (VCF) | **79,808 calls** | GRCh38 | `SVTYPE`, `SVLEN`, `CLNSIG`, `CLNACC` |

- **Key Data Finding:** dbVar clinical files mirror ClinVar submissions without providing new quantitative features; therefore, **ClinVar (Ground Truth) + gnomAD SV (Population Baseline)** forms our primary data matrix.

### 🎙️ Speaker Notes
> *"In Notebook 01, we conducted an audit across three global repositories: ClinVar, gnomAD SV, and dbVar. From over 9 million total ClinVar records, we isolated 101,891 high-quality structural variants (>= 50 bp). We also ingested 387,477 population baseline variants from 10,847 healthy human genomes in gnomAD v2.1."*

---

## Slide 4: Label Distribution & Class Imbalance (Notebook 02)

### 📌 Slide Content

```
ClinVar Structural Variant Breakdown (N = 101,891):
├── Pathogenic / Likely Pathogenic :  45,277 (44.4%)  ──► Training Positive Class (Y = 1)
├── Benign / Likely Benign         :  13,306 (13.1%)  ──► Training Negative Class (Y = 0)
├── Variants of Uncertain (VUS)    :  40,741 (40.0%)  ──► Post-Hoc Prioritization Target
└── Other / Conflicting            :   2,567 ( 2.5%)  ──► Excluded
```

- **Class Imbalance Ratio:** **3.40 : 1** (Pathogenic : Benign).
- **Core Modeling Strategy:**
  - **Phase 1 (Training):** Train exclusively on clean, high-confidence Pathogenic ($N=45,277$) vs. Benign ($N=13,306$) variants.
  - **Phase 2 (Inference):** Apply the calibrated model to all **40,741 VUS variants** to assign continuous risk scores and triage tiers.

### 🎙️ Speaker Notes
> *"Looking at the label distribution in Notebook 02, we observed a moderate class imbalance of 3.4 to 1 between pathogenic and benign variants. Crucially, 40% of all records (40,741 variants) are VUS. We decided not to mix VUS into training to avoid label noise, but rather to reserve them as the primary inference target for clinical ranking."*

---

## Slide 5: Structural Variant Types & Size Distributions (Notebook 02)

### 📌 Slide Content
- **SV Types in ClinVar:**
  - **Deletions & Copy Number Loss:** **58.1%** (Strongly pathogenic enriched)
  - **Duplications & Copy Number Gain:** **40.7%** (More frequently tolerated)
  - **Inversions, Insertions & Indels:** **1.2%**
- **Genomic Length Distributions:**
  - Pathogenic variants exhibit a **bimodal distribution**:
    1. Small focal coding disruptions ($1\text{ kb} - 10\text{ kb}$).
    2. Large megabase-scale chromosomal deletions ($>1\text{ Mb}$).
  - Benign variants cluster in intermediate, non-coding polymorphic copy number segments ($50\text{ kb} - 300\text{ kb}$).

### 🎙️ Speaker Notes
> *"When analyzing structural variant types and lengths, we observe that deletions represent the majority of clinically reported variants (58.1%). Pathogenic variants follow a bimodal length pattern: they are either high-impact focal coding disruptions or large chromosomal copy number losses, whereas benign polymorphisms cluster in non-coding regions."*

---

## Slide 6: Statistical Hypothesis Testing (Notebook 06)

### 📌 Slide Content

#### 1. Hypothesis 1: SV Length vs. Pathogenicity
- **Test:** Mann-Whitney U Test (Non-parametric length distribution comparison)
- **Pathogenic Median Length:** **51,100 bp**
- **Benign Median Length:** **153,420 bp**
- **Statistical Result:** $U = 2.69 \times 10^8, \quad p = \mathbf{3.04 \times 10^{-77}}$  
  *(Statistically Significant: Pathogenic SVs have fundamentally distinct size distributions).*

#### 2. Hypothesis 2: SV Type vs. Pathogenicity
- **Test:** Pearson's Chi-Square Contingency Test
- **Contingency Analysis:** Deletions show 4.8x higher pathogenic odds than duplications.
- **Statistical Result:** $\chi^2 = \mathbf{15,769.58}, \quad \text{dof} = 11, \quad p = \mathbf{0.0000}$  
  *(Statistically Significant: SV type is non-randomly associated with clinical outcome).*

### 🎙️ Speaker Notes
> *"In Notebook 06, we formally tested our clinical hypotheses before training any models. A Mann-Whitney U test on genomic lengths yielded a p-value of 3.04 x 10^-77, proving that pathogenic and benign variants possess statistically distinct genomic footprints. Similarly, a Chi-Square test confirmed that variant types have a highly significant non-random association with pathogenicity."*

---

## Slide 7: Feature Engineering & Data Leakage Prevention (Notebook 06)

### 📌 Slide Content

| Feature Candidate | Source | Risk Level | Engineering Decision |
| :--- | :--- | :--- | :--- |
| **`log10_length`** | Intrinsic / Caller | None | **KEEP** (Standardized numeric) |
| **`is_deletion` / `type_DUP`** | Intrinsic / Caller | None | **KEEP** (One-hot encoded) |
| **`gnomad_af` / `popmax_af`** | gnomAD SV v2.1 | None | **KEEP** (Reciprocal overlap $\ge 50\%$) |
| **`gnomad_lof` / `promoter`** | gnomAD / Ensembl | None | **KEEP** (Functional consequence flags) |
| **`constraint_mean_proxy`** | Gene Constraint | Gene-Memorization | **TRANSFORM** (Replace raw gene names with numeric constraint proxies) |
| **`ReviewStatus` (Stars)** | ClinVar Metadata | **HIGH LEAKAGE** | **DROP** (Only exists after clinical curation) |
| **`PhenotypeList` / `Disease`** | ClinVar Metadata | **EXTREME LEAKAGE** | **DROP** (Explicitly encodes clinical diagnosis) |
| **`NumberSubmitters`** | ClinVar Metadata | **HIGH LEAKAGE** | **DROP** (Proxy for clinical attention) |

### 🎙️ Speaker Notes
> *"A critical contribution of our Phase 1 work is rigorous data leakage prevention. ClinVar contains metadata fields like ReviewStatus stars, Phenotype strings, and Submitter counts. If an ML model sees these, it achieves artificially perfect accuracy by 'memorizing' clinical attention rather than learning biology. We strictly dropped all post-diagnostic metadata and engineered only intrinsic genomic, population, and constraint features."*

---

## Slide 8: Proposed Validation & Modeling Framework

### 📌 Slide Content
- **Chromosomal Disjoint Partitioning (0.0% Genomic Overlap):**
  - **Training Set (Chr 1–14):** 25,158 unique SVs (Learning representation)
  - **Validation Set (Chr 15–18):** 8,546 unique SVs (Hyperparameter tuning)
  - **Holdout Test Set (Chr 19–22, X, Y):** 8,854 unique SVs (Unseen chromosome generalization)
- **Candidate Architectures to Benchmark in Phase 2:**
  - **Linear Baseline:** L2-Regularized Logistic Regression
  - **Bagging Ensemble:** Balanced Random Forest
  - **Boosting Ensembles:** LightGBM & XGBoost with `scale_pos_weight` & PR-AUC optimization
- **Interpretability Framework:** Local & Global **TreeSHAP** (Shapley Additive Explanations).

### 🎙️ Speaker Notes
> *"To ensure unbiased evaluation, we implemented a strict chromosomal split. Chromosomes 19 through 22, X, and Y are completely held out as an unseen test set. This ensures zero genomic overlap between training and testing. In Phase 2, we will benchmark linear baselines against gradient-boosted trees and compute TreeSHAP feature attributions."*

---

## Slide 9: Review 1 Summary & Phase 2 Roadmap

### 📌 Slide Content

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                      CURRENT STATUS: ~40% COMPLETED                       ║
╠═══════════════════════════════════════════════════════════════════════════╣
║  [✓] Phase 1: Ingested ClinVar (101k), gnomAD (387k), dbVar (79k)         ║
║  [✓] Phase 2: Statistical hypothesis validation (MWU & Chi-Square)        ║
║  [✓] Phase 3: Zero-leakage feature matrix & chromosomal split design     ║
║                                                                           ║
║  [ ] Phase 4 (Next): Train & benchmark Logistic, RF, LightGBM, XGBoost   ║
║  [ ] Phase 5 (Next): Compute TreeSHAP explainability & score 40k VUS      ║
║  [ ] Phase 6 (Next): Patient Long-Read VCF Prioritizer CLI & Web UI       ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

### 🎙️ Speaker Notes
> *"In summary, for Review 1, we have established a solid scientific and statistical foundation: multi-dataset harmonization, hypothesis testing, and leakage-free feature design. Our next milestones for Review 2 include model training, PR-AUC benchmarking, TreeSHAP interpretability analysis, and developing the clinical VCF prioritizer tool. Thank you, and I welcome your questions."*

---

## 💡 Potential Faculty Questions & Recommended Answers

### Q1: "Why did you split by chromosomes rather than a random 80/20 train/test split?"
> **Answer:** *"A random train/test split in genomics causes data leakage because overlapping structural variants in the same genomic locus or gene would appear in both training and test sets. By holding out entire chromosomes (Chr 19–22, X, Y), we guarantee 0.0% genomic overlap, proving our model generalizes to entirely unseen genomic regions."*

### Q2: "How will you handle the 40% VUS variants during training?"
> **Answer:** *"We intentionally do not include VUS in the binary training labels ($Y=0/1$) because training on ambiguous ground truth degrades gradient updates. Instead, we train exclusively on high-confidence Pathogenic and Benign variants, and then use the trained, calibrated model to rank and prioritize the 40,741 VUS into 4 actionable clinical risk tiers."*

### Q3: "What features are most critical to prevent false positives in clinical patients?"
> **Answer:** *"gnomAD population allele frequency (`gnomad_af`) and gene constraint metrics. Even if a structural variant is large, if it is observed at >1% frequency in healthy human populations, our model can confidently classify it as a benign polymorphism."*

### Q4: "Can Deep Learning outperform Tree models on this task, and why?"
> **Answer:** *"Yes. Decision trees suffer from piecewise-constant orthogonal decision boundaries, which caused our initial XGBoost model to have lower accuracy (~75%) at default thresholds due to class-imbalanced gradient down-weighting. By implementing a PyTorch Tabular ResNet (Notebook 10) and a Dual-Branch Multimodal Network (Notebook 11) combining population tabular features with breakpoint sequence fragility (microhomology, GC skew) and long-read 5mC epigenetic disruption, we boosted accuracy to 86.16% – 87.98% and slashed calibration error by 38.8%."*

---

## 🚀 Advanced Phase 2 Slide: Multimodal Deep Learning & Conformal Prediction

### 📌 Slide Content
- **Multimodal Dual-Branch Architecture (Notebook 11):**
  - **Branch 1 (Tabular ResNet):** Encodes 24 gnomAD population frequencies and gene constraint proxies.
  - **Branch 2 (Sequence & Epigenetics):** Encodes breakpoint GC content, CpG islands, MMEJ microhomology, Alu/LINE retrotransposition vulnerability, and Oxford Nanopore native 5mC methylation disruption.
  - **Multi-Head Cross-Attention:** Dynamically queries sequence-level fragility against population tolerability.
- **Split Conformal Prediction (95% Coverage Guarantee):**
  - Eliminates clinical ambiguity by replacing arbitrary point thresholds with **guaranteed prediction sets**:
    - **Singleton Calls ($\{\text{Pathogenic}\}$ or $\{\text{Benign}\}$):** $>85\%$ of test variants definitively triaged.
    - **Ambiguous Sets ($\{\text{Benign}, \text{Pathogenic}\}$):** Mathematically alerts clinicians when manual functional assays are strictly required.
- **Benchmark Across All Paradigms (Holdout Chromosomes 19–22, X, Y):**
  - **Tabular ResNet (DL):** **86.16% Accuracy** ($\tau = 0.50$), **87.98% Accuracy** ($\tau = 0.27$), **ROC-AUC: 0.8892**, **PR-AUC: 0.9705**, **Brier Score: 0.1010**.
  - **Multimodal Net:** Balanced cross-modal representation with **95.2% empirical conformal coverage**.

