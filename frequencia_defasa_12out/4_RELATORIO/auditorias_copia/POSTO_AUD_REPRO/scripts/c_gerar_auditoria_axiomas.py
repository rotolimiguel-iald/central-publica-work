# -*- coding: utf-8 -*-
# Auditor REPRO, item (4): gera, por parser PROPRIO, o arquivo de auditoria com #print axioms de TODA declaracao nomeada
# da pedra (copia no sandbox do auditor). Depois de rodado o Lean, 'analisar' le a saida e confere os axiomas.
import os, re, sys, json, hashlib
AUD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PEDRA = os.path.join(AUD, "L", "TGLExt", "TheUnitIsTheRank.lean")
AUDIT = os.path.join(AUD, "L", "AuditRepro.lean")
SAIDA_LEAN = os.path.join(AUD, "saidas", "lean_logs", "auditoria_repro_SAIDA.txt")
NS = "TGLExt.TheUnitIsTheRank"
DECL = re.compile(r"^\s*(?:@\[[^\]]*\]\s*)?(?:(?:private|protected|noncomputable)\s+)*(theorem|lemma|def|abbrev|instance|structure)\s+([^\s:({\[]+)", re.M)


def nomes():
    t = open(PEDRA, encoding="utf-8").read()
    # tira comentarios de bloco e de linha antes de procurar declaracoes
    t2 = re.sub(r"/-.*?-/", lambda m: "\n" * m.group(0).count("\n"), t, flags=re.S)
    t2 = re.sub(r"--[^\n]*", "", t2)
    return [(k, n) for k, n in DECL.findall(t2)]


if sys.argv[1] == "gerar":
    ds = nomes()
    linhas = ["/- auditoria do auditor REPRO (parser proprio) -/", "import TheUnitIsTheRank", ""]
    linhas += ["#print axioms %s.%s" % (NS, n) for k, n in ds]
    open(AUDIT, "w", encoding="utf-8").write("\n".join(linhas) + "\n")
    print(json.dumps({"n_declaracoes": len(ds), "por_tipo": {k: sum(1 for x in ds if x[0] == k) for k in set(x[0] for x in ds)},
                      "audit_sha256": hashlib.sha256(open(AUDIT, "rb").read()).hexdigest()}, ensure_ascii=False))
else:
    ds = nomes()
    txt = open(SAIDA_LEAN, "rb").read().decode("utf-8", errors="replace")
    OK = {"propext", "Classical.choice", "Quot.sound"}
    res, fora, sem = {}, [], []
    for k, n in ds:
        full = "%s.%s" % (NS, n)
        m = re.search(r"'%s' depends on axioms: \[([^\]]*)\]" % re.escape(full), txt)
        m0 = re.search(r"'%s' does not depend on any axioms" % re.escape(full), txt)
        if m:
            ax = [a.strip() for a in m.group(1).split(",") if a.strip()]
            res[n] = ax
            if not set(ax) <= OK:
                fora.append([n, ax])
        elif m0:
            res[n] = []
        else:
            sem.append(n)
    out = {"n_declaracoes": len(ds), "n_com_resposta": len(res), "sem_resposta": sem, "fora_do_conjunto_padrao": fora,
           "sorryAx_na_saida": txt.count("sorryAx"), "n_sem_axioma": sum(1 for v in res.values() if not v),
           "uniao_dos_axiomas": sorted(set(a for v in res.values() for a in v)),
           "n_erros": txt.count(": error"), "n_avisos": txt.count(": warning")}
    open(os.path.join(AUD, "saidas", "C_AXIOMAS.json"), "w", encoding="utf-8").write(json.dumps(dict(out, por_declaracao=res), ensure_ascii=False, indent=1))
    print(json.dumps(out, ensure_ascii=False, indent=1))
