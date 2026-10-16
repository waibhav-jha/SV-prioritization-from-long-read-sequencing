const pptxgen = require('pptxgenjs');
const fs = require('fs');
const path = require('path');

const pptx = new pptxgen();

// Layout: Widescreen 16:9 (13.333 x 7.5 inches)
pptx.layout = 'LAYOUT_WIDE';
pptx.author = 'Group 15';
pptx.company = 'Department of Computer Science and Engineering';
pptx.title = 'AI-Based Structural Variant Prioritization from Long-Read Sequencing Using Explainable Machine Learning';
pptx.subject = 'Final Capstone Project Review Presentation';

// Color Palette Tokens
const C = {
  bg: 'F8FAFC',          // Light background
  white: 'FFFFFF',       // Card background
  navy: '0F172A',        // Main text & deep headers
  slate: '334155',       // Body text
  muted: '64748B',       // Subtitles & captions
  border: 'CBD5E1',      // Card borders
  blue: '2563EB',        // Primary accent
  blueLight: 'EFF6FF',   // Pill / soft badge bg
  blueBorder: 'BFDBFE',  // Pill border
  emerald: '059669',     // Positive / completed
  emeraldLight: 'ECFDF5',// Emerald soft badge bg
  amber: 'D97706',       // VUS / Warning
  amberLight: 'FFFBEB',  // Amber soft badge bg
  red: 'DC2626',         // Pathogenic / Critical
  redLight: 'FEF2F2',    // Red soft badge bg
  purple: '7C3AED',      // Deep Learning / Multimodal
  purpleLight: 'F5F3FF', // Purple soft badge bg
  cardHeaderBg: 'F1F5F9' // Table / card header bg
};

const FONT_TITLE = 'Calibri';
const FONT_BODY = 'Calibri';

const MARGIN_X = 0.8;
const USABLE_W = 11.733;
const TOTAL_SLIDES = 24;

// Standard Slide Header
function addSlideHeader(slide, category, title, subtitle) {
  slide.background = { color: C.bg };

  slide.addText(category.toUpperCase(), {
    x: MARGIN_X, y: 0.38, w: USABLE_W, h: 0.28,
    fontSize: 12, fontFace: FONT_BODY, bold: true,
    color: C.blue, tracking: 1.5
  });

  slide.addText(title, {
    x: MARGIN_X, y: 0.68, w: USABLE_W, h: 0.50,
    fontSize: 22, fontFace: FONT_TITLE, bold: true,
    color: C.navy, margin: 0
  });

  if (subtitle) {
    slide.addText(subtitle, {
      x: MARGIN_X, y: 1.20, w: USABLE_W, h: 0.32,
      fontSize: 14, fontFace: FONT_BODY,
      color: C.muted, margin: 0
    });
  }

  slide.addShape(pptx.ShapeType.line, {
    x: MARGIN_X, y: 1.56, w: USABLE_W, h: 0,
    line: { color: C.border, width: 1.0 }
  });
}

// Standard Slide Footer
function addSlideFooter(slide, current, total = TOTAL_SLIDES) {
  slide.addText('Group 15  |  Final Project Review  |  AI-Based Structural Variant Prioritization', {
    x: MARGIN_X, y: 6.95, w: 8.5, h: 0.32,
    fontSize: 11, fontFace: FONT_BODY, color: C.muted
  });
  slide.addText(`Slide ${current} of ${total}`, {
    x: 10.333, y: 6.95, w: 2.2, h: 0.32,
    fontSize: 11, fontFace: FONT_BODY, color: C.muted, align: 'right'
  });
}

// Metric Callout Card Helper
function addMetricCard(slide, x, y, w, h, number, label, subtext, color = C.blue) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x, y, w, h, rectRadius: 0.08,
    fill: { color: C.white },
    line: { color: C.border, width: 1.0 }
  });

  slide.addText(number, {
    x: x + 0.25, y: y + 0.15, w: w - 0.5, h: 0.65,
    fontSize: 32, fontFace: FONT_TITLE, bold: true, color: color, margin: 0
  });

  slide.addText(label, {
    x: x + 0.25, y: y + 0.82, w: w - 0.5, h: 0.35,
    fontSize: 13.5, fontFace: FONT_BODY, bold: true, color: C.navy, margin: 0
  });

  if (subtext) {
    slide.addText(subtext, {
      x: x + 0.25, y: y + 1.20, w: w - 0.5, h: h - 1.30,
      fontSize: 11.5, fontFace: FONT_BODY, color: C.muted, margin: 0
    });
  }
}

// =========================================================================
// SLIDE 1: Title Slide
// =========================================================================
{
  const s = pptx.addSlide();
  s.background = { color: '0F172A' };

  s.addText('FINAL PROJECT REVIEW  |  ACADEMIC PRESENTATION', {
    x: MARGIN_X, y: 0.90, w: USABLE_W, h: 0.35,
    fontSize: 13, fontFace: FONT_BODY, bold: true, color: '60A5FA', tracking: 2
  });

  s.addText('AI-Based Structural Variant Prioritization from Long-Read Sequencing Using Explainable Machine Learning', {
    x: MARGIN_X, y: 1.35, w: USABLE_W, h: 1.60,
    fontSize: 28, fontFace: FONT_TITLE, bold: true, color: 'FFFFFF', lineSpacingMultiple: 1.15
  });

  s.addShape(pptx.ShapeType.line, {
    x: MARGIN_X, y: 3.10, w: 4.0, h: 0,
    line: { color: '38BDF8', width: 2.5 }
  });

  s.addText('A Deep Learning & Multimodal Framework with Conformal Risk Guarantees and TreeSHAP Explainability for Clinical Diagnostics', {
    x: MARGIN_X, y: 3.30, w: USABLE_W, h: 0.70,
    fontSize: 15, fontFace: FONT_BODY, color: '94A3B8', lineSpacingMultiple: 1.1
  });

  const cardW = (USABLE_W - 0.9) / 4;
  const cards = [
    { label: 'PROJECT GROUP', val: 'Group 15\nB.Tech Final Year' },
    { label: 'DEPARTMENT', val: 'Department of Computer Science\nand Engineering' },
    { label: 'DATA MATRIX', val: 'ClinVar (101k SVs)\ngnomAD SV v2.1 (387k)' },
    { label: 'VALIDATION', val: 'Chr 19-22, X, Y Holdout\n0.0% Locus Overlap' }
  ];

  cards.forEach((c, idx) => {
    const x = MARGIN_X + idx * (cardW + 0.3);
    s.addShape(pptx.ShapeType.roundRect, {
      x, y: 4.60, w: cardW, h: 1.85, rectRadius: 0.08,
      fill: { color: '1E293B' },
      line: { color: '334155', width: 1.0 }
    });

    s.addText(c.label, {
      x: x + 0.25, y: 4.80, w: cardW - 0.5, h: 0.28,
      fontSize: 11, fontFace: FONT_BODY, bold: true, color: '38BDF8', tracking: 1
    });

    s.addText(c.val, {
      x: x + 0.25, y: 5.18, w: cardW - 0.5, h: 1.10,
      fontSize: 13, fontFace: FONT_BODY, color: 'F8FAFC', lineSpacingMultiple: 1.15
    });
  });
}

// =========================================================================
// SLIDE 2: Introduction
// =========================================================================
{
  const s = pptx.addSlide();
  addSlideHeader(s, 'Background', 'Introduction: Third-Generation Long-Read Sequencing', 'Long-read sequencing resolves dark genomic regions but introduces vast interpretation challenges');
  addSlideFooter(s, 2);

  const cardW = (USABLE_W - 0.6) / 3;
  const cards = [
    {
      title: 'Long-Read Sequencing Revolution',
      subtitle: 'PacBio HiFi & Oxford Nanopore',
      points: [
        'Single-molecule long reads (>10,000–25,000 bp) span repetitive genomic regions.',
        'Overcomes short-read mapping blindness in tandem repeats and segmental duplications.',
        'Routinely uncovers >25,000 structural variants (>= 50 bp) per individual genome.'
      ],
      color: C.blue
    },
    {
      title: 'Structural Variant Impact',
      subtitle: 'Pathogenicity & Disease Burden',
      points: [
        'SVs alter more total base pairs than all single-nucleotide variants (SNVs) combined.',
        'Primary drivers of rare congenital diseases, autism, developmental delay, and cancer.',
        'Include complex deletions, duplications, inversions, translocations, and insertions.'
      ],
      color: C.purple
    },
    {
      title: 'The Clinical Triage Bottleneck',
      subtitle: 'Automated Scoring Deficit',
      points: [
        'Overwhelming volume of candidate SVs in clinical long-read VCF files.',
        'Existing clinical tools focus almost exclusively on SNVs (CADD, REVEL, SIFT).',
        'Urgent need for automated, explainable machine learning prioritization algorithms.'
      ],
      color: C.emerald
    }
  ];

  cards.forEach((c, idx) => {
    const x = MARGIN_X + idx * (cardW + 0.3);
    s.addShape(pptx.ShapeType.roundRect, {
      x, y: 1.85, w: cardW, h: 4.80, rectRadius: 0.08,
      fill: { color: C.white }, line: { color: C.border, width: 1.0 }
    });

    s.addText(c.title, {
      x: x + 0.3, y: 2.15, w: cardW - 0.6, h: 0.60,
      fontSize: 18, fontFace: FONT_TITLE, bold: true, color: C.navy, margin: 0
    });

    s.addText(c.subtitle, {
      x: x + 0.3, y: 2.78, w: cardW - 0.6, h: 0.28,
      fontSize: 12.5, fontFace: FONT_BODY, bold: true, color: c.color, margin: 0
    });

    s.addShape(pptx.ShapeType.line, {
      x: x + 0.3, y: 3.15, w: cardW - 0.6, h: 0,
      line: { color: C.border, width: 1.0 }
    });

    const bText = c.points.map((p, i) => ({
      text: p,
      options: { bullet: true, breakLine: i < c.points.length - 1, fontSize: 13, color: C.slate, fontFace: FONT_BODY, paraSpaceAfter: 12 }
    }));

    s.addText(bText, {
      x: x + 0.3, y: 3.35, w: cardW - 0.6, h: 3.10, margin: 0
    });
  });
}

// =========================================================================
// SLIDE 3: Problem Statement
// =========================================================================
{
  const s = pptx.addSlide();
  addSlideHeader(s, 'Problem Formulation', 'Problem Statement: High-Dimensional Variant Ambiguity', 'Critical computational gaps preventing routine clinical adoption of long-read sequencing');
  addSlideFooter(s, 3);

  const cardW = (USABLE_W - 0.6) / 3;
  const cards = [
    {
      num: '01',
      title: 'Tool & Method Inadequacy',
      desc: 'Over 90% of current pathogenicity scoring tools are engineered exclusively for SNVs or micro-indels (<50 bp). They fail to model multi-kilobase structural context, exon-spanning disruptions, and topological chromatin domain boundaries.',
      color: C.red
    },
    {
      num: '02',
      title: 'Genomic Data Leakage',
      desc: 'Prior studies evaluate SV prioritization using naive random k-fold train/test splits. Overlapping variants from identical genomic loci or genes leak between folds, producing artificially inflated benchmark metrics that fail on real patients.',
      color: C.amber
    },
    {
      num: '03',
      title: 'Lack of Certified Safety',
      desc: 'Conventional AI models output uncalibrated probability scores without uncertainty quantification. In high-stakes clinical diagnostics, arbitrary cutoffs risk missing pathogenic mutations or triggering costly unnecessary medical interventions.',
      color: C.blue
    }
  ];

  cards.forEach((c, idx) => {
    const x = MARGIN_X + idx * (cardW + 0.3);
    s.addShape(pptx.ShapeType.roundRect, {
      x, y: 1.85, w: cardW, h: 4.80, rectRadius: 0.08,
      fill: { color: C.white }, line: { color: C.border, width: 1.0 }
    });

    s.addText(c.num, {
      x: x + 0.3, y: 2.15, w: cardW - 0.6, h: 0.45,
      fontSize: 26, fontFace: FONT_TITLE, bold: true, color: c.color, margin: 0
    });

    s.addText(c.title, {
      x: x + 0.3, y: 2.65, w: cardW - 0.6, h: 0.65,
      fontSize: 18, fontFace: FONT_TITLE, bold: true, color: C.navy, margin: 0
    });

    s.addShape(pptx.ShapeType.line, {
      x: x + 0.3, y: 3.35, w: cardW - 0.6, h: 0,
      line: { color: C.border, width: 1.0 }
    });

    s.addText(c.desc, {
      x: x + 0.3, y: 3.60, w: cardW - 0.6, h: 2.80,
      fontSize: 13.5, fontFace: FONT_BODY, color: C.slate, lineSpacingMultiple: 1.25, margin: 0
    });
  });
}

// =========================================================================
// SLIDE 4: Clinical Motivation
// =========================================================================
{
  const s = pptx.addSlide();
  addSlideHeader(s, 'Clinical Relevance', 'Clinical Motivation: Resolving the 40% VUS Dilemma', 'Transforming non-actionable genomic findings into certified diagnostic intelligence');
  addSlideFooter(s, 4);

  addMetricCard(s, MARGIN_X, 1.85, 4.3, 1.45, '~40%', 'Variants of Uncertain Significance', 'Up to 40% of discovered patient SVs cannot be clinically classified.', C.red);
  addMetricCard(s, MARGIN_X, 3.50, 4.3, 1.45, '>45 min', 'Manual Review per Variant', 'Exhaustive cytogenetic and PubMed literature searches stall reporting.', C.amber);
  addMetricCard(s, MARGIN_X, 5.15, 4.3, 1.50, '4.2s', 'Automated AI Pipeline Delivery', 'Our proposed workflow ranks and explains candidate variants in seconds.', C.emerald);

  s.addShape(pptx.ShapeType.roundRect, {
    x: 5.4, y: 1.85, w: 7.133, h: 4.80, rectRadius: 0.08,
    fill: { color: C.white }, line: { color: C.border, width: 1.0 }
  });

  s.addText('CLINICAL IMPLICATIONS & IMPACT', {
    x: 5.7, y: 2.15, w: 6.5, h: 0.28,
    fontSize: 12, fontFace: FONT_BODY, bold: true, color: C.blue, tracking: 1
  });

  s.addText('Why Solving VUS Prioritization is Paramount', {
    x: 5.7, y: 2.48, w: 6.5, h: 0.40,
    fontSize: 19, fontFace: FONT_TITLE, bold: true, color: C.navy, margin: 0
  });

  s.addShape(pptx.ShapeType.line, {
    x: 5.7, y: 2.95, w: 6.5, h: 0, line: { color: C.border, width: 1.0 }
  });

  const clinicalPoints = [
    { title: 'Delayed Medical Interventions:', desc: 'When a candidate mutation is tagged as VUS, oncologists and medical geneticists cannot prescribe targeted therapy or gene-editing treatments.' },
    { title: 'Severe Diagnostic Backlog:', desc: 'Clinical geneticists spend hours cross-referencing population frequencies, constraint metrics, and gene catalogs for hundreds of variants per patient.' },
    { title: 'Explainability Requirement:', desc: 'Clinicians cannot trust black-box neural scores. Automated prioritization must supply local biological feature attributions for hospital board validation.' }
  ];

  let currY = 3.15;
  clinicalPoints.forEach(cp => {
    s.addText([
      { text: cp.title + ' ', options: { bold: true, color: C.navy, fontSize: 13.5 } },
      { text: cp.desc, options: { color: C.slate, fontSize: 13 } }
    ], {
      x: 5.7, y: currY, w: 6.5, h: 1.0, margin: 0, lineSpacingMultiple: 1.2
    });
    currY += 1.15;
  });
}

// =========================================================================
// SLIDE 5: Literature Review
// =========================================================================
{
  const s = pptx.addSlide();
  addSlideHeader(s, 'State of the Art', 'Literature Review: Genomic Variant Interpretation', 'Foundational scientific milestones and existing scoring methodologies');
  addSlideFooter(s, 5);

  const tableRows = [
    [
      { text: 'Study & Year', options: { bold: true, color: 'FFFFFF', fill: { color: '1E293B' }, fontSize: 12 } },
      { text: 'Methodology', options: { bold: true, color: 'FFFFFF', fill: { color: '1E293B' }, fontSize: 12 } },
      { text: 'Key Findings & Strengths', options: { bold: true, color: 'FFFFFF', fill: { color: '1E293B' }, fontSize: 12 } },
      { text: 'Inherent Limitations', options: { bold: true, color: 'FFFFFF', fill: { color: '1E293B' }, fontSize: 12 } }
    ],
    [
      { text: 'Collins et al.\n(Nature 2020)', options: { bold: true, color: C.navy, fontSize: 11.5 } },
      { text: 'gnomAD SV v2.1 Population Catalog', options: { color: C.slate, fontSize: 11.5 } },
      { text: 'Mapped 387,700 SVs across 14,891 genomes; established allele frequency baseline.', options: { color: C.slate, fontSize: 11 } },
      { text: 'Purely reference catalog; lacks disease pathogenicity predictive scoring.', options: { color: C.slate, fontSize: 11 } }
    ],
    [
      { text: 'Rentzsch et al.\n(Genome Bio 2020)', options: { bold: true, color: C.navy, fontSize: 11.5 } },
      { text: 'CADD-SV Regional Scoring', options: { color: C.slate, fontSize: 11.5 } },
      { text: 'Integrates functional genomics and conservation tracks for large deletions.', options: { color: C.slate, fontSize: 11 } },
      { text: 'Linear kernel; struggles with non-coding complex balanced rearrangements.', options: { color: C.slate, fontSize: 11 } }
    ],
    [
      { text: 'Landrum et al.\n(NAR 2024)', options: { bold: true, color: C.navy, fontSize: 11.5 } },
      { text: 'NCBI ClinVar Database', options: { color: C.slate, fontSize: 11.5 } },
      { text: 'Gold-standard repository of 100k+ expert-asserted variant-disease records.', options: { color: C.slate, fontSize: 11 } },
      { text: 'Suffers from heavy class imbalance and unclassified VUS backlog.', options: { color: C.slate, fontSize: 11 } }
    ],
    [
      { text: 'Lundberg et al.\n(Nat MI 2020)', options: { bold: true, color: C.navy, fontSize: 11.5 } },
      { text: 'TreeSHAP Attribution', options: { color: C.slate, fontSize: 11.5 } },
      { text: 'Game-theoretic local Shapley attributions for complex tree ensembles.', options: { color: C.slate, fontSize: 11 } },
      { text: 'Diagnostic tool only; requires integration into end-to-end clinical pipelines.', options: { color: C.slate, fontSize: 11 } }
    ]
  ];

  s.addTable(tableRows, {
    x: MARGIN_X, y: 1.85, w: USABLE_W, h: 4.80,
    colW: [2.2, 2.5, 3.8, 3.233],
    border: { pt: 1, color: C.border },
    align: 'left', valign: 'middle'
  });
}

// =========================================================================
// SLIDE 6: Research Gap
// =========================================================================
{
  const s = pptx.addSlide();
  addSlideHeader(s, 'Research Motivation', 'Research Gap: Critical Unaddressed Challenges', 'Three major limitations in current genomic machine learning frameworks');
  addSlideFooter(s, 6);

  const cardW = (USABLE_W - 0.6) / 3;
  const cards = [
    {
      gap: 'GAP 1: EVALUATION INTEGRITY',
      title: 'Genomic Locus Leakage in Cross-Validation',
      desc: 'Most published genomic AI models evaluate performance using standard random splits. Because structural variants frequently cluster around recombination hotspots and shared genes, variants from the same locus appear in both training and test sets. This causes severe data leakage and artificially inflated performance estimates.',
      color: C.red
    },
    {
      gap: 'GAP 2: REPRESENTATION RIGIDITY',
      title: 'Tree Step-Function Discretization',
      desc: 'Popular gradient boosted trees (XGBoost, LightGBM) split continuous features using axis-aligned orthogonal boundaries. However, population allele frequencies follow continuous exponential decays under purifying selection. Decision trees fail to smoothly represent these manifolds, resulting in elevated false negative rates.',
      color: C.purple
    },
    {
      gap: 'GAP 3: CLINICAL UNCERTAINTY',
      title: 'Lack of Certified Risk Guarantees',
      desc: 'Existing algorithms output point probability estimates and apply subjective classification thresholds (e.g. tau = 0.50). In clinical genetics, subjective thresholds fail to distinguish between well-calibrated confidence and epistemic uncertainty, lacking distribution-free mathematical coverage guarantees.',
      color: C.blue
    }
  ];

  cards.forEach((c, idx) => {
    const x = MARGIN_X + idx * (cardW + 0.3);
    s.addShape(pptx.ShapeType.roundRect, {
      x, y: 1.85, w: cardW, h: 4.80, rectRadius: 0.08,
      fill: { color: C.white }, line: { color: C.border, width: 1.0 }
    });

    s.addText(c.gap, {
      x: x + 0.3, y: 2.10, w: cardW - 0.6, h: 0.28,
      fontSize: 10.5, fontFace: FONT_BODY, bold: true, color: c.color, tracking: 1
    });

    s.addText(c.title, {
      x: x + 0.3, y: 2.42, w: cardW - 0.6, h: 0.65,
      fontSize: 18, fontFace: FONT_TITLE, bold: true, color: C.navy, margin: 0
    });

    s.addShape(pptx.ShapeType.line, {
      x: x + 0.3, y: 3.15, w: cardW - 0.6, h: 0,
      line: { color: C.border, width: 1.0 }
    });

    s.addText(c.desc, {
      x: x + 0.3, y: 3.35, w: cardW - 0.6, h: 3.0,
      fontSize: 13, fontFace: FONT_BODY, color: C.slate, lineSpacingMultiple: 1.25, margin: 0
    });
  });
}

// =========================================================================
// SLIDE 7: Aim, Objectives and Contributions
// =========================================================================
{
  const s = pptx.addSlide();
  addSlideHeader(s, 'Project Scope', 'Aim, Objectives and Contributions', 'Formal project scope, methodology objectives, and achieved scientific contributions');
  addSlideFooter(s, 7);

  // Left Side: Aim & Objectives
  s.addShape(pptx.ShapeType.roundRect, {
    x: MARGIN_X, y: 1.85, w: 5.65, h: 4.80, rectRadius: 0.08,
    fill: { color: C.white }, line: { color: C.border, width: 1.0 }
  });

  s.addText('PRIMARY AIM & OBJECTIVES', {
    x: MARGIN_X + 0.3, y: 2.10, w: 5.05, h: 0.28,
    fontSize: 11.5, fontFace: FONT_BODY, bold: true, color: C.blue, tracking: 1
  });

  s.addText('Engineering Objectives', {
    x: MARGIN_X + 0.3, y: 2.40, w: 5.05, h: 0.40,
    fontSize: 18, fontFace: FONT_TITLE, bold: true, color: C.navy, margin: 0
  });

  s.addShape(pptx.ShapeType.line, {
    x: MARGIN_X + 0.3, y: 2.85, w: 5.05, h: 0, line: { color: C.border, width: 1.0 }
  });

  const objs = [
    'Harmonize multi-source genomic databases (ClinVar, gnomAD SV, 1000G) via 50% reciprocal overlap.',
    'Formulate a 24-dimensional non-leaking feature vector with strict chromosomal disjoint holdouts.',
    'Architect Deep Tabular ResNet and Multimodal Sequence-Epigenetics neural networks.',
    'Deploy Split Conformal Prediction (95% certified coverage) and TreeSHAP explainability in a production CLI tool.'
  ];

  const objText = objs.map((o, i) => ({
    text: o,
    options: { bullet: true, breakLine: i < objs.length - 1, fontSize: 12.5, color: C.slate, fontFace: FONT_BODY, paraSpaceAfter: 10 }
  }));

  s.addText(objText, {
    x: MARGIN_X + 0.3, y: 3.05, w: 5.05, h: 3.35, margin: 0
  });

  // Right Side: Contributions
  s.addShape(pptx.ShapeType.roundRect, {
    x: 6.883, y: 1.85, w: 5.65, h: 4.80, rectRadius: 0.08,
    fill: { color: C.white }, line: { color: C.border, width: 1.0 }
  });

  s.addText('KEY SCIENTIFIC CONTRIBUTIONS', {
    x: 7.183, y: 2.10, w: 5.05, h: 0.28,
    fontSize: 11.5, fontFace: FONT_BODY, bold: true, color: C.emerald, tracking: 1
  });

  s.addText('Demonstrated Outcomes', {
    x: 7.183, y: 2.40, w: 5.05, h: 0.40,
    fontSize: 18, fontFace: FONT_TITLE, bold: true, color: C.navy, margin: 0
  });

  s.addShape(pptx.ShapeType.line, {
    x: 7.183, y: 2.85, w: 5.05, h: 0, line: { color: C.border, width: 1.0 }
  });

  const contribs = [
    'Eliminated Genomic Leakage: Enforced 0.0% locus overlap via Chr 19–22, X, Y disjoint testing.',
    'Benchmark Superiority: Peak 0.9705 PR-AUC and 94.4% clinical sensitivity on unseen chromosomes.',
    'Drastic False Negative Reduction: Slashed missed pathogenic variants from 1,745 down to 414 (>60% reduction).',
    'Clinical Backlog Triage: Resolved 48.8% of 34,466 ClinVar VUS into actionable risk tiers.'
  ];

  const contribText = contribs.map((c, i) => ({
    text: c,
    options: { bullet: true, breakLine: i < contribs.length - 1, fontSize: 12.5, color: C.slate, fontFace: FONT_BODY, paraSpaceAfter: 10 }
  }));

  s.addText(contribText, {
    x: 7.183, y: 3.05, w: 5.05, h: 3.35, margin: 0
  });
}

// =========================================================================
// SLIDE 8: Proposed System Architecture
// =========================================================================
{
  const s = pptx.addSlide();
  addSlideHeader(s, 'System Architecture', 'Proposed System Architecture', 'Modular end-to-end framework translating patient sequencing data into actionable clinical intelligence');
  addSlideFooter(s, 8);

  const steps = [
    {
      num: '01', title: 'Data Ingestion', sub: 'Multi-Source Integration',
      points: [
        'Parse Sniffles2/cuteSV long-read VCFs',
        'Filter high-confidence SVs (>= 50 bp)',
        '50% reciprocal coordinate overlap',
        'Ingest ClinVar & gnomAD SV catalogs'
      ],
      color: C.blue
    },
    {
      num: '02', title: 'Feature Vector', sub: 'Zero-Leakage Engineering',
      points: [
        'Compute 24 biological features',
        'gnomAD global AF & 7 continental AFs',
        'pLI haploinsufficiency & LOEUF scores',
        'Chromosomal disjoint holdout split'
      ],
      color: C.navy
    },
    {
      num: '03', title: 'Dual-Paradigm AI', sub: 'DL & Multimodal Inference',
      points: [
        'PyTorch Tabular ResNet (skip connects)',
        'Multimodal Net (DNA seq + 5mC)',
        'Outputs continuous calibrated index',
        '94.4% clinical sensitivity'
      ],
      color: C.purple
    },
    {
      num: '04', title: 'Clinical Safety', sub: 'Certified Explainability',
      points: [
        'Split Conformal Prediction (95% guarantee)',
        'Local TreeSHAP waterfall attributions',
        'Production CLI tool (prioritize_sv.py)',
        'Interactive HTML & triage queue export'
      ],
      color: C.emerald
    }
  ];

  const colW = (USABLE_W - 0.9) / 4;
  steps.forEach((st, idx) => {
    const x = MARGIN_X + idx * (colW + 0.3);
    s.addShape(pptx.ShapeType.roundRect, {
      x, y: 1.85, w: colW, h: 4.80, rectRadius: 0.08,
      fill: { color: C.white }, line: { color: C.border, width: 1.0 }
    });

    s.addShape(pptx.ShapeType.roundRect, {
      x: x + 0.25, y: 2.10, w: 0.70, h: 0.40, rectRadius: 0.06,
      fill: { color: st.color === C.blue ? C.blueLight : (st.color === C.purple ? C.purpleLight : (st.color === C.emerald ? C.emeraldLight : C.cardHeaderBg)) },
      line: { color: st.color, width: 1.0 }
    });
    s.addText(st.num, {
      x: x + 0.25, y: 2.10, w: 0.70, h: 0.40,
      fontSize: 14, fontFace: FONT_TITLE, bold: true, color: st.color, align: 'center', margin: 0
    });

    s.addText(st.title, {
      x: x + 0.25, y: 2.65, w: colW - 0.5, h: 0.40,
      fontSize: 17, fontFace: FONT_TITLE, bold: true, color: C.navy, margin: 0
    });

    s.addText(st.sub, {
      x: x + 0.25, y: 3.05, w: colW - 0.5, h: 0.28,
      fontSize: 12, fontFace: FONT_BODY, bold: true, color: C.muted, margin: 0
    });

    s.addShape(pptx.ShapeType.line, {
      x: x + 0.25, y: 3.42, w: colW - 0.5, h: 0, line: { color: C.border, width: 1.0 }
    });

    const bulletText = st.points.map((p, i) => ({
      text: p,
      options: { bullet: true, breakLine: i < st.points.length - 1, fontSize: 12.5, color: C.slate, fontFace: FONT_BODY, paraSpaceAfter: 10 }
    }));

    s.addText(bulletText, {
      x: x + 0.25, y: 3.60, w: colW - 0.5, h: 2.85, margin: 0
    });
  });
}

// =========================================================================
// SLIDE 9: Dataset Description and Sources
// =========================================================================
{
  const s = pptx.addSlide();
  addSlideHeader(s, 'Genomic Repositories', 'Dataset Description and Sources', 'Multi-cohort genomic databases underpinning model development and independent validation');
  addSlideFooter(s, 9);

  const tableRows = [
    [
      { text: 'Source Database', options: { bold: true, color: 'FFFFFF', fill: { color: '1E293B' }, fontSize: 12 } },
      { text: 'Total Variants', options: { bold: true, color: 'FFFFFF', fill: { color: '1E293B' }, fontSize: 12 } },
      { text: 'Genomic Scope', options: { bold: true, color: 'FFFFFF', fill: { color: '1E293B' }, fontSize: 12 } },
      { text: 'Role in Pipeline', options: { bold: true, color: 'FFFFFF', fill: { color: '1E293B' }, fontSize: 12 } }
    ],
    [
      { text: 'NCBI ClinVar (2024)', options: { bold: true, color: C.navy, fontSize: 11.5 } },
      { text: '101,232 SVs', options: { color: C.slate, fontSize: 11.5, bold: true } },
      { text: 'Deletions, Duplications, Inversions, Insertions', options: { color: C.slate, fontSize: 11 } },
      { text: 'Clinical ground-truth labels (Pathogenic vs Benign)', options: { color: C.slate, fontSize: 11 } }
    ],
    [
      { text: 'gnomAD SV v2.1', options: { bold: true, color: C.navy, fontSize: 11.5 } },
      { text: '387,700 SVs', options: { color: C.slate, fontSize: 11.5, bold: true } },
      { text: '14,891 genomes across 7 continental populations', options: { color: C.slate, fontSize: 11 } },
      { text: 'Baseline allele frequency spectrum and PopMax', options: { color: C.slate, fontSize: 11 } }
    ],
    [
      { text: '1000 Genomes (Phase 3)', options: { bold: true, color: C.navy, fontSize: 11.5 } },
      { text: '68,818 SVs', options: { color: C.slate, fontSize: 11.5, bold: true } },
      { text: '2,504 multi-ethnic individuals', options: { color: C.slate, fontSize: 11 } },
      { text: 'Independent cross-validation for polymorphic SVs', options: { color: C.slate, fontSize: 11 } }
    ],
    [
      { text: 'Final Harmonized Matrix', options: { bold: true, color: C.blue, fontSize: 12, fill: { color: C.blueLight } } },
      { text: '44,268 SVs', options: { color: C.blue, fontSize: 12, bold: true, fill: { color: C.blueLight } } },
      { text: 'High-confidence labeled cohort (>= 50 bp)', options: { color: C.blue, fontSize: 11.5, fill: { color: C.blueLight } } },
      { text: '35,414 Train / 8,854 Chromosomal Holdout Test', options: { color: C.blue, fontSize: 11.5, bold: true, fill: { color: C.blueLight } } }
    ]
  ];

  s.addTable(tableRows, {
    x: MARGIN_X, y: 1.85, w: USABLE_W, h: 4.80,
    colW: [2.5, 1.8, 3.8, 3.633],
    border: { pt: 1, color: C.border },
    align: 'left', valign: 'middle'
  });
}

// =========================================================================
// SLIDE 10: Data Preprocessing and Harmonization
// =========================================================================
{
  const s = pptx.addSlide();
  addSlideHeader(s, 'Data Engineering', 'Data Preprocessing and Harmonization', 'Standardizing heterogeneous multi-database coordinates and resolving interval overlaps');
  addSlideFooter(s, 10);

  const cardW = (USABLE_W - 0.6) / 3;
  const cards = [
    {
      title: 'Coordinate Standardization',
      subtitle: 'GRCh38 Reference Genome',
      desc: 'All coordinates were mapped to the GRCh38/hg38 human reference assembly. Chromosomal nomenclature was unified to strict numerical and sex chromosomes (chr1–chr22, chrX, chrY). Unplaced contigs and centromeric gaps were pruned.',
      color: C.blue
    },
    {
      title: '50% Reciprocal Overlap',
      subtitle: 'Precise Interval Matching',
      desc: 'Variants between patient VCFs and gnomAD are matched strictly using reciprocal coordinate overlap: (A ∩ B) / size(A) >= 0.50 and (A ∩ B) / size(B) >= 0.50. Prevents spurious cross-matches between adjacent distinct variants.',
      color: C.purple
    },
    {
      title: 'Label Consolidation',
      subtitle: 'Binary Ground Truth Matrix',
      desc: 'ClinVar assertions were mapped to binary ground truth: Pathogenic & Likely Pathogenic (Y = 1); Benign & Likely Benign (Y = 0). Ambiguous VUS records (N = 34,466) were segregated for post-training downstream clinical triage.',
      color: C.emerald
    }
  ];

  cards.forEach((c, idx) => {
    const x = MARGIN_X + idx * (cardW + 0.3);
    s.addShape(pptx.ShapeType.roundRect, {
      x, y: 1.85, w: cardW, h: 4.80, rectRadius: 0.08,
      fill: { color: C.white }, line: { color: C.border, width: 1.0 }
    });

    s.addText(c.title, {
      x: x + 0.3, y: 2.15, w: cardW - 0.6, h: 0.65,
      fontSize: 18, fontFace: FONT_TITLE, bold: true, color: C.navy, margin: 0
    });

    s.addText(c.subtitle, {
      x: x + 0.3, y: 2.80, w: cardW - 0.6, h: 0.28,
      fontSize: 12.5, fontFace: FONT_BODY, bold: true, color: c.color, margin: 0
    });

    s.addShape(pptx.ShapeType.line, {
      x: x + 0.3, y: 3.15, w: cardW - 0.6, h: 0, line: { color: C.border, width: 1.0 }
    });

    s.addText(c.desc, {
      x: x + 0.3, y: 3.35, w: cardW - 0.6, h: 3.0,
      fontSize: 13.5, fontFace: FONT_BODY, color: C.slate, lineSpacingMultiple: 1.25, margin: 0
    });
  });
}

// =========================================================================
// SLIDE 11: Exploratory Genomic Data Analysis
// =========================================================================
{
  const s = pptx.addSlide();
  addSlideHeader(s, 'Genomic Analysis', 'Exploratory Genomic Data Analysis', 'Strong biological divergence between pathogenic and benign structural variants confirms ML signal');
  addSlideFooter(s, 11);

  const cardW = (USABLE_W - 0.6) / 3;
  const cards = [
    {
      title: 'Variant Type Dominance',
      subtitle: 'Deletions vs Duplications',
      stat: '58.1%',
      statLabel: 'Deletions in Pathogenic SVs',
      detail: 'Deletions dominate pathogenic assertions because loss of coding exons causes irreversible haploinsufficiency. Duplications (40.7%) are more frequently tolerated as copy-number polymorphisms unless overlapping dosage-sensitive genes.',
      color: C.blue
    },
    {
      title: 'Bimodal Size Distribution',
      subtitle: 'Retrotransposon Hotspots',
      stat: '~300 bp & ~6 kb',
      statLabel: 'Distinct Structural Peaks',
      detail: 'Structural variants follow a pronounced bimodal length spectrum. The first peak (~300 bp) aligns with Alu element retrotransposition; the second peak (~6,000 bp) corresponds to LINE-1 (L1) mobile element insertions and NHEJ double-strand break repair.',
      color: C.purple
    },
    {
      title: 'Purifying Selection Signal',
      subtitle: 'Extreme Frequency Shift',
      stat: 'p < 1e-300',
      statLabel: 'Mann-Whitney U Test',
      detail: 'Pathogenic structural variants undergo intense negative purifying selection in human populations (mean gnomAD AF = 0.00012). In contrast, benign variants reach high allele frequencies (mean AF = 0.0418). Proves popgen frequency is a top diagnostic predictor.',
      color: C.emerald
    }
  ];

  cards.forEach((c, idx) => {
    const x = MARGIN_X + idx * (cardW + 0.3);
    s.addShape(pptx.ShapeType.roundRect, {
      x, y: 1.85, w: cardW, h: 4.80, rectRadius: 0.08,
      fill: { color: C.white }, line: { color: C.border, width: 1.0 }
    });

    s.addText(c.title, {
      x: x + 0.3, y: 2.10, w: cardW - 0.6, h: 0.38,
      fontSize: 18, fontFace: FONT_TITLE, bold: true, color: C.navy, margin: 0
    });

    s.addText(c.subtitle, {
      x: x + 0.3, y: 2.48, w: cardW - 0.6, h: 0.28,
      fontSize: 12.5, fontFace: FONT_BODY, bold: true, color: c.color, margin: 0
    });

    s.addShape(pptx.ShapeType.line, {
      x: x + 0.3, y: 2.85, w: cardW - 0.6, h: 0, line: { color: C.border, width: 1.0 }
    });

    s.addText(c.stat, {
      x: x + 0.3, y: 3.05, w: cardW - 0.6, h: 0.55,
      fontSize: 26, fontFace: FONT_TITLE, bold: true, color: c.color, margin: 0
    });

    s.addText(c.statLabel, {
      x: x + 0.3, y: 3.62, w: cardW - 0.6, h: 0.28,
      fontSize: 11.5, fontFace: FONT_BODY, bold: true, color: C.muted, margin: 0
    });

    s.addText(c.detail, {
      x: x + 0.3, y: 4.05, w: cardW - 0.6, h: 2.35,
      fontSize: 13, fontFace: FONT_BODY, color: C.slate, lineSpacingMultiple: 1.25, margin: 0
    });
  });
}

// =========================================================================
// SLIDE 12: Feature Engineering and Data Leakage Prevention
// =========================================================================
{
  const s = pptx.addSlide();
  addSlideHeader(s, 'Methodological Rigor', 'Feature Engineering and Data Leakage Prevention', 'Formulating 24 non-leaking biological features with strict chromosomal holdout validation');
  addSlideFooter(s, 12);

  // Left Card: 24 Features
  s.addShape(pptx.ShapeType.roundRect, {
    x: MARGIN_X, y: 1.85, w: 5.65, h: 4.80, rectRadius: 0.08,
    fill: { color: C.white }, line: { color: C.border, width: 1.0 }
  });

  s.addText('BIOLOGICALLY-GROUNDED FEATURE VECTOR', {
    x: MARGIN_X + 0.3, y: 2.10, w: 5.05, h: 0.28,
    fontSize: 11.5, fontFace: FONT_BODY, bold: true, color: C.blue, tracking: 1
  });

  s.addText('24 Rigorous Engineering Features', {
    x: MARGIN_X + 0.3, y: 2.40, w: 5.05, h: 0.40,
    fontSize: 18, fontFace: FONT_TITLE, bold: true, color: C.navy, margin: 0
  });

  s.addShape(pptx.ShapeType.line, {
    x: MARGIN_X + 0.3, y: 2.85, w: 5.05, h: 0, line: { color: C.border, width: 1.0 }
  });

  const featGroups = [
    { title: 'Population Frequencies (12 features):', desc: 'gnomAD global AF, PopMax, continental AFs (AFR, AMR, EAS, FIN, NFE, SAS, OTH), hom/het counts.' },
    { title: 'Genomic Constraint (4 features):', desc: 'Gene overlap count, pLI haploinsufficiency score, LOEUF loss-of-function intolerance, coding exon overlap flag.' },
    { title: 'Structural Biometrics (4 features):', desc: 'log10(length), span length bp, SV type one-hot encoding (DEL, DUP, INV, INS).' },
    { title: 'Molecular Context (4 features):', desc: 'GC content isochore, CpG island proximity, repeat element overlap, sequence microhomology.' }
  ];

  let currY = 3.05;
  featGroups.forEach(fg => {
    s.addText([
      { text: fg.title + ' ', options: { bold: true, color: C.navy, fontSize: 12.5 } },
      { text: fg.desc, options: { color: C.slate, fontSize: 12 } }
    ], {
      x: MARGIN_X + 0.3, y: currY, w: 5.05, h: 0.80, margin: 0, lineSpacingMultiple: 1.15
    });
    currY += 0.85;
  });

  // Right Card: Chromosomal Disjoint Split
  s.addShape(pptx.ShapeType.roundRect, {
    x: 6.883, y: 1.85, w: 5.65, h: 4.80, rectRadius: 0.08,
    fill: { color: C.white }, line: { color: C.border, width: 1.0 }
  });

  s.addText('DATA LEAKAGE PREVENTION', {
    x: 7.183, y: 2.10, w: 5.05, h: 0.28,
    fontSize: 11.5, fontFace: FONT_BODY, bold: true, color: C.emerald, tracking: 1
  });

  s.addText('Chromosomal Disjoint Holdout (0% Leakage)', {
    x: 7.183, y: 2.40, w: 5.05, h: 0.40,
    fontSize: 18, fontFace: FONT_TITLE, bold: true, color: C.navy, margin: 0
  });

  s.addShape(pptx.ShapeType.line, {
    x: 7.183, y: 2.85, w: 5.05, h: 0, line: { color: C.border, width: 1.0 }
  });

  s.addText([
    { text: 'Flaw of Standard Random Splitting:\n', options: { bold: true, color: C.red, fontSize: 13 } },
    { text: 'Random 80/20 train/test splits place overlapping variants from the same genomic locus into both train and test sets. Models memorize locus-specific properties, reporting artificially inflated test metrics (PR-AUC > 0.99) that fail on new patients.\n\n', options: { color: C.slate, fontSize: 12.5 } },
    { text: 'Our Chromosomal Partitioning Solution:\n', options: { bold: true, color: C.emerald, fontSize: 13 } },
    { text: '• Train Cohort: Chromosomes 1 through 18 (N = 35,414 variants)\n', options: { color: C.slate, fontSize: 12.5 } },
    { text: '• Holdout Test Cohort: Chromosomes 19, 20, 21, 22, X, Y (N = 8,854 variants)\n\n', options: { color: C.slate, fontSize: 12.5, bold: true } },
    { text: 'Guarantees 0.0% locus overlap and zero linkage disequilibrium leakage.', options: { bold: true, color: C.navy, fontSize: 12.5 } }
  ], {
    x: 7.183, y: 3.05, w: 5.05, h: 3.35, margin: 0, lineSpacingMultiple: 1.2
  });
}

// =========================================================================
// SLIDE 13: Machine Learning and Deep Learning Models
// =========================================================================
{
  const s = pptx.addSlide();
  addSlideHeader(s, 'Model Zoo', 'Machine Learning and Deep Learning Models', 'Comparing tree-based ensembles with continuous PyTorch Tabular ResNet architectures');
  addSlideFooter(s, 13);

  // Left Side: Tree Ensembles
  s.addShape(pptx.ShapeType.roundRect, {
    x: MARGIN_X, y: 1.85, w: 5.65, h: 4.80, rectRadius: 0.08,
    fill: { color: C.white }, line: { color: C.border, width: 1.0 }
  });

  s.addText('CLASSICAL GRADIENT BOOSTING BASELINES', {
    x: MARGIN_X + 0.3, y: 2.10, w: 5.05, h: 0.28,
    fontSize: 11, fontFace: FONT_BODY, bold: true, color: C.blue, tracking: 1
  });

  s.addText('Tree Ensembles (XGBoost, LightGBM)', {
    x: MARGIN_X + 0.3, y: 2.40, w: 5.05, h: 0.40,
    fontSize: 17, fontFace: FONT_TITLE, bold: true, color: C.navy, margin: 0
  });

  s.addShape(pptx.ShapeType.line, {
    x: MARGIN_X + 0.3, y: 2.85, w: 5.05, h: 0, line: { color: C.border, width: 1.0 }
  });

  s.addText([
    { text: '• XGBoost: ', options: { bold: true, color: C.navy, fontSize: 12.5 } },
    { text: 'Depth-wise tree growth with column subsampling and scale_pos_weight = 3.35 to counter class imbalance.\n\n', options: { color: C.slate, fontSize: 12.5 } },
    { text: '• LightGBM: ', options: { bold: true, color: C.navy, fontSize: 12.5 } },
    { text: 'Leaf-wise tree growth optimizing histogram bins for fast training.\n\n', options: { color: C.slate, fontSize: 12.5 } },
    { text: '• Random Forest & Logistic Regression: ', options: { bold: true, color: C.navy, fontSize: 12.5 } },
    { text: 'Standard bagging and linear L2 regularization baselines.\n\n', options: { color: C.slate, fontSize: 12.5 } },
    { text: 'Limitation: ', options: { bold: true, color: C.amber, fontSize: 12.5 } },
    { text: 'Axis-aligned orthogonal splits struggle to model continuous exponential allele frequency decays.', options: { color: C.slate, fontSize: 12.5 } }
  ], {
    x: MARGIN_X + 0.3, y: 3.05, w: 5.05, h: 3.35, margin: 0, lineSpacingMultiple: 1.2
  });

  // Right Side: Tabular ResNet
  s.addShape(pptx.ShapeType.roundRect, {
    x: 6.883, y: 1.85, w: 5.65, h: 4.80, rectRadius: 0.08,
    fill: { color: C.white }, line: { color: C.border, width: 1.0 }
  });

  s.addText('DEEP LEARNING INNOVATION', {
    x: 7.183, y: 2.10, w: 5.05, h: 0.28,
    fontSize: 11, fontFace: FONT_BODY, bold: true, color: C.purple, tracking: 1
  });

  s.addText('PyTorch Tabular ResNet Architecture', {
    x: 7.183, y: 2.40, w: 5.05, h: 0.40,
    fontSize: 17, fontFace: FONT_TITLE, bold: true, color: C.navy, margin: 0
  });

  s.addShape(pptx.ShapeType.line, {
    x: 7.183, y: 2.85, w: 5.05, h: 0, line: { color: C.border, width: 1.0 }
  });

  s.addText([
    { text: '• Input Projection: ', options: { bold: true, color: C.navy, fontSize: 12.5 } },
    { text: 'Dense Linear layer (24 -> 128) + LayerNorm + GeLU continuous non-linear activation.\n\n', options: { color: C.slate, fontSize: 12.5 } },
    { text: '• Residual Skip Connections: ', options: { bold: true, color: C.navy, fontSize: 12.5 } },
    { text: 'Two stacked ResBlocks where x_{l+1} = x_l + F(x_l). Enables smooth gradient flow across dense genomic feature interactions.\n\n', options: { color: C.slate, fontSize: 12.5 } },
    { text: '• Regularization & Head: ', options: { bold: true, color: C.navy, fontSize: 12.5 } },
    { text: 'Dropout (0.20) + Cosine Annealing learning rate schedule + Sigmoid output head in [0, 1].', options: { color: C.slate, fontSize: 12.5 } }
  ], {
    x: 7.183, y: 3.05, w: 5.05, h: 3.35, margin: 0, lineSpacingMultiple: 1.2
  });
}

// =========================================================================
// SLIDE 14: Multimodal Learning and Explainable AI
// =========================================================================
{
  const s = pptx.addSlide();
  addSlideHeader(s, 'Advanced Methodologies', 'Multimodal Learning and Explainable AI', 'Cross-attention fusion between population genetics, DNA sequence fragility, and TreeSHAP');
  addSlideFooter(s, 14);

  // Left Side: Multimodal Cross-Attention
  s.addShape(pptx.ShapeType.roundRect, {
    x: MARGIN_X, y: 1.85, w: 5.65, h: 4.80, rectRadius: 0.08,
    fill: { color: C.white }, line: { color: C.border, width: 1.0 }
  });

  s.addText('MULTIMODAL NEURAL ARCHITECTURE', {
    x: MARGIN_X + 0.3, y: 2.10, w: 5.05, h: 0.28,
    fontSize: 11, fontFace: FONT_BODY, bold: true, color: C.purple, tracking: 1
  });

  s.addText('Sequence + 5mC Cross-Attention', {
    x: MARGIN_X + 0.3, y: 2.40, w: 5.05, h: 0.40,
    fontSize: 17, fontFace: FONT_TITLE, bold: true, color: C.navy, margin: 0
  });

  s.addShape(pptx.ShapeType.line, {
    x: MARGIN_X + 0.3, y: 2.85, w: 5.05, h: 0, line: { color: C.border, width: 1.0 }
  });

  s.addText([
    { text: '• Branch 1 (PopGen Vector, 24-dim): ', options: { bold: true, color: C.navy, fontSize: 12 } },
    { text: 'Encodes allele frequencies and pLI constraint scores.\n\n', options: { color: C.slate, fontSize: 12 } },
    { text: '• Branch 2 (Biophysics & 5mC, 6-dim): ', options: { bold: true, color: C.navy, fontSize: 12 } },
    { text: 'Encodes GC content, CpG islands, MMEJ microhomology, and Oxford Nanopore 5mC methylation disruption.\n\n', options: { color: C.slate, fontSize: 12 } },
    { text: '• Cross-Attention Fusion: ', options: { bold: true, color: C.purple, fontSize: 12 } },
    { text: 'Scaled dot-product attention softmax(Q K^T / sqrt(d)) V weights sequence vulnerability by population rarity.', options: { color: C.slate, fontSize: 12 } }
  ], {
    x: MARGIN_X + 0.3, y: 3.05, w: 5.05, h: 3.35, margin: 0, lineSpacingMultiple: 1.2
  });

  // Right Side: TreeSHAP
  s.addShape(pptx.ShapeType.roundRect, {
    x: 6.883, y: 1.85, w: 5.65, h: 4.80, rectRadius: 0.08,
    fill: { color: C.white }, line: { color: C.border, width: 1.0 }
  });

  s.addText('EXPLAINABLE AI ENGINE', {
    x: 7.183, y: 2.10, w: 5.05, h: 0.28,
    fontSize: 11, fontFace: FONT_BODY, bold: true, color: C.emerald, tracking: 1
  });

  s.addText('TreeSHAP Local & Global Attributions', {
    x: 7.183, y: 2.40, w: 5.05, h: 0.40,
    fontSize: 17, fontFace: FONT_TITLE, bold: true, color: C.navy, margin: 0
  });

  s.addShape(pptx.ShapeType.line, {
    x: 7.183, y: 2.85, w: 5.05, h: 0, line: { color: C.border, width: 1.0 }
  });

  s.addText([
    { text: '• Game-Theoretic Shapley Values: ', options: { bold: true, color: C.navy, fontSize: 12 } },
    { text: 'Guarantees fair distribution of marginal contributions across biological features.\n\n', options: { color: C.slate, fontSize: 12 } },
    { text: '• Global Impact Ranking: ', options: { bold: true, color: C.navy, fontSize: 12 } },
    { text: 'Identifies gnomad_af, gene_overlap_count, and pli_constraint as top global drivers across 44k variants.\n\n', options: { color: C.slate, fontSize: 12 } },
    { text: '• Individual Patient Waterfalls: ', options: { bold: true, color: C.emerald, fontSize: 12 } },
    { text: 'Computes exact feature-level attribution vectors for every prioritized candidate variant.', options: { color: C.slate, fontSize: 12 } }
  ], {
    x: 7.183, y: 3.05, w: 5.05, h: 3.35, margin: 0, lineSpacingMultiple: 1.2
  });
}

// =========================================================================
// SLIDE 15: Experimental Setup and Evaluation Metrics
// =========================================================================
{
  const s = pptx.addSlide();
  addSlideHeader(s, 'Evaluation Protocol', 'Experimental Setup and Evaluation Metrics', 'Rigorous benchmarking setup and clinical metrics for imbalanced genomic cohorts');
  addSlideFooter(s, 15);

  const cardW = (USABLE_W - 0.6) / 3;
  const cards = [
    {
      title: 'Holdout Test Cohort',
      subtitle: 'Chr 19–22, X, Y (N = 8,854)',
      desc: 'All models were evaluated strictly on unseen holdout chromosomes containing 8,854 variants (7,326 pathogenic, 1,528 benign; 4.8:1 imbalance ratio). Zero overlap with training chromosomes.',
      color: C.blue
    },
    {
      title: 'Primary Ranking Metrics',
      subtitle: 'PR-AUC & ROC-AUC',
      desc: 'PR-AUC (Precision-Recall Area Under Curve / Average Precision) serves as the primary metric under class imbalance. ROC-AUC measures true positive rate vs false alarm rate across all operational cutoffs.',
      color: C.purple
    },
    {
      title: 'Clinical Safety Metrics',
      subtitle: 'Sensitivity & Brier Score',
      desc: 'Clinical Sensitivity (Recall) ensures true disease-causing variants are captured. Precision@Top-5% verifies clinical triage purity. Brier Score measures probabilistic calibration reliability.',
      color: C.emerald
    }
  ];

  cards.forEach((c, idx) => {
    const x = MARGIN_X + idx * (cardW + 0.3);
    s.addShape(pptx.ShapeType.roundRect, {
      x, y: 1.85, w: cardW, h: 4.80, rectRadius: 0.08,
      fill: { color: C.white }, line: { color: C.border, width: 1.0 }
    });

    s.addText(c.title, {
      x: x + 0.3, y: 2.15, w: cardW - 0.6, h: 0.65,
      fontSize: 18, fontFace: FONT_TITLE, bold: true, color: C.navy, margin: 0
    });

    s.addText(c.subtitle, {
      x: x + 0.3, y: 2.80, w: cardW - 0.6, h: 0.28,
      fontSize: 12.5, fontFace: FONT_BODY, bold: true, color: c.color, margin: 0
    });

    s.addShape(pptx.ShapeType.line, {
      x: x + 0.3, y: 3.15, w: cardW - 0.6, h: 0, line: { color: C.border, width: 1.0 }
    });

    s.addText(c.desc, {
      x: x + 0.3, y: 3.35, w: cardW - 0.6, h: 3.0,
      fontSize: 13.5, fontFace: FONT_BODY, color: C.slate, lineSpacingMultiple: 1.25, margin: 0
    });
  });
}

// =========================================================================
// SLIDE 16: Baseline Model Results
// =========================================================================
{
  const s = pptx.addSlide();
  addSlideHeader(s, 'Baseline Performance', 'Baseline Model Results: Classical Tree Ensembles', 'Evaluating linear and tree models on unseen holdout test chromosomes (N = 8,854)');
  addSlideFooter(s, 16);

  const tableRows = [
    [
      { text: 'Algorithm', options: { bold: true, color: 'FFFFFF', fill: { color: '1E293B' }, fontSize: 12 } },
      { text: 'PR-AUC', options: { bold: true, color: 'FFFFFF', fill: { color: '1E293B' }, fontSize: 12 } },
      { text: 'ROC-AUC', options: { bold: true, color: 'FFFFFF', fill: { color: '1E293B' }, fontSize: 12 } },
      { text: 'F1-Score', options: { bold: true, color: 'FFFFFF', fill: { color: '1E293B' }, fontSize: 12 } },
      { text: 'Sensitivity', options: { bold: true, color: 'FFFFFF', fill: { color: '1E293B' }, fontSize: 12 } },
      { text: 'Top-5% Prec', options: { bold: true, color: 'FFFFFF', fill: { color: '1E293B' }, fontSize: 12 } }
    ],
    [
      { text: 'Logistic Regression', options: { bold: true, color: C.navy, fontSize: 11.5 } },
      { text: '0.9544', options: { color: C.slate, fontSize: 11.5 } },
      { text: '0.8411', options: { color: C.slate, fontSize: 11.5 } },
      { text: '0.925', options: { color: C.slate, fontSize: 11.5 } },
      { text: '88.2%', options: { color: C.slate, fontSize: 11.5 } },
      { text: '99.8%', options: { color: C.slate, fontSize: 11.5 } }
    ],
    [
      { text: 'Random Forest', options: { bold: true, color: C.navy, fontSize: 11.5 } },
      { text: '0.9682', options: { color: C.slate, fontSize: 11.5 } },
      { text: '0.8807', options: { color: C.slate, fontSize: 11.5 } },
      { text: '0.931', options: { color: C.slate, fontSize: 11.5 } },
      { text: '89.7%', options: { color: C.slate, fontSize: 11.5 } },
      { text: '99.1%', options: { color: C.slate, fontSize: 11.5 } }
    ],
    [
      { text: 'LightGBM', options: { bold: true, color: C.navy, fontSize: 11.5 } },
      { text: '0.9698', options: { color: C.slate, fontSize: 11.5 } },
      { text: '0.8877', options: { color: C.slate, fontSize: 11.5 } },
      { text: '0.935', options: { color: C.slate, fontSize: 11.5 } },
      { text: '88.6%', options: { color: C.slate, fontSize: 11.5 } },
      { text: '99.1%', options: { color: C.slate, fontSize: 11.5 } }
    ],
    [
      { text: 'XGBoost (Best Classical)', options: { bold: true, color: C.blue, fontSize: 12, fill: { color: C.blueLight } } },
      { text: '0.9696', options: { color: C.blue, fontSize: 12, bold: true, fill: { color: C.blueLight } } },
      { text: '0.8883', options: { color: C.blue, fontSize: 12, bold: true, fill: { color: C.blueLight } } },
      { text: '0.936', options: { color: C.blue, fontSize: 12, bold: true, fill: { color: C.blueLight } } },
      { text: '88.4%', options: { color: C.blue, fontSize: 12, bold: true, fill: { color: C.blueLight } } },
      { text: '98.9%', options: { color: C.blue, fontSize: 12, bold: true, fill: { color: C.blueLight } } }
    ]
  ];

  s.addTable(tableRows, {
    x: MARGIN_X, y: 1.85, w: 7.2, h: 4.80,
    colW: [2.1, 1.0, 1.0, 1.0, 1.05, 1.05],
    border: { pt: 1, color: C.border },
    align: 'center', valign: 'middle'
  });

  addMetricCard(s, 8.3, 1.85, 4.233, 2.25, '0.9696', 'XGBoost PR-AUC Score', 'High precision-recall ranking among top-decile pathogenic variants on holdout test set.', C.blue);

  s.addShape(pptx.ShapeType.roundRect, {
    x: 8.3, y: 4.35, w: 4.233, h: 2.30, rectRadius: 0.08,
    fill: { color: C.white }, line: { color: C.border, width: 1.0 }
  });

  s.addText('TREE ENSEMBLE LIMITATIONS', {
    x: 8.55, y: 4.55, w: 3.733, h: 0.28,
    fontSize: 11.5, fontFace: FONT_BODY, bold: true, color: C.amber, tracking: 1
  });

  s.addText('Why Tree Models Cap Out', {
    x: 8.55, y: 4.88, w: 3.733, h: 0.35,
    fontSize: 16, fontFace: FONT_TITLE, bold: true, color: C.navy, margin: 0
  });

  s.addText([
    { text: '1. Step-Function Discretization: ', options: { bold: true, color: C.navy, fontSize: 12 } },
    { text: 'Axis-aligned splits struggle to model continuous exponential allele frequency decays.\n', options: { color: C.slate, fontSize: 12 } },
    { text: '2. High False Negative Rate: ', options: { bold: true, color: C.navy, fontSize: 12 } },
    { text: 'At default 0.50 cutoff, XGBoost misses 1,745 pathogenic variants, requiring continuous neural representations.', options: { color: C.slate, fontSize: 12 } }
  ], {
    x: 8.55, y: 5.30, w: 3.733, h: 1.20, margin: 0, lineSpacingMultiple: 1.2
  });
}

// =========================================================================
// SLIDE 17: Deep Learning and Multimodal Results
// =========================================================================
{
  const s = pptx.addSlide();
  addSlideHeader(s, 'Benchmark Results', 'Deep Learning and Multimodal Results', '94.4% clinical sensitivity and 38.8% reduction in probability calibration loss');
  addSlideFooter(s, 17);

  addMetricCard(s, MARGIN_X, 1.85, 4.3, 1.45, '94.4%', 'Clinical Sensitivity (Recall)', 'Captures 6,916 of 7,326 pathogenic variants on unseen chromosomes.', C.emerald);
  addMetricCard(s, MARGIN_X, 3.50, 4.3, 1.45, '0.9705', 'Holdout PR-AUC Score', 'Tabular ResNet leads all classical tree models in true positive ranking.', C.purple);
  addMetricCard(s, MARGIN_X, 5.15, 4.3, 1.50, '0.1010', 'Brier Calibration Loss', '38.8% lower calibration error than decision trees (0.165).', C.blue);

  const imgPath = path.join(__dirname, 'figures', '12_confusion_matrices.png');
  if (fs.existsSync(imgPath)) {
    s.addImage({
      path: imgPath,
      x: 5.4, y: 1.85, w: 7.133, h: 4.80
    });
  } else {
    s.addShape(pptx.ShapeType.roundRect, {
      x: 5.4, y: 1.85, w: 7.133, h: 4.80, rectRadius: 0.08,
      fill: { color: C.white }, line: { color: C.border }
    });
    s.addText('Confusion Matrices (Holdout Test Set)', {
      x: 5.4, y: 3.8, w: 7.133, h: 0.5,
      fontSize: 18, color: C.navy, bold: true, align: 'center'
    });
  }
}

// =========================================================================
// SLIDE 18: Uncertainty Quantification and Explainability Results
// =========================================================================
{
  const s = pptx.addSlide();
  addSlideHeader(s, 'Clinical Verification', 'Uncertainty Quantification and Explainability Results', 'Conformal 95% coverage guarantees, 34k VUS triage, and local TreeSHAP attribution');
  addSlideFooter(s, 18);

  const cardW = (USABLE_W - 0.6) / 3;
  const cards = [
    {
      title: 'Split Conformal Prediction',
      subtitle: '95% Finite-Sample Guarantee',
      desc: 'Evaluated on calibration fold (Chr 17-18, N = 1,200). Non-conformity cutoff q_hat = 0.7241 guarantees P(Y_true in C(X_test)) >= 0.95 without distribution assumptions. Produces certified set outputs {Pathogenic}, {Benign}, or Ambiguous {Benign, Pathogenic}.',
      color: C.blue
    },
    {
      title: 'Resolving the VUS Backlog',
      subtitle: '34,466 ClinVar Variants Triaged',
      desc: 'Applied model across 34,466 ambiguous ClinVar VUS. Resolved 16,801 variants (48.8%) into high-confidence actionable tiers (Tier 1: 6,712 high-confidence pathogenic; Tier 2: 4,891 likely pathogenic; Tier 3: 5,198 likely benign; Tier 4: 17,665 true ambiguous).',
      color: C.emerald
    },
    {
      title: 'TreeSHAP Patient Waterfall',
      subtitle: 'Local Biological Decision Rationales',
      desc: 'Individual patient case (BRCA1 deletion, 81.1 kb): Model scores 0.982 Pathogenicity Index. TreeSHAP quantifies exact drivers: gnomad_af = 0 (+0.38), BRCA1 coding overlap (+0.29), pLI = 0.99 (+0.22), providing immediate biological rationales.',
      color: C.purple
    }
  ];

  cards.forEach((c, idx) => {
    const x = MARGIN_X + idx * (cardW + 0.3);
    s.addShape(pptx.ShapeType.roundRect, {
      x, y: 1.85, w: cardW, h: 4.80, rectRadius: 0.08,
      fill: { color: C.white }, line: { color: C.border, width: 1.0 }
    });

    s.addText(c.title, {
      x: x + 0.3, y: 2.15, w: cardW - 0.6, h: 0.65,
      fontSize: 18, fontFace: FONT_TITLE, bold: true, color: C.navy, margin: 0
    });

    s.addText(c.subtitle, {
      x: x + 0.3, y: 2.80, w: cardW - 0.6, h: 0.28,
      fontSize: 12.5, fontFace: FONT_BODY, bold: true, color: c.color, margin: 0
    });

    s.addShape(pptx.ShapeType.line, {
      x: x + 0.3, y: 3.15, w: cardW - 0.6, h: 0, line: { color: C.border, width: 1.0 }
    });

    s.addText(c.desc, {
      x: x + 0.3, y: 3.35, w: cardW - 0.6, h: 3.0,
      fontSize: 13.5, fontFace: FONT_BODY, color: C.slate, lineSpacingMultiple: 1.25, margin: 0
    });
  });
}

// =========================================================================
// SLIDE 19: End-to-End Pipeline and Demonstration
// =========================================================================
{
  const s = pptx.addSlide();
  addSlideHeader(s, 'Engineering Delivery', 'End-to-End Pipeline and Demonstration', 'Standalone production CLI tool prioritize_sv.py generating clinical reports in 4.2 seconds');
  addSlideFooter(s, 19);

  const steps = [
    { num: 'STEP 1', title: 'VCF Ingestion', desc: 'Parses Sniffles2, cuteSV, PBSV long-read calls; filters SV >= 50 bp.' },
    { num: 'STEP 2', title: 'Fast Annotation', desc: 'Interval overlap with gnomAD SV and gene constraint models in <1.5s.' },
    { num: 'STEP 3', title: 'Model Inference', desc: 'Calculates Pathogenicity Index via XGBoost, Tabular ResNet, or Ensemble mode.' },
    { num: 'STEP 4', title: 'TreeSHAP Waterfall', desc: 'Computes local Shapley explanations for the top candidate variants.' },
    { num: 'STEP 5', title: 'Clinical Export', desc: 'Exports Interactive HTML Report, Ranked CSV queue, and Prioritized VCF.' }
  ];

  const colW = (USABLE_W - 0.8) / 5;
  steps.forEach((st, idx) => {
    const x = MARGIN_X + idx * (colW + 0.2);
    s.addShape(pptx.ShapeType.roundRect, {
      x, y: 1.85, w: colW, h: 2.30, rectRadius: 0.08,
      fill: { color: C.white }, line: { color: C.border, width: 1.0 }
    });

    s.addText(st.num, {
      x: x + 0.15, y: 2.05, w: colW - 0.3, h: 0.25,
      fontSize: 11, fontFace: FONT_BODY, bold: true, color: C.blue, tracking: 1
    });

    s.addText(st.title, {
      x: x + 0.15, y: 2.35, w: colW - 0.3, h: 0.35,
      fontSize: 15, fontFace: FONT_TITLE, bold: true, color: C.navy, margin: 0
    });

    s.addShape(pptx.ShapeType.line, {
      x: x + 0.15, y: 2.75, w: colW - 0.3, h: 0, line: { color: C.border, width: 1.0 }
    });

    s.addText(st.desc, {
      x: x + 0.15, y: 2.90, w: colW - 0.3, h: 1.15,
      fontSize: 11.5, fontFace: FONT_BODY, color: C.slate, lineSpacingMultiple: 1.15, margin: 0
    });
  });

  s.addShape(pptx.ShapeType.roundRect, {
    x: MARGIN_X, y: 4.45, w: USABLE_W, h: 2.20, rectRadius: 0.08,
    fill: { color: '0F172A' }, line: { color: '334155', width: 1.0 }
  });

  s.addText('STANDALONE PRODUCTION CLI EXECUTION (TOTAL RUNTIME: 4.2 SECONDS)', {
    x: MARGIN_X + 0.3, y: 4.65, w: USABLE_W - 0.6, h: 0.25,
    fontSize: 11, fontFace: 'Courier New', bold: true, color: '38BDF8', tracking: 1
  });

  const termLines = [
    '$ python prioritize_sv.py -i patient_sample.vcf -o reports/patient_01/ --model-type dl',
    '[1/5] Ingesting & Parsing Long-Read VCF... Parsed 7 structural variants (>= 50 bp).',
    '[2/5] Annotating Population Frequencies & Gene Constraints in 1.26s.',
    '[3/5] Running Calibrated ML Model Inference (DL): 3 Tier 1 Pathogenic candidates triaged.',
    '[4/5] Computing TreeSHAP Attributions for Top Candidates in 2.89s.',
    '[5/5] Clinical Deliverables Exported: clinical_report.html, ranked_variants.csv, prioritized.vcf'
  ];

  s.addText(termLines.join('\n'), {
    x: MARGIN_X + 0.3, y: 5.00, w: USABLE_W - 0.6, h: 1.50,
    fontSize: 11.5, fontFace: 'Courier New', color: 'F8FAFC', lineSpacingMultiple: 1.25, margin: 0
  });
}

// =========================================================================
// SLIDE 20: Discussion
// =========================================================================
{
  const s = pptx.addSlide();
  addSlideHeader(s, 'Scientific Synthesis', 'Discussion', 'Biological alignment, continuous neural advantages, and clinical safety considerations');
  addSlideFooter(s, 20);

  const cardW = (USABLE_W - 0.6) / 3;
  const cards = [
    {
      title: 'Biological Concordance',
      subtitle: 'Validating Genetic Principles',
      desc: 'The model autonomously learned classic genomic mechanisms: deletions causing complete exon loss in dosage-sensitive genes (high pLI) with near-zero population frequency represent primary drivers of severe genetic disorders.',
      color: C.blue
    },
    {
      title: 'Neural vs Tree Manifolds',
      subtitle: 'Smooth Continuous Representations',
      desc: 'Tabular ResNet outperformed decision trees because biological allele frequencies follow exponential decays rather than step functions. Neural residual skip connections smoothly map continuous constraint features without orthogonal discretization.',
      color: C.purple
    },
    {
      title: 'Safety-First Clinical Triage',
      subtitle: 'Conformal Prediction Impact',
      desc: 'Replacing arbitrary classification cutoffs with 95% conformal prediction sets provides hospital geneticists with distribution-free certified bounds. Ambiguous variants are safely flagged for functional wet-lab verification.',
      color: C.emerald
    }
  ];

  cards.forEach((c, idx) => {
    const x = MARGIN_X + idx * (cardW + 0.3);
    s.addShape(pptx.ShapeType.roundRect, {
      x, y: 1.85, w: cardW, h: 4.80, rectRadius: 0.08,
      fill: { color: C.white }, line: { color: C.border, width: 1.0 }
    });

    s.addText(c.title, {
      x: x + 0.3, y: 2.15, w: cardW - 0.6, h: 0.65,
      fontSize: 18, fontFace: FONT_TITLE, bold: true, color: C.navy, margin: 0
    });

    s.addText(c.subtitle, {
      x: x + 0.3, y: 2.80, w: cardW - 0.6, h: 0.28,
      fontSize: 12.5, fontFace: FONT_BODY, bold: true, color: c.color, margin: 0
    });

    s.addShape(pptx.ShapeType.line, {
      x: x + 0.3, y: 3.15, w: cardW - 0.6, h: 0, line: { color: C.border, width: 1.0 }
    });

    s.addText(c.desc, {
      x: x + 0.3, y: 3.35, w: cardW - 0.6, h: 3.0,
      fontSize: 13.5, fontFace: FONT_BODY, color: C.slate, lineSpacingMultiple: 1.25, margin: 0
    });
  });
}

// =========================================================================
// SLIDE 21: Limitations
// =========================================================================
{
  const s = pptx.addSlide();
  addSlideHeader(s, 'Constraints', 'Limitations', 'Technical constraints and inherent boundaries of the current framework');
  addSlideFooter(s, 21);

  const cardW = (USABLE_W - 0.6) / 3;
  const cards = [
    {
      num: '01',
      title: 'Ascertainment Bias in Databases',
      desc: 'ClinVar ground truth assertions are heavily enriched for severe pediatric and cancer cohorts. Routine screening of healthy general populations may reveal rare but benign SVs that lack sufficient representation in curated disease databases.',
      color: C.amber
    },
    {
      num: '02',
      title: 'Linear Reference Genome Bias',
      desc: 'Coordinates rely on linear GRCh38 representation. Complex nested rearrangements, multiallelic copy-number polymorphisms, and complex translocations would benefit from graph-based pan-genome coordinate systems.',
      color: C.slate
    },
    {
      num: '03',
      title: 'Epigenetic Platform Specificity',
      desc: 'Long-read 5mC DNA methylation features are natively called by Oxford Nanopore sequencers. While highly informative for promoter disruption, they are unavailable in legacy PacBio CLR or standard short-read sequencing runs.',
      color: C.blue
    }
  ];

  cards.forEach((c, idx) => {
    const x = MARGIN_X + idx * (cardW + 0.3);
    s.addShape(pptx.ShapeType.roundRect, {
      x, y: 1.85, w: cardW, h: 4.80, rectRadius: 0.08,
      fill: { color: C.white }, line: { color: C.border, width: 1.0 }
    });

    s.addText(c.num, {
      x: x + 0.3, y: 2.15, w: cardW - 0.6, h: 0.45,
      fontSize: 26, fontFace: FONT_TITLE, bold: true, color: c.color, margin: 0
    });

    s.addText(c.title, {
      x: x + 0.3, y: 2.65, w: cardW - 0.6, h: 0.65,
      fontSize: 18, fontFace: FONT_TITLE, bold: true, color: C.navy, margin: 0
    });

    s.addShape(pptx.ShapeType.line, {
      x: x + 0.3, y: 3.35, w: cardW - 0.6, h: 0, line: { color: C.border, width: 1.0 }
    });

    s.addText(c.desc, {
      x: x + 0.3, y: 3.60, w: cardW - 0.6, h: 2.80,
      fontSize: 13.5, fontFace: FONT_BODY, color: C.slate, lineSpacingMultiple: 1.25, margin: 0
    });
  });
}

// =========================================================================
// SLIDE 22: Future Scope
// =========================================================================
{
  const s = pptx.addSlide();
  addSlideHeader(s, 'Roadmap', 'Future Scope', 'Strategic scientific enhancements for expanding platform capabilities');
  addSlideFooter(s, 22);

  const cardW = (USABLE_W - 0.6) / 3;
  const cards = [
    {
      num: '01',
      title: 'Pan-Genome Graph Integration',
      desc: 'Integrate variation graph toolkits (Minigraph-Cactus / VG) to resolve multiallelic copy-number variants and complex inversion breakpoints across ancestral pan-genome reference backbones.',
      color: C.blue
    },
    {
      num: '02',
      title: 'Phenotype-Driven Prioritization',
      desc: 'Incorporate patient electronic health records (EHR) and Human Phenotype Ontology (HPO) terms to dynamically weight pathogenicity scores by patient-specific clinical symptoms.',
      color: C.purple
    },
    {
      num: '03',
      title: 'Genomic Foundation Models',
      desc: 'Fine-tune pre-trained genomic language models (e.g. Nucleotide Transformer, HyenaDNA) on structural variant breakpoint sequences to capture deep non-coding regulatory syntax.',
      color: C.emerald
    }
  ];

  cards.forEach((c, idx) => {
    const x = MARGIN_X + idx * (cardW + 0.3);
    s.addShape(pptx.ShapeType.roundRect, {
      x, y: 1.85, w: cardW, h: 4.80, rectRadius: 0.08,
      fill: { color: C.white }, line: { color: C.border, width: 1.0 }
    });

    s.addText(c.num, {
      x: x + 0.3, y: 2.15, w: cardW - 0.6, h: 0.45,
      fontSize: 26, fontFace: FONT_TITLE, bold: true, color: c.color, margin: 0
    });

    s.addText(c.title, {
      x: x + 0.3, y: 2.65, w: cardW - 0.6, h: 0.65,
      fontSize: 18, fontFace: FONT_TITLE, bold: true, color: C.navy, margin: 0
    });

    s.addShape(pptx.ShapeType.line, {
      x: x + 0.3, y: 3.35, w: cardW - 0.6, h: 0, line: { color: C.border, width: 1.0 }
    });

    s.addText(c.desc, {
      x: x + 0.3, y: 3.60, w: cardW - 0.6, h: 2.80,
      fontSize: 13.5, fontFace: FONT_BODY, color: C.slate, lineSpacingMultiple: 1.25, margin: 0
    });
  });
}

// =========================================================================
// SLIDE 23: Conclusion
// =========================================================================
{
  const s = pptx.addSlide();
  s.background = { color: '0F172A' };

  s.addText('PROJECT SUMMARY & DEFENSE CONCLUSION', {
    x: MARGIN_X, y: 0.90, w: USABLE_W, h: 0.35,
    fontSize: 13, fontFace: FONT_BODY, bold: true, color: '60A5FA', tracking: 2
  });

  s.addText('Conclusion: Summary of Scientific Contributions', {
    x: MARGIN_X, y: 1.35, w: USABLE_W, h: 0.60,
    fontSize: 26, fontFace: FONT_TITLE, bold: true, color: 'FFFFFF'
  });

  s.addShape(pptx.ShapeType.line, {
    x: MARGIN_X, y: 2.10, w: 4.0, h: 0, line: { color: '38BDF8', width: 2.5 }
  });

  const takeaways = [
    {
      num: '01',
      title: 'Leakage-Free Genomic Framework',
      desc: 'Established strict chromosomal disjoint partitioning (0.0% locus leakage) across 44,268 harmonized ClinVar and gnomAD structural variants, preventing optimistic evaluation bias.'
    },
    {
      num: '02',
      title: 'Deep Learning & Calibration Breakthrough',
      desc: 'Developed PyTorch Tabular ResNet & Multimodal Cross-Attention architectures reaching peak 0.9705 PR-AUC and 94.4% clinical sensitivity, slashing false negatives from 1,745 down to 414.'
    },
    {
      num: '03',
      title: 'Certified Mathematical Safety',
      desc: 'Replaced arbitrary probability thresholding with Split Conformal Prediction, providing a distribution-free 95% coverage guarantee to prevent clinical overconfidence in genomic diagnoses.'
    },
    {
      num: '04',
      title: 'Clinical Utility & VUS Triage',
      desc: 'Successfully triaged 34,466 unclassified ClinVar VUS variants, resolving 48.8% into high-confidence actionable risk tiers with local TreeSHAP biological rationales via an automated <5-second CLI pipeline.'
    }
  ];

  const colW = (USABLE_W - 0.9) / 4;
  takeaways.forEach((t, idx) => {
    const x = MARGIN_X + idx * (colW + 0.3);
    s.addShape(pptx.ShapeType.roundRect, {
      x, y: 2.50, w: colW, h: 4.10, rectRadius: 0.08,
      fill: { color: '1E293B' }, line: { color: '334155', width: 1.0 }
    });

    s.addText(t.num, {
      x: x + 0.25, y: 2.75, w: colW - 0.5, h: 0.45,
      fontSize: 24, fontFace: FONT_TITLE, bold: true, color: '38BDF8', margin: 0
    });

    s.addText(t.title, {
      x: x + 0.25, y: 3.25, w: colW - 0.5, h: 0.65,
      fontSize: 16, fontFace: FONT_TITLE, bold: true, color: 'FFFFFF', margin: 0
    });

    s.addShape(pptx.ShapeType.line, {
      x: x + 0.25, y: 3.95, w: colW - 0.5, h: 0, line: { color: '334155', width: 1.0 }
    });

    s.addText(t.desc, {
      x: x + 0.25, y: 4.15, w: colW - 0.5, h: 2.25,
      fontSize: 12.5, fontFace: FONT_BODY, color: '94A3B8', lineSpacingMultiple: 1.25, margin: 0
    });
  });
}

// =========================================================================
// SLIDE 24: References
// =========================================================================
{
  const s = pptx.addSlide();
  addSlideHeader(s, 'Bibliography', 'References', 'Selected primary scientific literature and foundational citations');
  addSlideFooter(s, 24);

  const refs = [
    { num: '[1]', text: 'Collins, R. L., et al. (2020). A structural variation reference for medical and population genetics. Nature, 581(7809), 444–451.' },
    { num: '[2]', text: 'Rentzsch, P., et al. (2020). CADD-SV: scoring the variant effect of structural variants in the human genome. Genome Biology, 21(1), 1–20.' },
    { num: '[3]', text: 'Landrum, M. J., et al. (2024). ClinVar: improvements to accessing data. Nucleic Acids Research, 52(D1), D1389–D1397.' },
    { num: '[4]', text: 'Lundberg, S. M., et al. (2020). From local explanations to global understanding with explainable AI for trees. Nature Machine Intelligence, 2(1), 56–67.' },
    { num: '[5]', text: 'Angelopoulos, A. N., & Bates, S. (2023). Conformal prediction: A gentle introduction. Foundations and Trends in Machine Learning, 16(4), 494–591.' },
    { num: '[6]', text: 'Sedlazeck, F. J., et al. (2018). Accurate detection of complex structural variations using single-molecule sequencing. Nature Methods, 15(6), 461–468.' }
  ];

  s.addShape(pptx.ShapeType.roundRect, {
    x: MARGIN_X, y: 1.85, w: USABLE_W, h: 4.80, rectRadius: 0.08,
    fill: { color: C.white }, line: { color: C.border, width: 1.0 }
  });

  let currY = 2.15;
  refs.forEach(r => {
    s.addShape(pptx.ShapeType.roundRect, {
      x: MARGIN_X + 0.3, y: currY, w: 0.55, h: 0.38, rectRadius: 0.06,
      fill: { color: C.blueLight }, line: { color: C.blue, width: 1.0 }
    });
    s.addText(r.num, {
      x: MARGIN_X + 0.3, y: currY, w: 0.55, h: 0.38,
      fontSize: 11, bold: true, color: C.blue, align: 'center', margin: 0
    });

    s.addText(r.text, {
      x: MARGIN_X + 1.05, y: currY, w: USABLE_W - 1.35, h: 0.55,
      fontSize: 12.5, fontFace: FONT_BODY, color: C.slate, margin: 0, lineSpacingMultiple: 1.15
    });

    currY += 0.72;
  });
}

// =========================================================================
// WRITE DECK FILE
// =========================================================================
const outputPath = path.join(__dirname, 'End_Semester_Presentation.pptx');
pptx.writeFile({ fileName: outputPath })
  .then(() => {
    console.log('\n========================================================================');
    console.log(`SUCCESS: Generated ${TOTAL_SLIDES}-Slide Academic Review Presentation:`);
    console.log(`File: ${outputPath}`);
    console.log('========================================================================\n');
  })
  .catch(err => {
    console.error('ERROR writing presentation:', err);
    process.exit(1);
  });
