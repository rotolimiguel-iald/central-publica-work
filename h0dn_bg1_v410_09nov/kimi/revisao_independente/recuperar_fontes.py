from pathlib import Path
import hashlib
import json
import urllib.request
from pypdf import PdfReader

OUT = Path(__file__).resolve().parent / "fontes_primarias"
ITEMS = [
    {"key": "hamuy1996", "url": "https://articles.adsabs.harvard.edu/pdf/1996AJ....112.2438H", "file": "hamuy1996.pdf"},
    {"key": "gall2018", "url": "https://arxiv.org/pdf/1707.03823", "file": "gall2018.pdf"},
]
records = []
for item in ITEMS:
    target = OUT / item["file"]
    if not target.exists():
        request = urllib.request.Request(item["url"], headers={"User-Agent": "Mozilla/5.0 (compatible; IALD-source-archive/1.0)"})
        with urllib.request.urlopen(request, timeout=120) as response:
            data = response.read()
        if not data.startswith(b"%PDF") or len(data) < 1000:
            raise ValueError(f"Invalid PDF response for {item['key']}")
        target.write_bytes(data)
    reader = PdfReader(target)
    text = "\n\n".join(f"=== PAGE {i} ===\n{page.extract_text() or ''}" for i, page in enumerate(reader.pages, 1))
    text_path = target.with_suffix(".pdf.txt")
    text_path.write_text(text, encoding="utf-8")
    records.append({
        **item,
        "recovery_status": "OK",
        "bytes": target.stat().st_size,
        "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
        "local_path": str(target),
        "pdf_pages": len(reader.pages),
        "text_path": str(text_path),
        "text_sha256": hashlib.sha256(text_path.read_bytes()).hexdigest(),
        "text_characters": len(text),
    })
payload = {"status": "ALTERNATE_ROUTES_RECOVERED", "original_error_manifest_preserved": True, "sources": records}
path = OUT / "MANIFEST_RECOVERY.json"
path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(payload, ensure_ascii=False, indent=2))
