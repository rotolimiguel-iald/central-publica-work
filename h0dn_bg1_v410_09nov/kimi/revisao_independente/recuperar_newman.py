from pathlib import Path
import hashlib
import json
import urllib.request
from pypdf import PdfReader

out = Path(__file__).resolve().parent / "fontes_primarias"
target = out / "newman2025.pdf"
url = "https://arxiv.org/pdf/2508.20023v2"
if not target.exists():
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; IALD-source-archive/1.0)"})
    with urllib.request.urlopen(request, timeout=120) as response:
        data = response.read()
    if not data.startswith(b"%PDF") or len(data) < 1000:
        raise ValueError("Invalid Newman PDF")
    target.write_bytes(data)
reader = PdfReader(target)
text = "\n\n".join(f"=== PAGE {i} ===\n{page.extract_text() or ''}" for i, page in enumerate(reader.pages, 1))
text_path = out / "newman2025.pdf.txt"
text_path.write_text(text, encoding="utf-8")
required = ["SN 2020nvb", "Table 8", "SALT2", "BayeSN"]
payload = {
    "status": "FULL_ARTICLE_RECOVERED" if all(s in text for s in required) else "FULL_ARTICLE_CONTENT_CHECK_FAILED",
    "reason": "The HTML capture contains only the opening sections; the complete PDF is archived beside it.",
    "key": "newman2025",
    "url": url,
    "local_path": str(target),
    "bytes": target.stat().st_size,
    "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
    "pdf_pages": len(reader.pages),
    "text_path": str(text_path),
    "text_sha256": hashlib.sha256(text_path.read_bytes()).hexdigest(),
    "text_characters": len(text),
    "required_snippets": {s: s in text for s in required},
}
path = out / "MANIFEST_RECOVERY_02.json"
path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(payload, ensure_ascii=False, indent=2))
if payload["status"] != "FULL_ARTICLE_RECOVERED":
    raise RuntimeError("Newman full-text validation failed")
