const pptxgen = require('pptxgenjs');
const fs = require('fs');
const path = require('path');

const pptx = new pptxgen();

// Layout: Widescreen 16:9 (13.333 x 7.5 inches)
pptx.layout = 'LAYOUT_WIDE';
pptx.author = 'Group 15';
pptx.company = 'Department of Computer Science & Computational Genomics';
pptx.title = 'AI-Based Structural Variant Prioritization from Long-Read Sequencing Using Explainable Machine Learning';
pptx.subject = 'Project Review 1 - Milestone Presentation';

// Color Palette Tokens
const C = {
  bg: 'F8FAFC',          // Light background
  white: 'FFFFFF',       // Card background
  navy: '0F172A',        // Main text & deep headers
  slate: '334155',       // Body text
  muted: '64748B',       // Subtitles & captions
  border: 'E2E8F0',      // Card borders
  blue: '2563EB',        // Primary accent
  blueLight: 'EFF6FF',   // Pill / soft badge bg
  blueBorder: 'BFDBFE',  // Pill border
  emerald: '059669',     // Positive / completed
  emeraldLight: 'ECFDF5',// Emerald soft badge bg
  amber: 'D97706',       // VUS / Warning
  amberLight: 'FFFBEB',  // Amber soft badge bg
  red: 'DC2626',         // Pathogenic / Critical
  redLight: 'FEF2F2',    // Red soft badge bg
  cardHeaderBg: 'F1F5F9' // Table / card header bg
};

const FONT_TITLE = 'Calibri';
const FONT_BODY = 'Calibri';

// Layout coordinate constants
const MARGIN_X = 0.8;
const USABLE_W = 11.733;

// Helper: Standard Slide Header (Font sizes boosted by +3 to +4 pt)
function addSlideHeader(slide, category, title, subtitle) {
  slide.background = { color: C.bg };

  // Category Tag (Boosted from 10 -> 13)
  slide.addText(category.toUpperCase(), {
    x: MARGIN_X, y: 0.36, w: USABLE_W, h: 0.28,
    fontSize: 12.5, fontFace: FONT_BODY, bold: true,
    color: C.blue, tracking: 1.5
  });

  // Main Action Title (Boosted from 19.5 -> 23.5)
  slide.addText(title, {
    x: MARGIN_X, y: 0.64, w: USABLE_W, h: 0.52,
    fontSize: 23, fontFace: FONT_TITLE, bold: true,
    color: C.navy, margin: 0
  });

  // Subtitle / Framing line (Boosted from 12 -> 15)
  if (subtitle) {
    slide.addText(subtitle, {
      x: MARGIN_X, y: 1.18, w: USABLE_W, h: 0.32,
      fontSize: 14.5, fontFace: FONT_BODY,
      color: C.muted, margin: 0
    });
  }

  // Header Divider
  slide.addShape(pptx.ShapeType.line, {
    x: MARGIN_X, y: 1.54, w: USABLE_W, h: 0,
    line: { color: C.border, width: 1.2 }
  });
}

// Helper: Standard Slide Footer (Boosted from 9.5 -> 11.5)
function addSlideFooter(slide, current, total = 18) {
  slide.addText(`Group 15  |  Project Review 1  |  AI-Based Structural Variant Prioritization`, {
    x: MARGIN_X, y: 6.95, w: 8.5, h: 0.32,
    fontSize: 11.5, fontFace: FONT_BODY, color: C.muted
  });
  slide.addText(`Slide ${current} of ${total}`, {
    x: 10.333, y: 6.95, w: 2.2, h: 0.32,
    fontSize: 11.5, fontFace: FONT_BODY, color: C.muted, align: 'right'
  });
}

// =========================================================================
// SLIDE 1: TITLE SLIDE (Font sizes boosted)
// =========================================================================
{
  const s = pptx.addSlide();
  s.background = { color: '0F172A' };

  // Header Tag (Boosted: 11 -> 14)
  s.addText('ACADEMIC PROJECT REVIEW 1  |  FOUNDATION MILESTONE (~40%)', {
    x: MARGIN_X, y: 0.85, w: USABLE_W, h: 0.35,
    fontSize: 13.5, fontFace: FONT_BODY, bold: true, color: '60A5FA', tracking: 2
  });

  // Project Title (Boosted: 26 -> 30)
  s.addText('AI-Based Structural Variant Prioritization from\nLong-Read Sequencing Using Explainable ML', {
    x: MARGIN_X, y: 1.28, w: USABLE_W, h: 1.6,
    fontSize: 29, fontFace: FONT_TITLE, bold: true, color: 'FFFFFF', lineSpacingMultiple: 1.15
  });

  // Subtitle (Boosted: 13.5 -> 16.5)
  s.addText('Multi-Repository Genomic Ingestion, Statistical Hypothesis Validation & Zero-Leakage Architecture', {
    x: MARGIN_X, y: 3.00, w: USABLE_W, h: 0.45,
    fontSize: 16, fontFace: FONT_BODY, color: '94A3B8'
  });

  // Divider
  s.addShape(pptx.ShapeType.line, {
    x: MARGIN_X, y: 3.58, w: USABLE_W, h: 0,
    line: { color: '334155', width: 1.5 }
  });

  // 3 Info Cards
  const cardW = 3.67;
  const cardGap = 0.36;
  const cards = [
    { title: 'PROJECT TEAM', header: 'Group 15', desc: 'Computational Genomics & AI\nB.Tech Capstone Project' },
    { title: 'REVIEW 1 GOAL', header: 'Data & Validation', desc: 'Harmonize ClinVar & gnomAD\nStatistical Proof of SV Regimes' },
    { title: 'DELIVERABLES', header: 'Zero-Leakage Design', desc: 'Chromosomal Disjoint Partitions\nFeature Matrix & Target Formulation' }
  ];

  cards.forEach((c, idx) => {
    const cx = MARGIN_X + idx * (cardW + cardGap);
    s.addShape(pptx.ShapeType.roundRect, {
      x: cx, y: 3.85, w: cardW, h: 2.70,
      rectRadius: 0.08,
      fill: { color: '1E293B' },
      line: { color: '334155', width: 1 }
    });

    s.addText(c.title, {
      x: cx + 0.25, y: 4.08, w: cardW - 0.5, h: 0.28,
      fontSize: 12, fontFace: FONT_BODY, bold: true, color: '38BDF8', tracking: 1.2
    });

    s.addText(c.header, {
      x: cx + 0.25, y: 4.42, w: cardW - 0.5, h: 0.48,
      fontSize: 19, fontFace: FONT_TITLE, bold: true, color: 'FFFFFF'
    });

    s.addText(c.desc, {
      x: cx + 0.25, y: 4.98, w: cardW - 0.5, h: 1.35,
      fontSize: 13.5, fontFace: FONT_BODY, color: 'CBD5E1', lineSpacingMultiple: 1.2
    });
  });
}

// =========================================================================
// SLIDE 2: PROBLEM CONTEXT & THE VUS BOTTLENECK
// =========================================================================
{
  const s = pptx.addSlide();
  addSlideHeader(s, 'Problem Context', 'The Structural Variant Interpretation Bottleneck', 'High-throughput variant discovery creates an unsustainable manual curation bottleneck');
  addSlideFooter(s, 2);

  const cardW = 3.67;
  const cardGap = 0.36;
  const stats = [
    { num: '>20,000', label: 'SVs Per Genome', desc: 'Structural variants (>=50 bp) drive the majority of divergent base pairs and rare Mendelian genetic diseases.', color: C.blue },
    { num: '40.0%', label: 'Unresolved VUS', desc: '40,741 structural variants in ClinVar carry "Uncertain Significance", leaving patients without clear diagnoses.', color: C.amber },
    { num: 'Days / Case', label: 'Manual Curation', desc: 'Standard clinical evaluation requires labor-intensive manual guideline scoring, stalling diagnostic throughput.', color: C.red }
  ];

  stats.forEach((st, idx) => {
    const sx = MARGIN_X + idx * (cardW + cardGap);
    s.addShape(pptx.ShapeType.roundRect, {
      x: sx, y: 1.75, w: cardW, h: 2.65,
      rectRadius: 0.08, fill: { color: C.white }, line: { color: C.border, width: 1 }
    });

    s.addText(st.num, {
      x: sx + 0.25, y: 1.95, w: cardW - 0.5, h: 0.65,
      fontSize: 32, fontFace: FONT_TITLE, bold: true, color: st.color
    });

    s.addText(st.label, {
      x: sx + 0.25, y: 2.65, w: cardW - 0.5, h: 0.35,
      fontSize: 15.5, fontFace: FONT_TITLE, bold: true, color: C.navy
    });

    s.addText(st.desc, {
      x: sx + 0.25, y: 3.05, w: cardW - 0.5, h: 1.20,
      fontSize: 13, fontFace: FONT_BODY, color: C.slate, lineSpacingMultiple: 1.15
    });
  });

  // Bottom Summary Banner
  s.addShape(pptx.ShapeType.roundRect, {
    x: MARGIN_X, y: 4.60, w: USABLE_W, h: 2.15,
    rectRadius: 0.08, fill: { color: C.white }, line: { color: C.blueBorder, width: 1.2 }
  });

  s.addText('CORE PROBLEM STATEMENT', {
    x: MARGIN_X + 0.3, y: 4.78, w: USABLE_W - 0.6, h: 0.28,
    fontSize: 13, fontFace: FONT_BODY, bold: true, color: C.blue, tracking: 1.2
  });

  s.addText('While long-read sequencing reliably uncovers thousands of structural variants per patient, clinical genetics teams cannot manually evaluate them at scale. Over 40% of all submitted SVs remain trapped in the ambiguous VUS category. There is an urgent need for an automated, calibrated Machine Learning framework that ranks candidate variants, prioritizes true clinical risks, and explains the biological rationale behind every prediction.', {
    x: MARGIN_X + 0.3, y: 5.12, w: USABLE_W - 0.6, h: 1.45,
    fontSize: 14, fontFace: FONT_BODY, color: C.navy, lineSpacingMultiple: 1.22
  });
}

// =========================================================================
// SLIDE 3: MOTIVATION & TECHNOLOGY DRIVERS
// =========================================================================
{
  const s = pptx.addSlide();
  addSlideHeader(s, 'Technology Drivers', 'Motivation: Long-Read Sequencing & Explainable AI', 'Leveraging single-molecule long reads and interpretable machine learning');
  addSlideFooter(s, 3);

  const colW = 5.66;
  const colGap = 0.41;

  // Left Column: Long-Read Sequencing
  s.addShape(pptx.ShapeType.roundRect, {
    x: MARGIN_X, y: 1.75, w: colW, h: 4.98,
    rectRadius: 0.08, fill: { color: C.white }, line: { color: C.border, width: 1 }
  });

  s.addText('THE POWER OF LONG-READ SEQUENCING', {
    x: MARGIN_X + 0.3, y: 1.98, w: colW - 0.6, h: 0.28,
    fontSize: 12.5, fontFace: FONT_BODY, bold: true, color: C.blue, tracking: 1
  });
  s.addText('PacBio HiFi & Oxford Nanopore (>10 kb Reads)', {
    x: MARGIN_X + 0.3, y: 2.30, w: colW - 0.6, h: 0.42,
    fontSize: 16.5, fontFace: FONT_TITLE, bold: true, color: C.navy
  });

  const lrPoints = [
    { h: 'Spanning Complex Repeats:', t: 'Reads >10 kb span repetitive elements, segment duplications, and GC-rich regions inaccessible to short-read Illumina.' },
    { h: 'Single-Base Breakpoint Precision:', t: 'Dedicated SV callers (Sniffles2, cuteSV) resolve precise breakpoint coordinates at near-nucleotide resolution.' },
    { h: 'Comprehensive Variant Detection:', t: 'Simultaneously captures deletions, duplications, balanced inversions, insertions, and complex multi-breakend events.' }
  ];

  lrPoints.forEach((p, idx) => {
    s.addText(`•  ${p.h}`, {
      x: MARGIN_X + 0.3, y: 2.82 + idx * 1.30, w: colW - 0.6, h: 0.30,
      fontSize: 13.5, fontFace: FONT_BODY, bold: true, color: C.navy
    });
    s.addText(p.t, {
      x: MARGIN_X + 0.55, y: 3.14 + idx * 1.30, w: colW - 0.85, h: 0.88,
      fontSize: 13, fontFace: FONT_BODY, color: C.slate, lineSpacingMultiple: 1.15
    });
  });

  // Right Column: Explainable AI
  const rx = MARGIN_X + colW + colGap;
  s.addShape(pptx.ShapeType.roundRect, {
    x: rx, y: 1.75, w: colW, h: 4.98,
    rectRadius: 0.08, fill: { color: C.white }, line: { color: C.border, width: 1 }
  });

  s.addText('EXPLAINABLE MACHINE LEARNING', {
    x: rx + 0.3, y: 1.98, w: colW - 0.6, h: 0.28,
    fontSize: 12.5, fontFace: FONT_BODY, bold: true, color: C.emerald, tracking: 1
  });
  s.addText('Calibrated Risk Prioritization & Interpretation', {
    x: rx + 0.3, y: 2.30, w: colW - 0.6, h: 0.42,
    fontSize: 16.5, fontFace: FONT_TITLE, bold: true, color: C.navy
  });

  const aiPoints = [
    { h: 'Continuous Prioritization Index:', t: 'Outputs a well-calibrated risk probability (0.00 to 1.00) rather than coarse, rigid binary heuristic classifications.' },
    { h: 'Local TreeSHAP Feature Attribution:', t: 'Decomposes every individual variant score into exact additive contributions from population rarity, size, and gene constraint.' },
    { h: 'Clinical Actionability Triage:', t: 'Groups patient variants into 4 actionable clinical tiers (Tier 1 High Risk to Tier 4 Benign) to accelerate medical review.' }
  ];

  aiPoints.forEach((p, idx) => {
    s.addText(`•  ${p.h}`, {
      x: rx + 0.3, y: 2.82 + idx * 1.30, w: colW - 0.6, h: 0.30,
      fontSize: 13.5, fontFace: FONT_BODY, bold: true, color: C.navy
    });
    s.addText(p.t, {
      x: rx + 0.55, y: 3.14 + idx * 1.30, w: colW - 0.85, h: 0.88,
      fontSize: 13, fontFace: FONT_BODY, color: C.slate, lineSpacingMultiple: 1.15
    });
  });
}

// =========================================================================
// SLIDE 4: BACKGROUND & LITERATURE REVIEW
// =========================================================================
{
  const s = pptx.addSlide();
  addSlideHeader(s, 'Literature Foundation', 'Background & Literature Review', 'Clinical standards, population catalogs, and existing computational tools');
  addSlideFooter(s, 4);

  const cardW = 3.67;
  const cardGap = 0.36;
  const litCards = [
    {
      tag: 'CLINICAL GUIDELINES', title: 'ACMG/ClinGen Standards',
      citation: 'Riggs et al., Genetics in Medicine 2020',
      bullets: [
        'Defines a 5-tier point-based scoring rubric for constitutional CNVs.',
        'Requires extensive manual literature curation and expert consensus.',
        'Struggles with non-coding SVs, complex events, and novel variants.'
      ]
    },
    {
      tag: 'POPULATION BASELINE', title: 'gnomAD SV Reference',
      citation: 'Collins et al., Nature 2020',
      bullets: [
        'Curated 387,477 SV sites across 10,847 diverse deep human genomes.',
        'Proves that 90.12% of structural variants in healthy cohorts are rare.',
        'Establishes the gold-standard allele frequency baseline across ancestries.'
      ]
    },
    {
      tag: 'COMPUTATIONAL TOOLS', title: 'Existing Variant Scorers',
      citation: 'AnnotSV, CADD-SV, StrVCTVRE',
      bullets: [
        'AnnotSV compiles annotations; CADD-SV calculates heuristic scores.',
        'Published ML models often suffer from post-diagnostic metadata leakage.',
        'Lack patient-specific local explainability for clinical laboratory review.'
      ]
    }
  ];

  litCards.forEach((c, idx) => {
    const cx = MARGIN_X + idx * (cardW + cardGap);
    s.addShape(pptx.ShapeType.roundRect, {
      x: cx, y: 1.75, w: cardW, h: 4.98,
      rectRadius: 0.08, fill: { color: C.white }, line: { color: C.border, width: 1 }
    });

    s.addText(c.tag, {
      x: cx + 0.25, y: 2.00, w: cardW - 0.5, h: 0.28,
      fontSize: 12, fontFace: FONT_BODY, bold: true, color: C.blue, tracking: 1
    });

    s.addText(c.title, {
      x: cx + 0.25, y: 2.32, w: cardW - 0.5, h: 0.45,
      fontSize: 16.5, fontFace: FONT_TITLE, bold: true, color: C.navy
    });

    s.addText(c.citation, {
      x: cx + 0.25, y: 2.80, w: cardW - 0.5, h: 0.40,
      fontSize: 12, fontFace: FONT_BODY, italic: true, color: C.muted
    });

    s.addShape(pptx.ShapeType.line, {
      x: cx + 0.25, y: 3.28, w: cardW - 0.5, h: 0,
      line: { color: C.border, width: 1 }
    });

    c.bullets.forEach((b, bIdx) => {
      s.addText(`•  ${b}`, {
        x: cx + 0.25, y: 3.46 + bIdx * 1.10, w: cardW - 0.5, h: 1.00,
        fontSize: 13, fontFace: FONT_BODY, color: C.slate, lineSpacingMultiple: 1.15
      });
    });
  });
}

// =========================================================================
// SLIDE 5: RESEARCH GAPS
// =========================================================================
{
  const s = pptx.addSlide();
  addSlideHeader(s, 'Research Challenges', 'Research Gap: Critical Limitations in Existing Approaches', 'Four major scientific and methodological roadblocks identified in current practice');
  addSlideFooter(s, 5);

  const colW = 5.66;
  const colGap = 0.41;
  const gaps = [
    { num: '01', title: 'The 40% VUS Dilemma', desc: '40.0% of structural variants in ClinVar remain unresolved as Variants of Uncertain Significance. Current clinical pipelines lack continuous statistical ranking to triage these ambiguous variants.' },
    { num: '02', title: 'Severe Metadata Leakage', desc: 'Published ML tools frequently include post-diagnostic clinical metadata (ReviewStatus stars, submitter counts, disease strings), creating inflated, non-generalizable accuracy.' },
    { num: '03', title: 'Genomic Locus Leakage', desc: 'Standard random train/test splits allow variants from the same gene or CNV hotspot (e.g., 22q11.2, 16p11.2) to enter both folds, masking true out-of-sample generalization failure.' },
    { num: '04', title: 'Black-Box Opacity', desc: 'Existing computational tools output opaque risk scores without explaining the exact biological drivers (gene constraint vs population rarity) necessary for clinical confidence.' }
  ];

  gaps.forEach((g, idx) => {
    const row = Math.floor(idx / 2);
    const col = idx % 2;
    const gx = MARGIN_X + col * (colW + colGap);
    const gy = 1.75 + row * 2.52;

    s.addShape(pptx.ShapeType.roundRect, {
      x: gx, y: gy, w: colW, h: 2.36,
      rectRadius: 0.08, fill: { color: C.white }, line: { color: C.border, width: 1 }
    });

    s.addText(g.num, {
      x: gx + 0.25, y: gy + 0.18, w: 0.85, h: 0.48,
      fontSize: 24, fontFace: FONT_TITLE, bold: true, color: C.blue
    });

    s.addText(g.title, {
      x: gx + 1.15, y: gy + 0.20, w: colW - 1.4, h: 0.42,
      fontSize: 16.5, fontFace: FONT_TITLE, bold: true, color: C.navy
    });

    s.addText(g.desc, {
      x: gx + 0.25, y: gy + 0.72, w: colW - 0.5, h: 1.45,
      fontSize: 13.5, fontFace: FONT_BODY, color: C.slate, lineSpacingMultiple: 1.2
    });
  });
}

// =========================================================================
// SLIDE 6: PROJECT OBJECTIVES & SCOPE DEMARCATION
// =========================================================================
{
  const s = pptx.addSlide();
  addSlideHeader(s, 'Scope & Roadmap', 'Project Objectives & Scope: 1st Review Milestone', 'Demarcating the completed foundation (~40% milestone) from downstream phases');
  addSlideFooter(s, 6);

  const colW = 5.66;
  const colGap = 0.41;

  // Left Card: Work Completed So Far
  s.addShape(pptx.ShapeType.roundRect, {
    x: MARGIN_X, y: 1.75, w: colW, h: 4.98,
    rectRadius: 0.08, fill: { color: C.white }, line: { color: C.emerald, width: 1.5 }
  });

  s.addText('WORK COMPLETED SO FAR (REVIEW 1 SCOPE)', {
    x: MARGIN_X + 0.3, y: 1.98, w: colW - 0.6, h: 0.28,
    fontSize: 12.5, fontFace: FONT_BODY, bold: true, color: C.emerald, tracking: 1
  });
  s.addText('Data Foundation & Statistical Validation (~40%)', {
    x: MARGIN_X + 0.3, y: 2.28, w: colW - 0.6, h: 0.42,
    fontSize: 16.5, fontFace: FONT_TITLE, bold: true, color: C.navy
  });

  const completed = [
    { title: 'Multi-Source Data Ingestion', desc: 'Audited and ingested ClinVar (101k SVs), gnomAD SV (387k sites), and dbVar (79k calls).' },
    { title: 'Statistical Hypothesis Validation', desc: 'Formally proved size and type significance via Mann-Whitney U and Chi-Square tests.' },
    { title: 'Leakage-Free Feature Design', desc: 'Neutralized metadata, phenotype, and gene-memorization leakage channels.' },
    { title: 'Chromosomal Split Architecture', desc: 'Formulated strict 0.0% genomic overlap train/val/test chromosomal partitions.' }
  ];

  completed.forEach((item, idx) => {
    s.addText(`[Done]  ${item.title}`, {
      x: MARGIN_X + 0.3, y: 2.80 + idx * 1.02, w: colW - 0.6, h: 0.28,
      fontSize: 14, fontFace: FONT_BODY, bold: true, color: C.emerald
    });
    s.addText(item.desc, {
      x: MARGIN_X + 0.55, y: 3.10 + idx * 1.02, w: colW - 0.85, h: 0.65,
      fontSize: 13, fontFace: FONT_BODY, color: C.slate, lineSpacingMultiple: 1.15
    });
  });

  // Right Card: Future Work
  const rx = MARGIN_X + colW + colGap;
  s.addShape(pptx.ShapeType.roundRect, {
    x: rx, y: 1.75, w: colW, h: 4.98,
    rectRadius: 0.08, fill: { color: C.white }, line: { color: C.border, width: 1 }
  });

  s.addText('FUTURE WORK (REVIEW 2 & BEYOND)', {
    x: rx + 0.3, y: 1.98, w: colW - 0.6, h: 0.28,
    fontSize: 12.5, fontFace: FONT_BODY, bold: true, color: C.blue, tracking: 1
  });
  s.addText('Modeling, Explainability & Clinical CLI', {
    x: rx + 0.3, y: 2.28, w: colW - 0.6, h: 0.42,
    fontSize: 16.5, fontFace: FONT_TITLE, bold: true, color: C.navy
  });

  const future = [
    { title: 'ML Classifier Benchmarking', desc: 'Train Logistic Regression, Random Forest, LightGBM, and XGBoost on chromosomal splits.' },
    { title: 'PR-AUC Imbalance Optimization', desc: 'Handle the 3.4:1 class imbalance using scale_pos_weight and threshold tuning.' },
    { title: 'TreeSHAP Explainability Engine', desc: 'Generate global feature attributions and local patient single-variant waterfall plots.' },
    { title: '40k VUS Clinical Prioritization', desc: 'Score and categorize all 40,741 ClinVar VUS variants into 4 actionable risk tiers.' }
  ];

  future.forEach((item, idx) => {
    s.addText(`[Planned]  ${item.title}`, {
      x: rx + 0.3, y: 2.80 + idx * 1.02, w: colW - 0.6, h: 0.28,
      fontSize: 14, fontFace: FONT_BODY, bold: true, color: C.blue
    });
    s.addText(item.desc, {
      x: rx + 0.55, y: 3.10 + idx * 1.02, w: colW - 0.85, h: 0.65,
      fontSize: 13, fontFace: FONT_BODY, color: C.slate, lineSpacingMultiple: 1.15
    });
  });
}

// =========================================================================
// SLIDE 7: DATASET ACQUISITION & INVENTORY
// =========================================================================
{
  const s = pptx.addSlide();
  addSlideHeader(s, 'Data Acquisition', 'Dataset Ingestion & Comprehensive Data Inventory', 'Systematic multi-repository audit across ClinVar, gnomAD SV, and dbVar');
  addSlideFooter(s, 7);

  const tableData = [
    [
      { text: 'Database', options: { bold: true, color: C.navy, fill: { color: C.cardHeaderBg } } },
      { text: 'Records Analyzed', options: { bold: true, color: C.navy, fill: { color: C.cardHeaderBg } } },
      { text: 'Genome Build', options: { bold: true, color: C.navy, fill: { color: C.cardHeaderBg } } },
      { text: 'Extracted Features & Role in Project', options: { bold: true, color: C.navy, fill: { color: C.cardHeaderBg } } }
    ],
    [
      { text: 'ClinVar\n(NCBI)', options: { bold: true, color: C.navy } },
      { text: '101,891 SVs\n(>= 50 bp)', options: { bold: true, color: C.blue } },
      { text: 'Dual\n(GRCh37 / 38)', options: { color: C.slate } },
      { text: 'Ground truth clinical classifications (Pathogenic, Benign, VUS), gene symbols, and molecular variant types.', options: { color: C.slate } }
    ],
    [
      { text: 'gnomAD SV\n(v2.1 / Broad)', options: { bold: true, color: C.navy } },
      { text: '387,477 sites\n(10,847 genomes)', options: { bold: true, color: C.blue } },
      { text: 'GRCh37\n(Harmonized)', options: { color: C.slate } },
      { text: 'Global population allele frequencies (AF, POPMAX_AF), loss-of-function flags, and promoter overlap annotations.', options: { color: C.slate } }
    ],
    [
      { text: 'dbVar\n(NCBI)', options: { bold: true, color: C.navy } },
      { text: '79,808 calls\n(Clinical sets)', options: { bold: true, color: C.blue } },
      { text: 'GRCh38', options: { color: C.slate } },
      { text: 'Clinical callsets evaluated for cross-validation; confirmed as duplicate mirror of ClinVar submissions.', options: { color: C.slate } }
    ]
  ];

  s.addTable(tableData, {
    x: MARGIN_X, y: 1.75, w: USABLE_W, h: 3.00,
    colW: [1.8, 2.2, 1.8, 5.933],
    border: { pt: 1, color: C.border },
    fontSize: 13, fontFace: FONT_BODY,
    align: 'left', valign: 'middle'
  });

  // Callout Card at Bottom
  s.addShape(pptx.ShapeType.roundRect, {
    x: MARGIN_X, y: 4.90, w: USABLE_W, h: 1.85,
    rectRadius: 0.08, fill: { color: C.white }, line: { color: C.blueBorder, width: 1.2 }
  });

  s.addText('KEY DATA AUDIT FINDINGS', {
    x: MARGIN_X + 0.3, y: 5.08, w: USABLE_W - 0.6, h: 0.28,
    fontSize: 13, fontFace: FONT_BODY, bold: true, color: C.blue, tracking: 1
  });

  s.addText('•  ClinVar provides the authoritative ground truth clinical labels (N = 101,891), while gnomAD SV (N = 387,477) provides the non-redundant healthy population frequency baseline.\n•  dbVar clinical partition VCFs duplicate ClinVar submissions without contributing independent quantitative features (99.8% unpopulated experiment metadata). Therefore, ClinVar (Labels) + gnomAD SV (Population Frequencies) form our unified feature store.', {
    x: MARGIN_X + 0.3, y: 5.40, w: USABLE_W - 0.6, h: 1.25,
    fontSize: 13.5, fontFace: FONT_BODY, color: C.navy, lineSpacingMultiple: 1.2
  });
}

// =========================================================================
// SLIDE 8: GROUND TRUTH LABEL DISTRIBUTION & CLASS IMBALANCE
// =========================================================================
{
  const s = pptx.addSlide();
  addSlideHeader(s, 'Label Analysis', 'Ground Truth Label Distribution & Class Imbalance', 'Categorization of 101,891 ClinVar SVs and formulation of training cohorts');
  addSlideFooter(s, 8);

  const colW = 5.66;
  const colGap = 0.41;

  // Left Side: 4 Label Cards
  const labelCards = [
    { title: 'Pathogenic / Likely Pathogenic', count: '45,277 (44.4%)', role: 'Training Positive Class (Y = 1)', color: C.red },
    { title: 'Benign / Likely Benign', count: '13,306 (13.1%)', role: 'Training Negative Class (Y = 0)', color: C.emerald },
    { title: 'Variants of Uncertain Significance (VUS)', count: '40,741 (40.0%)', role: 'Primary Post-Hoc Prioritization Target', color: C.amber },
    { title: 'Conflicting / Other Classifications', count: '2,567 (2.5%)', role: 'Excluded from Binary Training Set', color: C.muted }
  ];

  labelCards.forEach((lc, idx) => {
    const ly = 1.75 + idx * 1.24;
    s.addShape(pptx.ShapeType.roundRect, {
      x: MARGIN_X, y: ly, w: colW, h: 1.14,
      rectRadius: 0.08, fill: { color: C.white }, line: { color: C.border, width: 1 }
    });

    s.addText(lc.count, {
      x: MARGIN_X + 0.25, y: ly + 0.15, w: 2.9, h: 0.40,
      fontSize: 18, fontFace: FONT_TITLE, bold: true, color: lc.color
    });

    s.addText(lc.title, {
      x: MARGIN_X + 0.25, y: ly + 0.58, w: 3.2, h: 0.45,
      fontSize: 13.5, fontFace: FONT_BODY, bold: true, color: C.navy
    });

    s.addText(lc.role, {
      x: MARGIN_X + 3.1, y: ly + 0.35, w: colW - 3.35, h: 0.45,
      fontSize: 13, fontFace: FONT_BODY, color: C.slate, align: 'right'
    });
  });

  // Right Side: Figure
  const rx = MARGIN_X + colW + colGap;
  const figPath = path.resolve(__dirname, 'figures/01_clinical_label_distribution.png');
  if (fs.existsSync(figPath)) {
    s.addImage({
      path: figPath,
      x: rx, y: 1.75, w: colW, h: 4.98
    });
  }
}

// =========================================================================
// SLIDE 9: STRUCTURAL VARIANT TYPES & PROPORTIONS
// =========================================================================
{
  const s = pptx.addSlide();
  addSlideHeader(s, 'Variant Characteristics', 'Structural Variant Types & Clinical Proportions', 'Deletions dominate clinical submissions and show strong pathogenic enrichment');
  addSlideFooter(s, 9);

  const colW = 5.66;
  const colGap = 0.41;

  // Left Side: 2 Structural Type Breakdown Cards
  const typeCards = [
    {
      title: 'Deletions & Copy Number Loss', prop: '58.1% of Total SVs',
      detail: '45,862 Deletions + 23,892 Copy Number Loss events.\nStrongly enriched for pathogenic outcomes due to haploinsufficiency and loss of essential coding sequences.',
      color: C.red
    },
    {
      title: 'Duplications & Copy Number Gain', prop: '40.7% of Total SVs',
      detail: '21,798 Copy Number Gain + 8,735 Duplication events.\nMore frequently tolerated as benign copy number polymorphisms across healthy human populations.',
      color: C.emerald
    }
  ];

  typeCards.forEach((tc, idx) => {
    const ty = 1.75 + idx * 1.95;
    s.addShape(pptx.ShapeType.roundRect, {
      x: MARGIN_X, y: ty, w: colW, h: 1.82,
      rectRadius: 0.08, fill: { color: C.white }, line: { color: C.border, width: 1 }
    });

    s.addText(tc.title, {
      x: MARGIN_X + 0.25, y: ty + 0.16, w: 3.6, h: 0.38,
      fontSize: 16.5, fontFace: FONT_TITLE, bold: true, color: C.navy
    });

    s.addText(tc.prop, {
      x: MARGIN_X + 3.6, y: ty + 0.16, w: colW - 3.85, h: 0.38,
      fontSize: 13.5, fontFace: FONT_BODY, bold: true, color: tc.color, align: 'right'
    });

    s.addText(tc.detail, {
      x: MARGIN_X + 0.25, y: ty + 0.58, w: colW - 0.5, h: 1.15,
      fontSize: 13.5, fontFace: FONT_BODY, color: C.slate, lineSpacingMultiple: 1.2
    });
  });

  // Highlight Box: 4.8x Odds
  s.addShape(pptx.ShapeType.roundRect, {
    x: MARGIN_X, y: 5.75, w: colW, h: 0.98,
    rectRadius: 0.08, fill: { color: C.amberLight }, line: { color: C.amber, width: 1 }
  });

  s.addText('CRITICAL OBSERVATION: 4.8x PATHOGENIC ODDS', {
    x: MARGIN_X + 0.25, y: 5.86, w: colW - 0.5, h: 0.28,
    fontSize: 12.5, fontFace: FONT_BODY, bold: true, color: C.amber, tracking: 1
  });

  s.addText('Deletions exhibit 4.8x higher pathogenic odds compared to duplications of equivalent genomic length.', {
    x: MARGIN_X + 0.25, y: 6.16, w: colW - 0.5, h: 0.48,
    fontSize: 13, fontFace: FONT_BODY, color: C.navy
  });

  // Right Side: Figure
  const rx = MARGIN_X + colW + colGap;
  const figPath = path.resolve(__dirname, 'figures/02_sv_type_distribution.png');
  if (fs.existsSync(figPath)) {
    s.addImage({
      path: figPath,
      x: rx, y: 1.75, w: colW, h: 4.98
    });
  }
}

// =========================================================================
// SLIDE 10: GENOMIC LENGTH SPECTRUM & BIMODAL DISTRIBUTIONS
// =========================================================================
{
  const s = pptx.addSlide();
  addSlideHeader(s, 'Size Dynamics', 'Genomic Length Spectrum & Bimodal Distributions', 'Pathogenic and benign structural variants occupy distinct genomic length regimes');
  addSlideFooter(s, 10);

  const colW = 5.66;
  const colGap = 0.41;

  // Left Side: Size Distribution Analysis
  const statBoxW = (colW - 0.2) / 2;
  s.addShape(pptx.ShapeType.roundRect, {
    x: MARGIN_X, y: 1.75, w: statBoxW, h: 1.45,
    rectRadius: 0.08, fill: { color: C.white }, line: { color: C.border, width: 1 }
  });

  s.addText('PATHOGENIC MEDIAN', {
    x: MARGIN_X + 0.15, y: 1.90, w: statBoxW - 0.3, h: 0.28,
    fontSize: 12, fontFace: FONT_BODY, bold: true, color: C.red, tracking: 1
  });
  s.addText('51,100 bp (51.1 kb)', {
    x: MARGIN_X + 0.15, y: 2.18, w: statBoxW - 0.3, h: 0.48,
    fontSize: 19, fontFace: FONT_TITLE, bold: true, color: C.navy
  });
  s.addText('IQR: 2.9 kb – 1.58 Mb', {
    x: MARGIN_X + 0.15, y: 2.70, w: statBoxW - 0.3, h: 0.38,
    fontSize: 13, fontFace: FONT_BODY, color: C.muted
  });

  const sb2X = MARGIN_X + statBoxW + 0.2;
  s.addShape(pptx.ShapeType.roundRect, {
    x: sb2X, y: 1.75, w: statBoxW, h: 1.45,
    rectRadius: 0.08, fill: { color: C.white }, line: { color: C.border, width: 1 }
  });

  s.addText('BENIGN MEDIAN', {
    x: sb2X + 0.15, y: 1.90, w: statBoxW - 0.3, h: 0.28,
    fontSize: 12, fontFace: FONT_BODY, bold: true, color: C.emerald, tracking: 1
  });
  s.addText('153,420 bp (153.4 kb)', {
    x: sb2X + 0.15, y: 2.18, w: statBoxW - 0.3, h: 0.48,
    fontSize: 19, fontFace: FONT_TITLE, bold: true, color: C.navy
  });
  s.addText('IQR: 56.2 kb – 401.2 kb', {
    x: sb2X + 0.15, y: 2.70, w: statBoxW - 0.3, h: 0.38,
    fontSize: 13, fontFace: FONT_BODY, color: C.muted
  });

  // Bimodal Regimes Explanation Box
  s.addShape(pptx.ShapeType.roundRect, {
    x: MARGIN_X, y: 3.32, w: colW, h: 3.41,
    rectRadius: 0.08, fill: { color: C.white }, line: { color: C.border, width: 1 }
  });

  s.addText('BIMODAL PATHOGENIC PROFILE', {
    x: MARGIN_X + 0.25, y: 3.52, w: colW - 0.5, h: 0.28,
    fontSize: 13, fontFace: FONT_BODY, bold: true, color: C.blue, tracking: 1
  });

  const regimes = [
    { title: '1. Focal Coding Disruptions (1 kb – 10 kb):', desc: 'High-impact single-exon deletions and frame-shifts in critical haploinsufficient genes.' },
    { title: '2. Megabase Chromosomal Syndromes (>1 Mb):', desc: 'Large multi-gene deletions and copy number aberrations affecting critical developmental loci.' },
    { title: '3. Benign Intermediate Clustering (50 kb – 300 kb):', desc: 'Reported benign variants cluster in non-coding polymorphic copy number segments.' }
  ];

  regimes.forEach((r, idx) => {
    s.addText(r.title, {
      x: MARGIN_X + 0.25, y: 3.86 + idx * 0.90, w: colW - 0.5, h: 0.28,
      fontSize: 13.5, fontFace: FONT_BODY, bold: true, color: C.navy
    });
    s.addText(r.desc, {
      x: MARGIN_X + 0.45, y: 4.14 + idx * 0.90, w: colW - 0.7, h: 0.58,
      fontSize: 13, fontFace: FONT_BODY, color: C.slate, lineSpacingMultiple: 1.15
    });
  });

  // Right Side: Figure
  const rx = MARGIN_X + colW + colGap;
  const figPath = path.resolve(__dirname, 'figures/03_sv_length_distribution.png');
  if (fs.existsSync(figPath)) {
    s.addImage({
      path: figPath,
      x: rx, y: 1.75, w: colW, h: 4.98
    });
  }
}

// =========================================================================
// SLIDE 11: POPULATION ALLELE FREQUENCIES & PURIFYING SELECTION
// =========================================================================
{
  const s = pptx.addSlide();
  addSlideHeader(s, 'Population Genetics', 'Population Allele Frequencies & Purifying Selection', 'gnomAD SV v2.1 baseline reveals extreme purifying selection on functional SVs');
  addSlideFooter(s, 11);

  const colW = 5.66;
  const colGap = 0.41;

  // Left Side: Population Statistics
  s.addShape(pptx.ShapeType.roundRect, {
    x: MARGIN_X, y: 1.75, w: colW, h: 4.98,
    rectRadius: 0.08, fill: { color: C.white }, line: { color: C.border, width: 1 }
  });

  s.addText('ALLELE FREQUENCY SPECTRUM (N = 387,477)', {
    x: MARGIN_X + 0.25, y: 1.98, w: colW - 0.5, h: 0.28,
    fontSize: 12.5, fontFace: FONT_BODY, bold: true, color: C.blue, tracking: 1
  });

  const popStats = [
    { stat: '90.12%', label: 'Rare in Population (AF < 1%)', desc: '349,202 SV sites are observed at less than 1% frequency across 10,847 healthy human genomes.' },
    { stat: '39.39%', label: 'Ultra-Rare Singletons (AF <= 0.0046%)', desc: '152,640 SVs appear exactly once in the entire population dataset.' },
    { stat: '9.88%', label: 'Common Polymorphisms (AF >= 1%)', desc: 'Only 38,275 SVs are common benign variants tolerated across global ancestries.' }
  ];

  popStats.forEach((ps, idx) => {
    s.addText(ps.stat, {
      x: MARGIN_X + 0.25, y: 2.34 + idx * 1.00, w: 1.5, h: 0.40,
      fontSize: 21, fontFace: FONT_TITLE, bold: true, color: C.blue
    });
    s.addText(ps.label, {
      x: MARGIN_X + 1.80, y: 2.34 + idx * 1.00, w: colW - 2.05, h: 0.28,
      fontSize: 13.5, fontFace: FONT_BODY, bold: true, color: C.navy
    });
    s.addText(ps.desc, {
      x: MARGIN_X + 1.80, y: 2.62 + idx * 1.00, w: colW - 2.05, h: 0.68,
      fontSize: 12.5, fontFace: FONT_BODY, color: C.slate, lineSpacingMultiple: 1.15
    });
  });

  // Purifying Selection Callout
  s.addShape(pptx.ShapeType.roundRect, {
    x: MARGIN_X + 0.25, y: 5.40, w: colW - 0.5, h: 1.20,
    rectRadius: 0.08, fill: { color: C.blueLight }, line: { color: C.blueBorder, width: 1 }
  });

  s.addText('PURIFYING SELECTION TAKEAWAY', {
    x: MARGIN_X + 0.45, y: 5.50, w: colW - 0.9, h: 0.24,
    fontSize: 12, fontFace: FONT_BODY, bold: true, color: C.blue, tracking: 1
  });
  s.addText('91.8% of Loss-of-Function (LoF) SVs and 84.3% of promoter SVs are ultra-rare (AF < 0.1%). Common population frequency (AF > 1%) is a highly reliable negative indicator of pathogenicity.', {
    x: MARGIN_X + 0.45, y: 5.75, w: colW - 0.9, h: 0.78,
    fontSize: 12.5, fontFace: FONT_BODY, color: C.navy, lineSpacingMultiple: 1.15
  });

  // Right Side: Figure
  const rx = MARGIN_X + colW + colGap;
  const figPath = path.resolve(__dirname, 'figures/04_allele_frequency_distribution.png');
  if (fs.existsSync(figPath)) {
    s.addImage({
      path: figPath,
      x: rx, y: 1.75, w: colW, h: 4.98
    });
  }
}

// =========================================================================
// SLIDE 12: STATISTICAL HYPOTHESIS TESTING
// =========================================================================
{
  const s = pptx.addSlide();
  addSlideHeader(s, 'Statistical Validation', 'Statistical Hypothesis Testing: Biological Differences', 'Formal pre-training statistical validation of size and variant type associations');
  addSlideFooter(s, 12);

  const colW = 5.66;
  const colGap = 0.41;

  // Left Card: Mann-Whitney U
  s.addShape(pptx.ShapeType.roundRect, {
    x: MARGIN_X, y: 1.75, w: colW, h: 4.98,
    rectRadius: 0.08, fill: { color: C.white }, line: { color: C.border, width: 1 }
  });

  s.addText('HYPOTHESIS 1: LENGTH VS PATHOGENICITY', {
    x: MARGIN_X + 0.3, y: 1.98, w: colW - 0.6, h: 0.28,
    fontSize: 12.5, fontFace: FONT_BODY, bold: true, color: C.blue, tracking: 1
  });
  s.addText('Mann-Whitney U Non-Parametric Test', {
    x: MARGIN_X + 0.3, y: 2.28, w: colW - 0.6, h: 0.42,
    fontSize: 16.5, fontFace: FONT_TITLE, bold: true, color: C.navy
  });

  const mwuData = [
    { label: 'Null Hypothesis (H0):', val: 'Pathogenic and benign SVs have identical length distributions.' },
    { label: 'Pathogenic Median Length:', val: '51,100 bp (IQR: 2.9 kb – 1.58 Mb)' },
    { label: 'Benign Median Length:', val: '153,420 bp (IQR: 56.2 kb – 401.2 kb)' },
    { label: 'Test Statistic:', val: 'U = 2.69 x 10^8' }
  ];

  mwuData.forEach((d, idx) => {
    s.addText(d.label, {
      x: MARGIN_X + 0.3, y: 2.80 + idx * 0.65, w: 2.3, h: 0.28,
      fontSize: 13, fontFace: FONT_BODY, bold: true, color: C.navy
    });
    s.addText(d.val, {
      x: MARGIN_X + 2.35, y: 2.80 + idx * 0.65, w: colW - 2.65, h: 0.58,
      fontSize: 13, fontFace: FONT_BODY, color: C.slate
    });
  });

  // Result Badge MWU
  s.addShape(pptx.ShapeType.roundRect, {
    x: MARGIN_X + 0.3, y: 5.35, w: colW - 0.6, h: 1.25,
    rectRadius: 0.08, fill: { color: C.emeraldLight }, line: { color: C.emerald, width: 1.2 }
  });
  s.addText('p-value: 3.04 x 10^-77  (Statistically Significant)', {
    x: MARGIN_X + 0.45, y: 5.48, w: colW - 0.9, h: 0.34,
    fontSize: 14.5, fontFace: FONT_TITLE, bold: true, color: C.emerald
  });
  s.addText('Rejects H0. Proves that pathogenic and benign variants follow fundamentally distinct genomic length distributions.', {
    x: MARGIN_X + 0.45, y: 5.84, w: colW - 0.9, h: 0.68,
    fontSize: 12.5, fontFace: FONT_BODY, color: C.navy, lineSpacingMultiple: 1.15
  });

  // Right Card: Chi-Square
  const rx = MARGIN_X + colW + colGap;
  s.addShape(pptx.ShapeType.roundRect, {
    x: rx, y: 1.75, w: colW, h: 4.98,
    rectRadius: 0.08, fill: { color: C.white }, line: { color: C.border, width: 1 }
  });

  s.addText('HYPOTHESIS 2: SV TYPE VS PATHOGENICITY', {
    x: rx + 0.3, y: 1.98, w: colW - 0.6, h: 0.28,
    fontSize: 12.5, fontFace: FONT_BODY, bold: true, color: C.blue, tracking: 1
  });
  s.addText('Pearson\'s Chi-Square Contingency Test', {
    x: rx + 0.3, y: 2.28, w: colW - 0.6, h: 0.42,
    fontSize: 16.5, fontFace: FONT_TITLE, bold: true, color: C.navy
  });

  const chiData = [
    { label: 'Null Hypothesis (H0):', val: 'SV type is independent of clinical classification.' },
    { label: 'Contingency Table:', val: 'Deletions: 23,781 Path / 624 Benign (4.8x odds)\nDuplications: 5,479 Path / 7,579 Benign' },
    { label: 'Degrees of Freedom:', val: 'dof = 11' },
    { label: 'Test Statistic:', val: 'Chi-Square = 15,769.58' }
  ];

  chiData.forEach((d, idx) => {
    s.addText(d.label, {
      x: rx + 0.3, y: 2.80 + idx * 0.65, w: 2.3, h: 0.28,
      fontSize: 13, fontFace: FONT_BODY, bold: true, color: C.navy
    });
    s.addText(d.val, {
      x: rx + 2.35, y: 2.80 + idx * 0.65, w: colW - 2.65, h: 0.58,
      fontSize: 13, fontFace: FONT_BODY, color: C.slate
    });
  });

  // Result Badge Chi
  s.addShape(pptx.ShapeType.roundRect, {
    x: rx + 0.3, y: 5.35, w: colW - 0.6, h: 1.25,
    rectRadius: 0.08, fill: { color: C.emeraldLight }, line: { color: C.emerald, width: 1.2 }
  });
  s.addText('p-value: 0.0000 (p < 10^-300)  (Significant)', {
    x: rx + 0.45, y: 5.48, w: colW - 0.9, h: 0.34,
    fontSize: 14.5, fontFace: FONT_TITLE, bold: true, color: C.emerald
  });
  s.addText('Rejects H0. Confirms a strong non-random biological dependency between structural variant type and clinical outcome.', {
    x: rx + 0.45, y: 5.84, w: colW - 0.9, h: 0.68,
    fontSize: 12.5, fontFace: FONT_BODY, color: C.navy, lineSpacingMultiple: 1.15
  });
}

// =========================================================================
// SLIDE 13: CROSS-DATASET HARMONIZATION & OVERLAP PROTOCOL
// =========================================================================
{
  const s = pptx.addSlide();
  addSlideHeader(s, 'Data Integration', 'Cross-Dataset Interval Matching & Harmonization', 'Resolving coordinate discrepancies and fuzzy breakpoints across databases');
  addSlideFooter(s, 13);

  const colW = 5.66;
  const colGap = 0.41;

  // Left Side: Why exact matching fails
  s.addShape(pptx.ShapeType.roundRect, {
    x: MARGIN_X, y: 1.75, w: colW, h: 4.98,
    rectRadius: 0.08, fill: { color: C.white }, line: { color: C.border, width: 1 }
  });

  s.addText('CHALLENGES IN SV MATCHING', {
    x: MARGIN_X + 0.3, y: 1.98, w: colW - 0.6, h: 0.28,
    fontSize: 12, fontFace: FONT_BODY, bold: true, color: C.red, tracking: 1
  });
  s.addText('Why Exact String / ID Joins Fail', {
    x: MARGIN_X + 0.3, y: 2.28, w: colW - 0.6, h: 0.42,
    fontSize: 16.5, fontFace: FONT_TITLE, bold: true, color: C.navy
  });

  const failPoints = [
    { title: 'Exact Identifier Match: 0.0% Overlap', desc: 'ClinVar uses Allele IDs, dbVar uses nsv/esv strings, and gnomAD uses synthetic coordinate names. There is zero global primary key overlap.' },
    { title: 'Strict Breakpoint Window (<= 100 bp): 0.38% Match', desc: 'Legacy microarray and short-read ClinVar entries have breakpoint uncertainty windows (+/- 50 to 500 bp), making strict coordinate matching fail.' },
    { title: 'Assembly Differences (GRCh37 vs GRCh38)', desc: 'gnomAD SV v2.1 uses GRCh37, while modern clinical workflows use GRCh38. Direct coordinate comparisons without LiftOver cause severe false negatives.' }
  ];

  failPoints.forEach((fp, idx) => {
    s.addText(`•  ${fp.title}`, {
      x: MARGIN_X + 0.3, y: 2.80 + idx * 1.30, w: colW - 0.6, h: 0.30,
      fontSize: 13.5, fontFace: FONT_BODY, bold: true, color: C.navy
    });
    s.addText(fp.desc, {
      x: MARGIN_X + 0.55, y: 3.12 + idx * 1.30, w: colW - 0.85, h: 0.88,
      fontSize: 12.5, fontFace: FONT_BODY, color: C.slate, lineSpacingMultiple: 1.15
    });
  });

  // Right Side: The Hierarchical Overlap Protocol
  const rx = MARGIN_X + colW + colGap;
  s.addShape(pptx.ShapeType.roundRect, {
    x: rx, y: 1.75, w: colW, h: 4.98,
    rectRadius: 0.08, fill: { color: C.white }, line: { color: C.emerald, width: 1.2 }
  });

  s.addText('STANDARDIZED PROTOCOL', {
    x: rx + 0.3, y: 1.98, w: colW - 0.6, h: 0.28,
    fontSize: 12.5, fontFace: FONT_BODY, bold: true, color: C.emerald, tracking: 1
  });
  s.addText('Hierarchical Reciprocal Overlap Protocol', {
    x: rx + 0.3, y: 2.28, w: colW - 0.6, h: 0.42,
    fontSize: 16.5, fontFace: FONT_TITLE, bold: true, color: C.navy
  });

  const steps = [
    { num: 'Step 1', title: 'Genome Assembly LiftOver', desc: 'Standardize all gnomAD and ClinVar records to GRCh38 via UCSC LiftOver chain files.' },
    { num: 'Step 2', title: 'SV Type Concordance', desc: 'Require strict structural type matching (DEL <-> DEL, DUP <-> DUP).' },
    { num: 'Step 3', title: 'Large CNVs (> 5 kb): >= 70% Overlap', desc: 'Require reciprocal overlap: Overlap / min(Len1, Len2) >= 0.70.' },
    { num: 'Step 4', title: 'Focal SVs (500 bp – 5 kb): >= 50% Overlap', desc: 'Require reciprocal overlap >= 0.50. Non-overlapping variants assigned AF = 0.0.' }
  ];

  steps.forEach((st, idx) => {
    s.addText(st.num, {
      x: rx + 0.3, y: 2.80 + idx * 0.98, w: 1.0, h: 0.28,
      fontSize: 13, fontFace: FONT_BODY, bold: true, color: C.emerald
    });
    s.addText(st.title, {
      x: rx + 1.25, y: 2.80 + idx * 0.98, w: colW - 1.55, h: 0.28,
      fontSize: 13.5, fontFace: FONT_BODY, bold: true, color: C.navy
    });
    s.addText(st.desc, {
      x: rx + 1.25, y: 3.08 + idx * 0.98, w: colW - 1.55, h: 0.62,
      fontSize: 12.5, fontFace: FONT_BODY, color: C.slate, lineSpacingMultiple: 1.15
    });
  });
}

// =========================================================================
// SLIDE 14: FEATURE ENGINEERING & DATA LEAKAGE PREVENTION
// =========================================================================
{
  const s = pptx.addSlide();
  addSlideHeader(s, 'Methodology', 'Feature Engineering & Data Leakage Prevention', 'Neutralizing 4 critical leakage channels to guarantee unbiased generalization');
  addSlideFooter(s, 14);

  const featTable = [
    [
      { text: 'Feature Candidate', options: { bold: true, color: C.navy, fill: { color: C.cardHeaderBg } } },
      { text: 'Source', options: { bold: true, color: C.navy, fill: { color: C.cardHeaderBg } } },
      { text: 'Leakage Risk', options: { bold: true, color: C.navy, fill: { color: C.cardHeaderBg } } },
      { text: 'Engineering Decision & Rationale', options: { bold: true, color: C.navy, fill: { color: C.cardHeaderBg } } }
    ],
    [
      { text: 'log10_sv_length, sv_type', options: { bold: true, color: C.navy } },
      { text: 'Caller / Intrinsic', options: { color: C.slate } },
      { text: 'None', options: { bold: true, color: C.emerald } },
      { text: 'KEEP: Normalized genomic size and one-hot encoded biological types.', options: { color: C.slate } }
    ],
    [
      { text: 'gnomad_af, popmax_af', options: { bold: true, color: C.navy } },
      { text: 'gnomAD SV v2.1', options: { color: C.slate } },
      { text: 'None', options: { bold: true, color: C.emerald } },
      { text: 'KEEP: Population allele frequencies via >=50% reciprocal overlap.', options: { color: C.slate } }
    ],
    [
      { text: 'has_lof, is_promoter', options: { bold: true, color: C.navy } },
      { text: 'gnomAD / Ensembl', options: { color: C.slate } },
      { text: 'None', options: { bold: true, color: C.emerald } },
      { text: 'KEEP: Functional consequence flags on protein-coding genes.', options: { color: C.slate } }
    ],
    [
      { text: 'GeneSymbol (Raw text)', options: { bold: true, color: C.navy } },
      { text: 'ClinVar', options: { color: C.slate } },
      { text: 'Memorization', options: { bold: true, color: C.amber } },
      { text: 'TRANSFORM: Replace raw gene strings with pLI & LOEUF numeric constraint.', options: { color: C.slate } }
    ],
    [
      { text: 'ReviewStatus (Stars)', options: { bold: true, color: C.navy } },
      { text: 'ClinVar Metadata', options: { color: C.slate } },
      { text: 'Severe Target', options: { bold: true, color: C.red } },
      { text: 'DROP: Post-diagnostic clinical confidence rating (only exists after curation).', options: { color: C.slate } }
    ],
    [
      { text: 'PhenotypeList / Disease', options: { bold: true, color: C.navy } },
      { text: 'ClinVar Metadata', options: { color: C.slate } },
      { text: 'Catastrophic', options: { bold: true, color: C.red } },
      { text: 'DROP: Directly encodes clinical diagnosis and disease status.', options: { color: C.slate } }
    ],
    [
      { text: 'NumberSubmitters', options: { bold: true, color: C.navy } },
      { text: 'ClinVar Metadata', options: { color: C.slate } },
      { text: 'Severe Target', options: { bold: true, color: C.red } },
      { text: 'DROP: Correlates directly with clinical attention and disease severity.', options: { color: C.slate } }
    ]
  ];

  s.addTable(featTable, {
    x: MARGIN_X, y: 1.75, w: USABLE_W, h: 4.95,
    colW: [2.2, 1.8, 1.6, 6.133],
    border: { pt: 1, color: C.border },
    fontSize: 12, fontFace: FONT_BODY,
    align: 'left', valign: 'middle'
  });
}

// =========================================================================
// SLIDE 15: CHROMOSOMAL VALIDATION STRATEGY & MODELING ARCHITECTURE
// =========================================================================
{
  const s = pptx.addSlide();
  addSlideHeader(s, 'Validation Strategy', 'Chromosomal Validation & Modeling Architecture Strategy', 'Chromosomal disjoint partitioning guarantees 0.0% genomic locus leakage');
  addSlideFooter(s, 15);

  const colW = 5.66;
  const colGap = 0.41;

  // Left Column: Chromosomal Partitions
  s.addShape(pptx.ShapeType.roundRect, {
    x: MARGIN_X, y: 1.75, w: colW, h: 4.98,
    rectRadius: 0.08, fill: { color: C.white }, line: { color: C.border, width: 1 }
  });

  s.addText('CHROMOSOMAL DISJOINT PARTITIONING', {
    x: MARGIN_X + 0.3, y: 1.98, w: colW - 0.6, h: 0.28,
    fontSize: 12.5, fontFace: FONT_BODY, bold: true, color: C.blue, tracking: 1
  });
  s.addText('Zero Genomic Locus Overlap', {
    x: MARGIN_X + 0.3, y: 2.28, w: colW - 0.6, h: 0.42,
    fontSize: 16.5, fontFace: FONT_TITLE, bold: true, color: C.navy
  });

  const splits = [
    { name: 'Training Set (Chromosomes 1–14)', count: '25,158 unique SVs (~65%)', desc: 'Model parameter optimization, feature representation learning, and weight updates.' },
    { name: 'Validation Set (Chromosomes 15–18)', count: '8,546 unique SVs (~15%)', desc: 'Hyperparameter tuning, threshold selection, and probability calibration.' },
    { name: 'Holdout Test Set (Chr 19–22, X, Y)', count: '8,854 unique SVs (~20%)', desc: 'Completely unseen chromosomes to benchmark true out-of-sample generalization.' }
  ];

  splits.forEach((sp, idx) => {
    s.addText(sp.name, {
      x: MARGIN_X + 0.3, y: 2.80 + idx * 1.30, w: colW - 0.6, h: 0.28,
      fontSize: 14, fontFace: FONT_BODY, bold: true, color: C.navy
    });
    s.addText(sp.count, {
      x: MARGIN_X + 0.3, y: 3.08 + idx * 1.30, w: colW - 0.6, h: 0.28,
      fontSize: 13, fontFace: FONT_BODY, bold: true, color: C.blue
    });
    s.addText(sp.desc, {
      x: MARGIN_X + 0.3, y: 3.36 + idx * 1.30, w: colW - 0.6, h: 0.68,
      fontSize: 12.5, fontFace: FONT_BODY, color: C.slate, lineSpacingMultiple: 1.15
    });
  });

  // Right Column: Planned Model Architecture
  const rx = MARGIN_X + colW + colGap;
  s.addShape(pptx.ShapeType.roundRect, {
    x: rx, y: 1.75, w: colW, h: 4.98,
    rectRadius: 0.08, fill: { color: C.white }, line: { color: C.border, width: 1 }
  });

  s.addText('PLANNED MODEL SUITE & BENCHMARKING', {
    x: rx + 0.3, y: 1.98, w: colW - 0.6, h: 0.28,
    fontSize: 12.5, fontFace: FONT_BODY, bold: true, color: C.emerald, tracking: 1
  });
  s.addText('Ensemble Benchmarking & Explainability', {
    x: rx + 0.3, y: 2.28, w: colW - 0.6, h: 0.42,
    fontSize: 16.5, fontFace: FONT_TITLE, bold: true, color: C.navy
  });

  const models = [
    { title: 'Linear Baseline: L2-Regularized Logistic Regression', desc: 'Establishes baseline linear separability on normalized genomic features.' },
    { title: 'Bagging & Boosting Ensembles', desc: 'Balanced Random Forest, LightGBM, and XGBoost configured with scale_pos_weight = 3.4 to account for class imbalance.' },
    { title: 'Primary Metric: PR-AUC (Precision-Recall)', desc: 'Prioritizes true positive pathogenic detection over ROC-AUC under 3.4:1 imbalance.' },
    { title: 'TreeSHAP Local Explainability Engine', desc: 'Calculates exact Shapley attributions for each patient variant prediction.' }
  ];

  models.forEach((m, idx) => {
    s.addText(`•  ${m.title}`, {
      x: rx + 0.3, y: 2.80 + idx * 1.00, w: colW - 0.6, h: 0.30,
      fontSize: 13.5, fontFace: FONT_BODY, bold: true, color: C.navy
    });
    s.addText(m.desc, {
      x: rx + 0.55, y: 3.10 + idx * 1.00, w: colW - 0.85, h: 0.65,
      fontSize: 12.5, fontFace: FONT_BODY, color: C.slate, lineSpacingMultiple: 1.15
    });
  });
}

// =========================================================================
// SLIDE 16: SUMMARY OF WORK COMPLETED FOR REVIEW 1
// =========================================================================
{
  const s = pptx.addSlide();
  addSlideHeader(s, 'Milestone Status', 'Summary of Work Completed for Review 1', 'Comprehensive foundation completed (~40% milestone) for the 1st Project Review');
  addSlideFooter(s, 16);

  const pillars = [
    { num: '01', title: 'Multi-Dataset Harmonization', desc: 'Ingested and standardized 101,891 ClinVar SVs, 387,477 gnomAD population SV sites, and 79,808 dbVar calls to GRCh38 coordinates.' },
    { num: '02', title: 'VUS Bottleneck Characterization', desc: 'Quantified the 40.0% VUS barrier (N = 40,741) and structured the 3.40 : 1 binary training cohort (45,277 Pathogenic vs 13,306 Benign).' },
    { num: '03', title: 'Statistical Hypothesis Testing', desc: 'Validated biological drivers via Mann-Whitney U test (p = 3.04 x 10^-77) and Pearson\'s Chi-Square test (p = 0.0000).' },
    { num: '04', title: 'Zero-Leakage Feature Store', desc: 'Eliminated metadata and phenotype leakage; replaced high-cardinality gene strings with numeric constraint metrics (pLI, LOEUF).' },
    { num: '05', title: 'Chromosomal Validation Split', desc: 'Formulated chromosomal block holdout partitions ensuring 0.0% genomic locus leakage between training and testing folds.' }
  ];

  pillars.forEach((p, idx) => {
    const py = 1.75 + idx * 0.98;
    s.addShape(pptx.ShapeType.roundRect, {
      x: MARGIN_X, y: py, w: USABLE_W, h: 0.88,
      rectRadius: 0.08, fill: { color: C.white }, line: { color: C.border, width: 1 }
    });

    s.addText(p.num, {
      x: MARGIN_X + 0.25, y: py + 0.15, w: 0.60, h: 0.48,
      fontSize: 20, fontFace: FONT_TITLE, bold: true, color: C.blue
    });

    s.addText(p.title, {
      x: MARGIN_X + 0.95, y: py + 0.15, w: 3.4, h: 0.48,
      fontSize: 14.5, fontFace: FONT_TITLE, bold: true, color: C.navy
    });

    s.addText(p.desc, {
      x: MARGIN_X + 4.45, y: py + 0.15, w: USABLE_W - 4.70, h: 0.58,
      fontSize: 12.5, fontFace: FONT_BODY, color: C.slate, lineSpacingMultiple: 1.15
    });
  });
}

// =========================================================================
// SLIDE 17: CURRENT UNDERSTANDING & PHASE 2 ROADMAP
// =========================================================================
{
  const s = pptx.addSlide();
  addSlideHeader(s, 'Roadmap & Next Steps', 'Current Understanding & Phase 2 Roadmap', 'Key scientific insights synthesized and actionable milestones for Review 2');
  addSlideFooter(s, 17);

  // Top Box: Current Understanding
  s.addShape(pptx.ShapeType.roundRect, {
    x: MARGIN_X, y: 1.75, w: USABLE_W, h: 1.60,
    rectRadius: 0.08, fill: { color: C.blueLight }, line: { color: C.blueBorder, width: 1.2 }
  });

  s.addText('SYNTHESIZED SCIENTIFIC UNDERSTANDING', {
    x: MARGIN_X + 0.3, y: 1.92, w: USABLE_W - 0.6, h: 0.28,
    fontSize: 12, fontFace: FONT_BODY, bold: true, color: C.blue, tracking: 1
  });

  s.addText('Structural variant pathogenicity is governed by structural category (Deletions > Duplications), size-dependent coding disruption, extreme population rarity (AF < 0.1%), and gene constraint (pLI / LOEUF). To prevent artificial model memorization, post-diagnostic metadata must be strictly excluded and evaluation must be performed across disjoint chromosomes.', {
    x: MARGIN_X + 0.3, y: 2.22, w: USABLE_W - 0.6, h: 1.05,
    fontSize: 13.5, fontFace: FONT_BODY, color: C.navy, lineSpacingMultiple: 1.22
  });

  // Bottom 4 Roadmap Cards
  const rCardW = 2.70;
  const rGap = 0.31;
  const phases = [
    { phase: 'PHASE 4', title: 'Model Training', desc: 'Benchmark Logistic, Random Forest, LightGBM, and XGBoost; tune PR-AUC on holdout chromosomes.' },
    { phase: 'PHASE 5', title: 'TreeSHAP Engine', desc: 'Compute global beeswarm summary and local waterfall plots for transparent clinical interpretability.' },
    { phase: 'PHASE 6', title: 'VUS Prioritization', desc: 'Score all 40,741 ClinVar VUS variants into 4 actionable clinical risk triage tiers.' },
    { phase: 'PHASE 7', title: 'Patient CLI Tool', desc: 'Build an end-to-end command-line and web tool to prioritize long-read VCF files in clinical workflows.' }
  ];

  phases.forEach((ph, idx) => {
    const px = MARGIN_X + idx * (rCardW + rGap);
    s.addShape(pptx.ShapeType.roundRect, {
      x: px, y: 3.55, w: rCardW, h: 3.18,
      rectRadius: 0.08, fill: { color: C.white }, line: { color: C.border, width: 1 }
    });

    s.addText(ph.phase, {
      x: px + 0.2, y: 3.75, w: rCardW - 0.4, h: 0.28,
      fontSize: 12, fontFace: FONT_BODY, bold: true, color: C.blue, tracking: 1
    });

    s.addText(ph.title, {
      x: px + 0.2, y: 4.05, w: rCardW - 0.4, h: 0.42,
      fontSize: 16, fontFace: FONT_TITLE, bold: true, color: C.navy
    });

    s.addText(ph.desc, {
      x: px + 0.2, y: 4.52, w: rCardW - 0.4, h: 2.05,
      fontSize: 12.5, fontFace: FONT_BODY, color: C.slate, lineSpacingMultiple: 1.2
    });
  });
}

// =========================================================================
// SLIDE 18: REFERENCES & SCIENTIFIC LITERATURE
// =========================================================================
{
  const s = pptx.addSlide();
  addSlideHeader(s, 'References', 'References & Scientific Literature', 'Key peer-reviewed literature informing datasets, clinical standards, and algorithms');
  addSlideFooter(s, 18);

  const refs = [
    { num: '1.', authors: 'Collins, R. L., Brand, H., Karczewski, K. J., Zhao, X., Alföldi, J., et al. (2020)', title: '"A structural variation reference for medical and population genetics."', journal: 'Nature, 581(7809), 444–451.', doi: 'https://doi.org/10.1038/s41586-020-2287-8' },
    { num: '2.', authors: 'Landrum, M. J., Lee, J. M., Benson, M., Brown, G. R., Chao, C., et al. (2018)', title: '"ClinVar: improving access to variant interpretations and supporting evidence."', journal: 'Nucleic Acids Research, 46(D1), D1062–D1067.', doi: 'https://doi.org/10.1093/nar/gkx1153' },
    { num: '3.', authors: 'Riggs, E. R., Andersen, E. F., Cherry, A. M., Kantarci, S., Kearney, H., et al. (2020)', title: '"Technical standards for the interpretation and reporting of constitutional copy number variants."', journal: 'Genetics in Medicine, 22(2), 245–257.', doi: 'https://doi.org/10.1038/s41436-019-0686-8' },
    { num: '4.', authors: 'Lundberg, S. M., & Lee, S. I. (2017)', title: '"A unified approach to interpreting model predictions."', journal: 'Advances in Neural Information Processing Systems (NeurIPS 2017), 30, 4765–4774.', doi: 'https://papers.nips.cc/paper/7062-a-unified-approach-to-interpreting-model-predictions' },
    { num: '5.', authors: 'Sedlazeck, F. J., Rescheneder, P., Smolka, M., Fang, H., Nattestad, M., et al. (2018)', title: '"Accurate detection of complex structural variation using single-molecule sequencing."', journal: 'Nature Methods, 15(6), 461–468.', doi: 'https://doi.org/10.1038/s41592-018-0001-7' }
  ];

  refs.forEach((r, idx) => {
    const ry = 1.75 + idx * 0.98;
    s.addShape(pptx.ShapeType.roundRect, {
      x: MARGIN_X, y: ry, w: USABLE_W, h: 0.88,
      rectRadius: 0.08, fill: { color: C.white }, line: { color: C.border, width: 1 }
    });

    s.addText(r.num, {
      x: MARGIN_X + 0.25, y: ry + 0.15, w: 0.40, h: 0.48,
      fontSize: 14.5, fontFace: FONT_TITLE, bold: true, color: C.blue
    });

    s.addText(`${r.authors} ${r.title} — ${r.journal}`, {
      x: MARGIN_X + 0.70, y: ry + 0.12, w: USABLE_W - 0.95, h: 0.42,
      fontSize: 12.5, fontFace: FONT_BODY, bold: true, color: C.navy
    });

    s.addText(r.doi, {
      x: MARGIN_X + 0.70, y: ry + 0.50, w: USABLE_W - 0.95, h: 0.28,
      fontSize: 11.5, fontFace: FONT_BODY, color: C.blue
    });
  });
}

// Generate the presentation file
const outputPath = path.resolve(__dirname, 'Review_1_Presentation.pptx');
pptx.writeFile({ fileName: outputPath })
  .then(() => {
    console.log(`[SUCCESS] Presentation with larger font sizes successfully written to: ${outputPath}`);
  })
  .catch(err => {
    console.error(`[ERROR] Failed to write presentation:`, err);
    process.exit(1);
  });
