from pathlib import Path
from pypdf import PdfReader

SOURCE = Path(r"C:\IALD\Central de Patentes\work\h0dn_bg1_v410_09nov\kimi\H0DN_paper_v1.pdf")
OUT = Path(r"C:\IALD\Central de Patentes\work\h0dn_bg1_v410_09nov\kimi\GRUPOS_NO_PDF.txt")
reader = PdfReader(SOURCE)
lines = []
for i, page in enumerate(reader.pages, 1):
    text = page.extract_text() or ""
    if "Fornax" in text or "Virgo" in text or "31.455" in text:
        lines.append(f"===== PAGE {i} =====\n{text}\n")
OUT.write_text("\n".join(lines), encoding="utf-8")
print(f"pages={len(reader.pages)} selected={len(lines)} output={OUT}")
