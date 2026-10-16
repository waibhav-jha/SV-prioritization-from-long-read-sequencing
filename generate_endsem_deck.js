const pptxgen = require('pptxgenjs');
const fs = require('fs');
const path = require('path');

const pptx = new pptxgen();

// Layout: Widescreen 16:9 (13.333 x 7.5 inches)
pptx.layout = 'LAYOUT_WIDE';
pptx.author = 'Waibhav Jha, Akash Bardia, Anantharaman T S, K S Jagan';
pptx.company = 'Department of Artificial Intelligence, School of Computing';
pptx.title = 'AI-Based Structural Variant Prioritization from Long-Read Sequencing Using Explainable Machine Learning';
pptx.subject = 'Final Capstone Project Technical Presentation';

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
  slide.addText('Department of Artificial Intelligence  |  Final Project Review  |  Amrita Vishwa Vidyapeetham', {
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

  s.addText('FINAL PROJECT TECHNICAL REVIEW  |  DEPARTMENT OF ARTIFICIAL INTELLIGENCE', {
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

  s.addText('A Deep Learning & Multimodal Framework with 95% Conformal Confidence Bounds and TreeSHAP Explainability for Clinical Diagnostics', {
    x: MARGIN_X, y: 3.30, w: USABLE_W, h: 0.70,
    fontSize: 15, fontFace: FONT_BODY, color: '94A3B8', lineSpacingMultiple: 1.1
  });

  const cardW = (USABLE_W - 0.9) / 4;
  const cards = [
    { label: 'PROJECT TEAM', val: 'Waibhav Jha (23162)\nAkash Bardia (23102)\nAnantharaman (23112)\nK S Jagan (23034)' },
    { label: 'DEPARTMENT', val: 'Department of AI\nSchool of Computing\nAmrita Vishwa Vidyapeetham' },
    { label: 'KEY INNOVATION', val: 'Tabular ResNet + Multimodal\nOver 60% Drop in Missed Diseases' },
    { label: 'CLINICAL OUTCOME', val: '0% Data Leakage Split\n48.8% of 34k VUS Resolved' }
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
      fontSize: 12.5, fontFace: FONT_BODY, color: 'F8FAFC', lineSpacingMultiple: 1.15
    });
  });
}

// =========================================================================
// SLIDE 2: Introduction
// =========================================================================
{
  const s = pptx.addSlide();
  addSlideHeader(s, 'Background', 'Introduction: What is Long-Read Sequencing?', 'Long-read sequencing uncovers thousands of large DNA mutations that older technologies completely missed');
  addSlideFooter(s, 2);

  const cardW = (USABLE_W - 0.6) / 3;
  const cards = [
    {
      title: 'Long-Read Sequencing',
      subtitle: 'Modern DNA Reading Tech',
      points: [
        'Reads continuous DNA fragments over 10,000–25,000 letters long at once.',
        'Effortlessly reads repetitive genomic regions where older short-read machines got stuck.',
        'Discovers over 25,000 large DNA variants in every individual patient genome.'
      ],
      color: C.blue
    },
    {
      title: 'Structural Variants (SVs)',
      subtitle: 'Large DNA Disruptions',
      points: [
        'Large mutations (>= 50 base pairs) such as large DNA cuts, copies, and flips.',
        'Affect more total DNA letters than all single-letter typos combined.',
        'Major cause of hereditary cancers, developmental delays, and rare genetic diseases.'
      ],
      color: C.purple
    },
    {
      title: 'The Clinical Bottleneck',
      subtitle: 'Why AI is Needed',
      points: [
        'Doctors face a massive list of 25,000+ variants per patient in their raw output file (VCF).',
        'Most existing tools only check tiny 1-letter typos, not large DNA rearrangements.',
        'Manual checking takes weeks; an automated AI prioritization system is urgently needed.'
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
  addSlideHeader(s, 'Problem Formulation', 'Problem Statement: Three Major Diagnostic Challenges', 'Why current clinical software fails on long-read structural variant data');
  addSlideFooter(s, 3);

  const cardW = (USABLE_W - 0.6) / 3;
  const cards = [
    {
      num: '01',
      title: 'Current Tools Check the Wrong Scale',
      desc: 'Over 90% of current scoring tools are built exclusively for 1-letter typos. They cannot model large multi-thousand-letter deletions or additions that span across entire functional human genes.',
      color: C.red
    },
    {
      num: '02',
      title: 'Data Leakage in Previous Research',
      desc: 'Previous AI papers made a fundamental mistake: they used naive random 80/20 splits. Overlapping variants from the same chromosome appeared in both train and test sets, creating fake high scores that fail on real patients.',
      color: C.amber
    },
    {
      num: '03',
      title: 'Missing Clinical Confidence Bounds',
      desc: 'Standard AI models output a single raw probability score without safety margins. In medical diagnosis, guessing without a certified confidence interval risks missing disease mutations or causing unnecessary surgeries.',
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
  addSlideHeader(s, 'Clinical Relevance', 'Clinical Motivation: Solving the 40% Uncertainty Trap', 'Helping doctors convert ambiguous genetic findings into clear, fast diagnostic actions');
  addSlideFooter(s, 4);

  addMetricCard(s, MARGIN_X, 1.85, 4.3, 1.45, '~40%', 'Variants of Uncertain Significance', 'Nearly 40% of patient mutations have unknown impact, leaving families without answers.', C.red);
  addMetricCard(s, MARGIN_X, 3.50, 4.3, 1.45, '>45 min', 'Manual Doctor Review Time', 'Doctors spend 45+ minutes per variant manually searching medical literature.', C.amber);
  addMetricCard(s, MARGIN_X, 5.15, 4.3, 1.50, '4.2s', 'Our Automated AI Pipeline', 'Our software ranks and explains patient variants in just 4.2 seconds.', C.emerald);

  s.addShape(pptx.ShapeType.roundRect, {
    x: 5.4, y: 1.85, w: 7.133, h: 4.80, rectRadius: 0.08,
    fill: { color: C.white }, line: { color: C.border, width: 1.0 }
  });

  s.addText('REAL-WORLD CLINICAL IMPACT', {
    x: 5.7, y: 2.15, w: 6.5, h: 0.28,
    fontSize: 12, fontFace: FONT_BODY, bold: true, color: C.blue, tracking: 1
  });

  s.addText('Why Automating Variant Triage Saves Lives', {
    x: 5.7, y: 2.48, w: 6.5, h: 0.40,
    fontSize: 19, fontFace: FONT_TITLE, bold: true, color: C.navy, margin: 0
  });

  s.addShape(pptx.ShapeType.line, {
    x: 5.7, y: 2.95, w: 6.5, h: 0, line: { color: C.border, width: 1.0 }
  });

  const clinicalPoints = [
    { title: 'Ending Patient Delays:', desc: 'When a mutation is labeled "Uncertain", doctors cannot legally prescribe targeted cancer drugs or genetic treatments. Patients are stuck waiting for months.' },
    { title: 'Clearing Hospital Backlogs:', desc: 'Geneticists must manually cross-check population databases, gene lists, and papers for dozens of candidate mutations per patient.' },
    { title: 'Doctors Need Explanations:', desc: 'Doctors will not trust a black-box AI score. Our system gives clear visual explanations showing exactly which biological features caused the high risk score.' }
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
  addSlideHeader(s, 'State of the Art', 'Literature Review: Key Milestones in Variant Analysis', 'Foundational databases and previous scoring attempts in genomics');
  addSlideFooter(s, 5);

  const tableRows = [
    [
      { text: 'Milestone Study', options: { bold: true, color: 'FFFFFF', fill: { color: '1E293B' }, fontSize: 12 } },
      { text: 'Core Contribution', options: { bold: true, color: 'FFFFFF', fill: { color: '1E293B' }, fontSize: 12 } },
      { text: 'What It Provided to Our Project', options: { bold: true, color: 'FFFFFF', fill: { color: '1E293B' }, fontSize: 12 } },
      { text: 'Remaining Limitation', options: { bold: true, color: 'FFFFFF', fill: { color: '1E293B' }, fontSize: 12 } }
    ],
    [
      { text: 'Collins et al.\n(Nature 2020)', options: { bold: true, color: C.navy, fontSize: 11.5 } },
      { text: 'gnomAD SV Population Catalog', options: { color: C.slate, fontSize: 11.5 } },
      { text: 'Cataloged 387,700 variants across 15,000 healthy genomes; established frequency baselines.', options: { color: C.slate, fontSize: 11 } },
      { text: 'Only a reference catalog; does not predict whether a variant causes disease.', options: { color: C.slate, fontSize: 11 } }
    ],
    [
      { text: 'Rentzsch et al.\n(Genome Bio 2020)', options: { bold: true, color: C.navy, fontSize: 11.5 } },
      { text: 'CADD-SV Regional Scorer', options: { color: C.slate, fontSize: 11.5 } },
      { text: 'Combined conservation and gene tracks to score large DNA deletions.', options: { color: C.slate, fontSize: 11 } },
      { text: 'Linear model; struggles on complex rearrangements and other variant types.', options: { color: C.slate, fontSize: 11 } }
    ],
    [
      { text: 'Landrum et al.\n(NAR 2024)', options: { bold: true, color: C.navy, fontSize: 11.5 } },
      { text: 'NCBI ClinVar Database', options: { color: C.slate, fontSize: 11.5 } },
      { text: 'Gold-standard library of doctor-verified variant classifications (Harmful vs Benign).', options: { color: C.slate, fontSize: 11 } },
      { text: 'Contains a huge backlog of unclassified "Uncertain" variants needing triage.', options: { color: C.slate, fontSize: 11 } }
    ],
    [
      { text: 'Lundberg et al.\n(Nat MI 2020)', options: { bold: true, color: C.navy, fontSize: 11.5 } },
      { text: 'TreeSHAP Framework', options: { color: C.slate, fontSize: 11.5 } },
      { text: 'Game-theory method to calculate exactly how much each feature contributed to a prediction.', options: { color: C.slate, fontSize: 11 } },
      { text: 'Explainability tool only; must be integrated into an active end-to-end clinical app.', options: { color: C.slate, fontSize: 11 } }
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
  addSlideHeader(s, 'Research Motivation', 'Research Gap: Three Unresolved Limitations', 'The three major technical flaws in existing machine learning papers');
  addSlideFooter(s, 6);

  const cardW = (USABLE_W - 0.6) / 3;
  const cards = [
    {
      gap: 'GAP 1: FAKE ACCURACY',
      title: 'Data Leakage in Cross-Validation',
      desc: 'Most published models split data randomly. Because related mutations share the same chromosome or gene, training data leaks into test sets. Models simply memorize the gene name instead of learning true mutation biology, giving false high scores.',
      color: C.red
    },
    {
      gap: 'GAP 2: RIGID DECISION TREES',
      title: 'Tree Models Miss Continuous Rarity',
      desc: 'Popular tree models (XGBoost, LightGBM) make rigid step-cuts across features. But genetic rarity in human populations follows smooth, continuous curves. Decision trees fail to model these curves properly, missing over 1,700 disease mutations.',
      color: C.purple
    },
    {
      gap: 'GAP 3: GUESSING WITHOUT CONFIDENCE',
      title: 'No Mathematical Safety Guarantees',
      desc: 'Existing software gives a single number and picks an arbitrary cutoff (like 0.5). In medical diagnostics, an arbitrary cutoff cannot tell doctors how confident the model is, risking dangerous false alarms and missed diagnoses.',
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
  addSlideHeader(s, 'Project Scope', 'Aim, Objectives and Contributions', 'Our concrete engineering goals and the verified experimental results achieved');
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

  s.addText('Engineering Goals', {
    x: MARGIN_X + 0.3, y: 2.40, w: 5.05, h: 0.40,
    fontSize: 18, fontFace: FONT_TITLE, bold: true, color: C.navy, margin: 0
  });

  s.addShape(pptx.ShapeType.line, {
    x: MARGIN_X + 0.3, y: 2.85, w: 5.05, h: 0, line: { color: C.border, width: 1.0 }
  });

  const objs = [
    'Combine multi-source DNA databases (ClinVar, gnomAD) using a strict 50% length overlap rule.',
    'Engineer 24 leak-free features and evaluate on completely unseen holdout chromosomes.',
    'Build Deep Tabular ResNet and Multimodal sequence models to outperform classical tree models.',
    'Deploy 95% mathematical confidence bounds and TreeSHAP visual explanations into a fast CLI tool.'
  ];

  const objText = objs.map((o, i) => ({
    text: o,
    options: { bullet: true, breakLine: i < objs.length - 1, fontSize: 13, color: C.slate, fontFace: FONT_BODY, paraSpaceAfter: 12 }
  }));

  s.addText(objText, {
    x: MARGIN_X + 0.3, y: 3.05, w: 5.05, h: 3.35, margin: 0
  });

  // Right Side: Contributions
  s.addShape(pptx.ShapeType.roundRect, {
    x: 6.883, y: 1.85, w: 5.65, h: 4.80, rectRadius: 0.08,
    fill: { color: C.white }, line: { color: C.border, width: 1.0 }
  });

  s.addText('KEY DEMONSTRATED OUTCOMES', {
    x: 7.183, y: 2.10, w: 5.05, h: 0.28,
    fontSize: 11.5, fontFace: FONT_BODY, bold: true, color: C.emerald, tracking: 1
  });

  s.addText('What We Actually Delivered', {
    x: 7.183, y: 2.40, w: 5.05, h: 0.40,
    fontSize: 18, fontFace: FONT_TITLE, bold: true, color: C.navy, margin: 0
  });

  s.addShape(pptx.ShapeType.line, {
    x: 7.183, y: 2.85, w: 5.05, h: 0, line: { color: C.border, width: 1.0 }
  });

  const contribs = [
    'Zero-Leakage Benchmark: Tested strictly on unseen Chromosomes 19–22, X, Y (0% data leakage).',
    'State-of-the-Art Detection: 0.9705 PR-AUC and 94.4% clinical sensitivity on unseen test chromosomes.',
    'Slashed Missed Diseases: Cut false negatives from 1,745 down to 414 (over 60% reduction vs XGBoost).',
    'Solved 48.8% of Uncertain Variants: Successfully triaged 16,801 of 34,466 unreviewed ClinVar VUS.'
  ];

  const contribText = contribs.map((c, i) => ({
    text: c,
    options: { bullet: true, breakLine: i < contribs.length - 1, fontSize: 13, color: C.slate, fontFace: FONT_BODY, paraSpaceAfter: 12 }
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
  addSlideHeader(s, 'System Architecture', 'Proposed System Architecture', 'A modular end-to-end pipeline turning raw patient sequencing files into fast clinical decisions');
  addSlideFooter(s, 8);

  const steps = [
    {
      num: '01', title: 'Data Ingestion', sub: 'Read Patient Files',
      points: [
        'Parse patient sequencing files (VCF)',
        'Filter large variants (>= 50 base pairs)',
        'Match with reference databases',
        'Use 50% length overlap rule'
      ],
      color: C.blue
    },
    {
      num: '02', title: 'Feature Vector', sub: 'Calculate 24 Signals',
      points: [
        'Compute population rarity in humans',
        'Score gene importance to survival',
        'Extract mutation length & type',
        'Split chromosomes to prevent leakage'
      ],
      color: C.navy
    },
    {
      num: '03', title: 'Dual-Paradigm AI', sub: 'Run Neural Models',
      points: [
        'Tabular ResNet with skip connections',
        'Multimodal net with DNA sequence context',
        'Outputs calibrated risk score (0 to 1)',
        'Reaches 94.4% disease detection rate'
      ],
      color: C.purple
    },
    {
      num: '04', title: 'Clinical Safety', sub: 'Explain & Guarantee',
      points: [
        '95% mathematical confidence intervals',
        'TreeSHAP visual feature explanations',
        'Fast CLI tool (prioritize_sv.py)',
        'Generates interactive HTML doctor report'
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
  addSlideHeader(s, 'Genomic Repositories', 'Dataset Description and Sources', 'The verified gold-standard databases used for model training and test validation');
  addSlideFooter(s, 9);

  const tableRows = [
    [
      { text: 'Source Database', options: { bold: true, color: 'FFFFFF', fill: { color: '1E293B' }, fontSize: 12 } },
      { text: 'Total Variants', options: { bold: true, color: 'FFFFFF', fill: { color: '1E293B' }, fontSize: 12 } },
      { text: 'Variant Types Included', options: { bold: true, color: 'FFFFFF', fill: { color: '1E293B' }, fontSize: 12 } },
      { text: 'What We Used It For', options: { bold: true, color: 'FFFFFF', fill: { color: '1E293B' }, fontSize: 12 } }
    ],
    [
      { text: 'NCBI ClinVar (2024)', options: { bold: true, color: C.navy, fontSize: 11.5 } },
      { text: '101,232 SVs', options: { color: C.slate, fontSize: 11.5, bold: true } },
      { text: 'Deletions, Duplications, Inversions, Insertions', options: { color: C.slate, fontSize: 11 } },
      { text: 'Doctor-verified labels (1 = Disease-causing, 0 = Harmless).', options: { color: C.slate, fontSize: 11 } }
    ],
    [
      { text: 'gnomAD SV v2.1', options: { bold: true, color: C.navy, fontSize: 11.5 } },
      { text: '387,700 SVs', options: { color: C.slate, fontSize: 11.5, bold: true } },
      { text: 'Sequenced from 15,000 healthy individuals worldwide', options: { color: C.slate, fontSize: 11 } },
      { text: 'Baseline population frequencies (to check how rare a variant is in healthy humans).', options: { color: C.slate, fontSize: 11 } }
    ],
    [
      { text: '1000 Genomes Project', options: { bold: true, color: C.navy, fontSize: 11.5 } },
      { text: '68,818 SVs', options: { color: C.slate, fontSize: 11.5, bold: true } },
      { text: 'Diverse population samples from across the globe', options: { color: C.slate, fontSize: 11 } },
      { text: 'Independent cross-checking to confirm harmless common mutations.', options: { color: C.slate, fontSize: 11 } }
    ],
    [
      { text: 'Our Harmonized Dataset', options: { bold: true, color: C.blue, fontSize: 12, fill: { color: C.blueLight } } },
      { text: '44,268 SVs', options: { color: C.blue, fontSize: 12, bold: true, fill: { color: C.blueLight } } },
      { text: 'High-confidence labeled mutations (>= 50 bp)', options: { color: C.blue, fontSize: 11.5, fill: { color: C.blueLight } } },
      { text: '35,414 Training (Chr 1-18) / 8,854 Unseen Test (Chr 19-22, X, Y).', options: { color: C.blue, fontSize: 11.5, bold: true, fill: { color: C.blueLight } } }
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
  addSlideHeader(s, 'Data Engineering', 'Data Preprocessing and Harmonization', 'Standardizing different database coordinates and matching overlapping genomic regions');
  addSlideFooter(s, 10);

  const cardW = (USABLE_W - 0.6) / 3;
  const cards = [
    {
      title: 'Standardizing Coordinates',
      subtitle: 'GRCh38 Reference Genome',
      desc: 'All coordinates were converted to the latest human reference genome (GRCh38). Chromosome names were standardized (Chr 1 to 22, X, Y), and unplaced fragments were pruned.',
      color: C.blue
    },
    {
      title: '50% Reciprocal Overlap',
      subtitle: 'Preventing False Matches',
      desc: 'Variants from patient files and gnomAD are matched only if they share at least 50% of their DNA length. This prevents accidentally matching two different neighboring mutations.',
      color: C.purple
    },
    {
      title: 'Binary Label Mapping',
      subtitle: 'Ground Truth Formulation',
      desc: 'ClinVar labels were cleanly grouped into binary ground truth: 1 = Disease-Causing (Pathogenic), 0 = Harmless (Benign). 34,466 uncertain variants were saved for real-world testing.',
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
// SLIDE 11: Exploratory Genomic Data Analysis (JARGON REMOVED!)
// =========================================================================
{
  const s = pptx.addSlide();
  addSlideHeader(s, 'Genomic Analysis', 'Exploratory Genomic Data Analysis', 'Key biological patterns that give machine learning models a strong predictive signal');
  addSlideFooter(s, 11);

  const cardW = (USABLE_W - 0.6) / 3;
  const cards = [
    {
      title: 'Missing DNA is More Harmful',
      subtitle: 'Deletions vs Duplications',
      stat: '58.1%',
      statLabel: 'Deletions in Disease Variants',
      detail: 'Deletions make up 58.1% of disease-causing mutations because completely losing a DNA segment breaks essential genes. In contrast, duplications (extra copies) are often tolerated by the body and are much more likely to be harmless.',
      color: C.blue
    },
    {
      title: 'Two Clear Mutation Sizes',
      subtitle: 'Distinct Structural Peaks',
      stat: '~300 bp & ~6 kb',
      statLabel: 'Clustered Length Peaks',
      detail: 'Mutations naturally cluster into two distinct sizes: smaller jumps (~300 base pairs) and larger genomic cuts (~6,000 base pairs). This clear bimodal pattern gives our machine learning models a strong numerical signal to separate different variant types.',
      color: C.purple
    },
    {
      title: 'Rarity Identifies Disease',
      subtitle: 'Population Frequency Contrast',
      stat: 'p < 1e-300',
      statLabel: 'Statistical Separation',
      detail: 'Dangerous mutations are kept extremely rare in healthy humans (average frequency = 0.00012) because harmful variants get filtered out over generations. Harmless variants are common (frequency = 0.0418). This makes population rarity our #1 predictive feature.',
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

  s.addText('24 Clear Engineering Features', {
    x: MARGIN_X + 0.3, y: 2.40, w: 5.05, h: 0.40,
    fontSize: 18, fontFace: FONT_TITLE, bold: true, color: C.navy, margin: 0
  });

  s.addShape(pptx.ShapeType.line, {
    x: MARGIN_X + 0.3, y: 2.85, w: 5.05, h: 0, line: { color: C.border, width: 1.0 }
  });

  const featGroups = [
    { title: 'Population Rarity (12 features):', desc: 'How rare is the mutation in healthy people globally and across different ancestries (gnomAD AF, continental frequencies, homozygote counts).' },
    { title: 'Gene Importance (4 features):', desc: 'Does the mutation hit a vital gene needed for human survival (gene overlap count, pLI constraint score, LOEUF loss-of-function score).' },
    { title: 'Mutation Geometry (4 features):', desc: 'Length of the mutation in base pairs, log-scaled span, and type of variant (deletion, duplication, inversion, insertion).' },
    { title: 'DNA Sequence Context (4 features):', desc: 'Surrounding DNA stability (GC content ratio, CpG islands, and sequence repeat patterns).' }
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

  s.addText('Chromosomal Split (Zero Data Leakage)', {
    x: 7.183, y: 2.40, w: 5.05, h: 0.40,
    fontSize: 18, fontFace: FONT_TITLE, bold: true, color: C.navy, margin: 0
  });

  s.addShape(pptx.ShapeType.line, {
    x: 7.183, y: 2.85, w: 5.05, h: 0, line: { color: C.border, width: 1.0 }
  });

  s.addText([
    { text: 'The Flaw of Random Splitting:\n', options: { bold: true, color: C.red, fontSize: 13 } },
    { text: 'Standard 80/20 random splits place mutations from the same chromosome into both training and test sets. The model simply memorizes the chromosome location instead of learning biology, giving fake high scores that fail in real hospitals.\n\n', options: { color: C.slate, fontSize: 12.5 } },
    { text: 'Our Chromosomal Separation Solution:\n', options: { bold: true, color: C.emerald, fontSize: 13 } },
    { text: '• Training Set: Chromosomes 1 through 18 (35,414 variants)\n', options: { color: C.slate, fontSize: 12.5 } },
    { text: '• Test Set: Chromosomes 19, 20, 21, 22, X, Y (8,854 variants)\n\n', options: { color: C.slate, fontSize: 12.5, bold: true } },
    { text: 'Guarantees 100% zero overlap: the test set tests only completely unseen chromosomes.', options: { bold: true, color: C.navy, fontSize: 12.5 } }
  ], {
    x: 7.183, y: 3.05, w: 5.05, h: 3.35, margin: 0, lineSpacingMultiple: 1.2
  });
}

// =========================================================================
// SLIDE 13: Machine Learning and Deep Learning Models
// =========================================================================
{
  const s = pptx.addSlide();
  addSlideHeader(s, 'Model Zoo', 'Machine Learning and Deep Learning Models', 'Comparing classical tree algorithms with our custom continuous PyTorch Tabular ResNet');
  addSlideFooter(s, 13);

  // Left Side: Tree Ensembles
  s.addShape(pptx.ShapeType.roundRect, {
    x: MARGIN_X, y: 1.85, w: 5.65, h: 4.80, rectRadius: 0.08,
    fill: { color: C.white }, line: { color: C.border, width: 1.0 }
  });

  s.addText('CLASSICAL BASELINE MODELS', {
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
    { text: 'Gradient boosted trees with class weighting to handle the 4.8:1 imbalance between benign and disease variants.\n\n', options: { color: C.slate, fontSize: 12.5 } },
    { text: '• LightGBM: ', options: { bold: true, color: C.navy, fontSize: 12.5 } },
    { text: 'Fast histogram-based tree algorithm optimized for large feature tables.\n\n', options: { color: C.slate, fontSize: 12.5 } },
    { text: '• Random Forest & Logistic Regression: ', options: { bold: true, color: C.navy, fontSize: 12.5 } },
    { text: 'Standard bagging and linear baseline models for benchmarking.\n\n', options: { color: C.slate, fontSize: 12.5 } },
    { text: 'Why Trees Plateau: ', options: { bold: true, color: C.amber, fontSize: 12.5 } },
    { text: 'Trees cut features using rigid rectangular steps. They struggle to model smooth continuous drops in genetic frequency.', options: { color: C.slate, fontSize: 12.5 } }
  ], {
    x: MARGIN_X + 0.3, y: 3.05, w: 5.05, h: 3.35, margin: 0, lineSpacingMultiple: 1.2
  });

  // Right Side: Tabular ResNet
  s.addShape(pptx.ShapeType.roundRect, {
    x: 6.883, y: 1.85, w: 5.65, h: 4.80, rectRadius: 0.08,
    fill: { color: C.white }, line: { color: C.border, width: 1.0 }
  });

  s.addText('DEEP LEARNING ARCHITECTURE', {
    x: 7.183, y: 2.10, w: 5.05, h: 0.28,
    fontSize: 11, fontFace: FONT_BODY, bold: true, color: C.purple, tracking: 1
  });

  s.addText('PyTorch Tabular ResNet (Skip Connections)', {
    x: 7.183, y: 2.40, w: 5.05, h: 0.40,
    fontSize: 17, fontFace: FONT_TITLE, bold: true, color: C.navy, margin: 0
  });

  s.addShape(pptx.ShapeType.line, {
    x: 7.183, y: 2.85, w: 5.05, h: 0, line: { color: C.border, width: 1.0 }
  });

  s.addText([
    { text: '• Input Dense Layer: ', options: { bold: true, color: C.navy, fontSize: 12.5 } },
    { text: 'Projects 24 biological features into a 128-dimensional dense embedding space.\n\n', options: { color: C.slate, fontSize: 12.5 } },
    { text: '• Residual Skip Connections: ', options: { bold: true, color: C.navy, fontSize: 12.5 } },
    { text: 'Skip connections allow mathematical signals to flow freely through layers without vanishing gradients. Captures smooth non-linear curves.\n\n', options: { color: C.slate, fontSize: 12.5 } },
    { text: '• Focal Loss Optimization: ', options: { bold: true, color: C.navy, fontSize: 12.5 } },
    { text: 'Forces the neural network to ignore easy harmless variants and focus all learning capacity on catching hard-to-find disease mutations.', options: { color: C.slate, fontSize: 12.5 } }
  ], {
    x: 7.183, y: 3.05, w: 5.05, h: 3.35, margin: 0, lineSpacingMultiple: 1.2
  });
}

// =========================================================================
// SLIDE 14: Multimodal Learning and Explainable AI
// =========================================================================
{
  const s = pptx.addSlide();
  addSlideHeader(s, 'Advanced Methodologies', 'Multimodal Learning and Explainable AI', 'Combining tabular biological numbers with raw DNA sequence features and TreeSHAP');
  addSlideFooter(s, 14);

  // Left Side: Multimodal Architecture
  s.addShape(pptx.ShapeType.roundRect, {
    x: MARGIN_X, y: 1.85, w: 5.65, h: 4.80, rectRadius: 0.08,
    fill: { color: C.white }, line: { color: C.border, width: 1.0 }
  });

  s.addText('MULTIMODAL NEURAL ARCHITECTURE', {
    x: MARGIN_X + 0.3, y: 2.10, w: 5.05, h: 0.28,
    fontSize: 11, fontFace: FONT_BODY, bold: true, color: C.purple, tracking: 1
  });

  s.addText('Dual-Branch Cross-Attention Network', {
    x: MARGIN_X + 0.3, y: 2.40, w: 5.05, h: 0.40,
    fontSize: 17, fontFace: FONT_TITLE, bold: true, color: C.navy, margin: 0
  });

  s.addShape(pptx.ShapeType.line, {
    x: MARGIN_X + 0.3, y: 2.85, w: 5.05, h: 0, line: { color: C.border, width: 1.0 }
  });

  s.addText([
    { text: '• Branch 1 (Numerical Genetics, 24-dim): ', options: { bold: true, color: C.navy, fontSize: 12 } },
    { text: 'Encodes population frequencies, rarity, and gene importance scores.\n\n', options: { color: C.slate, fontSize: 12 } },
    { text: '• Branch 2 (Sequence Context, 6-dim): ', options: { bold: true, color: C.navy, fontSize: 12 } },
    { text: 'Encodes surrounding DNA letters, sequence stability, and breakpoint vulnerability.\n\n', options: { color: C.slate, fontSize: 12 } },
    { text: '• Cross-Attention Fusion: ', options: { bold: true, color: C.purple, fontSize: 12 } },
    { text: 'The attention mechanism uses DNA sequence context to dynamically amplify or dampen tabular frequency signals.', options: { color: C.slate, fontSize: 12 } }
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

  s.addText('TreeSHAP: Why Did the Model Decide This?', {
    x: 7.183, y: 2.40, w: 5.05, h: 0.40,
    fontSize: 17, fontFace: FONT_TITLE, bold: true, color: C.navy, margin: 0
  });

  s.addShape(pptx.ShapeType.line, {
    x: 7.183, y: 2.85, w: 5.05, h: 0, line: { color: C.border, width: 1.0 }
  });

  s.addText([
    { text: '• Fair Feature Contributions: ', options: { bold: true, color: C.navy, fontSize: 12 } },
    { text: 'Based on cooperative game theory: mathematically computes exactly how much each feature raised or lowered the risk score.\n\n', options: { color: C.slate, fontSize: 12 } },
    { text: '• Global Feature Ranking: ', options: { bold: true, color: C.navy, fontSize: 12 } },
    { text: 'Reveals that population rarity, gene importance, and variant length drive >70% of all decisions across 44,000 variants.\n\n', options: { color: C.slate, fontSize: 12 } },
    { text: '• Individual Patient Explanations: ', options: { bold: true, color: C.emerald, fontSize: 12 } },
    { text: 'Draws a clear visual waterfall plot for any patient, showing doctors the exact biological reasons behind the score.', options: { color: C.slate, fontSize: 12 } }
  ], {
    x: 7.183, y: 3.05, w: 5.05, h: 3.35, margin: 0, lineSpacingMultiple: 1.2
  });
}

// =========================================================================
// SLIDE 15: Experimental Setup and Evaluation Metrics
// =========================================================================
{
  const s = pptx.addSlide();
  addSlideHeader(s, 'Evaluation Protocol', 'Experimental Setup and Evaluation Metrics', 'Why accuracy is banned in medical AI and which metrics actually matter');
  addSlideFooter(s, 15);

  const cardW = (USABLE_W - 0.6) / 3;
  const cards = [
    {
      title: 'Unseen Test Cohort',
      subtitle: 'Chr 19–22, X, Y (N = 8,854)',
      desc: 'All models were evaluated on unseen chromosomes containing 8,854 variants (7,326 disease variants and 1,528 benign variants; 4.8:1 imbalance ratio). Zero overlap with training chromosomes.',
      color: C.blue
    },
    {
      title: 'PR-AUC Over Accuracy',
      subtitle: 'Precision-Recall Area',
      desc: 'Why Accuracy is Banned: 83% of variants are benign. A lazy model predicting "Benign" for everything gets 83% accuracy while missing 100% of diseases! PR-AUC measures true disease detection without being tricked by harmless variants.',
      color: C.purple
    },
    {
      title: 'Clinical Safety Metrics',
      subtitle: 'Sensitivity & Brier Score',
      desc: 'Clinical Sensitivity (Recall) measures the % of true disease mutations captured (minimizing missed diseases). Top-5% Precision checks purity at the top of the queue. Brier Score measures probability honesty.',
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
  addSlideHeader(s, 'Baseline Performance', 'Baseline Model Results: Classical Tree Ensembles', 'Benchmarking standard machine learning models on unseen test chromosomes');
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

  addMetricCard(s, 8.3, 1.85, 4.233, 2.25, '0.9696', 'XGBoost PR-AUC Baseline', 'Strong baseline ranking on the holdout test set, leading all other tree algorithms.', C.blue);

  s.addShape(pptx.ShapeType.roundRect, {
    x: 8.3, y: 4.35, w: 4.233, h: 2.30, rectRadius: 0.08,
    fill: { color: C.white }, line: { color: C.border, width: 1.0 }
  });

  s.addText('THE DANGEROUS TREE LIMITATION', {
    x: 8.55, y: 4.55, w: 3.733, h: 0.28,
    fontSize: 11.5, fontFace: FONT_BODY, bold: true, color: C.amber, tracking: 1
  });

  s.addText('Why Trees Alone Are Not Enough', {
    x: 8.55, y: 4.88, w: 3.733, h: 0.35,
    fontSize: 16, fontFace: FONT_TITLE, bold: true, color: C.navy, margin: 0
  });

  s.addText([
    { text: '1. Rigid Step Cuts: ', options: { bold: true, color: C.navy, fontSize: 12 } },
    { text: 'Trees cut continuous rarity curves into rigid blocks, losing fine-grained signals.\n', options: { color: C.slate, fontSize: 12 } },
    { text: '2. 1,745 Missed Diseases: ', options: { bold: true, color: C.navy, fontSize: 12 } },
    { text: 'At standard cutoffs, XGBoost misses 1,745 disease variants. In healthcare, missing sick patients is unacceptable.', options: { color: C.slate, fontSize: 12 } }
  ], {
    x: 8.55, y: 5.30, w: 3.733, h: 1.20, margin: 0, lineSpacingMultiple: 1.2
  });
}

// =========================================================================
// SLIDE 17: Deep Learning and Multimodal Results
// =========================================================================
{
  const s = pptx.addSlide();
  addSlideHeader(s, 'Benchmark Results', 'Deep Learning Results: Slashed Missed Diseases', 'Capturing 94.4% of disease variants and cutting false negatives by over 60%');
  addSlideFooter(s, 17);

  addMetricCard(s, MARGIN_X, 1.85, 4.3, 1.45, '94.4%', 'Clinical Sensitivity (Recall)', 'Captures 6,916 of 7,326 disease variants on unseen test chromosomes.', C.emerald);
  addMetricCard(s, MARGIN_X, 3.50, 4.3, 1.45, '414 vs 1,745', 'Missed Disease Variants', 'Slashed false negatives by >60% compared to standard XGBoost.', C.purple);
  addMetricCard(s, MARGIN_X, 5.15, 4.3, 1.50, '0.1010', 'Brier Calibration Loss', '38.8% lower probability calibration error than tree algorithms (0.165).', C.blue);

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
  addSlideHeader(s, 'Clinical Verification', 'Uncertainty Bounds & Real-World VUS Triage', 'Mathematical safety guarantees, sorting 34,466 uncertain variants, and patient explanations');
  addSlideFooter(s, 18);

  const cardW = (USABLE_W - 0.6) / 3;
  const cards = [
    {
      title: '95% Safety Guarantee',
      subtitle: 'Split Conformal Prediction',
      desc: 'Instead of arbitrary guessing, we use conformal prediction to output certified prediction sets: {Disease}, {Harmless}, or {Uncertain}. Guaranteed 95% mathematical coverage without making unverified probability assumptions.',
      color: C.blue
    },
    {
      title: 'Sorting 34,466 VUS',
      subtitle: 'Clearing Hospital Backlogs',
      desc: 'We tested the model on 34,466 uncertain ClinVar variants. It resolved 48.8% (16,801 variants) into confident categories: 6,712 High-Risk Disease, 5,198 Harmless Benign, and 4,891 Likely Disease. Cuts doctor backlogs in half.',
      color: C.emerald
    },
    {
      title: 'Patient Waterfall Plot',
      subtitle: 'Clear Case Study: BRCA1',
      desc: 'Tested on a real patient with a BRCA1 breast cancer gene deletion: Model assigns a 0.982 high-risk score. TreeSHAP visualizes why: 0% population rarity (+0.38) and vital cancer gene disruption (+0.29).',
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
  addSlideHeader(s, 'Engineering Delivery', 'End-to-End Pipeline and Demonstration', 'Our standalone CLI tool prioritize_sv.py analyzes patient files and outputs reports in 4.2 seconds');
  addSlideFooter(s, 19);

  const steps = [
    { num: 'STEP 1', title: 'File Ingestion', desc: 'Reads patient sequencing file (VCF); extracts large variants (>= 50 bp).' },
    { num: 'STEP 2', title: 'Fast Annotation', desc: 'Cross-checks with gnomAD frequency and gene importance in < 1.5s.' },
    { num: 'STEP 3', title: 'Model Scoring', desc: 'Computes continuous risk score using our Tabular ResNet or XGBoost.' },
    { num: 'STEP 4', title: 'TreeSHAP Plot', desc: 'Draws a clear visual waterfall explanation for the top-risk mutations.' },
    { num: 'STEP 5', title: 'Doctor Export', desc: 'Saves interactive HTML report, prioritized VCF, and sorted CSV queue.' }
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
    '[3/5] Running Calibrated ML Model Inference (DL): 3 High-Risk Disease candidates triaged.',
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
  addSlideHeader(s, 'Scientific Synthesis', 'Discussion', 'What our results mean: biological alignment, deep learning benefits, and clinical safety');
  addSlideFooter(s, 20);

  const cardW = (USABLE_W - 0.6) / 3;
  const cards = [
    {
      title: 'Biological Common Sense',
      subtitle: 'Model Matches Genetics',
      desc: 'The model independently learned fundamental biological rules: large deletions that cut out essential survival genes with zero frequency in healthy populations are the primary cause of severe genetic diseases.',
      color: C.blue
    },
    {
      title: 'Why Neural Beats Trees',
      subtitle: 'Continuous Math Curves',
      desc: 'Tabular ResNet outperformed decision trees because genetic rarity follows smooth continuous decay curves rather than rigid rectangular step-cuts. Residual connections map these curves smoothly, slashing missed diseases.',
      color: C.purple
    },
    {
      title: 'Safety-First Healthcare',
      subtitle: 'Conformal Prediction Impact',
      desc: 'Replacing arbitrary classification cutoffs with 95% conformal prediction intervals gives doctors certified bounds. Ambiguous edge cases are safely flagged for human doctor review instead of blindly guessed.',
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
  addSlideHeader(s, 'Constraints', 'Limitations', 'Honest technical boundaries and data constraints of the current framework');
  addSlideFooter(s, 21);

  const cardW = (USABLE_W - 0.6) / 3;
  const cards = [
    {
      num: '01',
      title: 'Database Research Bias',
      desc: 'ClinVar ground truth records are naturally biased toward heavily studied conditions like childhood illnesses and hereditary cancers. General healthy populations may carry rare harmless mutations that need wider cataloging.',
      color: C.amber
    },
    {
      num: '02',
      title: 'Linear Reference Genome',
      desc: 'Coordinates rely on standard linear human genome reference GRCh38. Complex nested loops, multi-copy changes, and complex translocations would benefit from graph-based pan-genome coordinate systems in the future.',
      color: C.slate
    },
    {
      num: '03',
      title: 'Sequencer-Specific Features',
      desc: 'Specialized chemical DNA modification marks (5mC methylation) are called natively by Oxford Nanopore devices. While very useful, they are not available in older legacy machines or short-read sequencers.',
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
  addSlideHeader(s, 'Roadmap', 'Future Scope', 'Strategic next steps for expanding the platform into clinical practice');
  addSlideFooter(s, 22);

  const cardW = (USABLE_W - 0.6) / 3;
  const cards = [
    {
      num: '01',
      title: 'Pan-Genome Variation Graphs',
      desc: 'Integrate graph-based genome tools (Minigraph-Cactus / VG) to resolve complex copy number variations and multi-way chromosomal rearrangements across diverse ancestral reference graphs.',
      color: C.blue
    },
    {
      num: '02',
      title: 'Patient Symptom Integration',
      desc: 'Connect patient hospital records (EHR) and clinical symptom tags (HPO terms) to dynamically boost risk scores for mutations directly linked to the patient\'s specific physical symptoms.',
      color: C.purple
    },
    {
      num: '03',
      title: 'Genomic Foundation Models',
      desc: 'Fine-tune pre-trained DNA foundation models (e.g., HyenaDNA, Nucleotide Transformer) on breakpoint sequences to learn deep regulatory patterns directly from raw DNA letters.',
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

  s.addText('PROJECT SUMMARY & TECHNICAL DEFENSE CONCLUSION', {
    x: MARGIN_X, y: 0.90, w: USABLE_W, h: 0.35,
    fontSize: 13, fontFace: FONT_BODY, bold: true, color: '60A5FA', tracking: 2
  });

  s.addText('Conclusion: Summary of Project Achievements', {
    x: MARGIN_X, y: 1.35, w: USABLE_W, h: 0.60,
    fontSize: 26, fontFace: FONT_TITLE, bold: true, color: 'FFFFFF'
  });

  s.addShape(pptx.ShapeType.line, {
    x: MARGIN_X, y: 2.10, w: 4.0, h: 0, line: { color: '38BDF8', width: 2.5 }
  });

  const takeaways = [
    {
      num: '01',
      title: 'Zero-Leakage Benchmark',
      desc: 'Proved true generalizability by evaluating strictly on unseen holdout Chromosomes 19–22, X, Y (0% data leakage), ensuring reliable real-world performance.'
    },
    {
      num: '02',
      title: 'Slashed Missed Diseases',
      desc: 'Our Tabular ResNet deep learning architecture reached 94.4% clinical sensitivity, cutting missed disease mutations from 1,745 down to 414 (>60% reduction vs XGBoost).'
    },
    {
      num: '03',
      title: 'Mathematical Safety Guarantee',
      desc: 'Replaced arbitrary guessing with 95% conformal prediction intervals, giving doctors certified safety bounds to avoid overconfident misdiagnoses.'
    },
    {
      num: '04',
      title: 'Real-World VUS Resolution',
      desc: 'Successfully triaged 34,466 unreviewed ClinVar variants, resolving 48.8% into clear actionable tiers with fast, visual TreeSHAP explanations in under 5 seconds.'
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
