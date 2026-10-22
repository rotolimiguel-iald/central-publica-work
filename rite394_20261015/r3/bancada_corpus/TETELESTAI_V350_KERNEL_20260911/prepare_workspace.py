"""Create the isolated v350 workspace without importing or executing um.py."""
import ast
import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")

def sha(data):
    return hashlib.sha256(data).hexdigest()

def create(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != data:
            raise RuntimeError(f"Refusing to overwrite existing work: {path}")
        return
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_bytes(data)
    assert temporary.stat().st_size == len(data)
    os.replace(temporary, path)

raw = (SOURCE / "um.py").read_bytes()
seal = json.loads((SOURCE / "um_absoluto_selo.json").read_bytes())
assert sha(raw) == seal["sha256"]["um.py"], "Source no longer matches the seal"
create(ROOT / "fontes" / "um_v350_original.py", raw)
create(ROOT / "um.py", raw)
tree = ast.parse(raw.decode("utf-8-sig"))
embedded = next(ast.literal_eval(n.value) for n in tree.body
    if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name)
    and t.id == "_EMBEDDED_KERNEL_FILES" for t in n.targets))
for relative, text in embedded.items():
    target = (ROOT / "kernel" / relative).resolve()
    assert target.is_relative_to(ROOT / "kernel")
    create(target, text.encode("utf-8"))
for name in ("um_absoluto_selo.json", "um_absoluto.json", "tgl_kernel_proof_manifest.json",
             "rodada_v350_stdout.txt", "HANDOFF_v350_A_NATUREZA_RESPONDEU.md"):
    create(ROOT / "fontes" / name, (SOURCE / name).read_bytes())
original_kernel = SOURCE / "tgl_kernel"
libraries = [ROOT / "build", original_kernel / ".lake" / "build" / "lib" / "lean"]
libraries += sorted(p / ".lake" / "build" / "lib" / "lean"
                    for p in (original_kernel / ".lake" / "packages").iterdir()
                    if (p / ".lake" / "build" / "lib" / "lean").is_dir())
env = {"lean": r"C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe",
       "lean_path": [str(p) for p in libraries],
       "original_sha256": sha(raw), "original_source": str(SOURCE / "um.py"),
       "embedded_files": len(embedded)}
create(ROOT / "environment.json", json.dumps(env, indent=2).encode())
print(json.dumps({"workspace": str(ROOT), **env}, indent=2))
