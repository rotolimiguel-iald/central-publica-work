from __future__ import annotations

import hashlib
import json
import time
import urllib.request
from pathlib import Path

from bs4 import BeautifulSoup
from pypdf import PdfReader

OUT = Path(__file__).resolve().parent / "fontes_primarias"
OUT.mkdir(exist_ok=True)

SOURCES = [
    {"key": "hamuy1991", "objects": ["1980N", "1981D"], "title": "The Optical Light Curves of SN 1980N and SN 1981D in NGC 1316", "url": "https://adsabs.harvard.edu/pdf/1991AJ....102..208H", "file": "hamuy1991.pdf", "kind": "pdf"},
    {"key": "elias1981", "objects": ["1980N", "1981D"], "title": "Infrared Light Curves of Type I Supernovae", "url": "https://articles.adsabs.harvard.edu/pdf/1981ApJ...251L..13E", "file": "elias1981.pdf", "kind": "pdf"},
    {"key": "wells1994", "objects": ["1989B"], "title": "The Type Ia Supernova 1989B in NGC 3627 (M66)", "url": "https://adsabs.harvard.edu/pdf/1994AJ....108.2233W", "file": "wells1994.pdf", "kind": "pdf"},
    {"key": "saha1999", "objects": ["1989B"], "title": "Cepheid Calibration of the Peak Brightness of SNe Ia IX SN 1989B", "url": "https://arxiv.org/pdf/astro-ph/9904389", "file": "saha1999.pdf", "kind": "pdf"},
    {"key": "hamuy1996", "objects": ["1992A"], "title": "The Morphology of Type Ia Supernova Light Curves", "url": "https://adsabs.harvard.edu/pdf/1996AJ....112.2438H", "file": "hamuy1996.pdf", "kind": "pdf"},
    {"key": "richmond1995", "objects": ["1994D"], "title": "UBVRI Photometry of the Type Ia SN 1994D in NGC 4526", "url": "https://articles.adsabs.harvard.edu/pdf/1995AJ....109.2121R", "file": "richmond1995.pdf", "kind": "pdf"},
    {"key": "patat1996", "objects": ["1994D"], "title": "The Type Ia Supernova 1994D in NGC 4526 the Early Phases", "url": "https://articles.adsabs.harvard.edu/pdf/1996MNRAS.278..111P", "file": "patat1996.pdf", "kind": "pdf"},
    {"key": "jha1999", "objects": ["1998bu"], "title": "The Type Ia Supernova 1998bu in M96 and the Hubble Constant", "url": "https://arxiv.org/pdf/astro-ph/9906220", "file": "jha1999.pdf", "kind": "pdf"},
    {"key": "suntzeff1999", "objects": ["1998bu", "1992A"], "title": "Optical Light Curve of SN 1998bu in M96 and the Supernova Calibration of H0", "url": "https://arxiv.org/pdf/astro-ph/9811205", "file": "suntzeff1999.pdf", "kind": "pdf"},
    {"key": "stritzinger2010", "objects": ["2006dd", "1980N", "1981D"], "title": "The Distance to NGC 1316 from Observations of Four Type Ia Supernovae", "url": "https://arxiv.org/pdf/1009.4390", "file": "stritzinger2010.pdf", "kind": "pdf"},
    {"key": "gall2018", "objects": ["2011iv", "2007on"], "title": "Two transitional Type Ia supernovae in NGC 1404", "url": "https://www.aanda.org/articles/aa/full_html/2018/03/aa30886-17/aa30886-17.html", "file": "gall2018.html", "kind": "html"},
    {"key": "dhawan2022", "objects": ["2021rhu"], "title": "TRGB distances to SN 2021rhu and calibrators", "url": "https://arxiv.org/html/2203.04241", "file": "dhawan2022.html", "kind": "html"},
    {"key": "harvey2023", "objects": ["2021rhu"], "title": "SN 2021rhu photometry and analysis", "url": "https://arxiv.org/html/2304.10129v2", "file": "harvey2023.html", "kind": "html"},
    {"key": "shappee2016", "objects": ["ASASSN-14lp"], "title": "ASASSN-14lp photometry and light-curve analysis", "url": "https://arxiv.org/html/1507.04257v2", "file": "shappee2016.html", "kind": "html"},
    {"key": "li2025", "objects": ["ASASSN-14lp", "2021J", "2020nvb"], "title": "Independent TRGB routes for SN calibrator hosts", "url": "https://arxiv.org/html/2504.08921v1", "file": "li2025.html", "kind": "html"},
    {"key": "gallego2022", "objects": ["2021J"], "title": "SN 2021J in NGC 4414", "url": "https://arxiv.org/html/2204.10668v3", "file": "gallego2022.html", "kind": "html"},
    {"key": "newman2025", "objects": ["2020nvb", "2011iv", "2007on"], "title": "TRGB and SN analysis including SN 2020nvb", "url": "https://arxiv.org/html/2508.20023v2", "file": "newman2025.html", "kind": "html"},
    {"key": "aavso709", "objects": ["2020nvb"], "title": "AAVSO Alert Notice 709", "url": "https://www.aavso.org/index.php/aavso-alert-notice-709", "file": "aavso709.html", "kind": "html"},
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


manifest = {"status": "SOURCE_ARCHIVE_PARTIAL_UNTIL_ALL_VERIFIED", "opening_allowed": False, "sources": []}
for item in SOURCES:
    record = dict(item)
    target = OUT / item["file"]
    try:
        request = urllib.request.Request(item["url"], headers={"User-Agent": "Mozilla/5.0 (compatible; IALD-source-archive/1.0)"})
        with urllib.request.urlopen(request, timeout=60) as response:
            data = response.read()
            record["final_url"] = response.geturl()
            record["http_content_type"] = response.headers.get("Content-Type")
        if len(data) < 1000:
            raise ValueError(f"Response too small: {len(data)} bytes")
        if item["kind"] == "pdf" and not data.startswith(b"%PDF"):
            raise ValueError("Response is not a PDF")
        target.write_bytes(data)
        record.update({"download_status": "OK", "bytes": len(data), "sha256": sha(target), "local_path": str(target)})
        text_path = target.with_suffix(target.suffix + ".txt")
        if item["kind"] == "pdf":
            reader = PdfReader(target)
            text = "\n\n".join(f"=== PAGE {i} ===\n{page.extract_text() or ''}" for i, page in enumerate(reader.pages, 1))
            record["pdf_pages"] = len(reader.pages)
        else:
            soup = BeautifulSoup(data, "html.parser")
            for node in soup(["script", "style", "noscript"]):
                node.decompose()
            text = soup.get_text("\n", strip=True)
        text_path.write_text(text, encoding="utf-8")
        record.update({"text_path": str(text_path), "text_sha256": sha(text_path), "text_characters": len(text)})
    except Exception as exc:
        record.update({"download_status": "ERROR", "error": f"{type(exc).__name__}: {exc}"})
    manifest["sources"].append(record)
    time.sleep(0.4)

manifest["downloaded_ok"] = sum(s["download_status"] == "OK" for s in manifest["sources"])
manifest["download_errors"] = sum(s["download_status"] != "OK" for s in manifest["sources"])
manifest["status"] = "SOURCE_ARCHIVE_COMPLETE" if manifest["download_errors"] == 0 else "SOURCE_ARCHIVE_INCOMPLETE_SEE_ERRORS"
path = OUT / "MANIFEST_DOWNLOAD.json"
path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": manifest["status"], "ok": manifest["downloaded_ok"], "errors": manifest["download_errors"], "manifest": str(path), "manifest_sha256": sha(path)}, ensure_ascii=False, indent=2))
