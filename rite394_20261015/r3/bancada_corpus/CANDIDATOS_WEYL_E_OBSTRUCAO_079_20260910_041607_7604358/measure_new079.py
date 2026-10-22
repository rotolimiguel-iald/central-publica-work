"""Measure source bytes and finalize only new files in this task directory."""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(r"C:\IALD\Central de Patentes\Chatgpt")
HERE = Path(__file__).resolve().parent
SOURCES = [
    ROOT / "LIBERDADE_DE_LEVANTAMENTO_079_20260910/CORRECOES_E4_E5_PROJECAO_SIGMA_E_SISTEMA_LOCAL.md",
    ROOT / "RESIDUO_PONTRYAGIN_S0_078_20260910/CERTIFICADO_NAO_EXATIDAO_A6_E_LIMITE_DO_RAMO.md",
    ROOT / "SOBREVIVENTE_PONTRYAGIN_077_20260910/DICIONARIO_CARTAN_DO_RECIBO_077.md",
    ROOT / "PRIMEIROS_TRUNCAMENTOS_BRST_077_20260910_030228_0972771/S0_KILLING_E_PRIMEIRA_TRANSICAO.md",
    ROOT / "PRIMEIROS_TRUNCAMENTOS_BRST_077_20260910_030228_0972771/ADENDO_SINAL_KOSZUL_TATE_077.md",
]

def pin(path):
    data = path.read_bytes()
    return {"path": str(path), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}

def write_new(path, value):
    data = json.dumps(value, ensure_ascii=False, indent=2).encode("utf-8") + b"\n"
    temp = path.with_suffix(path.suffix + ".pending")
    if path.exists() or temp.exists():
        raise FileExistsError(str(path))
    with temp.open("xb") as stream:
        stream.write(data)
    if temp.read_bytes() != data or not data:
        raise RuntimeError("Byte verification failed")
    temp.rename(path)

if HERE.parent != ROOT:
    raise RuntimeError("Output directory outside Chatgpt")
if sys.argv[1] == "begin":
    write_new(HERE / "PINS_INICIAIS_079.json", [pin(p) for p in SOURCES])
    print("Measured", len(SOURCES), "read-only sources")
elif sys.argv[1] == "close":
    initial = json.loads((HERE / "PINS_INICIAIS_079.json").read_text(encoding="utf-8"))
    final = [pin(p) for p in SOURCES]
    if final != initial:
        raise RuntimeError("A source changed during this task")
    pending = HERE / "WEYL_CC_M_E_FALHA_DO_COMPLETAMENTO.md.pending"
    note = HERE / "WEYL_CC_M_E_FALHA_DO_COMPLETAMENTO.md"
    if note.exists():
        raise FileExistsError(str(note))
    data = pending.read_bytes()
    if len(data) < 10000:
        raise RuntimeError("Unexpected note size")
    links = re.findall(r"\]\(<(C:/[^>]+)>\)", data.decode("utf-8"))
    for target in links:
        path = re.sub(r":\d+$", "", target)
        if not Path(path).is_file():
            raise FileNotFoundError(target)
    pending.rename(note)
    manifest = {
        "status": "REAL documentary measurements; DERIVED written mathematics, no CAS/Lean",
        "sources_before": initial,
        "sources_after": final,
        "all_sources_unchanged": True,
        "note": pin(note),
        "measurement_script": pin(Path(__file__)),
        "local_links_checked": len(links),
        "um_py_executed_or_imported": False,
        "original_or_frozen_file_modified": False,
        "mathematical_scope": "The two Weyl CC m candidates and their inherited-scalar span fail equation (9); no exhaustive classification of P or delta(K)",
    }
    write_new(HERE / "MANIFESTO_CANDIDATOS_WEYL_079.json", manifest)
    print(json.dumps({"note": pin(note), "manifest": pin(HERE / "MANIFESTO_CANDIDATOS_WEYL_079.json"), "sources_unchanged": True, "links": len(links)}, ensure_ascii=False))
else:
    raise RuntimeError("Unknown operation")
