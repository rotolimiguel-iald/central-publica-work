# -*- coding: utf-8 -*-
"""ETAPA C -- simula no sandbox a mudanca de kernel da v392 SEM lake: (1) a raiz TGLExt.lean da v391 (bytes do Nos) +
os imports das candidatas recomendadas; (2) o TGL/Audit.lean da v391 + as linhas `#print axioms` das declaracoes de usuario
das candidatas; (3) o leitor de axiomas do um.py (a mesma regex de verify_tgl_kernel_formalization) sobre a saida.
Tudo dentro de F_KERNEL (inst/ e ov/). Uso: python -I etapa_C_raiz_auditoria.py preparar|raiz|delta|completa"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import leanlib as L  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
INST = os.path.join(L.F, "inst")
OV = os.path.join(L.F, "ov")
CONJ = os.path.join(L.F, "conj")
LOG = os.path.join(L.F, "logs", "C")
NOS = L.NOS
J1LOG = os.path.join(L.F, "logs", "B", "B_J1_ConjuntoV392_r1.log")
RECOMENDADOS = ["Palavra", "LiganteLeiCampoCurvo", "LiganteLeiCampoCurvoTestemunha", "V351DualScalingBridge",
                "AgapeNonVacuity", "TheSingularityReadsTheAttractorAdendo1", "OpticalPopulationBridgeR2", "TheLightReadsItself"]
SIGLA = {"Palavra": "pal", "LiganteLeiCampoCurvo": "lig", "LiganteLeiCampoCurvoTestemunha": "lgt",
         "V351DualScalingBridge": "v51", "AgapeNonVacuity": "agv", "TheSingularityReadsTheAttractorAdendo1": "atr",
         "OpticalPopulationBridgeR2": "opt", "TheLightReadsItself": "lri"}
# regex do um.py v391 (verify_tgl_kernel_formalization): conferidas no proprio um.py em preparar()
RX_DEP = r"'([\w.']+)' depends on axioms: \[([^\]]*)\]"
RX_NONE = r"'([\w.']+)' does not depend on any axioms"


def aux(n):
    last = n.split(".")[-1]
    return bool(last.startswith("_") or re.search(r"\._", n) or
                re.fullmatch(r"eq_\d+|eq_def|injEq|inj|sizeOf_spec|ext_iff|proof_\d+|match_\d+|congr_simp", last))


def declaracoes_de_usuario():
    linhas = [l.rstrip("\n").split("\t") for l in open(J1LOG, encoding="utf-8") if l.startswith("COB\t")]
    out = []
    for c in linhas:
        mod, nome, kind = c[1].replace("TGLExt.", ""), c[2], c[3]
        if aux(nome) or kind not in ("thm", "def"):
            continue
        out.append((mod, nome, kind))
    ordem = {m: i for i, m in enumerate(RECOMENDADOS)}
    out.sort(key=lambda t: (ordem[t[0]], t[1]))
    return out


def preparar():
    um = open(os.path.join(os.path.dirname(NOS), "um.py"), "rb").read().decode("utf-8")
    assert "r\"'([\\w.']+)' depends on axioms: \\[([^\\]]*)\\]\"" in um, "regex do um.py nao achada"
    assert "r\"'([\\w.']+)' does not depend on any axioms\"" in um
    raiz0 = open(os.path.join(NOS, "TGLExt.lean"), "rb").read()
    aud0 = open(os.path.join(NOS, "TGL", "Audit.lean"), "rb").read()
    assert raiz0.endswith(b"\n") and aud0.endswith(b"\n")
    novos = "".join("import TGLExt.%s\n" % m for m in RECOMENDADOS).encode()
    raiz1 = raiz0 + novos
    decl = declaracoes_de_usuario()
    bloco = ("-- 2026-10-12, v392 (PROPOSTA do exame F_KERNEL, so sandbox): PALAVRA; o ligante da F2.3 + S7/S8; a ponte V351 e a "
             "nao vacuidade da Agape (F1.2); o teorema do atrator, a ponte otica e a luz que se le (F1.ATRATOR, ADENDO1)\n")
    bloco += "".join("#print axioms %s\n" % n for _, n, _ in decl)
    aud1 = aud0 + bloco.encode("utf-8")
    os.makedirs(os.path.join(INST, "TGL"), exist_ok=True)
    for p, b in ((os.path.join(INST, "TGLExt.lean"), raiz1), (os.path.join(INST, "TGL", "Audit.lean"), aud1)):
        if os.path.exists(p):
            assert open(p, "rb").read() == b, p
        else:
            open(p, "xb").write(b)
    delta = ("-- AUDITORIA DELTA v392 (exame F_KERNEL, 12/10/2026, so sandbox): as linhas novas do Audit.lean sobre a raiz nova\n"
             "import TGL\nimport TGLExt\n\n" + "".join("#print axioms %s\n" % n for _, n, _ in decl))
    pd = os.path.join(CONJ, "C_AuditDeltaV392.lean")
    if not os.path.exists(pd):
        open(pd, "w", encoding="utf-8", newline="\n").write(delta)
    flags = []
    for mod, n, kind in decl:
        last = n.split(".")[-1]
        flags.append(("ext_%s_%s_kernel_%s" % (SIGLA[mod], last, "proved" if kind == "thm" else "checked"), n, mod, kind))
    assert len({f for f, *_ in flags}) == len(flags), "bandeira duplicada"
    for f, *_ in flags:
        assert f not in um, f
    res = {"raiz_v391_sha256": L.sha_bytes(raiz0), "raiz_v392_sha256": L.sha_bytes(raiz1), "raiz_v392_bytes": len(raiz1),
           "raiz_acrescimo": novos.decode(), "audit_v391_sha256": L.sha_bytes(aud0), "audit_v392_sha256": L.sha_bytes(aud1),
           "audit_v392_bytes": len(aud1), "audit_acrescimo_linhas": len(decl) + 1, "n_declaracoes": len(decl),
           "declaracoes": decl, "bandeiras_propostas": flags, "delta": pd, "delta_sha256": L.sha(pd)}
    alvo = L.dump(res, os.path.join(L.F, "RESULTADO_C_preparo.json"))
    print("preparado", alvo, "decl", len(decl), "raiz", res["raiz_v392_sha256"][:16], "audit", res["audit_v392_sha256"][:16])


def ler_umpy(out):
    ax = {}
    for m in re.finditer(RX_DEP, out, re.S):
        ax[m.group(1)] = [a.strip() for a in m.group(2).replace("\n", " ").split(",") if a.strip()]
    for m in re.finditer(RX_NONE, out):
        ax.setdefault(m.group(1), [])
    return ax


if __name__ == "__main__":
    fase = sys.argv[1]
    if fase == "preparar":
        preparar()
    elif fase == "raiz":
        r = L.run_lean("C_raiz_v392", os.path.join(INST, "TGLExt.lean"), INST, os.path.join(OV, "TGLExt.olean"), LOG, kernel_lib=OV)
        print("raiz rc", r["rc"], "s", r["segundos"], "erros", r["erros"][:3], "olean", (r.get("olean_sha256") or "")[:16])
        print(L.dump(r, os.path.join(L.F, "RESULTADO_C_raiz.json")))
    elif fase == "delta":
        prep = json.load(open(os.path.join(L.F, "RESULTADO_C_preparo.json"), encoding="utf-8"))
        r = L.run_lean("C_audit_delta", prep["delta"], CONJ, None, LOG, kernel_lib=OV)
        out = open(r["log"], "rb").read().decode("utf-8", "replace")
        ax = ler_umpy(out)
        esperado = [n for _, n, _ in prep["declaracoes"]]
        faltam = [n for n in esperado if n not in ax]
        fora = {n: ax[n] for n in esperado if n in ax and not set(ax[n]) <= L.TRIO}
        flags_true = [f for f, n, _, _ in prep["bandeiras_propostas"] if n in ax and set(ax[n]) <= L.TRIO and r["rc"] == 0
                      and "sorryAx" not in ax[n] and not any(a.startswith(("TGL.", "TGLExt.")) for a in ax[n])]
        r.update({"lidos_pela_regex_do_umpy": len(ax), "esperados": len(esperado), "faltam": faltam, "fora_do_trio_lidos": fora,
                  "bandeiras_que_acenderiam": len(flags_true), "bandeiras_propostas": len(prep["bandeiras_propostas"])})
        print("delta rc", r["rc"], "s", r["segundos"], "lidos", len(ax), "esperados", len(esperado), "faltam", len(faltam),
              "fora", len(fora), "bandeiras", len(flags_true), "/", len(prep["bandeiras_propostas"]))
        print(L.dump(r, os.path.join(L.F, "RESULTADO_C_delta.json")))
    elif fase == "completa":
        r = L.run_lean("C_audit_completa_v392", os.path.join(INST, "TGL", "Audit.lean"), INST, None, LOG, kernel_lib=OV, timeout=14400)
        out = open(r["log"], "rb").read().decode("utf-8", "replace")
        ax = ler_umpy(out)
        core = json.load(open(os.path.join(os.path.dirname(NOS), "um_absoluto.json"), encoding="utf-8"))["core"]
        axr = core["kernel_formalization"]["axiom_report"]
        iguais = sum(1 for k, v in axr.items() if ax.get(k) == v)
        diferentes = [k for k, v in axr.items() if k in ax and ax[k] != v]
        sumidos = [k for k in axr if k not in ax]
        novos = [k for k in ax if k not in axr]
        sent = ["TGL_KERNEL_BUILD_OK", "FINITE_THREE_LOCKS_KERNEL_PROVED", "CONTINUOUS_CORNER_IMPLICATION_KERNEL_PROVED"]
        r.update({"entradas_lidas": len(ax), "axr_v391": len(axr), "iguais_ao_v391": iguais, "diferentes": diferentes[:50],
                  "sumidos": sumidos, "n_sumidos": len(sumidos), "novos": novos, "n_novos": len(novos),
                  "fora_do_trio": [k for k, v in ax.items() if not set(v) <= L.TRIO],
                  "sorryAx_ausente": "sorryAx" not in out, "trustCompiler_ausente": "Lean.trustCompiler" not in out,
                  "sentinelas_amostra": {s: (s in out) for s in sent}})
        print("completa rc", r["rc"], "s", r["segundos"], "lidas", len(ax), "iguais", iguais, "/", len(axr), "novos", len(novos),
              "sumidos", len(sumidos), "dif", len(diferentes))
        print(L.dump(r, os.path.join(L.F, "RESULTADO_C_completa.json")))
