"""Read a public primary source into a new local research folder; preserve exact bytes."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
import urllib.request

out = Path(__file__).resolve().parent
assert out.parent == Path(r"C:\IALD\Central de Patentes\Chatgpt")
url = "https://ems.press/content/serial-article-files/41744"
target = out / "Araki_1973_Relative_Hamiltonian.pdf"
assert not target.exists()
request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(request, timeout=45) as response:
    data = response.read()
    final_url = response.url
assert data.startswith(b"%PDF-") and len(data) > 10000


def write_new(path, raw):
    assert path.parent == out and not path.exists()
    temp = path.with_name(path.name + ".tmp")
    with temp.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert temp.read_bytes() == raw
    os.rename(temp, path)
    assert path.read_bytes() == raw


write_new(target, data)
record = {"source_url": url, "resolved_url": final_url,
          "downloaded_utc": datetime.now(timezone.utc).isoformat(),
          "path": target.as_posix(), "bytes": len(data),
          "sha256": hashlib.sha256(data).hexdigest(),
          "operation": "read_only_public_source_copy",
          "render_libraries": {name: importlib.util.find_spec(name) is not None
                               for name in ["pypdfium2", "pdfplumber", "pypdf", "PIL"]}}
write_new(out / "PRIMARY_SOURCE_RECEIPT.json",
          (json.dumps(record, indent=2) + "\n").encode("utf-8"))
print(json.dumps(record))
