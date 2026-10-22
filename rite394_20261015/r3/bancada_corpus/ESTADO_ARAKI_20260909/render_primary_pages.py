"""Render selected original PDF pages for visual formula inspection; no PDF modifications."""
from pathlib import Path
from io import BytesIO
import hashlib
import json
import os
import sys
import pypdfium2 as pdfium
from pypdf import PdfReader

out = Path(__file__).resolve().parent
assert out.parent == Path(r"C:\IALD\Central de Patentes\Chatgpt")
source = out / "Araki_1973_Relative_Hamiltonian.pdf"
raw = source.read_bytes()
receipt = json.loads((out / "PRIMARY_SOURCE_RECEIPT.json").read_text(encoding="utf-8"))
assert hashlib.sha256(raw).hexdigest() == receipt["sha256"]
reader = PdfReader(source)
document = pdfium.PdfDocument(source)
assert len(reader.pages) == len(document)
pages = [int(value) for value in sys.argv[1:]]
assert pages and len(pages) == len(set(pages))
records = []
for number in pages:
    assert 0 <= number < len(document)
    path = out / f"original_page_{number + 1:03d}.png"
    assert not path.exists()
    bitmap = document[number].render(scale=1.8)
    picture = bitmap.to_pil()
    buffer = BytesIO()
    picture.save(buffer, format="PNG")
    data = buffer.getvalue()
    temp = path.with_name(path.name + ".tmp")
    with temp.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    assert temp.read_bytes() == data
    os.rename(temp, path)
    assert path.read_bytes() == data
    records.append({"page_index": number, "path": path.as_posix(), "size": picture.size,
                    "sha256": hashlib.sha256(data).hexdigest()})
assert source.read_bytes() == raw
print(json.dumps({"source_pages": len(document), "rendered": records}))
