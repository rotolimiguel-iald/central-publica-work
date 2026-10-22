from pathlib import Path
from datetime import datetime, timezone
import ast
import hashlib
import json
import os
import re

ROOT = Path(r"C:\IALD\Central de Patentes\Chatgpt").resolve()
OUT = Path(__file__).resolve().parent
CANON = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
NAV = Path(r"C:\IALD\Central de Patentes\memory")
PINS = {}; RAW = {}
def pin(path):
    p = Path(path).resolve(); raw = p.read_bytes(); st = p.stat()
    return {"path": p.as_posix(), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
            "mtime_utc": datetime.fromtimestamp(st.st_mtime, timezone.utc).isoformat()}
def read(path):
    p = Path(path).resolve(); raw = p.read_bytes(); item = pin(p)
    assert item["bytes"] == len(raw) and item["sha256"] == hashlib.sha256(raw).hexdigest()
    if item["path"] in PINS: assert PINS[item["path"]] == item
    else: PINS[item["path"]] = item; RAW[item["path"]] = raw
    return raw
def new(name, raw):
    p = OUT / name
    assert p.resolve().is_relative_to(ROOT) and not p.exists() and raw
    tmp = p.with_name(p.name + ".tmp_" + datetime.now().strftime("%H%M%S_%f"))
    with tmp.open("xb") as f:
        f.write(raw); f.flush(); os.fsync(f.fileno())
    assert tmp.read_bytes() == raw
    tmp.rename(p)
    assert p.read_bytes() == raw
    return pin(p)
read(Path(__file__))
priorpath = ROOT / "REEXAME_SUFICIENCIA_085_20260910/ESTADO_CANONICO_085.json"
prior = json.loads(read(priorpath))
planpath = ROOT / "INTEGRADOR_SIGMA_GIBBS_ASSINADO_20260909_210226_8753655/BUILD_SUCCESSOR_20260909_211448_468856/BUILD_PLAN.json"
plan = json.loads(read(planpath))
names = [m["module"] for m in plan["modules"]]
assert len(names) == len(set(names)) == 98
source = read(CANON / "um.py")
tree = ast.parse(source.decode("utf-8-sig"))
embedded_nodes = [n for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "_EMBEDDED_KERNEL_FILES" for t in n.targets)]
assert len(embedded_nodes) == 1
embedded = ast.literal_eval(embedded_nodes[0].value)
sealraw = read(CANON / "um_absoluto_selo.json")
seal = json.loads(sealraw)
read(CANON / "tgl_kernel_proof_manifest.json")
read(CANON / "rodada_v338_stdout.txt")
inventory = []
for p in CANON.iterdir():
    st = p.stat()
    inventory.append({"name": p.name, "is_directory": p.is_dir(), "bytes": st.st_size if p.is_file() else None,
                      "mtime_utc": datetime.fromtimestamp(st.st_mtime, timezone.utc).isoformat()})
inventory.sort(key=lambda x: x["mtime_utc"], reverse=True)
stdout_inventory = [e for e in inventory if not e["is_directory"] and re.fullmatch(r"rodada_v\d+.*stdout.*\.txt", e["name"])]
assert stdout_inventory
latest_stdout = CANON / stdout_inventory[0]["name"]
read(latest_stdout)
index = read(NAV / "TGL_INDICE_VIVO.md").decode("utf-8-sig")
atlas = read(NAV / "TGL_ATLAS.md").decode("utf-8-sig")
def anchors(text, predicates, tail=None):
    rows = [{"line": i, "text": line} for i, line in enumerate(text.splitlines(), 1) if any(p(line) for p in predicates)]
    return rows[-tail:] if tail else rows
nav_anchors = {
    "index": anchors(index, [lambda s: "| versão |" in s, lambda s: "última COMPLETA" in s, lambda s: "rodada |" in s, lambda s: s.startswith("2. **Ponte"), lambda s: s.startswith("1. **H3"), lambda s: s.startswith("8. **Colapso")]),
    "atlas": anchors(atlas, [lambda s: "RE-ÂNCORA" in s and "v338" in s,
                             lambda s: s.startswith("## ") and "v338" in s,
                             lambda s: "ultima COMPLETA custodiada" in s], 5)
}
lines = source.decode("utf-8-sig").splitlines()
entry = next(i for i, line in enumerate(lines, 1) if line.strip() == '"TGLExt/SelectedGravitationalAtlas.lean":')
source_anchors = [{"line": i, "text": line.strip()} for i, line in enumerate(lines, 1)
                  if entry <= i <= entry + 40 and any(x in line for x in ("[INPUT]", "correspondencia fisica", "alem da classe", "leis de area", "condicionado a area"))]
seal_anchors = [{"line": i, "text": line.strip()} for i, line in enumerate(sealraw.decode("utf-8-sig").splitlines(), 1)
                if any('"' + k + '"' in line for k in ("qg_closure_verdict", "renormalization_wall_verdict", "fail_closed_selftest"))]
previous_pins = {Path(p["path"]).resolve().as_posix(): p for p in prior["pins"]}
comparisons = []
for name in ("um.py", "um_absoluto_selo.json", "tgl_kernel_proof_manifest.json", "rodada_v338_stdout.txt"):
    key = (CANON / name).resolve().as_posix()
    old, current = previous_pins[key], PINS[key]
    comparisons.append({"path": key, "unchanged": current["sha256"] == old["sha256"] and current["bytes"] == old["bytes"],
                        "bytes": current["bytes"], "sha256": current["sha256"]})
presence = [{"module": name, "present": "TGLExt/" + name + ".lean" in embedded} for name in names]
absent = [m["module"] for m in presence if not m["present"]]
all_same = all(c["unchanged"] for c in comparisons)
no_successor_stdout = latest_stdout.name == "rodada_v338_stdout.txt"
before = list(PINS.values())
after = [pin(p["path"]) for p in before]
assert before == after
now = datetime.now(timezone.utc).isoformat()
result = {
    "status": "READ_ONLY_STABLE_SNAPSHOT",
    "created_utc": now, "embedded_files": len(embedded), "modules": presence,
    "present": sum(m["present"] for m in presence), "absent": absent,
    "comparison_with_delivery085": comparisons,
    "new_canonical_content_detected": not all_same,
    "latest_stdout": latest_stdout.as_posix(), "no_successor_stdout_in_this_directory": no_successor_stdout,
    "seal_um_hash_matches": seal["sha256"]["um.py"] == hashlib.sha256(source).hexdigest(),
    "seal_excerpt": {key: seal[key] for key in ("qg_closure_verdict", "renormalization_wall_verdict", "fail_closed_selftest")},
    "source_anchors": source_anchors, "seal_anchors": seal_anchors, "navigation_anchors": nav_anchors,
    "canonical_recent_entries": inventory[:25], "stdout_recent_entries": stdout_inventory[:12],
    "pins": before, "pins_after": after, "all_read_sources_unchanged": True,
    "um_executed_or_imported": False, "originals_written": False,
    "navigation_latest_complete_discrepancy": "Index calls v320 latest complete; final Atlas append v338 calls v336. Historical statements preserved, not resolved here.",
    "scope": "Current canonical four files, latest stdout names, AST/literal_eval and plan98; bounded canonical directory plus read-only index/Atlas navigation. No other houses or recursive scan."
}
snapshot_pin = new("ESTADO_CANONICO_INSPECAO_086.json", (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
if not all_same or not no_successor_stdout:
    verdict = "Há delta de conteúdo ou novo stdout; este snapshot não o promove a prova e exige revisão substantiva adicional."
else:
    verdict = "Não foi observado delta canônico desde085: os quatro arquivos continuam byte a byte idênticos, e o stdout mais recente neste diretório ainda é o da v338."
rows = []
for c in comparisons:
    info = PINS[c["path"]]
    rows.append("| " + Path(c["path"]).name + " | " + str(info["bytes"]) + " | " + info["sha256"] + " | " + info["mtime_utc"] + " |")
md = f"""# Nova inspeção086 do canônico e de sua navegação

[REAL — leitura estática em {now}] {verdict}

O caminho efetivamente conferido é C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós. A ausência de sucessora nesse caminho não nega trabalho em outra cópia ou em preparação na sessão codificadora. Não houve busca em outras casas ou varredura recursiva do acervo.

| Artefato | Bytes | SHA-256 medido | Mtime UTC |
|---|---:|---|---|
""" + "\n".join(rows) + f"""

[REAL — AST e plano] O embutido contém {len(embedded)} arquivos. A lista de98 módulos foi lida do BUILD_PLAN da sucessão verificada, não reconstruída de memória. Presentes: {result['present']}; ausentes: {len(absent)}. A lista completa está no snapshot. O hash de um.py confere com o selo: {result['seal_um_hash_matches']}. Presença AST não significa recompilação nesta inspeção.

[REAL — conteúdo lido] Foram conferidos o cabeçalho atual de SelectedGravitationalAtlas, o selo e os registros de navegação pertinentes, além dos hashes completos. A reconstrução selecionada mantém área e conservação como condições; o registro R e a origem física permanecem INPUT, e correspondência física, matéria/área dos mesmos dados, atlas físico, anomalias e UV permanecem pendências expressas no cabeçalho. Sem delta de bytes, não há nova alteração concreta a interpretar nesses artefatos desde085.

As linhas medidas de um.py são:
""" + "\n".join(f"- {a['line']}: {a['text']}" for a in source_anchors) + """

Os campos do selo foram lidos como vereditos DECLARADOS pelo programa; o rito, os testes e Lean não foram reexecutados:
""" + "\n".join(f"- {a['line']}: {a['text']}" for a in seal_anchors) + """

[REAL — navegação] TGL_INDICE_VIVO.md e a última reâncora/append do TGL_ATLAS.md continuam apontando para v338. Seus bytes/hashes/mtimes foram medidos antes/depois, sem copiar ou bifurcar o Atlas. A consulta foi pontual; não se afirma leitura integral de todos os verbetes.

Há uma divergência histórica preservada: o índice chama v320 de última COMPLETA custodiada, enquanto o append final v338 do Atlas chama v336. Esta inspeção não decidiu qual custódia completa deve prevalecer; isso exigiria os recibos específicos. Nenhuma das duas frases é evidência de sucessora da v338. A fonte e o stdout atuais foram medidos separadamente da navegação.

O índice mantém fase/ramo e a resposta H3 da tela reconhecidos no modelo, com seus limites físicos explicitados; não se reabrem esses antecedentes pela comparação. A inspeção também não atribui ao canônico as demonstrações085/086 ainda documentadas na bancada.

[REAL — custódia] Todos os arquivos pinados permaneceram idênticos antes/depois da janela. Somente novos emissor, snapshot, parecer e manifesto nesta pasta Chatgpt. Nenhum um.py, Atlas, índice, selo, memória ou original foi alterado, executado ou importado. A lista de25 entradas recentes no canônico e12 saídas de rodada no recorte está no snapshot. Zero novo CAS, Lean ou rito de natureza.
"""
note_pin = new("PARECER_INSPECAO_CANONICA_086.md", md.encode("utf-8"))
manifest = {"created_utc": now, "status": "READ_ONLY_CANONICAL_INSPECTION",
            "snapshot": snapshot_pin, "note": note_pin, "sources_before": before,
            "sources_after": after, "all_sources_unchanged": True,
            "canonical_four_unchanged_from085": all_same, "new_math_runs": 0,
            "um_executed_or_imported": False, "originals_written": False}
manifest_pin = new("MANIFESTO_INSPECAO_CANONICA_086.json", (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
print(json.dumps({"canonical_four_unchanged_from085": all_same, "latest_stdout": latest_stdout.name,
                  "embedded_files": len(embedded), "present": result["present"], "absent": len(absent),
                  "sources_preserved": len(before), "snapshot": snapshot_pin, "note": note_pin, "manifest": manifest_pin}, ensure_ascii=False))

