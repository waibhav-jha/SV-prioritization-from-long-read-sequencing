"""
Master Study Guide PDF Generator for Capstone Review & Viva Defense (6-Page Exact Flow)
Project: Multimodal Deep Learning and Explainable AI for Clinical Pathogenicity Classification & VUS Triage
Authors: Waibhav Jha, Akash Bardia, Anantharaman T S, K S Jagan
Department of Artificial Intelligence, School of Computing, Amrita Vishwa Vidyapeetham
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, Image
)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register Arial Unicode TrueType Fonts from Windows Fonts directory
FONT_DIR = "C:/Windows/Fonts"
HAS_ARIAL = False

if os.path.exists(os.path.join(FONT_DIR, "arial.ttf")):
    try:
        pdfmetrics.registerFont(TTFont('Arial', os.path.join(FONT_DIR, "arial.ttf")))
        pdfmetrics.registerFont(TTFont('Arial-Bold', os.path.join(FONT_DIR, "arialbd.ttf")))
        pdfmetrics.registerFont(TTFont('Arial-Italic', os.path.join(FONT_DIR, "ariali.ttf")))
        pdfmetrics.registerFont(TTFont('Arial-BoldItalic', os.path.join(FONT_DIR, "arialbi.ttf")))
        HAS_ARIAL = True
    except Exception as e:
        print("Warning: Arial registration failed, falling back to Helvetica:", e)

F_NORM = 'Arial' if HAS_ARIAL else 'Helvetica'
F_BOLD = 'Arial-Bold' if HAS_ARIAL else 'Helvetica-Bold'
F_ITALIC = 'Arial-Italic' if HAS_ARIAL else 'Helvetica-Oblique'
F_BOLDITALIC = 'Arial-BoldItalic' if HAS_ARIAL else 'Helvetica-BoldOblique'


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont(F_NORM, 7.5)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header on pages after the first page
        if self._pageNumber > 1:
            self.drawString(36, letter[1] - 26, "CAPSTONE TECHNICAL STUDY GUIDE | Genomic Pathogenicity Classification & VUS Triage")
            self.drawRightString(letter[0] - 36, letter[1] - 26, "Amrita Vishwa Vidyapeetham")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(36, letter[1] - 30, letter[0] - 36, letter[1] - 30)
            
            # Running Footer
            self.line(36, 32, letter[0] - 36, 32)
            self.drawString(36, 20, "Department of Artificial Intelligence | Final Technical Review & Viva Defense")
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(letter[0] - 36, 20, page_text)
            
        self.restoreState()


def build_pdf():
    pdf_filename = "Genomics_Capstone_Master_Study_Guide.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=38,
        bottomMargin=38
    )

    styles = getSampleStyleSheet()

    c_primary = colors.HexColor("#1E3A8A")     # Navy
    c_secondary = colors.HexColor("#2563EB")   # Royal Blue
    c_dark = colors.HexColor("#0F172A")        # Slate Dark
    c_body = colors.HexColor("#334155")        # Charcoal body
    c_bg_card = colors.HexColor("#F8FAFC")     # Card fill

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName=F_BOLD,
        fontSize=18,
        leading=22,
        textColor=c_primary,
        spaceAfter=2
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName=F_NORM,
        fontSize=10.5,
        leading=14,
        textColor=c_secondary,
        spaceAfter=8
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName=F_BOLD,
        fontSize=12,
        leading=15,
        textColor=c_primary,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName=F_NORM,
        fontSize=8.2,
        leading=11.4,
        textColor=c_body,
        spaceAfter=3
    )

    body_bold = ParagraphStyle(
        'Body_Bold_Custom',
        parent=body_style,
        fontName=F_BOLD,
        textColor=c_dark
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=11,
        firstLineIndent=-8,
        spaceAfter=2.5
    )

    callout_style = ParagraphStyle(
        'Callout_Text',
        parent=body_style,
        fontSize=8.0,
        leading=11.2,
        textColor=c_dark
    )

    qa_q_style = ParagraphStyle(
        'QA_Q',
        parent=styles['Normal'],
        fontName=F_BOLD,
        fontSize=8.6,
        leading=12.0,
        textColor=c_primary,
        spaceBefore=4,
        spaceAfter=1.5,
        keepWithNext=True
    )

    qa_a_style = ParagraphStyle(
        'QA_A',
        parent=body_style,
        fontSize=8.0,
        leading=11.0,
        leftIndent=8,
        spaceAfter=4
    )

    code_style = ParagraphStyle(
        'Code_Snippet',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.4,
        leading=10.0,
        textColor=colors.HexColor("#0F172A")
    )

    def card_box(text_flowables, bg_color=c_bg_card, border_color=c_secondary, border_width=1):
        content = text_flowables if isinstance(text_flowables, list) else [text_flowables]
        t = Table([[content]], colWidths=[letter[0] - 72])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), bg_color),
            ('BOX', (0,0), (-1,-1), border_width, border_color),
            ('TOPPADDING', (0,0), (-1,-1), 4.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        return t

    story = []

    # ==========================================
    # PAGE 1: TITLE, PITCH, GOLDEN METRICS, BIOLOGY PRIMER
    # ==========================================
    story.append(Paragraph("CAPSTONE TECHNICAL VIVA & REVIEW MASTER STUDY GUIDE", title_style))
    story.append(Paragraph("Multimodal Deep Learning & Explainable AI for Clinical Pathogenicity Classification & VUS Triage", subtitle_style))
    
    meta_table_data = [
        [
            Paragraph("<b>Project Team & Roll Numbers:</b><br/>"
                      "&bull; <b>Waibhav Jha</b> — CB.SC.U4AIE23162<br/>"
                      "&bull; <b>Akash Bardia</b> — CB.SC.U4AIE23102<br/>"
                      "&bull; <b>Anantharaman T S</b> — CB.SC.U4AIE23112<br/>"
                      "&bull; <b>K S Jagan</b> — CB.SC.U4AIE23034", body_style),
            Paragraph("<b>Academic Profile:</b><br/>"
                      "<b>Department:</b> Artificial Intelligence<br/>"
                      "<b>School:</b> School of Computing<br/>"
                      "<b>Institution:</b> Amrita Vishwa Vidyapeetham, Coimbatore<br/>"
                      "<b>Evaluation Target:</b> End-Semester Capstone Technical Review", body_style)
        ]
    ]
    meta_table = Table(meta_table_data, colWidths=[270, 270])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#93C5FD")),
        ('PADDING', (0,0), (-1,-1), 5.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 5))

    story.append(Paragraph("1. Executive Summary & The 60-Second Elevator Pitch", h1_style))
    pitch_text = [
        Paragraph("<b>The Core Pitch to Faculty:</b> <i>\"Next-Generation Sequencing identifies thousands of missense mutations per patient, but over 40% are cataloged as Variants of Uncertain Significance (VUS), creating a critical diagnostic bottleneck. Conventional in-silico tree predictors treat variants as flat tabular records, struggle with non-linear epistatic interactions, and output over 1,700 dangerous false negatives in our test benchmark. We developed an end-to-end multimodal deep learning framework coupling a custom Tabular ResNet with Meta's 650M-parameter ESM-2 protein language representations. Under strict zero-leakage gene stratification on 137k+ ClinVar variants, our system achieves a PR-AUC of 0.9721 and clinical sensitivity of 95.1%, slashing false negatives by over 60% compared to XGBoost. Augmented with post-hoc Temperature Scaling calibration and TreeSHAP explainability, we deployed the model on 34,466 unreviewed ClinVar VUS, definitively resolving 48.8% into high-confidence actionable risk tiers at under 25 milliseconds per variant.\"</i>", callout_style)
    ]
    story.append(card_box(pitch_text, bg_color=colors.HexColor("#F0FDF4"), border_color=colors.HexColor("#22C55E"), border_width=1.2))
    story.append(Spacer(1, 5))

    story.append(Paragraph("<b>The 6 Golden Benchmark Metrics (Memorize Exactly):</b>", body_bold))
    stat_data = [
        [
            Paragraph("<b>137,708</b><br/><font color='#475569'>Variants Curated</font>", callout_style),
            Paragraph("<b>0.9721</b><br/><font color='#475569'>PR-AUC (Multimodal)</font>", callout_style),
            Paragraph("<b>95.1%</b><br/><font color='#475569'>Clinical Sensitivity</font>", callout_style),
            Paragraph("<b>414 vs 1,745</b><br/><font color='#475569'>False Negatives (>60% drop)</font>", callout_style),
            Paragraph("<b>48.8%</b><br/><font color='#475569'>VUS Resolved (16,820 / 34k)</font>", callout_style),
            Paragraph("<b>< 25 ms</b><br/><font color='#475569'>Inference Latency</font>", callout_style)
        ]
    ]
    stat_table = Table(stat_data, colWidths=[90, 90, 90, 90, 90, 90])
    stat_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(stat_table)
    story.append(Spacer(1, 5))

    story.append(Paragraph("2. Biological & Clinical Foundations (Genomics Primer)", h1_style))
    bio_items = [
        ("Missense Single Nucleotide Variant (SNV):", "A point mutation in DNA where a single nucleotide change alters a codon, producing a different amino acid in the encoded protein. This substitution can disrupt catalytic active sites, destabilize core tertiary folding, or break critical ligand interfaces."),
        ("ClinVar Archive:", "The international public archive maintained by NCBI where diagnostic testing laboratories deposit observed human genomic variants alongside clinical evidence and pathogenic interpretations."),
        ("ACMG/AMP 5-Tier Guidelines:", "The global clinical standard for variant reporting: (1) Pathogenic, (2) Likely Pathogenic, (3) Variant of Uncertain Significance (VUS), (4) Likely Benign, and (5) Benign."),
        ("The VUS Bottleneck:", "Variants with conflicting, scarce, or ambiguous clinical evidence. Physicians cannot act on a VUS (no preventative surgeries, no targeted therapies). Patients remain trapped in 'diagnostic purgatory'."),
        ("PhyloP & GERP++ Conservation:", "Evolutionary conservation metrics computed across 100-way vertebrate alignments. Positions conserved across evolutionary epochs are functionally intolerant; mutating them is overwhelmingly pathogenic."),
        ("CADD Phred Score:", "Combined Annotation-Dependent Depletion. Contrasts simulated de novo variants against fixed neutral variation. A Phred score ≥ 20 indicates the top 1% most deleterious variants in the genome; ≥ 30 indicates top 0.1%."),
        ("REVEL Score:", "Rare Exome Variant Ensemble Learner. An ACMG-endorsed ensemble predictor combining 13 tools, widely regarded as the clinical benchmark for missense deleteriousness."),
        ("Gene Constraint (pLI & LOEUF):", "pLI (Probability of Loss-of-function Intolerance) and LOEUF from gnomAD. Genes with pLI > 0.9 or low LOEUF cannot tolerate heterozygous loss; mutations here are substantially more likely to cause disease."),
        ("Allele Frequency (AF):", "How frequently the variant occurs in healthy populations (gnomAD, ExAC, 1000G). Pathogenic mutations are kept rare by natural selection (AF < 0.0001). Any variant with AF > 1% is almost certainly benign.")
    ]
    for term, desc in bio_items:
        story.append(Paragraph(f"&bull; <b>{term}</b> {desc}", bullet_style))

    # Explicit clean PageBreak after Page 1
    story.append(PageBreak())

    # ==========================================
    # PAGE 2: DATA ENGINEERING, LEAKAGE, ARCHITECTURE, FIGURE 1
    # ==========================================
    story.append(Paragraph("3. Dataset, Preprocessing & Zero-Leakage Protocol", h1_style))
    data_points = [
        ("Cohort Scale & Composition:", "137,708 annotated missense variants (23,607 Pathogenic / Likely Pathogenic; 114,101 Benign / Likely Benign). An independent cohort of 34,466 unreviewed VUS was held out strictly for real-world triage evaluation."),
        ("Severe Class Imbalance:", "Benign variants outnumber pathogenic mutations by ~4.8:1 in the holdout test set (82.9% Benign vs. 17.1% Pathogenic). This matches real-world clinical sequencing registries."),
        ("Handling Missing Genomic Data:", "Genomic annotation tables feature non-random missingness. We used <b>domain-specific median imputation</b> combined with <b>binary missingness indicator masks (m_i in {0, 1}^19)</b> so the neural network treats missingness as an informative biological signal rather than noise."),
        ("Feature Normalization:", "Robust quantile scaling applied to wide-range continuous conservation scores (PhyloP, GERP++, CADD) to prevent gradient instability.")
    ]
    for t, d in data_points:
        story.append(Paragraph(f"&bull; <b>{t}</b> {d}", bullet_style))
    story.append(Spacer(1, 4))

    leakage_box = [
        Paragraph("<b>CRITICAL EXAM QUESTION: How Did You Prevent Data Leakage?</b><br/>"
                  "<b>The Trap:</b> If you use standard random <code>train_test_split</code>, variants from the <i>same gene</i> (e.g., <i>BRCA1</i>) appear in both train and test partitions. Shallow models simply memorize that <i>BRCA1</i> is a cancer gene and artificially inflate accuracy without learning mutation biology.<br/>"
                  "<b>Our Zero-Leakage Solution:</b> We strictly enforced <b>Gene-Stratified Group Partitioning</b> (GroupKFold by Ensembl Gene ID). All mutations in any given gene belong 100% exclusively to Train (70%), Val (15%), or Test (15%). The test set evaluates performance on <i>completely unseen proteins</i>, reflecting genuine clinical diagnostic reality.", callout_style)
    ]
    story.append(card_box(leakage_box, bg_color=colors.HexColor("#FEF2F2"), border_color=colors.HexColor("#EF4444"), border_width=1.2))
    story.append(Spacer(1, 5))

    story.append(Paragraph("4. Model Architecture: Tabular ResNet & Multimodal Fusion", h1_style))
    arch_points = [
        ("The Limitation of Tree Ensembles (XGBoost / LightGBM):", "Trees make orthogonal, axis-aligned feature splits. They struggle to model continuous, non-linear epistatic interactions across protein domains, leading to <b>1,745 missed pathogenic mutations</b>."),
        ("Tabular ResNet Formulation:", "Uses residual skip connections adapted for continuous genomic annotations. Architecture: Linear Projection → Residual Blocks (LayerNorm → ReLU → Dropout(0.2) → Linear → Residual Addition with scale factor α = 0.2). LayerNorm stabilizes wide-ranging conservation scales; skip connections prevent gradient dissipation."),
        ("Focal Loss Objective:", "Standard binary cross-entropy treats all errors equally. We implemented Focal Loss: L_focal = -α_t (1 - p_t)^γ log(p_t) with focusing parameter γ = 2.0. This heavily downweights easy benign examples and forces the optimizer to focus gradients on hard, ambiguous pathogenic mutations."),
        ("ESM-2 650M Protein Language Embeddings:", "Meta's ESM-2 (esm2_t33_650M_UR50D) was trained on millions of evolutionary sequences via masked language modeling. It captures hidden 3D structural stability, residue contacts, and secondary structures without requiring crystallographic coordinates. We extract 1280-dimensional embeddings from Layer 33."),
        ("Gated Bilinear Cross-Modal Pooling:", "Branch 1 (Tabular ResNet 19 features → 128-d) and Branch 2 (ESM-2 1280-d → dense bottleneck 128-d) are fused using gated bilinear interaction: f_fused = σ(W_g [h_tab; e_seq]) * (W_m [h_tab; e_seq]). This allows sequence embeddings to dynamically gate and amplify relevant conservation signals.")
    ]
    for t, d in arch_points:
        story.append(Paragraph(f"&bull; <b>{t}</b> {d}", bullet_style))
    story.append(Spacer(1, 4))

    # Embed Figure 1
    if os.path.exists("figures/13_multimodal_architecture_and_curves.png"):
        img1 = Image("figures/13_multimodal_architecture_and_curves.png", width=515, height=195)
        story.append(KeepTogether([
            img1,
            Spacer(1, 2),
            Paragraph("<b>Figure 1:</b> (A) Multimodal Architecture dual-branch schematic; (B) Precision-Recall curves on imbalanced holdout test cohort; (C) ROC curves demonstrating high diagnostic discrimination.", callout_style)
        ]))

    # Explicit clean PageBreak after Page 2
    story.append(PageBreak())

    # ==========================================
    # PAGE 3: METRICS DEEP DIVE, BENCHMARK TABLE, FIGURE 2
    # ==========================================
    story.append(Paragraph("5. Evaluation Metrics Deep Dive: Why Accuracy is Banned", h1_style))
    acc_box = [
        Paragraph("<b>THE FACULTY TRAP: \"Why didn't you report Accuracy?\"</b><br/>"
                  "<b>The Mathematical Proof:</b> In clinical genomics with an imbalanced cohort (4.8:1 benign-to-pathogenic ratio; 82.9% Benign), accuracy is mathematically deceptive. A trivial dummy model that blindly predicts <i>every single variant as Benign</i> achieves an <b>accuracy of 82.9%</b> while missing <b>100% of deadly diseases</b>! In medical AI, false negatives mean missed cancer diagnoses and untreated patients. Therefore, clinical genetics benchmarks strictly ban raw accuracy in favor of imbalance-aware metrics.", callout_style)
    ]
    story.append(card_box(acc_box, bg_color=colors.HexColor("#FFFBEB"), border_color=colors.HexColor("#F59E0B"), border_width=1.2))
    story.append(Spacer(1, 4))

    metric_items = [
        ("PR-AUC (Precision-Recall Area Under Curve):", "The primary clinical triage metric. Evaluates precision and recall across all thresholds without being artificially boosted by the massive volume of true negatives."),
        ("Clinical Sensitivity (Recall = TP / (TP + FN)):", "Our top clinical safety priority. Measures the fraction of true pathogenic variants successfully detected. A higher sensitivity directly eliminates dangerous false negatives."),
        ("Specificity (TN / (TN + FP)):", "Measures the fraction of benign variants correctly classified. Prevents unnecessary invasive medical interventions on healthy carriers."),
        ("Top-5% Precision:", "The purity of the top 5% highest-risk predicted mutations. Critical for clinical laboratory workflow because geneticists inspect the top-ranked variants first."),
        ("Brier Calibration Score:", "Brier = (1/N) Σ (p_i - y_i)^2. Measures probability calibration error. A model with low Brier score outputs true empirical risk probabilities (e.g., p = 0.90 means 9 out of 10 variants are genuinely pathogenic).")
    ]
    for m, d in metric_items:
        story.append(Paragraph(f"&bull; <b>{m}</b> {d}", bullet_style))
    story.append(Spacer(1, 5))

    story.append(Paragraph("6. Comprehensive Benchmark Results & Master Table", h1_style))
    story.append(Paragraph("All models benchmarked on the <b>same 20,657 holdout variants under strict gene stratification</b>:", body_style))

    results_table_data = [
        [
            Paragraph("<b>Architecture</b>", callout_style),
            Paragraph("<b>PR-AUC</b>", callout_style),
            Paragraph("<b>ROC-AUC</b>", callout_style),
            Paragraph("<b>F1-Score</b>", callout_style),
            Paragraph("<b>Sensitivity</b>", callout_style),
            Paragraph("<b>Specificity</b>", callout_style),
            Paragraph("<b>Top-5% P.</b>", callout_style),
            Paragraph("<b>False Neg.</b>", callout_style)
        ],
        [
            Paragraph("Random Forest", body_style),
            Paragraph("0.9612", body_style),
            Paragraph("0.8794", body_style),
            Paragraph("0.9250", body_style),
            Paragraph("85.6%", body_style),
            Paragraph("91.2%", body_style),
            Paragraph("98.1%", body_style),
            Paragraph("2,143", body_style)
        ],
        [
            Paragraph("LightGBM", body_style),
            Paragraph("0.9689", body_style),
            Paragraph("0.8871", body_style),
            Paragraph("0.9340", body_style),
            Paragraph("87.9%", body_style),
            Paragraph("92.1%", body_style),
            Paragraph("98.8%", body_style),
            Paragraph("1,821", body_style)
        ],
        [
            Paragraph("CatBoost", body_style),
            Paragraph("0.9691", body_style),
            Paragraph("0.8875", body_style),
            Paragraph("0.9350", body_style),
            Paragraph("88.1%", body_style),
            Paragraph("92.2%", body_style),
            Paragraph("98.8%", body_style),
            Paragraph("1,790", body_style)
        ],
        [
            Paragraph("XGBoost (Baseline)", body_style),
            Paragraph("0.9696", body_style),
            Paragraph("0.8883", body_style),
            Paragraph("0.9360", body_style),
            Paragraph("88.4%", body_style),
            Paragraph("92.3%", body_style),
            Paragraph("98.9%", body_style),
            Paragraph("1,745", body_style)
        ],
        [
            Paragraph("Multi-Layer Perceptron", body_style),
            Paragraph("0.9678", body_style),
            Paragraph("0.8850", body_style),
            Paragraph("0.9310", body_style),
            Paragraph("90.2%", body_style),
            Paragraph("91.5%", body_style),
            Paragraph("98.5%", body_style),
            Paragraph("1,478", body_style)
        ],
        [
            Paragraph("<b>Tabular ResNet (Ours)</b>", body_style),
            Paragraph("<b>0.9705</b>", body_style),
            Paragraph("<b>0.8892</b>", body_style),
            Paragraph("0.9290", body_style),
            Paragraph("<b>94.4%</b>", body_style),
            Paragraph("89.8%", body_style),
            Paragraph("0.9890", body_style),
            Paragraph("<b>414</b>", body_style)
        ],
        [
            Paragraph("<b>Multimodal (ResNet+ESM-2)</b>", body_style),
            Paragraph("<b>0.9721</b>", body_style),
            Paragraph("<b>0.8915</b>", body_style),
            Paragraph("<b>0.9380</b>", body_style),
            Paragraph("<b>95.1%</b>", body_style),
            Paragraph("<b>90.6%</b>", body_style),
            Paragraph("<b>99.1%</b>", body_style),
            Paragraph("<b>362</b>", body_style)
        ]
    ]

    res_table = Table(results_table_data, colWidths=[120, 55, 55, 55, 65, 65, 60, 65])
    res_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('ALIGN', (0,0), (0,-1), 'LEFT'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-3), [colors.white, colors.HexColor("#F8FAFC")]),
        ('BACKGROUND', (0,-2), (-1,-2), colors.HexColor("#EFF6FF")),  # Highlight ResNet
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#DCFCE7")),  # Highlight Multimodal
        ('PADDING', (0,0), (-1,-1), 3.5),
    ]))
    story.append(res_table)
    story.append(Spacer(1, 4))

    # Embed Figure 2 (Confusion Matrices)
    if os.path.exists("figures/12_confusion_matrices.png"):
        img2 = Image("figures/12_confusion_matrices.png", width=515, height=205)
        story.append(KeepTogether([
            img2,
            Spacer(1, 2),
            Paragraph("<b>Figure 2:</b> Confusion Matrix Comparison across Models. Note that Tabular ResNet drops false negatives from 1,745 (XGBoost) down to 414 (>60% reduction in missed disease-causing mutations).", callout_style)
        ]))

    # Explicit clean PageBreak after Page 3
    story.append(PageBreak())

    # ==========================================
    # PAGE 4: XAI, VUS TRIAGE, VIVA Q1-Q5
    # ==========================================
    story.append(Paragraph("7. Uncertainty Quantification & Explainable AI (XAI)", h1_style))
    xai_points = [
        ("Temperature Scaling Calibration:", "Deep networks and tree ensembles frequently suffer from overconfidence. We applied post-hoc Temperature Scaling: p_calibrated = σ(z / T). The optimal temperature T* = 1.34 was learned on validation logits via NLL minimization. This reduced Expected Calibration Error (ECE) by <b>42%</b>, bringing Brier score down to 0.1010."),
        ("Conformal Prediction Intervals:", "Using non-conformity scores on validation variants, we compute prediction sets with a <b>95% coverage guarantee</b>. Any variant with ambiguous confidence bounds is automatically routed to human geneticists for manual review."),
        ("Global Explainability (TreeSHAP / KernelSHAP):", "SHAP feature attribution identified that <b>REVEL score</b>, <b>CADD Phred</b>, and <b>vertebrate PhyloP</b> drive >65% of the total predictive gain. Gene constraint (pLI) acts as a non-linear amplifier (mutations in pLI > 0.9 genes require lower conservation thresholds to be flagged pathogenic)."),
        ("Local Patient Waterfall Plots:", "For any individual variant, our pipeline generates a patient-level waterfall plot showing exactly how much each biological feature (e.g., CADD = 28.4 pushing +1.4, gnomAD AF = 0.00001 pushing +0.8) contributed to the final pathogenic probability.")
    ]
    for t, d in xai_points:
        story.append(Paragraph(f"&bull; <b>{t}</b> {d}", bullet_style))
    story.append(Spacer(1, 5))

    story.append(Paragraph("8. Real-World Clinical Triage Outcome (34,466 VUS Cohort)", h1_style))
    triage_table_data = [
        [
            Paragraph("<b>Clinical Triage Tier</b>", callout_style),
            Paragraph("<b>Calibrated Prob. Range</b>", callout_style),
            Paragraph("<b>Variant Count</b>", callout_style),
            Paragraph("<b>Percentage</b>", callout_style),
            Paragraph("<b>Clinical Action & Recommended Workflow</b>", callout_style)
        ],
        [
            Paragraph("<b>Tier 1: Actionable Pathogenic</b>", body_style),
            Paragraph("p ≥ 0.90", body_style),
            Paragraph("<b>6,238</b>", body_style),
            Paragraph("<b>18.1%</b>", body_style),
            Paragraph("High-priority clinical geneticist review; expedite targeted cancer panels or functional assay confirmation.", body_style)
        ],
        [
            Paragraph("<b>Tier 3: Confidently Benign</b>", body_style),
            Paragraph("p ≤ 0.10", body_style),
            Paragraph("<b>10,582</b>", body_style),
            Paragraph("<b>30.7%</b>", body_style),
            Paragraph("Ruled out as non-deleterious neutral polymorphisms; de-escalate patient anxiety, avoid invasive biopsies.", body_style)
        ],
        [
            Paragraph("<b>Tier 2: Borderline / Indeterminate</b>", body_style),
            Paragraph("0.10 < p < 0.90", body_style),
            Paragraph("<b>17,646</b>", body_style),
            Paragraph("51.2%", body_style),
            Paragraph("Reserved for multidisciplinary tumor board review; paired with conformal 95% uncertainty interval and SHAP explanation.", body_style)
        ]
    ]

    triage_table = Table(triage_table_data, colWidths=[130, 80, 70, 60, 200])
    triage_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#334155")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#FEE2E2")),
        ('BACKGROUND', (0,2), (-1,2), colors.HexColor("#DCFCE7")),
        ('BACKGROUND', (0,3), (-1,3), colors.HexColor("#FEF3C7")),
        ('ALIGN', (1,0), (3,-1), 'CENTER'),
        ('PADDING', (0,0), (-1,-1), 3.5),
    ]))
    story.append(triage_table)
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>The Definitive Clinical Outcome:</b> <b>48.8% of unreviewed VUS (16,820 variants)</b> were definitively reclassified into high-confidence clinical tiers (Tier 1 + Tier 3), cutting the manual laboratory geneticist backlog by nearly 50% at sub-25 ms per-variant latency.", callout_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("9. Faculty Viva Defense: Top 15 Tough Questions & Bulletproof Answers", h1_style))
    story.append(Paragraph("Study these answers thoroughly. They address the exact questions faculty will raise during evaluation:", body_style))

    viva_qa_part1 = [
        (
            "Q1: Why did you build a Deep Learning model when XGBoost is already known as the king of tabular data?",
            "\"While XGBoost achieved a respectable F1-score of 0.936, it has an orthogonal decision tree architecture that struggles with complex epistatic, non-linear biological interactions. This resulted in 1,745 missed pathogenic mutations (false negatives) in our test set. Our Tabular ResNet utilizes residual manifold learning and focal loss, which increased clinical sensitivity from 88.4% to 94.4%, slashing false negatives down to 414. In healthcare, missed diagnoses are unacceptable, making deep representation learning clinically superior.\""
        ),
        (
            "Q2: Why did you not report Accuracy in your main results?",
            "\"Because our genomic dataset exhibits a 4.8:1 class imbalance (82.9% Benign vs. 17.1% Pathogenic). In imbalanced medical data, accuracy is mathematically misleading. A naive classifier predicting all variants as Benign achieves 82.9% accuracy while missing 100% of diseases. In compliance with clinical AI standards, we evaluate on PR-AUC, ROC-AUC, Sensitivity, Specificity, Top-5% Precision, and Brier calibration loss.\""
        ),
        (
            "Q3: How do you prove your model didn't just overfit or memorize specific genes?",
            "\"We enforced a strict, zero-leakage Gene-Stratified Split (GroupKFold by Ensembl Gene ID). All mutations belonging to any individual gene were strictly restricted to either Train (70%), Validation (15%), or Test (15%). There is zero gene overlap between splits. Our model was evaluated exclusively on completely unseen genes, proving true generalizability to novel protein folds.\""
        ),
        (
            "Q4: What is ESM-2 and why is it better than one-hot encoding amino acids?",
            "\"One-hot encoding only tells the model the identity of an amino acid (e.g., Alanine vs. Proline) with zero biochemical or structural context. ESM-2 is a 650M-parameter protein language foundation model pre-trained by Meta on millions of evolutionary sequences. Its internal representations capture secondary structure, solvent accessibility, and residue-residue contact networks. By extracting 1280-dimensional embeddings from Layer 33, our model learns how a mutation disrupts the entire local 3D protein microenvironment.\""
        ),
        (
            "Q5: Why did you choose Focal Loss instead of standard Cross-Entropy?",
            "\"Standard Cross-Entropy sums errors across all samples, causing the abundant easy benign variants to dominate the gradient updates. Focal Loss introduces a dynamic modulating factor (1 - p_t)^γ with γ = 2.0. As the model becomes confident on easy benign variants, their gradient contribution drops to near zero, forcing the network to focus its capacity on hard, ambiguous pathogenic mutations.\""
        )
    ]
    for q, a in viva_qa_part1:
        story.append(Paragraph(f"<b>{q}</b>", qa_q_style))
        story.append(Paragraph(a, qa_a_style))

    # Explicit clean PageBreak after Page 4
    story.append(PageBreak())

    # ==========================================
    # PAGE 5: VIVA Q6-Q12
    # ==========================================
    story.append(Paragraph("9. Faculty Viva Defense (Continued): Technical & Methodological Cross-Examination", h1_style))

    viva_qa_part2 = [
        (
            "Q6: What is a Brier Score and why does calibration matter in healthcare?",
            "\"Modern deep networks are notorious for uncalibrated overconfidence—outputting probabilities of 0.99 even when wrong. The Brier score measures the mean squared difference between predicted probabilities and actual binary outcomes. Through post-hoc Temperature Scaling, we reduced Expected Calibration Error (ECE) by 42% and achieved a Brier score of 0.1010. This ensures our probability outputs represent genuine empirical likelihoods for clinical risk assessment.\""
        ),
        (
            "Q7: What is the biological difference between PhyloP and GERP++?",
            "\"Both evaluate evolutionary conservation, but with distinct statistical formulations. GERP++ calculates 'rejected substitutions'—the difference between neutral substitution rates and observed rates across mammalian alignments. PhyloP performs hypothesis testing against a neutral evolutionary model across 100 vertebrate genomes, detecting both evolutionary acceleration and negative selection. Their correlation in our data is r = 0.74, and using both provides cross-species conservation stability.\""
        ),
        (
            "Q8: How did you handle missing values without biasing your predictions?",
            "\"In genomics, missingness is not missing-at-random (MAR); it is often informative (e.g., certain scores exist only for specific protein classes). Discarding incomplete variants would lose critical mutations. We used domain-specific median imputation and augmented each sample with a binary missingness vector m_i in {0, 1}^19. This allows the neural network to learn whether the absence of a test is biologically meaningful.\""
        ),
        (
            "Q9: What is the difference between Gene Constraint metrics pLI and LOEUF?",
            "\"pLI (Probability of Loss-of-function Intolerance) from gnomAD is a probability score between 0 and 1; genes with pLI > 0.9 are deemed severely intolerant to mutations. LOEUF (Loss-of-function Observed/Expected Upper bound Fraction) is a continuous metric representing the upper bound of the 90% confidence interval of observed/expected loss-of-function variants. Lower LOEUF values indicate stronger selective constraint against mutations.\""
        ),
        (
            "Q10: How does your tool help a clinician in a hospital tomorrow?",
            "\"In our triage simulation of 34,466 uncharacterized ClinVar VUS, our system immediately reclassified 48.8% into high-confidence actionable tiers (Tier 1 Pathogenic: 18.1%, Tier 3 Benign: 30.7%) with sub-25 ms latency. For the remaining 51.2% borderline variants, it outputs conformal confidence intervals and SHAP waterfall plots explaining the exact biophysical drivers, allowing clinical geneticists to prioritize their manual review queue.\""
        ),
        (
            "Q11: Why did you use SHAP instead of LIME for explainability?",
            "\"LIME creates local linear approximations by perturbing inputs, which can produce unstable, non-deterministic explanations for nearby points. SHAP (Shapley Additive exPlanations) is rooted in cooperative game theory and satisfies mathematical axioms of Local Accuracy, Missingness, and Consistency. For tabular and multimodal genomic data, TreeSHAP and KernelSHAP provide exact, stable feature attributions.\""
        ),
        (
            "Q12: Why did Tabular ResNet have slightly lower overall F1 (0.929 vs 0.936) than XGBoost?",
            "\"XGBoost maximized overall F1 by being conservative, achieving high specificity (92.3%) at the cost of missing 1,745 pathogenic mutations (sensitivity 88.4%). In a clinical setting, specificity at the expense of sensitivity is dangerous. Tabular ResNet intentionally prioritized sensitivity (94.4%), accepting a modest 2.5% increase in benign false alarms to rescue over 1,300 missed disease cases. Furthermore, when fused with ESM-2 embeddings in our Multimodal model, F1 rose back to 0.9380.\""
        )
    ]
    for q, a in viva_qa_part2:
        story.append(Paragraph(f"<b>{q}</b>", qa_q_style))
        story.append(Paragraph(a, qa_a_style))

    # Explicit clean PageBreak after Page 5
    story.append(PageBreak())

    # ==========================================
    # PAGE 6: VIVA Q13-Q15, FORMULA CHEAT SHEET, VIVA MINDSET
    # ==========================================
    story.append(Paragraph("9. Faculty Viva Defense (Continued): Advanced Edge Cases & Limitations", h1_style))

    viva_qa_part3 = [
        (
            "Q13: What happens if a patient has an insertion/deletion (InDel) or structural variant?",
            "\"Our current architecture is specifically specialized for missense single nucleotide variants (SNVs), which represent the largest and most ambiguous subset of coding variation. Structural variants and InDels alter reading frames and copy numbers, requiring specialized breakpoint and sequence-graph tools. Extending this architecture to non-coding and structural variants is part of our future roadmap.\""
        ),
        (
            "Q14: How does Conformal Prediction provide a mathematical guarantee?",
            "\"Conformal prediction utilizes non-conformity scores computed on a calibration partition to build prediction sets C(x) such that P(Y in C(x)) ≥ 1 - ε, where ε = 0.05 for a 95% confidence guarantee. If a variant's prediction set contains both {Benign, Pathogenic}, the model formally declares the prediction ambiguous, triggering mandatory manual laboratory review.\""
        ),
        (
            "Q15: What are the primary limitations of your study?",
            "\"First, our ground truth labels from ClinVar reflect historical clinical research bias toward well-studied medical panels like hereditary cancers (BRCA1/2) and cardiomyopathy. Second, our protein representations rely on 1D sequence language models rather than direct 3D atomic coordinates from cryo-EM or AlphaFold graphs. Addressing these via Geometric Graph Neural Networks (GNNs) is our primary future direction.\""
        )
    ]
    for q, a in viva_qa_part3:
        story.append(Paragraph(f"<b>{q}</b>", qa_q_style))
        story.append(Paragraph(a, qa_a_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("10. Master Mathematical Formula & Metric Cheat Sheet", h1_style))

    formulas = [
        ("Sensitivity (Recall):", "TP / (TP + FN)  [Target: Maximize to eliminate false negatives]"),
        ("Specificity:", "TN / (TN + FP)  [Target: Rule out healthy benign polymorphisms]"),
        ("Precision:", "TP / (TP + FP)  [Purity of pathogenic calls]"),
        ("F1-Score:", "2 × (Precision × Recall) / (Precision + Recall)"),
        ("Focal Loss:", "L_focal = -α_t (1 - p_t)^γ log(p_t)  [γ = 2.0 downweights easy benign samples]"),
        ("Temperature Scaling:", "p_calibrated = 1 / (1 + exp(-z / T))  [T* = 1.34 learned on validation logits]"),
        ("Gated Bilinear Fusion:", "f_fused = σ(W_g [h_tab; e_seq]) * (W_m [h_tab; e_seq])"),
        ("Brier Calibration Loss:", "Brier = (1/N) Σ (p_i - y_i)^2  [Lower is better; measures calibrated probability error]")
    ]

    form_table_data = [[Paragraph(f"<b>{name}</b>", callout_style), Paragraph(f"<code>{formula}</code>", code_style)] for name, formula in formulas]
    form_table = Table(form_table_data, colWidths=[150, 390])
    form_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('PADDING', (0,0), (-1,-1), 3.0),
    ]))
    story.append(form_table)
    story.append(Spacer(1, 8))

    closing_box = [
        Paragraph("<b>Final Viva Reminder & Presentation Mindset:</b> Speak with calm academic confidence. When asked about metrics, immediately lead with <b>PR-AUC and Clinical Sensitivity</b> (explain why accuracy is clinically dangerous). When asked about machine learning design, explain the <b>Tabular ResNet + ESM-2 multimodal synergy</b>. When asked about clinical translation, cite the <b>48.8% resolution rate on 34,466 VUS</b>. You have engineered a complete, verified, and defensible genomic AI system.", callout_style)
    ]
    story.append(card_box(closing_box, bg_color=colors.HexColor("#EFF6FF"), border_color=colors.HexColor("#3B82F6"), border_width=1.2))

    doc.build(story, canvasmaker=NumberedCanvas)
    print("SUCCESS: Master Study Guide compiled cleanly.")

if __name__ == "__main__":
    build_pdf()
