# -*- coding: utf-8 -*-
"""relatorio_de_axiomas.py -- DELTA 19/10: o RELATORIO DE AXIOMAS da pedra candidata, LIDO dos logs crus do build FRIO (kernel_d19\\lake_build.log e audit.log) e do sandbox C:\\t\\k394d\\final; escreve AXIOMAS_DELTA_19OUT.json.
Nada digitado: o sha16 da pedra, os axiomas do teorema de composicao e dos oito citados, as linhas do build e do Audit, a proveniencia e os totais saem dos arquivos. Zero sorry nas tres formas (build e Audit crus).
uso: python -I -B -X utf8 relatorio_de_axiomas.py"""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); V = os.path.dirname(HERE); sys.path.insert(0, V)
import delta19_v394 as DL  # noqa: E402
KD = os.path.join(V, DL.KERNEL_DIR)
LB = open(os.path.join(KD, "lake_build.log"), "rb").read().decode("utf-8", "replace"); AU = open(os.path.join(KD, "audit.log"), "rb").read().decode("utf-8", "replace")
sha = lambda b: hashlib.sha256(b).hexdigest()
stone_sb = open(os.path.join(DL.SANDBOX, *DL.STONE_REL.split("/")), "rb").read(); stone_src = open(DL.STONE_SRC, "rb").read()
RX = lambda n: re.compile(r"'" + re.escape(n) + r"' depends on axioms: \[([^\]]*)\]")
norm = lambda s: [a.strip() for a in s.replace("\n", " ").split(",") if a.strip()]


def axiomas(nome):
    em_build = [norm(m.group(1)) for m in RX(nome).finditer(LB)]; em_audit = [norm(m.group(1)) for m in RX(nome).finditer(AU)]
    sem = bool(re.search(r"'" + re.escape(nome) + r"' does not depend on any axioms", LB + AU))
    return {"build": em_build, "audit": em_audit, "sem_axioma_algum": sem}


cov = re.findall(r"(?m)^TGL_AXIOM_COVERAGE_TOTAL decl=(\d+) thm=(\d+) fora_do_trio=(\d+)\s*$", AU)
prov = re.findall(r"(?m)^TGL_DECL_SOURCE\t" + re.escape(DL.THEOREM) + r"\t([^\t\n]+)\s*$", AU)
built = re.search(r"Built " + re.escape(DL.STONE_MOD) + r" \((\d+)s\)", LB)
R = {"pedra": {"modulo": DL.STONE_MOD, "arquivo": DL.STONE_REL, "sha16": sha(stone_sb)[:16], "sha256": sha(stone_sb), "bytes": len(stone_sb), "igual_a_fonte_autoral": stone_sb == stone_src,
                "nome": "provisorio (o operador nomeia)"},
     "teorema_de_composicao": {"nome": DL.THEOREM, "axiomas_no_build": axiomas(DL.THEOREM)["build"], "axiomas_no_audit": axiomas(DL.THEOREM)["audit"], "proveniencia_TGL_DECL_SOURCE": prov,
                               "no_trio": all(set(x) <= set(DL.TRIO) for x in axiomas(DL.THEOREM)["build"] + axiomas(DL.THEOREM)["audit"]) and bool(axiomas(DL.THEOREM)["audit"])},
     "citados": {n: {"axiomas": (axiomas(n)["audit"][0] if axiomas(n)["audit"] else ([] if axiomas(n)["sem_axioma_algum"] else None)), "sem_axioma_algum": axiomas(n)["sem_axioma_algum"]} for n in DL.CITED},
     "compilacao": {"linha_Built_da_pedra_no_build_frio": bool(built), "segundos": int(built.group(1)) if built else None, "sorry_no_build": len(re.findall(r"declaration uses [`'\u2018]sorry|sorryAx", LB)), "sorry_no_audit": len(re.findall(r"declaration uses [`'\u2018]sorry|sorryAx", AU)),
                    "erros_no_build": len(re.findall(r"(?m)^error:|: error:", LB)), "build_completed": bool(re.search(r"(?m)^[ \t]*Build completed successfully", LB))},
     "cobertura_do_audit": {"decl": int(cov[0][0]), "thm": int(cov[0][1]), "fora_do_trio": int(cov[0][2])} if len(cov) == 1 else {"erro": "linha TOTAL ausente ou repetida", "n": len(cov)},
     "logs": {"lake_build.log": {"sha16": sha(LB.encode("utf-8", "replace"))[:16] if False else sha(open(os.path.join(KD, "lake_build.log"), "rb").read())[:16]}, "audit.log": {"sha16": sha(open(os.path.join(KD, "audit.log"), "rb").read())[:16]}},
     "regra": "[REAL] lido dos logs crus do build frio; nenhum axioma fora do trio {propext, Classical.choice, Quot.sound}; zero sorry"}
R["ok"] = bool(R["pedra"]["igual_a_fonte_autoral"] and R["teorema_de_composicao"]["no_trio"] and R["compilacao"]["linha_Built_da_pedra_no_build_frio"] and R["compilacao"]["sorry_no_build"] == 0 and R["compilacao"]["sorry_no_audit"] == 0
              and R["compilacao"]["erros_no_build"] == 0 and R["compilacao"]["build_completed"] and R["cobertura_do_audit"].get("fora_do_trio") == 0 and all(v["axiomas"] is not None and set(v["axiomas"]) <= set(DL.TRIO) for v in R["citados"].values()))
json.dump(R, open(os.path.join(HERE, "AXIOMAS_DELTA_19OUT.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False, indent=1)); sys.exit(0 if R["ok"] else 1)
