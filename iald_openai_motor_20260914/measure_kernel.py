"""Inspect literal embedded Lean sources without importing or executing um.py."""
import ast
import hashlib
import json
import os
from pathlib import Path
import sys

root = Path(__file__).resolve().parent
sys.path.insert(0, str(root / "dependencies"))
os.environ["TIKTOKEN_CACHE_DIR"] = str(root / "tokenizer_cache")
import tiktoken

source = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py")
raw = source.read_bytes()
tree = ast.parse(raw)
assignment = next(node for node in tree.body if isinstance(node, ast.Assign)
                  and any(isinstance(target, ast.Name) and target.id == "_EMBEDDED_KERNEL_FILES"
                          for target in node.targets))
files = ast.literal_eval(assignment.value)
if not isinstance(files, dict) or not files or not all(isinstance(name, str) and isinstance(text, str)
                                                     for name, text in files.items()):
    raise RuntimeError("Unexpected embedded kernel format")
encoder = tiktoken.get_encoding("o200k_base")
records = []
for name, text in files.items():
    payload = text.encode("utf-8")
    disk = source.parent / "tgl_kernel" / name
    records.append({"path": name, "bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest(),
                    "text_tokens": len(encoder.encode_ordinary(text)),
                    "materialized_exists": disk.is_file(),
                    "materialized_bytes_equal": disk.is_file() and disk.read_bytes() == payload})
lean = [record for record in records if record["path"].endswith(".lean")]
report = {"source": str(source), "source_sha256": hashlib.sha256(raw).hexdigest(),
          "method": "ast.literal_eval; um.py not imported or executed",
          "files": len(records), "lean_files": len(lean),
          "lean_source_tokens_o200k_base": sum(record["text_tokens"] for record in lean),
          "lean_source_bytes": sum(record["bytes"] for record in lean),
          "non_lean_paths": [record["path"] for record in records if not record["path"].endswith(".lean")],
          "materialized_exact_matches": sum(record["materialized_bytes_equal"] for record in records),
          "records": records}
destination = root / "embedded_kernel_measurement.json"
if destination.exists():
    raise RuntimeError("Measurement already exists; preserve the prior evidence")
temporary = destination.with_suffix(".tmp")
temporary.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
temporary.replace(destination)
print(json.dumps({key: value for key, value in report.items() if key != "records"}, ensure_ascii=False, indent=2))
