# -*- coding: utf-8 -*-
"""SÓ LEITURA — a sondagem da v398 antes do handoff (24/10/2026, regra do operador: «pode custodiar sempre que o handoff aparecer»): tudo
o que os scripts da custódia precisam saber, LIDO do selo, do core, do manifesto, do um.py e do cofre v397 — nenhum número digitado.
Grava fatos_v398.json (os números) e imprime os textos dos registros novos (para os textos do LEDGER e do arco)."""
import ast, json, re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
NOS = Path(r"C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós")
ESP = Path(r"C:/IALD/Artigo/the_boundary/Um (absoluto) — Grande Atrator")
COF6 = Path(r"C:/IALD/Central de Patentes/vault/originals_copy/um_unificado_v397")
CS = Path(r"C:/IALD/Central de Patentes/work/cadeia_de_selo")
W = Path(__file__).resolve().parent
selo = json.loads((NOS / "um_absoluto_selo.json").read_text(encoding="utf-8"))
core = json.loads((NOS / "um_absoluto.json").read_text(encoding="utf-8"))["core"]
core6 = json.loads((COF6 / "um_absoluto.json").read_text(encoding="utf-8"))["core"]
pm = json.loads((NOS / "tgl_kernel_proof_manifest.json").read_text(encoding="utf-8"))
pm6 = json.loads((COF6 / "tgl_kernel_proof_manifest.json").read_text(encoding="utf-8"))
V, PIN = selo["um_version"], selo["sha256"]["um.py"]
F = {"versao": V, "pin": PIN, "pin16": PIN[:16], "timestamp": selo["timestamp"], "bytes_um_py": (NOS / "um.py").stat().st_size,
     "selftest": selo.get("fail_closed_selftest"), "gate": selo["qg_closure_verdict"],
     "registros_novos": sorted(k for k in core if k not in core6), "registros_sumidos": sorted(k for k in core6 if k not in core)}
kf, kf6 = core.get("kernel_formalization") or {}, core6.get("kernel_formalization") or {}
F["bandeiras_novas"] = [k for k in kf if k not in kf6]
F["kernel"] = {"formais": len(pm["formal_files_sha256"]), "declaracoes": len(pm["axiom_report"]),
               "fora_do_trio": sum(1 for v in pm["axiom_report"].values() for x in (v or []) if x not in ("propext", "Classical.choice", "Quot.sound")),
               "modulos_novos": sorted(set(pm["formal_files_sha256"]) - set(pm6["formal_files_sha256"])),
               "formais_v397": len(pm6["formal_files_sha256"]), "declaracoes_v397": len(pm6["axiom_report"])}
P1 = core["estatuto_da_prova_v391"]["prova_1_kernel"]
F["escada"] = "%d/%d" % (P1["n_theorems_clean"], P1["n_theorems_expected"])
F["no_trio"] = P1["no_trio"]
P16 = core6["estatuto_da_prova_v391"]["prova_1_kernel"]
F["escada_v397"] = "%d/%d" % (P16["n_theorems_clean"], P16["n_theorems_expected"])
mk = re.search(r"CLOSURE_(\d+)_CONSTANTS_(\d+)_THEOREMS", core["kh_n1_cobertura_%s" % V]["verdict"])
mk6 = re.search(r"CLOSURE_(\d+)_CONSTANTS_(\d+)_THEOREMS", core6["kh_n1_cobertura_v397"]["verdict"])
F["kh"] = {"constantes": int(mk.group(1)), "teoremas": int(mk.group(2)), "constantes_v397": int(mk6.group(1)), "teoremas_v397": int(mk6.group(2))}
# o registro PT/EN (os nomes & vereditos), contra o cofre v397
pat = re.compile(r"^([a-z][a-z0-9_]{3,}) & ([A-Z][A-Z0-9_]{12,})", re.M)
rp, re_, r6 = dict(pat.findall((NOS / "um_absoluto_pt.txt").read_text(encoding="utf-8", errors="replace"))), \
    dict(pat.findall((NOS / "um_absoluto_en.txt").read_text(encoding="utf-8", errors="replace"))), \
    dict(pat.findall((COF6 / "um_absoluto_pt.txt").read_text(encoding="utf-8", errors="replace")))
F["registro"] = {"pt": len(rp), "en": len(re_), "v397": len(r6), "novos": sorted(k for k in rp if k not in r6),
                 "mudados_desde_v397": sorted(k for k in r6 if rp.get(k) != r6[k])}
# os dicionários _V397_* do um.py e os contratos
arv = ast.parse((NOS / "um.py").read_text(encoding="utf-8"))
dics, contratos = [], {}
for n in arv.body:
    if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
        nm = n.targets[0].id
        if nm.startswith("_V%s_" % V[1:]):
            dics.append(nm)
        if nm.endswith("_CONTRACT"):
            try:
                v = ast.literal_eval(n.value)
                contratos[nm] = v.get("expected_ladder") if isinstance(v, dict) else None
            except Exception:  # noqa: BLE001
                contratos[nm] = "não literal"
F["dicionarios_v398"] = dics
F["contratos_expected_ladder"] = contratos
# a cadeia de selo: diffs e recibos
F["cadeia"] = {"pastas": sorted(p.name for p in CS.glob("%s*" % V)),
               "diffs": sorted(p.name for p in (CS / V).glob("DIFF_*") if ".bak_" not in p.name) if (CS / V).is_dir() else [],
               "recibos": sorted(str(p.relative_to(CS / V)) for p in (CS / V).rglob("RECIBO_*") if p.is_file() and ".bak_" not in p.name and "ensaio" not in str(p.relative_to(CS / V))) if (CS / V).is_dir() else []}
F["nos"] = {"handoff": (NOS / ("HANDOFF_%s_CUSTODIA.md" % V)).is_file(), "stdout": (NOS / ("rodada_%s_stdout.txt" % V)).is_file(),
            "diario_bloco": bool(re.search(r"^## [^\n]*\*\*%s SELADA" % V, (NOS / "MEMORIA_DA_LINHAGEM.md").read_text(encoding="utf-8"), re.M))}
(W / "fatos_v398.json").write_text(json.dumps(F, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({k: F[k] for k in ("versao", "pin16", "timestamp", "registros_novos", "bandeiras_novas", "kernel", "escada", "escada_v397", "kh", "registro", "dicionarios_v398", "contratos_expected_ladder", "cadeia", "nos")}, ensure_ascii=False, indent=1)[:3500])
for k in F["registros_novos"]:
    r = core[k]
    print("\n==", k, "\nESTATUTO:", str(r.get("estatuto"))[:600])
    for campo in ("diz", "nao_diz", "limites"):
        for x in (r.get(campo) or [])[:8]:
            print("  %s: %s" % (campo.upper(), str(x)[:420]))
    for e in r.get("erratas") or []:
        print("  ERRATA:", json.dumps(e, ensure_ascii=False)[:600])
    kn = r.get("kernel")
    if kn:
        print("  KERNEL:", json.dumps(kn, ensure_ascii=False)[:700])
    for x in (r.get("leituras_do_operador") or [])[:6]:
        print("  LEITURA:", json.dumps(x, ensure_ascii=False)[:260])
    print("  VERDICT:", r["verdict"])
