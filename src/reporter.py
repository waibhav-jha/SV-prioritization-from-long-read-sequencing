"""
src/reporter.py
===============
Enterprise-Grade Clinical Genomics Triage Report Generator.
Features Scientific Blue UI, embedded custom fonts (Daffiys & Finish Lines) for branding/headlines,
Hanken Grotesque for clinical text, interactive filters, expandable variant rows, and SVG wave background.
"""

import os
import json
import base64
import pandas as pd
import numpy as np

class ClinicalReporter:
    def __init__(self, df_prioritized, sample_name="Patient_Sample", top_shap_images=None):
        self.df = df_prioritized
        self.sample_name = sample_name
        self.top_shap_images = top_shap_images or []
        
    def _resolve_path(self, p):
        for candidate in [p, os.path.join("..", p), os.path.join("data", p), os.path.join("..", "data", p)]:
            if os.path.exists(candidate):
                return candidate
        return p
        
    def _load_font_b64(self, font_rel_path):
        p = self._resolve_path(font_rel_path)
        if os.path.exists(p):
            with open(p, "rb") as f:
                return base64.b64encode(f.read()).decode("utf-8")
        return None
        
    def save_csv(self, out_path):
        """Save prioritized variants to structured CSV."""
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        export_cols = [
            "var_id", "chrom", "start", "stop", "length", "raw_svtype",
            "pathogenicity_score", "priority_tier", "clinical_recommendation",
            "gnomad_af", "gnomad_popmax_af", "gene_count", "gnomad_lof", "support"
        ]
        available_cols = [c for c in export_cols if c in self.df.columns]
        self.df[available_cols].to_csv(out_path, index=False)
        print(f"Saved ranked CSV report to: {out_path}")
        
    def save_annotated_vcf(self, raw_vcf_path, out_vcf_path):
        """Output new VCF with PRIORITY_SCORE and PRIORITY_TIER added to INFO."""
        os.makedirs(os.path.dirname(out_vcf_path), exist_ok=True)
        
        score_lookup = {}
        for _, r in self.df.iterrows():
            key = (str(r["chrom"]), int(r["start"]))
            score_lookup[key] = (r["pathogenicity_score"], r["priority_tier"].split(" ")[0])
            
        with open(raw_vcf_path, "r", encoding="utf-8") as f_in, open(out_vcf_path, "w", encoding="utf-8") as f_out:
            for line in f_in:
                if line.startswith("##INFO"):
                    f_out.write(line)
                    continue
                if line.startswith("#CHROM"):
                    f_out.write('##INFO=<ID=PRIORITY_SCORE,Number=1,Type=Float,Description="AI-Predicted Pathogenicity Prioritization Score (0.0 to 1.0)">\n')
                    f_out.write('##INFO=<ID=PRIORITY_TIER,Number=1,Type=String,Description="Clinical Triage Risk Tier (Tier1 to Tier4)">\n')
                    f_out.write(line)
                    continue
                if line.startswith("#"):
                    f_out.write(line)
                    continue
                    
                parts = line.strip().split("\t")
                if len(parts) < 8:
                    f_out.write(line)
                    continue
                    
                chrom = parts[0].replace("chr", "")
                try:
                    pos = int(parts[1])
                except ValueError:
                    f_out.write(line)
                    continue
                    
                key = (chrom, pos)
                if key in score_lookup:
                    score, tier = score_lookup[key]
                    parts[7] = parts[7] + f";PRIORITY_SCORE={score:.4f};PRIORITY_TIER={tier}"
                    
                f_out.write("\t".join(parts) + "\n")
                
        print(f"Saved annotated VCF to: {out_vcf_path}")
        
    def generate_html_report(self, out_html_path):
        """Generate enterprise-grade clinical triage HTML report with custom fonts."""
        os.makedirs(os.path.dirname(out_html_path), exist_ok=True)
        
        total_svs = len(self.df)
        tier1_count = int((self.df["priority_tier"].str.contains("Tier 1")).sum())
        tier2_count = int((self.df["priority_tier"].str.contains("Tier 2")).sum())
        tier3_count = int((self.df["priority_tier"].str.contains("Tier 3")).sum())
        tier4_count = int((self.df["priority_tier"].str.contains("Tier 4")).sum())
        
        # Load custom fonts
        daffiys_b64 = self._load_font_b64("font/Daffiys.ttf")
        finishlines_b64 = self._load_font_b64("font/Finish Lines.otf")
        
        font_faces_css = ""
        if daffiys_b64:
            font_faces_css += f"""
            @font-face {{
                font-family: 'Daffiys';
                src: url(data:font/truetype;charset=utf-8;base64,{daffiys_b64}) format('truetype');
                font-weight: normal;
                font-style: normal;
            }}
            """
        if finishlines_b64:
            font_faces_css += f"""
            @font-face {{
                font-family: 'Finish Lines';
                src: url(data:font/opentype;charset=utf-8;base64,{finishlines_b64}) format('opentype');
                font-weight: normal;
                font-style: normal;
            }}
            """
            
        # Build Table Rows & Interactive Details
        table_rows_html = ""
        for i, row in self.df.iterrows():
            tier_str = row.get("priority_tier", "")
            score = float(row.get("pathogenicity_score", 0.0))
            score_pct = int(score * 100)
            
            if "Tier 1" in tier_str:
                tier_slug = "tier1"
                badge_label = "Tier 1: Pathogenic"
                score_bar_color = "#f43f5e"
            elif "Tier 2" in tier_str:
                tier_slug = "tier2"
                badge_label = "Tier 2: Moderate"
                score_bar_color = "#f59e0b"
            elif "Tier 3" in tier_str:
                tier_slug = "tier3"
                badge_label = "Tier 3: Low Risk"
                score_bar_color = "#38bdf8"
            else:
                tier_slug = "tier4"
                badge_label = "Tier 4: Benign"
                score_bar_color = "#10b981"
                
            af_val = float(row.get("gnomad_af", 0.0))
            if af_val > 0:
                af_display = f"{af_val:.5f}"
            else:
                af_display = '<span class="text-muted">Novel (&lt;1e-5)</span>'
                
            var_id = str(row.get("var_id", f"SV_{i+1}"))
            chrom = str(row.get("chrom", ""))
            start = int(row.get("start", 0))
            stop = int(row.get("stop", 0))
            svtype = str(row.get("raw_svtype", "SV")).upper()
            length = int(row.get("length", 0))
            gene_count = int(row.get("gene_count", 0))
            support = row.get("support", 20)
            rec = row.get("clinical_recommendation", "Standard evaluation recommended")
            
            if length >= 1_000_000:
                len_str = f"{length/1_000_000:.2f} Mb"
            elif length >= 1_000:
                len_str = f"{length/1_000:.1f} kb"
            else:
                len_str = f"{length} bp"
                
            table_rows_html += f"""
            <tr class="variant-row {tier_slug}" onclick="toggleRowDetail({i})">
                <td class="col-rank">#{i+1}</td>
                <td class="col-id">
                    <div class="id-primary">{var_id}</div>
                    <div class="id-sub locus-font">chr{chrom}:{start:,}-{stop:,}</div>
                </td>
                <td class="col-type">
                    <span class="type-badge type-{svtype.lower()}">{svtype}</span>
                </td>
                <td class="col-size locus-font">{len_str}</td>
                <td class="col-genes">
                    <span class="gene-count-tag">{gene_count} gene{'s' if gene_count != 1 else ''}</span>
                </td>
                <td class="col-af locus-font">{af_display}</td>
                <td class="col-score">
                    <div class="score-container">
                        <span class="score-num locus-font">{score:.4f}</span>
                        <div class="score-track">
                            <div class="score-fill" style="width: {score_pct}%; background-color: {score_bar_color};"></div>
                        </div>
                    </div>
                </td>
                <td class="col-tier">
                    <span class="tier-pill {tier_slug}">{badge_label}</span>
                </td>
                <td class="col-action">
                    <div class="action-text">{rec}</div>
                </td>
            </tr>
            <tr id="detail-row-{i}" class="detail-row" style="display: none;">
                <td colspan="9">
                    <div class="detail-panel">
                        <div class="detail-grid">
                            <div class="detail-col">
                                <span class="detail-label">Exact Breakpoints (GRCh38)</span>
                                <span class="detail-value locus-font">chr{chrom}:{start} - {stop} (Span: {length:,} bp)</span>
                            </div>
                            <div class="detail-col">
                                <span class="detail-label">Long-Read Support</span>
                                <span class="detail-value">{support} spanning reads</span>
                            </div>
                            <div class="detail-col">
                                <span class="detail-label">gnomAD PopMax AF</span>
                                <span class="detail-value locus-font">{float(row.get('gnomad_popmax_af', 0.0)):.6f}</span>
                            </div>
                            <div class="detail-col">
                                <span class="detail-label">Loss-of-Function Overlap</span>
                                <span class="detail-value">{'Yes (Disrupts Coding Exon)' if row.get('gnomad_lof', 0) == 1 else 'None / Intronic'}</span>
                            </div>
                        </div>
                    </div>
                </td>
            </tr>
            """
            
        # Build SHAP Waterfall Gallery
        shap_gallery_html = ""
        for i, img_b64 in enumerate(self.top_shap_images):
            c_row = self.df.iloc[i] if i < len(self.df) else None
            c_id = c_row.get("var_id", f"Candidate #{i+1}") if c_row is not None else f"Candidate #{i+1}"
            c_score = float(c_row.get("pathogenicity_score", 0.0)) if c_row is not None else 0.0
            c_tier = c_row.get("priority_tier", "").split(" (")[0] if c_row is not None else ""
            c_rec = c_row.get("clinical_recommendation", "") if c_row is not None else ""
            
            shap_gallery_html += f"""
            <div class="shap-card">
                <div class="shap-card-header">
                    <div class="shap-card-title-group">
                        <span class="shap-card-badge">Prioritized Candidate #{i+1}</span>
                        <h3 class="shap-card-id">{c_id}</h3>
                    </div>
                    <div class="shap-card-status">
                        <span class="shap-score-val locus-font">{c_score:.4f}</span>
                        <span class="tier-pill tier1">{c_tier}</span>
                    </div>
                </div>
                <div class="shap-canvas-wrapper">
                    <img src="data:image/png;base64,{img_b64}" alt="SHAP Waterfall for {c_id}" class="shap-image" />
                </div>
                <div class="shap-card-footer">
                    <strong>Clinical Summary:</strong> {c_rec}
                </div>
            </div>
            """
            
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Clinical SV Prioritization Report | {self.sample_name}</title>
    <!-- Google Fonts & Custom Embedded Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesque:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        {font_faces_css}
        
        :root {{
            --bg-base: #08121e;
            --bg-surface: #0d1b2a;
            --bg-elevated: #132438;
            --border-subtle: rgba(255, 255, 255, 0.08);
            --border-highlight: rgba(56, 189, 248, 0.28);
            
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            
            --brand-blue: #0066ff;
            --brand-cyan: #38bdf8;
            
            --tier1-color: #f43f5e;
            --tier2-color: #f59e0b;
            --tier3-color: #38bdf8;
            --tier4-color: #10b981;
        }}
        
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        
        body {{
            font-family: 'Hanken Grotesque', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: var(--bg-base);
            color: var(--text-primary);
            min-height: 100vh;
            padding: 40px 24px 120px;
            -webkit-font-smoothing: antialiased;
        }}
        
        /* Font Utility Classes */
        .font-finishlines {{
            font-family: 'Finish Lines', 'Hanken Grotesque', sans-serif;
            letter-spacing: 0.5px;
        }}
        
        .font-daffiys {{
            font-family: 'Daffiys', serif;
            letter-spacing: 0.8px;
        }}
        
        .locus-font {{
            font-family: 'JetBrains Mono', ui-monospace, monospace;
        }}
        
        /* Subtle Ocean Contour SVG Background */
        .ocean-bg {{
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 380px;
            z-index: 0;
            pointer-events: none;
            opacity: 0.65;
        }}
        
        .page-container {{
            max-width: 1380px;
            margin: 0 auto;
            position: relative;
            z-index: 1;
        }}
        
        /* Enterprise Header */
        .app-header {{
            background: linear-gradient(180deg, rgba(13, 27, 42, 0.9) 0%, rgba(8, 18, 30, 0.95) 100%);
            border: 1px solid var(--border-subtle);
            border-radius: 16px;
            padding: 28px 36px;
            margin-bottom: 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
            backdrop-filter: blur(16px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
        }}
        
        .header-brand {{
            display: flex;
            align-items: center;
            gap: 18px;
        }}
        
        .brand-logo-mark {{
            font-family: 'Daffiys', serif;
            font-size: 26px;
            background: linear-gradient(135deg, var(--brand-cyan), var(--brand-blue));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: bold;
            padding-right: 12px;
            border-right: 1px solid var(--border-subtle);
        }}
        
        .header-title-group h1 {{
            font-family: 'Finish Lines', 'Hanken Grotesque', sans-serif;
            font-size: 26px;
            font-weight: 700;
            color: #ffffff;
            letter-spacing: -0.2px;
        }}
        
        .header-subtitle {{
            font-size: 13.5px;
            color: var(--text-secondary);
            margin-top: 4px;
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        
        .meta-tag {{
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-subtle);
            padding: 2px 8px;
            border-radius: 6px;
            font-size: 12px;
            color: var(--brand-cyan);
        }}
        
        .btn-print {{
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid var(--border-subtle);
            color: var(--text-primary);
            font-family: inherit;
            font-size: 13.5px;
            font-weight: 600;
            padding: 9px 18px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s ease;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }}
        
        .btn-print:hover {{
            background: rgba(255, 255, 255, 0.12);
            border-color: var(--brand-cyan);
        }}
        
        /* Executive Metrics Cards */
        .metrics-row {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }}
        
        .metric-tile {{
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: 14px;
            padding: 20px 24px;
            position: relative;
            overflow: hidden;
            transition: transform 0.2s ease, border-color 0.2s ease;
        }}
        
        .metric-tile:hover {{
            border-color: var(--border-highlight);
            transform: translateY(-2px);
        }}
        
        .metric-tile .tile-title {{
            font-family: 'Daffiys', serif;
            font-size: 13px;
            font-weight: 600;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-bottom: 6px;
        }}
        
        .metric-tile .tile-val {{
            font-family: 'Finish Lines', 'Hanken Grotesque', sans-serif;
            font-size: 36px;
            font-weight: 700;
            color: #ffffff;
            line-height: 1.1;
        }}
        
        .metric-tile .tile-desc {{
            font-size: 12px;
            color: var(--text-muted);
            margin-top: 6px;
        }}
        
        .accent-tier1 {{ border-top: 3px solid var(--tier1-color); }}
        .accent-tier2 {{ border-top: 3px solid var(--tier2-color); }}
        .accent-tier3 {{ border-top: 3px solid var(--tier3-color); }}
        .accent-tier4 {{ border-top: 3px solid var(--tier4-color); }}
        
        /* Main Section Container */
        .content-card {{
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: 16px;
            padding: 28px;
            margin-bottom: 24px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        }}
        
        .section-headline {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 16px;
            margin-bottom: 20px;
        }}
        
        .section-headline h2 {{
            font-family: 'Finish Lines', 'Hanken Grotesque', sans-serif;
            font-size: 20px;
            font-weight: 700;
            letter-spacing: 0.3px;
            color: #ffffff;
        }}
        
        /* Table Filters & Toolbar */
        .table-toolbar {{
            display: flex;
            gap: 12px;
            align-items: center;
            flex-wrap: wrap;
        }}
        
        .filter-pill {{
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid var(--border-subtle);
            color: var(--text-secondary);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 12.5px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.15s ease;
        }}
        
        .filter-pill:hover, .filter-pill.active {{
            background: rgba(56, 189, 248, 0.15);
            border-color: var(--brand-cyan);
            color: #ffffff;
        }}
        
        /* High-End Clean Table */
        .table-wrapper {{
            overflow-x: auto;
            border: 1px solid var(--border-subtle);
            border-radius: 10px;
        }}
        
        table.clinical-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13.5px;
            text-align: left;
        }}
        
        table.clinical-table th {{
            background: var(--bg-elevated);
            color: var(--text-secondary);
            font-weight: 600;
            font-size: 11.5px;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            padding: 14px 16px;
            border-bottom: 1px solid var(--border-subtle);
        }}
        
        table.clinical-table td {{
            padding: 14px 16px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.04);
            vertical-align: middle;
        }}
        
        tr.variant-row {{
            cursor: pointer;
            transition: background-color 0.15s ease;
        }}
        
        tr.variant-row:hover {{
            background-color: rgba(56, 189, 248, 0.04);
        }}
        
        .col-rank {{
            color: var(--text-muted);
            font-weight: 600;
            width: 40px;
        }}
        
        .col-id .id-primary {{
            font-weight: 600;
            color: #ffffff;
        }}
        
        .col-id .id-sub {{
            font-size: 12px;
            color: var(--brand-cyan);
            margin-top: 2px;
        }}
        
        .type-badge {{
            display: inline-block;
            padding: 2px 7px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 700;
            font-family: 'JetBrains Mono', monospace;
            text-transform: uppercase;
        }}
        .type-del {{ background: rgba(244, 63, 94, 0.15); color: #fb7185; }}
        .type-dup {{ background: rgba(56, 189, 248, 0.15); color: #38bdf8; }}
        .type-inv {{ background: rgba(245, 158, 11, 0.15); color: #fbbf24; }}
        .type-ins {{ background: rgba(168, 85, 247, 0.15); color: #c084fc; }}
        
        .gene-count-tag {{
            background: rgba(255, 255, 255, 0.05);
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 12px;
            color: var(--text-secondary);
        }}
        
        .score-container {{
            display: flex;
            flex-direction: column;
            gap: 4px;
            min-width: 90px;
        }}
        
        .score-num {{
            font-size: 13px;
            font-weight: 600;
            color: #ffffff;
        }}
        
        .score-track {{
            width: 100%;
            height: 4px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 2px;
            overflow: hidden;
        }}
        
        .score-fill {{
            height: 100%;
            border-radius: 2px;
        }}
        
        .tier-pill {{
            display: inline-block;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 11.5px;
            font-weight: 700;
            white-space: nowrap;
        }}
        .tier-pill.tier1 {{ background: rgba(244, 63, 94, 0.15); color: #fda4af; border: 1px solid rgba(244, 63, 94, 0.35); }}
        .tier-pill.tier2 {{ background: rgba(245, 158, 11, 0.15); color: #fde68a; border: 1px solid rgba(245, 158, 11, 0.35); }}
        .tier-pill.tier3 {{ background: rgba(56, 189, 248, 0.15); color: #bae6fd; border: 1px solid rgba(56, 189, 248, 0.35); }}
        .tier-pill.tier4 {{ background: rgba(16, 185, 129, 0.15); color: #a7f3d0; border: 1px solid rgba(16, 185, 129, 0.35); }}
        
        .action-text {{
            font-size: 12.5px;
            color: var(--text-secondary);
            line-height: 1.4;
        }}
        
        /* Expandable Details Drawer */
        tr.detail-row td {{
            background: #091524;
            padding: 16px 24px;
            border-bottom: 1px solid var(--border-subtle);
        }}
        
        .detail-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
        }}
        
        .detail-col .detail-label {{
            font-family: 'Daffiys', serif;
            font-size: 11.5px;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            color: var(--text-muted);
            display: block;
            margin-bottom: 4px;
        }}
        
        .detail-col .detail-value {{
            font-size: 13px;
            color: #ffffff;
            font-weight: 500;
        }}
        
        /* TreeSHAP Gallery */
        .shap-gallery-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(580px, 1fr));
            gap: 20px;
        }}
        
        .shap-card {{
            background: var(--bg-elevated);
            border: 1px solid var(--border-subtle);
            border-radius: 14px;
            padding: 22px;
            transition: border-color 0.2s ease;
        }}
        
        .shap-card:hover {{
            border-color: var(--border-highlight);
        }}
        
        .shap-card-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 16px;
        }}
        
        .shap-card-badge {{
            font-family: 'Daffiys', serif;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            color: var(--brand-cyan);
            display: block;
            margin-bottom: 4px;
        }}
        
        .shap-card-id {{
            font-size: 16px;
            font-weight: 700;
            color: #ffffff;
        }}
        
        .shap-card-status {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .shap-score-val {{
            font-size: 13px;
            color: var(--text-secondary);
        }}
        
        .shap-canvas-wrapper {{
            background: #ffffff;
            border-radius: 8px;
            padding: 12px;
            margin-bottom: 14px;
        }}
        
        .shap-image {{
            width: 100%;
            height: auto;
            display: block;
            border-radius: 4px;
        }}
        
        .shap-card-footer {{
            font-size: 12.5px;
            color: var(--text-secondary);
            line-height: 1.4;
        }}
        
        footer {{
            text-align: center;
            color: var(--text-muted);
            font-size: 12.5px;
            margin-top: 48px;
        }}
        
        @media (max-width: 768px) {{
            .shap-gallery-grid {{ grid-template-columns: 1fr; }}
            .app-header {{ padding: 20px; }}
        }}
    </style>
</head>
<body>
    <!-- Subtle Ocean Contours SVG Background -->
    <svg class="ocean-bg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 380" preserveAspectRatio="none">
        <path fill="#040e1a" fill-opacity="0.6" d="M0,200 C320,150 440,240 720,190 C1000,140 1140,230 1440,180 L1440,380 L0,380 Z"></path>
        <path fill="#061626" fill-opacity="0.75" d="M0,240 C360,290 540,190 840,240 C1140,290 1280,210 1440,240 L1440,380 L0,380 Z"></path>
        <path fill="#082038" fill-opacity="0.9" d="M0,290 C300,250 600,320 900,280 C1200,240 1320,300 1440,290 L1440,380 L0,380 Z"></path>
    </svg>

    <div class="page-container">
        <!-- Header -->
        <header class="app-header">
            <div class="header-brand">
                <div class="brand-logo-mark">DNA // AI</div>
                <div class="header-title-group">
                    <h1>Structural Variant Clinical Prioritization</h1>
                    <div class="header-subtitle">
                        <span>Sample: <strong>{self.sample_name}</strong></span>
                        <span class="meta-tag">PacBio / ONT WGS</span>
                        <span class="meta-tag">GRCh38</span>
                        <span class="meta-tag">TreeSHAP Engine v1.0</span>
                    </div>
                </div>
            </div>
            <div>
                <button onclick="window.print()" class="btn-print">
                    <svg width="15" height="15" fill="currentColor" viewBox="0 0 16 16"><path d="M2.5 8a.5.5 0 1 0 0-1 .5.5 0 0 0 0 1z"/><path d="M5 1a2 2 0 0 0-2 2v2H2a2 2 0 0 0-2 2v3a2 2 0 0 0 2 2h1v1a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2v-1h1a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-1V3a2 2 0 0 0-2-2H5zM4 3a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v2H4V3zm1 5a2 2 0 0 0-2 2v1H2a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1h-1v-1a2 2 0 0 0-2-2H5zm7 2v3a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1v-3a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1z"/></svg>
                    Print Clinical PDF
                </button>
            </div>
        </header>

        <!-- Metric Tiles -->
        <div class="metrics-row">
            <div class="metric-tile">
                <div class="tile-title">Total Evaluated</div>
                <div class="tile-val">{total_svs:,}</div>
                <div class="tile-desc">High-quality calls &ge; 50 bp</div>
            </div>
            <div class="metric-tile accent-tier1">
                <div class="tile-title" style="color: var(--tier1-color);">Tier 1: Pathogenic</div>
                <div class="tile-val" style="color: var(--tier1-color);">{tier1_count:,}</div>
                <div class="tile-desc">Immediate diagnostic follow-up</div>
            </div>
            <div class="metric-tile accent-tier2">
                <div class="tile-title" style="color: var(--tier2-color);">Tier 2: Moderate</div>
                <div class="tile-val" style="color: var(--tier2-color);">{tier2_count:,}</div>
                <div class="tile-desc">Phenotypic match suggested</div>
            </div>
            <div class="metric-tile accent-tier3">
                <div class="tile-title" style="color: var(--tier3-color);">Tier 3: Low Risk</div>
                <div class="tile-val">{tier3_count:,}</div>
                <div class="tile-desc">Likely tolerated background</div>
            </div>
            <div class="metric-tile accent-tier4">
                <div class="tile-title" style="color: var(--tier4-color);">Tier 4: Benign</div>
                <div class="tile-val">{tier4_count:,}</div>
                <div class="tile-desc">Common in population baseline</div>
            </div>
        </div>

        <!-- Table Section -->
        <div class="content-card">
            <div class="section-headline">
                <div>
                    <h2>Prioritized Structural Variants</h2>
                    <p style="color: var(--text-secondary); font-size: 13.5px; margin-top: 4px;">
                        Click on any variant row to expand breakpoint evidence and population details.
                    </p>
                </div>
                <div class="table-toolbar">
                    <button class="filter-pill active" onclick="filterTier('all', this)">All ({total_svs})</button>
                    <button class="filter-pill" onclick="filterTier('tier1', this)">Tier 1 ({tier1_count})</button>
                    <button class="filter-pill" onclick="filterTier('tier2', this)">Tier 2 ({tier2_count})</button>
                    <button class="filter-pill" onclick="filterTier('tier4', this)">Tier 4 ({tier4_count})</button>
                </div>
            </div>

            <div class="table-wrapper">
                <table class="clinical-table">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Variant & Locus (GRCh38)</th>
                            <th>Type</th>
                            <th>Span</th>
                            <th>Gene Impact</th>
                            <th>gnomAD AF</th>
                            <th>AI Score</th>
                            <th>Clinical Tier</th>
                            <th>Actionable Recommendation</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_rows_html}
                    </tbody>
                </table>
            </div>
        </div>

        <!-- TreeSHAP Section -->
        <div class="content-card">
            <div class="section-headline">
                <div>
                    <h2>Explainable AI: Feature Attribution (Top Candidates)</h2>
                    <p style="color: var(--text-secondary); font-size: 13.5px; margin-top: 4px;">
                        Local TreeSHAP waterfall decompositions showing exact positive (red) and negative (blue) log-odds contributions for each biological feature.
                    </p>
                </div>
            </div>

            <div class="shap-gallery-grid">
                {shap_gallery_html}
            </div>
        </div>

        <footer>
            AI Structural Variant Prioritizer &copy; 2026. Built with explainable machine learning for long-read genome diagnostics.
        </footer>
    </div>

    <script>
        function toggleRowDetail(index) {{
            const row = document.getElementById('detail-row-' + index);
            if (row) {{
                row.style.display = (row.style.display === 'none' || row.style.display === '') ? 'table-row' : 'none';
            }}
        }}

        function filterTier(tierClass, element) {{
            // Update active pill
            document.querySelectorAll('.filter-pill').forEach(btn => btn.classList.remove('active'));
            if (element) element.classList.add('active');

            const rows = document.querySelectorAll('.variant-row');
            const details = document.querySelectorAll('.detail-row');
            
            // Close any open details
            details.forEach(d => d.style.display = 'none');

            rows.forEach(r => {{
                if (tierClass === 'all' || r.classList.contains(tierClass)) {{
                    r.style.display = 'table-row';
                }} else {{
                    r.style.display = 'none';
                }}
            }});
        }}
    </script>
</body>
</html>
"""
        with open(out_html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"Saved interactive HTML report to: {out_html_path}")
