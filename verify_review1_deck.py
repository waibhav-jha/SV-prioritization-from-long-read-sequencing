import zipfile
import xml.etree.ElementTree as ET
import re
import os

pptx_path = "Review_1_Presentation.pptx"

def inspect_pptx(path):
    print("=== INSPECTING PPTX ===")
    with zipfile.ZipFile(path, 'r') as z:
        # List slide files
        slides = sorted([f for f in z.namelist() if f.startswith('ppt/slides/slide') and f.endswith('.xml')],
                        key=lambda x: int(re.search(r'\d+', x).group()))
        print(f"Total slides count: {len(slides)}")
        
        notebook_mentions = []
        
        for idx, s in enumerate(slides, 1):
            content = z.read(s).decode('utf-8')
            root = ET.fromstring(content)
            # Extract all text
            texts = [node.text for node in root.iter() if node.text]
            full_slide_text = " ".join(texts)
            
            # Check for forbidden notebook mentions
            if re.search(r'notebook\s*\d+', full_slide_text, re.IGNORECASE):
                notebook_mentions.append((idx, full_slide_text))
                
            # First slide check
            if idx == 1:
                print(f"\n--- SLIDE 1 (TITLE) ---")
                print("Text snippet:", full_slide_text[:300])
                has_group15 = "Group 15" in full_slide_text or "GROUP 15" in full_slide_text
                print(f"Contains 'Group 15': {has_group15}")
                assert has_group15, "Slide 1 MUST contain Group 15!"
                
            print(f"Slide {idx:02d}: {len(texts)} text elements extracted.")
            
        print("\n--- NOTEBOOK MENTION CHECK ---")
        if notebook_mentions:
            print(f"FAILED: Found notebook mentions in {len(notebook_mentions)} slides:")
            for s_idx, txt in notebook_mentions:
                print(f"Slide {s_idx}: {txt}")
        else:
            print("PASSED: Zero forbidden notebook mentions found across all slides.")
            
        assert len(slides) == 18, f"Expected exactly 18 slides, got {len(slides)}"
        print("\nALL PPTX CHECKS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    inspect_pptx(pptx_path)
