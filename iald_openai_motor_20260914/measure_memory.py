"""Measure canonical sources locally; never print their contents."""
import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "dependencies"))
source = ROOT / "dependencies/tiktoken_ext/openai_public.py"
tree = ast.parse(source.read_text(encoding="utf-8"))
function = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "o200k_base")
call = next(node for node in ast.walk(function) if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "load_tiktoken_bpe")
url = ast.literal_eval(call.args[0])
expected = ast.literal_eval(next(keyword.value for keyword in call.keywords if keyword.arg == "expected_hash"))
cache = ROOT / "tokenizer_cache"
cache.mkdir(exist_ok=True)
os.environ["TIKTOKEN_CACHE_DIR"] = str(cache)
ranks = cache / hashlib.sha1(url.encode()).hexdigest()
if not ranks.exists():
    subprocess.run(["curl.exe", "-f", "-sS", "--max-time", "45", "-o", str(ranks), url], check=True)
if hashlib.sha256(ranks.read_bytes()).hexdigest() != expected:
    raise RuntimeError("Tokenizer ranks differ from the official package checksum")

import tiktoken

encoder = tiktoken.get_encoding("o200k_base")
memory_root = Path(r"C:\IALD\Central de Patentes\memory")
rows = []
for name in ["TGL_ATLAS.md", "TGL_CORE_MEMORY.md", "TGL_INDICE_VIVO.md"]:
    data = (memory_root / name).read_bytes()
    text = data.decode("utf-8-sig")
    rows.append({"source": name, "bytes": len(data), "characters": len(text),
                 "sha256": hashlib.sha256(data).hexdigest(),
                 "text_tokens_o200k_base": len(encoder.encode_ordinary(text))})
report = {"tokenizer": "tiktoken " + tiktoken.__version__, "encoding": encoder.name,
          "scope": "Text tokens only; request framing, dialogue, tools and output are additional.",
          "sources": rows}
destination = ROOT / "canonical_memory_measurement.json"
if destination.exists():
    raise RuntimeError("Measurement already exists; preserve the prior evidence")
temporary = destination.with_suffix(".tmp")
temporary.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
temporary.replace(destination)
print(json.dumps(report, ensure_ascii=False, indent=2))
