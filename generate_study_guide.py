import os
import base64
import subprocess
import time

def get_image_base64(filepath):
    if os.path.exists(filepath):
        with open(filepath, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
            return f"data:image/png;base64,{encoded}"
    return ""

# Load all 10 figures as base64
figures_dir = "figures"
fig_b64 = {}
for i in range(1, 11):
    prefix = f"{i:02d}"
    matched = [f for f in os.listdir(figures_dir) if f.startswith(prefix) and f.endswith(".png")]
    if matched:
        fig_b64[prefix] = get_image_base64(os.path.join(figures_dir, matched[0]))
    else:
        fig_b64[prefix] = ""

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Review 1 Comprehensive Study Material & Viva Guide - Group 15</title>
<style>
    @page {
        size: A4;
        margin: 18mm 16mm 18mm 16mm;
        @bottom-right {
            content: counter(page) " / " counter(pages);
            font-size: 9.5pt;
            color: #64748b;
            font-family: 'Segoe UI', Arial, sans-serif;
        }
    }
    body {
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
        color: #1e293b;
        background-color: #ffffff;
        line-height: 1.55;
        font-size: 11pt;
        margin: 0;
        padding: 0;
    }
    h1, h2, h3, h4 {
        color: #0f172a;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-weight: 700;
        margin-top: 1.2em;
        margin-bottom: 0.4em;
        page-break-after: avoid;
    }
    h1 {
        font-size: 20pt;
        border-bottom: 2.5px solid #2563eb;
        padding-bottom: 6px;
        margin-top: 0;
        color: #0f172a;
    }
    h2 {
        font-size: 14pt;
        border-bottom: 1.5px solid #e2e8f0;
        padding-bottom: 4px;
        color: #1e3a8a;
        margin-top: 1.4em;
    }
    h3 {
        font-size: 11.5pt;
        color: #2563eb;
        margin-top: 1em;
    }
    h4 {
        font-size: 10.5pt;
        color: #334155;
        margin-top: 0.8em;
    }
    p {
        margin: 0.5em 0;
        text-align: justify;
    }
    .page-break {
        page-break-before: always;
    }
    .no-break {
        page-break-inside: avoid;
    }
    /* Header Card */
    .header-box {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #ffffff;
        padding: 16px 20px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    .header-box h1 {
        color: #ffffff;
        border-bottom: 1.5px solid #3b82f6;
        font-size: 17pt;
        margin: 0 0 8px 0;
        padding-bottom: 6px;
    }
    .header-meta {
        display: flex;
        justify-content: space-between;
        font-size: 10.5pt;
        color: #94a3b8;
    }
    .header-meta span strong {
        color: #38bdf8;
    }
    /* Cards & Callouts */
    .callout {
        background-color: #f8fafc;
        border-left: 4px solid #2563eb;
        padding: 10px 14px;
        margin: 12px 0;
        border-radius: 0 6px 6px 0;
        font-size: 11pt;
    }
    .callout-warning {
        background-color: #fffbeb;
        border-left-color: #d97706;
    }
    .callout-success {
        background-color: #ecfdf5;
        border-left-color: #059669;
    }
    .callout-danger {
        background-color: #fef2f2;
        border-left-color: #dc2626;
    }
    .stat-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 10px;
        margin: 12px 0;
    }
    .stat-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 10px;
        text-align: center;
    }
    .stat-num {
        font-size: 16pt;
        font-weight: 700;
        color: #2563eb;
        margin-bottom: 2px;
    }
    .stat-label {
        font-size: 9.5pt;
        font-weight: 600;
        color: #475569;
        text-transform: uppercase;
    }
    /* Tables */
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 12px 0;
        font-size: 10.5pt;
    }
    th, td {
        border: 1px solid #cbd5e1;
        padding: 6px 10px;
        text-align: left;
        vertical-align: middle;
    }
    th {
        background-color: #f1f5f9;
        color: #0f172a;
        font-weight: 700;
    }
    tr:nth-child(even) {
        background-color: #f8fafc;
    }
    /* Figures */
    .fig-container {
        text-align: center;
        margin: 14px 0;
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 10px;
        page-break-inside: avoid;
    }
    .fig-container img {
        max-width: 90%;
        max-height: 240px;
        height: auto;
        border-radius: 4px;
    }
    .fig-caption {
        font-size: 8.5pt;
        color: #475569;
        font-weight: 600;
        margin-top: 6px;
    }
    /* Q&A section */
    .qa-box {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 10px 14px;
        margin: 10px 0;
        page-break-inside: avoid;
    }
    .qa-question {
        font-weight: 700;
        color: #1e3a8a;
        font-size: 11pt;
        margin-bottom: 4px;
    }
    .qa-answer {
        color: #334155;
        font-size: 11pt;
        line-height: 1.5;
    }
    .badge {
        display: inline-block;
        padding: 2px 6px;
        font-size: 7.5pt;
        font-weight: 700;
        border-radius: 4px;
        text-transform: uppercase;
        margin-right: 4px;
    }
    .badge-blue { background: #eff6ff; color: #2563eb; border: 1px solid #bfdbfe; }
    .badge-green { background: #ecfdf5; color: #059669; border: 1px solid #a7f3d0; }
    .badge-amber { background: #fffbeb; color: #d97706; border: 1px solid #fde68a; }
    .badge-red { background: #fef2f2; color: #dc2626; border: 1px solid #fecaca; }
    ul, ol {
        margin: 0.4em 0;
        padding-left: 1.4em;
    }
    li {
        margin-bottom: 0.25em;
    }
    code {
        background: #f1f5f9;
        color: #0f172a;
        padding: 1px 4px;
        border-radius: 3px;
        font-size: 8.5pt;
        font-family: Consolas, 'Courier New', monospace;
    }
    .math-block {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 4px;
        padding: 8px 12px;
        font-family: 'Cambria Math', 'Times New Roman', serif;
        font-size: 11pt;
        margin: 8px 0;
        color: #0f172a;
    }
</style>
</head>
<body>

<!-- COVER / HEADER -->
<div class="header-box">
    <h1>AI-Based Structural Variant Prioritization from Long-Read Sequencing</h1>
    <div style="font-size: 11pt; color: #cbd5e1; margin-bottom: 10px;">
        1st Academic Project Review — Comprehensive Study Guide, Statistical Compendium & Viva Preparation Document
    </div>
    <div class="header-meta">
        <span><strong>Team:</strong> Group 15</span>
        <span><strong>Milestone:</strong> Review 1 (~40% Foundation Stage)</span>
        <span><strong>Domain:</strong> Computational Genomics & Explainable AI</span>
    </div>
</div>

<!-- SECTION 1: EXECUTIVE SUMMARY -->
<h2>1. Executive Summary & Review 1 Foundation Scope</h2>
<p>
This document serves as the exhaustive scientific companion and viva preparation guide for <strong>Group 15's 1st Academic Project Review</strong> on <em>"AI-Based Structural Variant Prioritization from Long-Read Sequencing Using Explainable Machine Learning"</em>.
</p>
<p>
In this foundational milestone (~40% completion), the project scope is intentionally and rigorously focused on establishing the multi-dataset genomic infrastructure, proving the statistical significance of biological feature regimes, neutralizing fatal data leakage channels, and formulating a spatial chromosomal validation partition.
</p>

<div class="stat-grid">
    <div class="stat-card">
        <div class="stat-num">101,891</div>
        <div class="stat-label">ClinVar SVs Ingested</div>
    </div>
    <div class="stat-card">
        <div class="stat-num">387,477</div>
        <div class="stat-label">gnomAD Population Sites</div>
    </div>
    <div class="stat-card">
        <div class="stat-num">40.0%</div>
        <div class="stat-label">ClinVar VUS Barrier</div>
    </div>
    <div class="stat-card">
        <div class="stat-num">0.0%</div>
        <div class="stat-label">Genomic Split Overlap</div>
    </div>
</div>

<div class="callout callout-success">
    <strong>Milestone Scope Demarcation:</strong>
    <ul>
        <li><strong>Completed Work (Review 1):</strong> Multi-repository data audit & harmonization (ClinVar, gnomAD SV, dbVar); Ground truth class imbalance characterization; Non-parametric length hypothesis validation (p = 3.04 x 10^-77); Chi-Square variant type dependency validation (p < 10^-300); Zero-leakage feature matrix design; Chromosomal disjoint split formulation (0.0% locus overlap).</li>
        <li><strong>Future Work (Review 2 & Beyond):</strong> Classifier training (Logistic Regression, Random Forest, LightGBM, XGBoost); PR-AUC optimization under 3.4:1 imbalance; TreeSHAP global/local interpretability engine; 40,741 ClinVar VUS scoring & clinical triage; End-to-end patient VCF CLI/Web tool.</li>
    </ul>
</div>

<!-- SECTION 2: SLIDE-BY-SLIDE TECHNICAL BREAKDOWN -->
<div class="page-break"></div>
<h2>2. Slide-by-Slide Technical Reference & Deep Dive</h2>

<h3>Slide 01: Title Slide & Overview</h3>
<p><strong>Slide Purpose:</strong> Establish the project identity, project team (<strong>Group 15</strong>), core academic problem, and 1st review milestone boundaries.</p>
<ul>
    <li><strong>Project Title:</strong> AI-Based Structural Variant Prioritization from Long-Read Sequencing Using Explainable Machine Learning.</li>
    <li><strong>Review 1 Goal:</strong> Establish the quantitative data foundation, validate statistical differences between pathogenic and benign SVs, eliminate data leakage risks, and define the machine learning prioritization framework.</li>
</ul>

<h3>Slide 02: Clinical Problem — The Structural Variant Interpretation Bottleneck</h3>
<p><strong>Clinical Context:</strong> Structural variants (SVs), defined as genomic alterations spanning &ge; 50 base pairs (including deletions, duplications, insertions, inversions, and translocations), account for the largest number of divergent nucleotides between individual human genomes (~10–20 Mb) and are the primary genetic drivers of rare developmental, neurological, and cardiovascular Mendelian diseases.</p>
<ul>
    <li><strong>>20,000 SVs Per Genome:</strong> Long-read sequencing pipelines discover tens of thousands of candidate structural variants per patient.</li>
    <li><strong>The 40.0% VUS Barrier:</strong> In NCBI ClinVar, 40,741 out of 101,891 structural variants (40.0%) are cataloged as "Variants of Uncertain Significance" (VUS). Clinicians cannot determine whether these variants are pathogenic disease drivers or benign polymorphic background.</li>
    <li><strong>Unsustainable Manual Curation:</strong> Standard ACMG/ClinGen manual scoring requires extensive literature review and expert panel deliberation, taking days per patient case.</li>
</ul>

<h3>Slide 03: Motivation — Long-Read Sequencing & Explainable AI</h3>
<p><strong>Technological Convergence:</strong></p>
<ul>
    <li><strong>Why Long-Read Sequencing?</strong> Third-generation platforms (Pacific Biosciences HiFi circular consensus sequencing and Oxford Nanopore ultra-long reads) generate continuous reads exceeding 10 kb to >100 kb. These long reads effortlessly span repetitive transposable elements (LINEs, SINEs, Alu elements) and segmental duplications where short-read Illumina sequencing fails due to mapping ambiguity. Modern SV callers (Sniffles2, cuteSV, PBSV) resolve breakpoint boundaries at single-base or near-single-base resolution.</li>
    <li><strong>Why Explainable Machine Learning?</strong> A black-box classifier is unacceptable in clinical diagnostics. Our framework computes a continuous <strong>Prioritization Index (0.00 - 1.00)</strong> and utilizes <strong>TreeSHAP (Shapley Additive Explanations)</strong> to output patient-specific waterfall plots detailing exactly how much population frequency, gene constraint, and deletion length contributed to the classification.</li>
</ul>

<h3>Slide 04: Literature Foundation & Background</h3>
<table>
    <tr>
        <th>Domain</th>
        <th>Key Reference</th>
        <th>Contributions & Inherent Limitations</th>
    </tr>
    <tr>
        <td><strong>Clinical Standards</strong></td>
        <td>Riggs et al., <em>Genetics in Medicine</em> 2020</td>
        <td>Establishes ACMG/ClinGen 5-tier point rubric for constitutional CNVs. Highly reliant on manual expert curation; struggles with non-coding SVs and complex events.</td>
    </tr>
    <tr>
        <td><strong>Population Baseline</strong></td>
        <td>Collins et al., <em>Nature</em> 2020</td>
        <td>gnomAD SV v2.1 benchmark (387,477 SVs across 10,847 diverse genomes). Proves that 90.12% of SVs in healthy individuals are rare (AF &lt; 1%).</td>
    </tr>
    <tr>
        <td><strong>Computational Scorers</strong></td>
        <td>AnnotSV, CADD-SV, StrVCTVRE</td>
        <td>AnnotSV compiles annotations; CADD-SV computes heuristic impact. Many past ML models suffer from severe post-diagnostic metadata leakage and lack patient-specific local explainability.</td>
    </tr>
</table>

<h3>Slide 05: Research Gaps in Current Practice</h3>
<ul>
    <li><strong>Gap 1 (The 40% VUS Dilemma):</strong> Ambiguous clinical variants lack continuous statistical risk scoring for prioritization.</li>
    <li><strong>Gap 2 (Severe Metadata Leakage):</strong> Existing tools often include ClinVar review stars or submitter counts during training, achieving artificially high accuracy that collapses on real-world raw patient VCFs.</li>
    <li><strong>Gap 3 (Genomic Locus Leakage):</strong> Standard random 80/20 train/test splits allow variants overlapping the same gene or CNV hotspot (e.g. 22q11.2) to appear in both sets, masking model memorization.</li>
    <li><strong>Gap 4 (Diagnostic Opacity):</strong> Clinical adoption requires transparent, additive feature attributions rather than uninterpretable probability outputs.</li>
</ul>

<div class="page-break"></div>
<h3>Slide 06: Project Objectives & Scope Demarcation</h3>
<p><strong>Demarcation Matrix:</strong></p>
<table>
    <tr>
        <th style="width: 50%;">Work Completed So Far (~40% Review 1 Milestone)</th>
        <th style="width: 50%;">Future Work (Review 2 & Final Submission)</th>
    </tr>
    <tr>
        <td>
            <ul>
                <li><strong>Multi-Source Data Ingestion:</strong> Standardized 101,891 ClinVar SVs, 387,477 gnomAD sites, and 79,808 dbVar calls.</li>
                <li><strong>Class Imbalance Characterization:</strong> Isolated 45,277 Pathogenic vs 13,306 Benign variants (3.40:1 ratio).</li>
                <li><strong>Statistical Validation:</strong> Mann-Whitney U test (p = 3.04 x 10^-77) and Chi-Square test (p &lt; 10^-300).</li>
                <li><strong>Zero-Leakage Feature Matrix:</strong> Eliminated post-diagnostic metadata; replaced gene strings with pLI/LOEUF constraint.</li>
                <li><strong>Chromosomal Partitions:</strong> Formulated strict 0.0% locus overlap train/val/test splits.</li>
            </ul>
        </td>
        <td>
            <ul>
                <li><strong>Classifier Benchmarking:</strong> Train Logistic Regression, Random Forest, LightGBM, XGBoost.</li>
                <li><strong>PR-AUC Imbalance Tuning:</strong> Optimize PR-AUC using <code>scale_pos_weight = 3.4</code> and threshold calibration.</li>
                <li><strong>TreeSHAP Explainability:</strong> Compute global summary beeswarm and local waterfall plots.</li>
                <li><strong>40k VUS Scoring:</strong> Prioritize and triage all 40,741 ClinVar VUS into 4 clinical risk tiers.</li>
                <li><strong>Clinical CLI Pipeline:</strong> Develop end-to-end Python CLI and HTML reporting dashboard for patient VCF files.</li>
            </ul>
        </td>
    </tr>
</table>

<h3>Slide 07: Dataset Ingestion & Comprehensive Data Inventory</h3>
<p><strong>Inventory Breakdown:</strong></p>
<ul>
    <li><strong>ClinVar (NCBI):</strong> 101,891 SVs (&ge; 50 bp) extracted from <code>variant_summary.txt.gz</code>. Acts as our ground-truth label provider and VUS target set.</li>
    <li><strong>gnomAD SV v2.1 (Broad Institute):</strong> 387,477 SV sites from 10,847 deep genomes (<code>gnomad_v2.1_sv.sites.bed.gz</code>). Acts as our population frequency baseline.</li>
    <li><strong>dbVar (NCBI):</strong> 79,808 clinical calls. Audit revealed 99.8% unpopulated experiment metadata and exact duplication of ClinVar submissions; therefore, ClinVar + gnomAD SV forms our primary feature matrix.</li>
</ul>

<h3>Slide 08: Ground Truth Label Distribution & Class Imbalance</h3>
<div class="fig-container">
    <img src="FIG_01" alt="Clinical Label Distribution">
    <div class="fig-caption">Figure 1: Breakdown of 101,891 ClinVar structural variants into Pathogenic, Benign, and VUS cohorts.</div>
</div>
<ul>
    <li><strong>Pathogenic / Likely Pathogenic:</strong> 45,277 (44.4%) — Positive Training Class (Y = 1).</li>
    <li><strong>Benign / Likely Benign:</strong> 13,306 (13.1%) — Negative Training Class (Y = 0).</li>
    <li><strong>Variants of Uncertain Significance (VUS):</strong> 40,741 (40.0%) — Reserved for post-hoc clinical prioritization.</li>
    <li><strong>Conflicting / Other:</strong> 2,567 (2.5%) — Excluded from binary training.</li>
    <li><strong>Class Imbalance Ratio:</strong> <strong>3.40 : 1</strong> (Pathogenic : Benign).</li>
</ul>

<div class="page-break"></div>
<h3>Slide 09: Structural Variant Types & Proportions</h3>
<div class="fig-container">
    <img src="FIG_02" alt="SV Type Distribution">
    <div class="fig-caption">Figure 2: Distribution of structural variant types and pathogenic enrichment across ClinVar.</div>
</div>
<ul>
    <li><strong>Deletions & Copy Number Loss:</strong> 58.1% of all records (45,862 Deletions + 23,892 CN Loss). Highly enriched for pathogenicity due to haploinsufficiency.</li>
    <li><strong>Duplications & Copy Number Gain:</strong> 40.7% of all records (21,798 CN Gain + 8,735 Duplications). Significantly more tolerated in healthy populations.</li>
    <li><strong>Inversions, Insertions, Indels:</strong> 1.2% of clinical submissions.</li>
    <li><strong>Critical Discovery (4.8x Pathogenic Odds):</strong> Deletions demonstrate 4.8x higher odds of pathogenicity than duplications of equivalent genomic size (p &lt; 10^-300).</li>
</ul>

<h3>Slide 10: Genomic Length Spectrum & Bimodal Distributions</h3>
<div class="fig-container">
    <img src="FIG_03" alt="SV Length Distribution">
    <div class="fig-caption">Figure 3: Genomic length distributions demonstrating the bimodal pathogenic distribution vs intermediate benign clustering.</div>
</div>
<ul>
    <li><strong>Pathogenic Median Length:</strong> <strong>51,100 bp (51.1 kb)</strong>; Interquartile Range (IQR): 2.9 kb – 1.58 Mb.</li>
    <li><strong>Benign Median Length:</strong> <strong>153,420 bp (153.4 kb)</strong>; Interquartile Range (IQR): 56.2 kb – 401.2 kb.</li>
    <li><strong>Bimodal Pathogenic Profile:</strong>
        <ol>
            <li><em>Focal coding disruptions (1 kb – 10 kb):</em> Single-exon deletions causing frameshifts in dosage-sensitive genes.</li>
            <li><em>Megabase chromosomal syndromes (>1 Mb):</em> Large multi-gene deletions causing severe developmental syndromes (e.g. DiGeorge 22q11.2, Williams-Beuren 7q11.23).</li>
            <li><em>Benign intermediate clustering (50 kb – 300 kb):</em> Benign polymorphisms cluster in non-coding intergenic segments.</li>
        </ol>
    </li>
</ul>

<div class="page-break"></div>
<h3>Slide 11: Population Allele Frequencies & Purifying Selection</h3>
<div class="fig-container">
    <img src="FIG_04" alt="Allele Frequency Distribution">
    <div class="fig-caption">Figure 4: Population allele frequency spectrum across 387,477 gnomAD SV sites showing extreme purifying selection.</div>
</div>
<ul>
    <li><strong>90.12% Rare (AF &lt; 1%):</strong> 349,202 SV sites are observed at &lt;1% frequency across 10,847 healthy genomes.</li>
    <li><strong>39.39% Singletons (AF &le; 0.0046%):</strong> 152,640 SVs appear exactly once in the entire dataset.</li>
    <li><strong>Purifying Selection:</strong> <strong>91.8%</strong> of Loss-of-Function (LoF) SVs and <strong>84.3%</strong> of promoter SVs are ultra-rare (AF &lt; 0.1%). In contrast, intergenic SVs are frequently common (AF &gt; 1%).</li>
    <li><strong>Key Biological Rule:</strong> High population allele frequency (AF &ge; 1%) is a nearly definitive negative predictor of clinical pathogenicity.</li>
</ul>

<h3>Slide 12: Statistical Hypothesis Testing — Formal Biological Proofs</h3>
<div class="callout callout-success">
    <h4>Hypothesis 1: SV Length vs. Pathogenicity (Mann-Whitney U Test)</h4>
    <ul>
        <li><strong>Null Hypothesis (H0):</strong> Pathogenic and benign SVs share identical genomic length distributions.</li>
        <li><strong>Test Statistic:</strong> U = 2.69 x 10^8</li>
        <li><strong>p-value:</strong> <strong>3.04 x 10^-77</strong> (Statistically Significant, p &lt; 10^-5).</li>
        <li><strong>Conclusion:</strong> Reject H0. Genomic length is a statistically validated predictor of clinical outcome.</li>
    </ul>
</div>

<div class="callout callout-success">
    <h4>Hypothesis 2: SV Type vs. Pathogenicity (Pearson's Chi-Square Test)</h4>
    <ul>
        <li><strong>Null Hypothesis (H0):</strong> Structural variant type is independent of clinical classification.</li>
        <li><strong>Contingency Breakdown:</strong> Deletions (23,781 Path vs 624 Benign); Duplications (5,479 Path vs 7,579 Benign).</li>
        <li><strong>Degrees of Freedom:</strong> dof = 11</li>
        <li><strong>Test Statistic:</strong> Chi-Square = <strong>15,769.58</strong></li>
        <li><strong>p-value:</strong> <strong>0.0000</strong> (p &lt; 10^-300, Statistically Significant).</li>
        <li><strong>Conclusion:</strong> Reject H0. SV type is non-randomly associated with clinical severity.</li>
    </ul>
</div>

<div class="page-break"></div>
<h3>Slide 13: Cross-Dataset Harmonization & Overlap Protocol</h3>
<p><strong>The Identification Mismatch:</strong></p>
<ul>
    <li>Exact ID matching yields <strong>0.0% overlap</strong> because ClinVar, dbVar, and gnomAD utilize independent, disjoint accession systems.</li>
    <li>Strict breakpoint matching (&le; 100 bp) yields only <strong>0.38% match</strong> due to legacy array coordinate uncertainty (&plusmn; 50 - 500 bp).</li>
</ul>
<p><strong>Standardized Hierarchical Protocol:</strong></p>
<ol>
    <li><em>Coordinate Standardization:</em> LiftOver all gnomAD GRCh37 coordinates to GRCh38.</li>
    <li><em>SV Type Concordance:</em> Require exact type matching (<code>DEL == DEL</code>, <code>DUP == DUP</code>).</li>
    <li><em>Large CNVs (>5 kb):</em> Require &ge; 70% reciprocal overlap [Overlap / min(len1, len2) &ge; 0.70].</li>
    <li><em>Focal SVs (500 bp – 5 kb):</em> Require &ge; 50% reciprocal overlap.</li>
    <li><em>Unmatched Variants:</em> Assigned AF = 0.0 (reflecting extreme population rarity).</li>
</ol>

<h3>Slide 14: Feature Engineering & Data Leakage Prevention Matrix</h3>
<table>
    <tr>
        <th>Feature Candidate</th>
        <th>Source</th>
        <th>Leakage Risk</th>
        <th>Engineering Decision & Rationale</th>
    </tr>
    <tr>
        <td><code>log10_sv_length</code>, <code>sv_type</code></td>
        <td>Caller / Intrinsic</td>
        <td><span class="badge badge-green">None</span></td>
        <td><strong>KEEP:</strong> Normalized continuous size and one-hot encoded biological types.</td>
    </tr>
    <tr>
        <td><code>gnomad_af</code>, <code>popmax_af</code></td>
        <td>gnomAD SV v2.1</td>
        <td><span class="badge badge-green">None</span></td>
        <td><strong>KEEP:</strong> Population allele frequencies mapped via reciprocal overlap.</td>
    </tr>
    <tr>
        <td><code>has_lof</code>, <code>is_promoter</code></td>
        <td>gnomAD / Ensembl</td>
        <td><span class="badge badge-green">None</span></td>
        <td><strong>KEEP:</strong> Biological flags indicating coding disruption or promoter overlap.</td>
    </tr>
    <tr>
        <td><code>GeneSymbol</code> (Raw String)</td>
        <td>ClinVar</td>
        <td><span class="badge badge-amber">Memorization</span></td>
        <td><strong>TRANSFORM:</strong> Replaced with numeric gene constraint metrics (pLI & LOEUF).</td>
    </tr>
    <tr>
        <td><code>ReviewStatus</code> (Stars)</td>
        <td>ClinVar Metadata</td>
        <td><span class="badge badge-red">Severe Target</span></td>
        <td><strong>DROP:</strong> Post-diagnostic clinical confidence rating only available after curation.</td>
    </tr>
    <tr>
        <td><code>PhenotypeList</code> / Disease</td>
        <td>ClinVar Metadata</td>
        <td><span class="badge badge-red">Catastrophic</span></td>
        <td><strong>DROP:</strong> Explicitly encodes the medical diagnosis and disease phenotype.</td>
    </tr>
    <tr>
        <td><code>NumberSubmitters</code></td>
        <td>ClinVar Metadata</td>
        <td><span class="badge badge-red">Severe Target</span></td>
        <td><strong>DROP:</strong> Directly correlates with clinical attention and disease severity.</td>
    </tr>
</table>

<div class="page-break"></div>
<h3>Slide 15: Chromosomal Validation Strategy & Modeling Architecture</h3>
<p><strong>Spatial Independence Partitioning:</strong> Standard random splits cause genomic locus leakage because overlapping SVs in the same gene or recurrent microdeletion hotspot (e.g. 22q11.2) appear in both training and test sets. By partitioning strictly by chromosome, we guarantee <strong>0.0% locus overlap</strong>:</p>
<ul>
    <li><strong>Training Fold (Chromosomes 1–14):</strong> 25,158 unique SVs (~65% of data) — Representation learning & weight updates.</li>
    <li><strong>Validation Fold (Chromosomes 15–18):</strong> 8,546 unique SVs (~15% of data) — Hyperparameter tuning & probability calibration.</li>
    <li><strong>Holdout Test Fold (Chromosomes 19–22, X, Y):</strong> 8,854 unique SVs (~20% of data) — Unseen chromosome generalization benchmark.</li>
</ul>
<p><strong>Planned Model Suite (Review 2 Benchmarks):</strong></p>
<ul>
    <li><em>Linear Baseline:</em> L2-Regularized Logistic Regression (evaluates linear feature separability).</li>
    <li><em>Tree Ensembles:</em> Balanced Random Forest, LightGBM, and XGBoost configured with <code>scale_pos_weight = 3.4</code>.</li>
    <li><em>Evaluation Metric:</em> <strong>PR-AUC (Precision-Recall Area Under Curve)</strong> over ROC-AUC to prioritize true positive detection under 3.4:1 imbalance.</li>
    <li><em>Interpretability:</em> <strong>TreeSHAP</strong> exact Shapley attributions for all test predictions.</li>
</ul>

<h3>Slide 16: Summary of Work Completed for Review 1</h3>
<ol>
    <li><strong>Multi-Dataset Harmonization:</strong> Standardized 101,891 ClinVar SVs, 387,477 gnomAD sites, and 79,808 dbVar calls to GRCh38.</li>
    <li><strong>VUS Bottleneck Characterization:</strong> Quantified the 40.0% VUS barrier (N = 40,741) and formulated the 3.40:1 binary training set (N = 58,583).</li>
    <li><strong>Statistical Hypothesis Validation:</strong> Proved size (p = 3.04 x 10^-77) and variant type (p &lt; 10^-300) significance prior to model training.</li>
    <li><strong>Zero-Leakage Feature Store:</strong> Neutralized all 4 leakage channels (metadata, phenotypes, submitters, gene memorization).</li>
    <li><strong>Chromosomal Partitions:</strong> Formulated strict 0.0% locus overlap train/val/test splits across 24 human chromosomes.</li>
</ol>

<h3>Slide 17: Current Understanding & Phase 2 Roadmap</h3>
<ul>
    <li><strong>Synthesized Understanding:</strong> Structural variant pathogenicity is fundamentally governed by structural category (Deletions > Duplications), size-dependent coding disruption, extreme population rarity (AF &lt; 0.1%), and gene constraint (pLI / LOEUF).</li>
    <li><strong>Phase 4 (Next):</strong> Train and tune Logistic Regression, Random Forest, LightGBM, and XGBoost on chromosomal folds.</li>
    <li><strong>Phase 5 (Next):</strong> Compute TreeSHAP feature attributions and global beeswarm plots.</li>
    <li><strong>Phase 6 (Next):</strong> Score and prioritize all 40,741 ClinVar VUS into 4 clinical triage tiers.</li>
    <li><strong>Phase 7 (Next):</strong> Build an end-to-end Python CLI and HTML reporting dashboard for patient long-read VCF files.</li>
</ul>

<h3>Slide 18: References & Scientific Literature</h3>
<ol>
    <li>Collins, R. L., Brand, H., et al. (2020). <em>A structural variation reference for medical and population genetics.</em> <strong>Nature</strong>, 581(7809), 444–451.</li>
    <li>Landrum, M. J., Lee, J. M., et al. (2018). <em>ClinVar: improving access to variant interpretations and supporting evidence.</em> <strong>Nucleic Acids Research</strong>, 46(D1), D1062–D1067.</li>
    <li>Riggs, E. R., Andersen, E. F., et al. (2020). <em>Technical standards for the interpretation and reporting of constitutional copy number variants.</em> <strong>Genetics in Medicine</strong>, 22(2), 245–257.</li>
    <li>Lundberg, S. M., & Lee, S. I. (2017). <em>A unified approach to interpreting model predictions.</em> <strong>NeurIPS 2017</strong>, 30, 4765–4774.</li>
    <li>Sedlazeck, F. J., Rescheneder, P., et al. (2018). <em>Accurate detection of complex structural variation using single-molecule sequencing.</em> <strong>Nature Methods</strong>, 15(6), 461–468.</li>
</ol>

<!-- SECTION 3: MATHEMATICAL & STATISTICAL FORMULAS -->
<div class="page-break"></div>
<h2>3. Mathematical & Statistical Formulas & Formal Derivations</h2>

<h3>1. Mann-Whitney U Test (Wilcoxon Rank-Sum)</h3>
<p>
The Mann-Whitney U test is a non-parametric test evaluating whether randomly selected values from population X (Pathogenic SV lengths) tend to be larger or smaller than values from population Y (Benign SV lengths). It does not assume a normal distribution, making it ideal for heavily skewed genomic lengths spanning 50 bp to >10 Mb.
</p>
<div class="math-block">
    <strong>Mathematical Formulation:</strong><br>
    Let n1 be the number of pathogenic variants (n1 = 45,277) and n2 be the number of benign variants (n2 = 13,306). All N = n1 + n2 = 58,583 observations are ranked jointly in ascending order. The test statistics are:<br><br>
    &bull; U1 = R1 - [n1 &times; (n1 + 1)] / 2<br>
    &bull; U2 = R2 - [n2 &times; (n2 + 1)] / 2<br>
    &bull; U = min(U1, U2) = 2.69 &times; 10^8<br><br>
    Under the null hypothesis, for large sample sizes, U asymptotically follows a normal distribution with:<br>
    &bull; Mean (&mu;_U) = (n1 &times; n2) / 2<br>
    &bull; Standard Deviation (&sigma;_U) = &radic;[ (n1 &times; n2 &times; (n1 + n2 + 1)) / 12 ]<br>
    &bull; Z = (U - &mu;_U) / &sigma;_U &rArr; <strong>p = 3.04 &times; 10^-77</strong>
</div>

<h3>2. Pearson's Chi-Square Contingency Test of Independence</h3>
<p>
The Chi-Square test tests whether structural variant type and clinical pathogenicity are independent nominal variables.
</p>
<div class="math-block">
    <strong>Mathematical Formulation:</strong><br>
    For a contingency table with r rows (SV types, r = 12) and c columns (Clinical classes, c = 2):<br><br>
    &bull; &Chi;^2 = &sum; [ (O_ij - E_ij)^2 / E_ij ]<br>
    where O_ij is the observed count and E_ij = (Row_Total_i &times; Col_Total_j) / Grand_Total is the expected count under independence.<br><br>
    &bull; Degrees of Freedom (dof) = (r - 1) &times; (c - 1) = (12 - 1) &times; (2 - 1) = 11<br>
    &bull; &Chi;^2 = <strong>15,769.58</strong>,  <strong>p = 0.0000 (p &lt; 10^-300)</strong><br><br>
    <strong>Odds Ratio for Deletions vs Duplications:</strong><br>
    Odds Ratio (OR) = (Pathogenic_DEL &times; Benign_DUP) / (Benign_DEL &times; Pathogenic_DUP) = (23,781 &times; 7,579) / (624 &times; 5,479) &approx; <strong>4.8&times;</strong>
</div>

<h3>3. Reciprocal Overlap Metric</h3>
<p>
Given two genomic intervals A = [start_A, end_A] and B = [start_B, end_B] on the same chromosome:
</p>
<div class="math-block">
    &bull; Overlap(A, B) = max(0, min(end_A, end_B) - max(start_A, start_B))<br>
    &bull; Reciprocal Overlap Fraction = Overlap(A, B) / min(length(A), length(B)) &ge; &theta;<br><br>
    Thresholds applied: &theta; = 0.70 for CNVs >5 kb; &theta; = 0.50 for focal SVs (500 bp – 5 kb).
</div>

<!-- SECTION 4: 25 ANTICIPATED VIVA QUESTIONS -->
<div class="page-break"></div>
<h2>4. 25 Comprehensive Viva / Examiner Questions & Model Answers</h2>

<div class="qa-box">
    <div class="qa-question">Q1: What is the formal definition of a structural variant, and why do long reads resolve them better than short reads?</div>
    <div class="qa-answer">A structural variant (SV) is any genomic alteration spanning &ge; 50 base pairs, including deletions, duplications, insertions, inversions, and translocations. Short-read Illumina sequencing generates 150 bp reads that cannot span repetitive elements (such as Alu, LINE-1, and segmental duplications), leading to ambiguous multi-mapping (mapQ = 0) and missing breakpoints. In contrast, long-read sequencing (PacBio HiFi / Oxford Nanopore) yields continuous reads of 10 kb to >100 kb that span entire repeat regions, enabling single-base breakpoint resolution.</div>
</div>

<div class="qa-box">
    <div class="qa-question">Q2: Why is the 40% VUS proportion considered a major clinical bottleneck?</div>
    <div class="qa-answer">In NCBI ClinVar, 40,741 out of 101,891 structural variants (40.0%) are classified as Variants of Uncertain Significance (VUS). When a patient receives a VUS in a clinical genetic report, clinicians cannot determine if the variant is causing the patient's disease or if it is a harmless polymorphism. This creates diagnostic uncertainty and delays treatment. Our project builds an explainable AI model to compute continuous risk scores and triage these 40,741 VUS into actionable tiers.</div>
</div>

<div class="qa-box">
    <div class="qa-question">Q3: Why did you not include VUS variants in your binary training labels (Y = 0/1)?</div>
    <div class="qa-answer">Including VUS in binary training labels introduces severe label noise. If an ambiguous variant is arbitrarily assigned a label of 0 or 1, gradient updates in supervised models will be penalized on uncertain ground truth. Instead, we train exclusively on high-confidence Pathogenic (N = 45,277) vs Benign (N = 13,306) variants, and then use the trained model to rank and prioritize the 40,741 VUS during inference.</div>
</div>

<div class="qa-box">
    <div class="qa-question">Q4: What is the class imbalance ratio in your training set, and how will you handle it?</div>
    <div class="qa-answer">The ratio is 3.40 : 1 (45,277 Pathogenic vs 13,306 Benign). In Phase 2, we handle this by configuring tree ensembles with <code>scale_pos_weight = 3.4</code>, using Balanced Random Forests, optimizing Precision-Recall AUC (PR-AUC) rather than ROC-AUC, and tuning probability decision thresholds.</div>
</div>

<div class="qa-box">
    <div class="qa-question">Q5: Why did you split your data by chromosomes rather than using a random 80/20 train/test split?</div>
    <div class="qa-answer">In genomics, standard random splitting causes severe spatial data leakage. Multiple patients in ClinVar often share overlapping structural variants in the exact same gene or recurrent microdeletion hotspot (e.g. 22q11.2, 16p11.2). A random split would place identical genomic loci in both training and test sets, causing the model to achieve artificially high accuracy through locus memorization. By holding out entire chromosomes (Chr 19–22, X, Y), we guarantee 0.0% locus overlap and prove true generalization to unseen chromosomes.</div>
</div>

<div class="qa-box">
    <div class="qa-question">Q6: What is data leakage, and what specific features did you drop from ClinVar?</div>
    <div class="qa-answer">Data leakage occurs when features contain information that would only be available after the clinical diagnosis is already made. We dropped: (1) <code>ReviewStatus</code> stars (reflects curation confidence), (2) <code>PhenotypeList</code> / Disease strings (explicitly encodes diagnosis), and (3) <code>NumberSubmitters</code> (proxy for clinical attention). Including these causes the model to learn curation metadata rather than biology.</div>
</div>

<div class="qa-box">
    <div class="qa-question">Q7: Why did you transform raw gene symbol text into constraint scores?</div>
    <div class="qa-answer">Raw gene symbols represent high-cardinality categorical variables (>19,000 human genes). If one-hot encoded, tree models overfit by memorizing specific cancer/disease gene names (e.g., TP53, BRCA1). If a test variant appears in an uncurated gene, the model fails. Replacing gene names with continuous constraint scores (pLI and LOEUF from gnomAD) forces the model to learn the generalizable biological principle of dosage sensitivity.</div>
</div>

<div class="qa-box">
    <div class="qa-question">Q8: What do pLI and LOEUF measure biologically?</div>
    <div class="qa-answer"><strong>pLI (Probability of Loss-of-Function Intolerance):</strong> Measures the likelihood that a gene cannot tolerate heterozygous loss-of-function variants. Genes with pLI &ge; 0.9 are haploinsufficient. <strong>LOEUF (Loss-of-function Observed/Expected Upper bound Fraction):</strong> A continuous metric where lower values indicate stronger purifying selection against loss-of-function variants (LOEUF &lt; 0.35 indicates extreme constraint).</div>
</div>

<div class="qa-box">
    <div class="qa-question">Q9: What was the result of your Mann-Whitney U test on genomic lengths?</div>
    <div class="qa-answer">The Mann-Whitney U test comparing pathogenic SV lengths (median 51.1 kb) vs benign SV lengths (median 153.4 kb) yielded U = 2.69 &times; 10^8 and p = 3.04 &times; 10^-77. Because p &lt; 10^-5, we rejected the null hypothesis, formally proving that pathogenic and benign SVs occupy distinct genomic size regimes.</div>
</div>

<div class="qa-box">
    <div class="qa-question">Q10: Why do pathogenic structural variants show a bimodal length distribution?</div>
    <div class="qa-answer">Pathogenic SVs fall into two distinct biological classes: (1) <em>Focal coding disruptions (1 kb – 10 kb):</em> precise deletions that disrupt critical single exons or cause frameshifts in dosage-sensitive genes; and (2) <em>Megabase chromosomal deletions (>1 Mb):</em> large multi-gene copy number losses that delete entire developmental chromosomal regions. Benign polymorphisms cluster in intermediate non-coding segments (50 kb – 300 kb).</div>
</div>

<div class="qa-box">
    <div class="qa-question">Q11: What was the result of your Pearson's Chi-Square test on variant types?</div>
    <div class="qa-answer">The Chi-Square test yielded &Chi;^2 = 15,769.58 with dof = 11 and p = 0.0000 (p &lt; 10^-300). This confirmed that structural variant type is non-randomly associated with clinical outcome. Deletions show 4.8x higher pathogenic odds compared to duplications of equal length due to haploinsufficiency.</div>
</div>

<div class="qa-box">
    <div class="qa-question">Q12: Why did direct ID string matching between ClinVar and gnomAD fail with 0.0% overlap?</div>
    <div class="qa-answer">ClinVar uses internal numeric Allele/Variation IDs, dbVar uses accession strings (<code>nsv/esv</code>), and gnomAD generates coordinate-based synthetic strings (e.g. <code>gnomAD-SV_v2.1_DEL_chr1_102</code>). Because there is no universal primary key across databases, cross-repository integration requires coordinate-based reciprocal overlap matching.</div>
</div>

<div class="qa-box">
    <div class="qa-question">Q13: Why did strict 100 bp breakpoint matching yield only a 0.38% match between databases?</div>
    <div class="qa-answer">Legacy ClinVar records were generated using chromosomal microarrays and short-read sequencing, which have breakpoint uncertainty windows of &plusmn; 50 to 500 bp. Strict base-pair matching fails; therefore, a hierarchical reciprocal overlap protocol (&ge; 70% for large CNVs, &ge; 50% for focal SVs) is required.</div>
</div>

<div class="qa-box">
    <div class="qa-question">Q14: What is purifying selection, and how does it manifest in gnomAD SV?</div>
    <div class="qa-answer">Purifying selection is the evolutionary pressure that eliminates deleterious alleles from the population gene pool. In gnomAD SV, 91.8% of Loss-of-Function SVs and 84.3% of promoter SVs are ultra-rare (AF &lt; 0.1%). Highly functional SVs are suppressed by natural selection, making high population frequency (AF &ge; 1%) a strong negative predictor of pathogenicity.</div>
</div>

<div class="qa-box">
    <div class="qa-question">Q15: Why is dbVar not used as a third independent feature source in your primary training set?</div>
    <div class="qa-answer">Our data audit revealed that dbVar clinical VCFs duplicate ClinVar submissions without adding new quantitative features (99.8% of experimental assay metadata columns are unpopulated). Therefore, ClinVar (ground truth labels) + gnomAD SV (population allele frequencies) forms our clean, non-redundant feature matrix.</div>
</div>

<div class="qa-box">
    <div class="qa-question">Q16: What models will be benchmarked in Phase 2, and what is the baseline?</div>
    <div class="qa-answer">We will benchmark L2-Regularized Logistic Regression (as the linear baseline) against Balanced Random Forest, LightGBM, and XGBoost. This will evaluate whether complex non-linear feature interactions (such as size interacting with gene constraint) improve classification performance over linear models.</div>
</div>

<div class="qa-box">
    <div class="qa-question">Q17: Why is PR-AUC preferred over ROC-AUC for this project?</div>
    <div class="qa-answer">ROC-AUC is known to be overly optimistic on imbalanced datasets because the False Positive Rate denominator (FP + TN) is dominated by the large negative class. Precision-Recall AUC (PR-AUC) evaluates Precision [TP / (TP + FP)] against Recall [TP / (TP + FN)], focusing directly on the clinical priority of detecting true pathogenic variants without excessive false alarms.</div>
</div>

<div class="qa-box">
    <div class="qa-question">Q18: What is TreeSHAP, and why is it preferred over LIME or KernelSHAP?</div>
    <div class="qa-answer">TreeSHAP is an exact, polynomial-time algorithm [O(TLD^2) complexity] for computing Shapley values in tree ensembles. Unlike LIME (which uses local linear sampling approximations that can be unstable) or KernelSHAP (which requires exponential sampling), TreeSHAP guarantees the game-theoretic axioms of efficiency, symmetry, dummy player, and additivity, providing exact and consistent local feature attributions for every patient prediction.</div>
</div>

<div class="qa-box">
    <div class="qa-question">Q19: How will the trained model prioritize the 40,741 VUS variants?</div>
    <div class="qa-answer">The calibrated model will assign each VUS a continuous risk probability from 0.00 to 1.00. We will categorize variants into 4 actionable triage tiers: Tier 1 (High Risk, score &ge; 0.80), Tier 2 (Moderate Risk, 0.50 - 0.79), Tier 3 (Low Risk, 0.20 - 0.49), and Tier 4 (Likely Benign, &lt; 0.20), accompanied by TreeSHAP waterfall explanation plots.</div>
</div>

<div class="qa-box">
    <div class="qa-question">Q20: What is LiftOver, and why was it necessary in data harmonization?</div>
    <div class="qa-answer">LiftOver is a bioinformatics tool that converts genomic coordinates between reference genome builds using pairwise alignment chain files. gnomAD SV v2.1 coordinates are aligned to GRCh37 (hg19), whereas modern clinical long-read sequencing uses GRCh38 (hg38). Lifting over coordinates to GRCh38 ensures correct spatial intersection without false positional discordance.</div>
</div>

<div class="qa-box">
    <div class="qa-question">Q21: If a patient has a 1 Mb duplication overlapping non-coding regions with AF = 0.0, how will the model score it?</div>
    <div class="qa-answer">Even though the duplication is large and rare, because duplications have lower pathogenic odds than deletions and the variant does not overlap coding exons of constrained genes (pLI &approx; 0, LOEUF > 1.0), the model will assign it a lower risk score. TreeSHAP will show that while rarity pushed the score up, lack of gene constraint and duplication type pushed the score back down.</div>
</div>

<div class="qa-box">
    <div class="qa-question">Q22: How will your tool integrate into a real hospital or genetics lab workflow?</div>
    <div class="qa-answer">We are developing a lightweight Python CLI and web interface. A bioinformatician inputs a patient's raw long-read VCF file (from Sniffles2 or cuteSV). The pipeline annotates each SV with gnomAD frequency and gene constraint, executes the trained XGBoost model, and outputs a ranked clinical HTML report highlighting Tier 1 variants with interactive TreeSHAP waterfall charts.</div>
</div>

<div class="qa-box">
    <div class="qa-question">Q23: What are the primary milestones scheduled for Review 2?</div>
    <div class="qa-answer">For Review 2, our milestones are: (1) Complete classifier training and hyperparameter tuning on the chromosomal training fold; (2) Benchmark PR-AUC on the holdout test chromosomes (Chr 19–22, X, Y); (3) Generate global TreeSHAP beeswarm summaries; (4) Score and prioritize all 40,741 ClinVar VUS; and (5) Develop the patient VCF CLI tool prototype.</div>
</div>

<div class="qa-box">
    <div class="qa-question">Q24: What is the main takeaway from your Review 1 milestone presentation?</div>
    <div class="qa-answer">We have established a rigorous, factually validated data and statistical foundation: ingested 101k ClinVar, 387k gnomAD, and 79k dbVar records; statistically proved size (p = 3.04 &times; 10^-77) and variant type (p &lt; 10^-300) differences; neutralized 4 fatal data leakage channels; and structured a 0.0% locus overlap chromosomal partition ready for unbiased model benchmarking.</div>
</div>

<div class="qa-box">
    <div class="qa-question">Q25: Why is Group 15 well-positioned to complete Phase 2 successfully?</div>
    <div class="qa-answer">Because all data harmonization, statistical proofs, leakage-free feature stores, and chromosomal splits are already completed, Phase 2 can proceed immediately to model optimization, TreeSHAP interpretability, and clinical tool development without any data pipeline bottlenecks.</div>
</div>

<div style="margin-top: 30px; padding: 14px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; text-align: center; font-size: 8.5pt; color: #64748b;">
    <strong>Group 15</strong> — AI-Based Structural Variant Prioritization from Long-Read Sequencing Using Explainable Machine Learning<br>
    Academic Project Review 1 Foundation Milestone (~40%) | Department of Computer Science & Computational Genomics
</div>

</body>
</html>
"""

# Substitute the base64 images
for i in range(1, 11):
    prefix = f"{i:02d}"
    placeholder = f"FIG_{prefix}"
    html_template = html_template.replace(placeholder, fig_b64.get(prefix, ""))

# Write HTML file
html_path = "Review_1_Study_Material_and_Viva_Prep.html"
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_template)

print(f"[OK] Generated HTML study guide: {html_path} ({len(html_template)} bytes)")

# Convert to PDF using Chrome Headless
pdf_path = os.path.abspath("Review_1_Study_Material_and_Viva_Prep.pdf")
chrome_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
html_abs_path = os.path.abspath(html_path)

cmd = [
    chrome_exe,
    "--headless=new",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_path}",
    f"file:///{html_abs_path.replace(os.sep, '/')}"
]

print("Executing Chrome headless PDF conversion...")
res = subprocess.run(cmd, capture_output=True, text=True)
print("Return code:", res.returncode)

time.sleep(2)
if os.path.exists(pdf_path):
    print(f"[SUCCESS] PDF generated: {pdf_path} (Size: {os.path.getsize(pdf_path)} bytes)")
else:
    print(f"[ERROR] PDF generation failed!")
