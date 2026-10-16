"""
src/vcf_parser.py
=================
Long-Read Sequencing Structural Variant VCF Parser.
Supports outputs from Sniffles2, cuteSV, PBSV, and Nanomonsv.
"""

import gzip
import re
import pandas as pd
import numpy as np

class LongReadVCFParser:
    def __init__(self, vcf_path, min_support=3, min_gq=10):
        self.vcf_path = vcf_path
        self.min_support = min_support
        self.min_gq = min_gq
        self.raw_header_lines = []
        
    def parse(self):
        """
        Parse the VCF file and return a standardized DataFrame of SV records.
        """
        records = []
        is_gzip = self.vcf_path.endswith(".gz")
        open_fn = gzip.open if is_gzip else open
        mode = "rt"
        
        with open_fn(self.vcf_path, mode, encoding="utf-8", errors="replace") as f:
            for line in f:
                if line.startswith("##"):
                    self.raw_header_lines.append(line)
                    continue
                if line.startswith("#CHROM"):
                    self.raw_header_lines.append(line)
                    continue
                    
                parts = line.strip().split("\t")
                if len(parts) < 8:
                    continue
                    
                chrom = parts[0].replace("chr", "")
                pos = int(parts[1])
                var_id = parts[2]
                ref = parts[3]
                alt = parts[4]
                qual = parts[5]
                filt = parts[6]
                info = parts[7]
                
                # Parse INFO key-values
                info_dict = {}
                for item in info.split(";"):
                    if "=" in item:
                        k, v = item.split("=", 1)
                        info_dict[k] = v
                    else:
                        info_dict[item] = True
                        
                # Extract SV type
                svtype = info_dict.get("SVTYPE", None)
                if svtype is None:
                    if alt.startswith("<") and alt.endswith(">"):
                        svtype = alt[1:-1]
                    elif len(ref) > len(alt):
                        svtype = "DEL"
                    elif len(alt) > len(ref):
                        svtype = "DUP" if alt in ref else "INS"
                    else:
                        svtype = "OTHER"
                svtype = str(svtype).upper()
                
                # Extract SV End coordinate
                end = info_dict.get("END", None)
                if end is not None:
                    try:
                        end = int(end)
                    except ValueError:
                        end = pos + max(1, len(ref))
                else:
                    end = pos + max(1, len(ref))
                    
                # Extract SV length
                svlen_raw = info_dict.get("SVLEN", None)
                if svlen_raw is not None:
                    try:
                        svlen = abs(int(str(svlen_raw).split(",")[0]))
                    except ValueError:
                        svlen = abs(end - pos)
                else:
                    svlen = abs(end - pos)
                    
                # Filter length >= 50 bp
                if svlen < 50 and abs(end - pos) < 50:
                    continue
                if svlen < 50:
                    svlen = abs(end - pos)
                    
                # Read support / coverage from INFO or FORMAT if available
                support = info_dict.get("SUPPORT", info_dict.get("RE", info_dict.get("DV", 5)))
                try:
                    support = int(support)
                except ValueError:
                    support = 5
                    
                records.append({
                    "var_id": var_id if var_id != "." else f"{chrom}_{pos}_{svtype}",
                    "chrom": str(chrom),
                    "start": pos,
                    "stop": max(end, pos + 1),
                    "length": max(svlen, abs(end - pos)),
                    "raw_svtype": svtype,
                    "ref": ref[:20],
                    "alt": alt[:20],
                    "qual": qual,
                    "filter": filt,
                    "support": support,
                    "raw_info": info
                })
                
        df = pd.DataFrame(records)
        return df
