# -*- coding: utf-8 -*-
"""Medição (só leitura) do cofre v394 contra o cofre v394, para a pedra v43 do runner da Fronteira (v59)."""
import json, re
from pathlib import Path

OC = Path(r"C:\IALD\Central de Patentes\vault\originals_copy")
C4, C1 = OC / "um_unificado_v395", OC / "um_unificado_v394"
can4 = json.loads((C4 / "um_absoluto.json").read_text(encoding="utf-8"))
can1 = json.loads((C1 / "um_absoluto.json").read_text(encoding="utf-8"))
sl4 = json.loads((C4 / "um_absoluto_selo.json").read_text(encoding="utf-8"))
mf4 = json.loads((C4 / "tgl_kernel_proof_manifest.json").read_text(encoding="utf-8"))
g1 = json.loads((C1 / "CUSTODY_MANIFEST.json").read_text(encoding="utf-8")).get("gate")
g4 = json.loads((C4 / "CUSTODY_MANIFEST.json").read_text(encoding="utf-8")).get("gate")
core4, core1 = can4.get("core") or {}, can1.get("core") or {}
novos = sorted(k for k in core4 if k not in core1)
sumidos = sorted(k for k in core1 if k not in core4)
print("blocos novos desde v394:", len(novos), novos)
print("blocos que sumiram:", sumidos)
kf4, kf1 = core4.get("kernel_formalization") or {}, core1.get("kernel_formalization") or {}
print("kernel_formalization chaves novas:", len([k for k in kf4 if k not in kf1]), "| total v391/v394:", len(kf1), len(kf4))
for k in novos:
    v = core4[k]
    if isinstance(v, dict):
        vd = str(v.get("verdict") or "")
        print("  %-42s all_verified=%s | gate=%s | CONFIRMED=%s" % (k, v.get("all_verified"), ("GATE_UNMOVED" in vd or "GATE_UNTOUCHED" in vd),
              bool(re.search(r"(?<![A-Z_])CONFIRMED", vd.replace("NOT_CONFIRMED", "")))))
    else:
        print("  %-42s (tipo %s)" % (k, type(v).__name__))
pat = re.compile(r"^([a-z][a-z0-9_]{3,}) & ([A-Z][A-Z0-9_]{12,})", re.M)
pt4 = (C4 / "um_absoluto_pt.txt").read_text(encoding="utf-8", errors="replace")
en4 = (C4 / "um_absoluto_en.txt").read_text(encoding="utf-8", errors="replace")
pt1 = (C1 / "um_absoluto_pt.txt").read_text(encoding="utf-8", errors="replace")
r4, e4, r1 = dict(pat.findall(pt4)), dict(pat.findall(en4)), dict(pat.findall(pt1))
mud = sorted(k for k in r1 if r4.get(k) != r1[k])
print("registro PT/EN v394:", len(r4), len(e4), "| v391:", len(r1), "| mudados desde v394:", mud)
print("registro novos:", sorted(k for k in r4 if k not in r1))
fm, ar = mf4.get("formal_files_sha256") or {}, mf4.get("axiom_report") or {}
fora = sum(1 for v in ar.values() for x in (v or []) if x not in ("propext", "Classical.choice", "Quot.sound"))
print("kernel v394:", len(fm), "formais |", len(ar), "termos | fora do trio:", fora)
gate = (core4.get("qg_closure") or {}).get("gate") or {}
print("gate: full_static_witness_exists =", gate.get("full_static_witness_exists"), "| selo == cofre v391:", str(sl4.get("qg_closure_verdict")) == str(g1),
      "| manifesto v394 == v391:", g4 == g1, "| um_version:", sl4.get("um_version"))
confs = [k for k, v in sl4.items() if str(k).endswith("_verdict") and re.search(r"(?<![A-Z_])CONFIRMED", str(v)) and "NOT_CONFIRMED" not in str(v)]
print("vereditos do selo com CONFIRMED:", confs)
e = core4.get("estatuto_da_prova_v391") or {}
print("estatuto p1:", (e.get("prova_1_kernel") or {}).get("n_theorems_clean"), (e.get("prova_1_kernel") or {}).get("declaracoes_auditadas"))
