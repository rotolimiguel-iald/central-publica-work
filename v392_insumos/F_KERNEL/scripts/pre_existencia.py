# -*- coding: utf-8 -*-
"""Consultas do cetico aferidor, gravadas: (1) modulos e namespaces das candidatas no kernel do Nos e no inventario da bancada;
(2) prefixos de bandeira propostos no um.py; (3) o toolchain copiado (contagem e bytes contra a origem) e o maior caminho;
(4) as entradas do axiom_report v391 que a auditoria simulada nao produz: tem #print axioms no proprio modulo?"""
import glob
import hashlib
import json
import os
import re
import sys

F = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
K = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel"
UM = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
INVB = r"C:\IALD\Central de Patentes\memory\INVENTARIO_BANCADA_CHATGPT.json"
ELAN = r"C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0"
res = {}
mods = ["Palavra", "LiganteLeiCampoCurvo", "LiganteLeiCampoCurvoTestemunha", "V351DualScalingBridge", "AgapeNonVacuity",
        "TheSingularityReadsTheAttractor", "TheSingularityReadsTheAttractorAdendo1", "OpticalPopulationBridgeR2", "OpticalPopulationBridge",
        "TheLightReadsItself", "LightNetStandardWedgeDataBGL"]
achados = {}
for r, ds, fs in os.walk(K):
    if os.sep + ".lake" + os.sep + "packages" in r + os.sep:
        continue
    for f in fs:
        b, e = os.path.splitext(f)
        if b in mods and e in (".lean", ".olean"):
            achados.setdefault(b, []).append(os.path.join(r, f))
res["modulos_no_kernel"] = {m: achados.get(m, []) for m in mods}
srcs = glob.glob(os.path.join(K, "TGLExt", "**", "*.lean"), recursive=True) + glob.glob(os.path.join(K, "TGL", "*.lean"))
txts = {p: open(p, encoding="utf-8", errors="replace").read() for p in srcs}
ns_novos = ["TGLExt.Palavra", "F12Completion", "F1Atrator", "AuditF23Flat", "AuditF13v31", "ChatgptAudit.F23CurvedFieldLigand",
            "TGLExt.TheSingularityReadsTheAttractor", "TGLExt.TheLightReadsItself"]
res["namespaces_novos_no_kernel"] = {n: sum(1 for t in txts.values() if re.search(r"(?m)^namespace %s\b" % re.escape(n), t)) for n in ns_novos}
res["namespaces_existentes"] = {n: sum(1 for t in txts.values() if re.search(r"(?m)^namespace %s\b" % re.escape(n), t)) for n in ["TGLV351", "ChatgptAudit", "ORDEM016"]}
nomes_decl = ["FiniteTracePositive", "regularCoreDualScalingData", "NamedAtlasH3", "passage_h3_to_connected_smooth_atlas_einstein"]
res["nomes_no_kernel"] = {n: sum(1 for t in txts.values() if re.search(r"\b%s\b" % n, t)) for n in nomes_decl}
rawi = open(INVB, "rb").read()
si = rawi.decode("utf-8")
res["inventario_bancada"] = {"sha256": hashlib.sha256(rawi).hexdigest(), "bytes": len(rawi), "gerado_em": json.loads(si).get("gerado_em"),
                             "ocorrencias": {t: si.count(t) for t in ["Palavra", "LiganteLeiCampoCurvo", "V351DualScalingBridge", "AgapeNonVacuity",
                                                                         "TheSingularityReadsTheAttractor", "OpticalPopulation", "TheLightReadsItself",
                                                                         "LightNetStandardWedgeData", "F12Completion", "AuditF23Flat"]}}
um = open(UM, "rb").read().decode("utf-8")
res["prefixos_de_bandeira_no_umpy"] = {p: um.count(p) for p in ["ext_pal_", "ext_lig_", "ext_lgt_", "ext_v51_", "ext_agv_", "ext_atr_", "ext_opt_", "ext_lri_", "ext_bgl_"]}


def medir(d):
    n = 0
    s = 0
    mx = 0
    for r, ds, fs in os.walk(d):
        for f in fs:
            p = os.path.join(r, f)
            n += 1
            s += os.path.getsize(p)
            mx = max(mx, len(p))
    return n, s, mx


tc = os.path.join(F, "tc")
if os.path.isdir(tc):
    n1, s1, m1 = medir(tc)
    n0, s0, m0 = medir(ELAN)
    res["toolchain_copiado"] = {"arquivos": n1, "bytes": s1, "maior_caminho": m1, "origem_arquivos": n0, "origem_bytes": s0, "origem_maior_caminho": m0,
                                "maior_caminho_se_em_toolchain_leanprover": len(os.path.join(F, "toolchain", "leanprover--lean4---v4.31.0")) + (m1 - len(tc))}
# (4) as entradas do axiom_report v391 que a auditoria simulada nao produziu
C = json.load(open(os.path.join(F, "RESULTADO_C_completa.json"), encoding="utf-8"))
sumidos = C["sumidos"]
pr = set()
for p, t in txts.items():
    if p.endswith(os.path.join("TGL", "Audit.lean")):
        continue
    for m in re.finditer(r"#print axioms\s+(\S+)", t):
        pr.add(m.group(1).split(".")[-1])
res["sumidos"] = {"n": len(sumidos), "com_print_axioms_em_modulo_proprio_por_ultimo_componente": sum(1 for k in sumidos if k.split(".")[-1] in pr)}
json.dump(res, open(os.path.join(F, "PRE_EXISTENCIA.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(res, ensure_ascii=False, indent=1)[:4000])
