# -*- coding: utf-8 -*-
"""KH-N1, D2: (enum) enumera o fecho TGL+TGLExt; (blocos N) collectAxioms -- o mesmo metodo da auditoria de 07/10 -- sobre TODAS
as constantes, em N blocos de modulos rodados em paralelo, cada um num processo lean proprio, contra os .olean do Nos (so leitura);
(merge) junta, confere contra a enumeracao e contra o axiom_report do core v391 (so leitura); (final) numeros do KH-N1."""
import collections
import hashlib
import json
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import leanlib as L  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
F = L.F
KH = os.path.join(F, "kh")
LOG = os.path.join(F, "logs", "KH")
CORE = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json"
M73 = r"C:\IALD\PROGRAMA_IALD\levantamento_qg\cobertura_axiomas\modulos_73.json"
TRIO = L.TRIO


def enum():
    r = L.run_lean("D2_enumerar", os.path.join(KH, "Enumerar.lean"), KH, None, LOG)
    out = open(r["log"], "rb").read().decode("utf-8", "replace")
    mods = [l.split("\t")[1] for l in out.splitlines() if l.startswith("MOD\t")]
    consts = [l.split("\t")[1:] for l in out.splitlines() if l.startswith("CONST\t")]
    kinds = collections.Counter(c[2] for c in consts)
    print("rc", r["rc"], "s", r["segundos"], "modulos", len(mods), "constantes", len(consts), dict(kinds))
    json.dump({"modulos": mods, "constantes": consts, "kinds": kinds, "rc": r["rc"], "log": r["log"], "log_sha256": r["log_sha256"]},
              open(os.path.join(KH, "enumeracao.json"), "w", encoding="utf-8"), ensure_ascii=False)


def blocos(N):
    E = json.load(open(os.path.join(KH, "enumeracao.json"), encoding="utf-8"))
    cnt = collections.Counter(c[0] for c in E["constantes"])
    mods = sorted(E["modulos"], key=lambda m: -cnt.get(m, 0))
    bl = [[] for _ in range(N)]
    peso = [0] * N
    for m in mods:
        i = min(range(N), key=lambda k: peso[k])
        bl[i].append(m)
        peso[i] += cnt.get(m, 0) + 1

    def gerar(i, b):
        L_ = ["-- KH-N1 D2 bloco %d/%d (exame F_KERNEL 12/10/2026, so sandbox): collectAxioms de TODAS as constantes destes modulos." % (i + 1, N)]
        L_ += ["import " + m for m in sorted(b)]
        L_ += ["", "open Lean Elab Command", "", "run_cmd do", "  let env ← getEnv",
               "  let alvoL : List Name := [" + ", ".join("`" + m for m in sorted(b)) + "]",
               "  let alvo : NameSet := alvoL.foldl (fun s n => s.insert n) {}",
               "  let mut n_decl := 0", "  let mut n_fora := 0",
               "  for (n, ci) in env.constants.map₁.toList do",
               "    match env.getModuleIdxFor? n with", "    | none => pure ()", "    | some idx =>",
               "      let m := env.header.moduleNames[idx.toNat]!",
               "      if alvo.contains m then",
               "        let axs ← liftCoreM (collectAxioms n)",
               "        let kind : String := match ci with",
               "          | .thmInfo _ => \"thm\" | .defnInfo _ => \"def\" | .axiomInfo _ => \"AXIOM\"",
               "          | .opaqueInfo _ => \"opaque\" | .quotInfo _ => \"quot\" | .inductInfo _ => \"induct\"",
               "          | .ctorInfo _ => \"ctor\" | .recInfo _ => \"rec\"",
               "        n_decl := n_decl + 1",
               "        let ok := axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound)",
               "        unless ok do n_fora := n_fora + 1",
               "        IO.println (\"COB\\t\" ++ m.toString ++ \"\\t\" ++ n.toString ++ \"\\t\" ++ kind ++ \"\\t\" ++ (if ok then \"TRIO\" else \"FORA\") ++ \"\\t\" ++ String.intercalate \",\" (axs.toList.map Name.toString))",
               "  IO.println (\"COB_TOTAL\\tdecl=\" ++ toString n_decl ++ \"\\tfora_do_trio=\" ++ toString n_fora)", ""]
        p = os.path.join(KH, "D2_bloco_%02d.lean" % (i + 1))
        if not os.path.exists(p):
            open(p, "w", encoding="utf-8", newline="\n").write("\n".join(L_))
        return p

    arqs = [gerar(i, b) for i, b in enumerate(bl)]

    def rodar(i):
        r = L.run_lean("D2_bloco_%02d" % (i + 1), arqs[i], KH, None, LOG, timeout=7200)
        out = open(r["log"], "rb").read().decode("utf-8", "replace")
        cob = [l for l in out.splitlines() if l.startswith("COB\t")]
        tot = [l for l in out.splitlines() if l.startswith("COB_TOTAL")]
        print("bloco", i + 1, "rc", r["rc"], "s", r["segundos"], "linhas", len(cob), tot, "esperado", peso[i] - len(bl[i]), flush=True)
        return {"bloco": i + 1, "rc": r["rc"], "s": r["segundos"], "log": r["log"], "log_sha256": r["log_sha256"], "fonte": arqs[i],
                "fonte_sha256": L.sha(arqs[i]), "n_cob": len(cob), "total": tot, "esperado": peso[i] - len(bl[i]), "erros": r["erros"][:5]}

    with ThreadPoolExecutor(max_workers=N) as ex:
        res = list(ex.map(rodar, range(N)))
    print(L.dump({"N": N, "blocos": res}, os.path.join(F, "RESULTADO_KH_D2.json")))


def aux(n):
    last = n.split(".")[-1]
    return bool(last.startswith("_") or re.fullmatch(r"eq_\d+|eq_def|injEq|inj|sizeOf_spec|ext_iff|proof_\d+|match_\d+|congr_simp|casesOn|recOn|noConfusion|noConfusionType|below|brecOn|binductionOn|ibelow|mk|rec|ext", last) or re.search(r"\._", n))


def merge():
    R = json.load(open(os.path.join(F, "RESULTADO_KH_D2.json"), encoding="utf-8"))
    E = json.load(open(os.path.join(KH, "enumeracao.json"), encoding="utf-8"))
    ax = {}
    mod_of = collections.defaultdict(set)
    dup = 0
    for b in R["blocos"]:
        for l in open(b["log"], encoding="utf-8"):
            if l.startswith("COB\t"):
                c = l.rstrip("\n").split("\t")
                m, n = c[1], c[2]
                a = [x for x in (c[5] if len(c) > 5 else "").split(",") if x]
                if n in ax:
                    dup += 1
                    assert set(ax[n]) == set(a), ("divergencia", n)
                ax[n] = a
                mod_of[n].add(m)
    enum_ = {c[1]: c for c in E["constantes"]}
    faltam = [n for n in enum_ if n not in ax]
    extras = [n for n in ax if n not in enum_]
    fora = [n for n, a in ax.items() if not set(a) <= TRIO]
    multi = sorted(n for n, s in mod_of.items() if len(s) > 1)
    dist = collections.Counter(",".join(sorted(a)) or "(nenhum)" for n, a in ax.items())
    raw = open(CORE, "rb").read()
    axr = json.loads(raw.decode("utf-8"))["core"]["kernel_formalization"]["axiom_report"]
    inter = [n for n in axr if n in ax]
    dif = [n for n in inter if set(axr[n]) != set(ax[n])]
    thm = [n for n, c in enum_.items() if c[2] == "thm"]
    m73 = [m["modulo"] for m in json.load(open(M73, encoding="utf-8"))["modulos"]]
    c73 = [n for n, c in enum_.items() if c[0] in set(m73)]
    dist73 = collections.Counter(",".join(sorted(ax[n])) or "(nenhum)" for n in c73 if enum_[n][2] == "thm")
    thm_user = [n for n in thm if not aux(n)]
    res = {"n": len(ax), "enumeradas": len(enum_), "faltam": faltam, "extras": extras, "fora_do_trio": fora, "distribuicao": dist,
           "duplicadas_entre_blocos": dup, "atribuidas_a_mais_de_um_modulo": multi, "axr_v391": len(axr), "em_ambos": len(inter),
           "divergentes": dif, "teoremas": len(thm), "teoremas_no_axr": sum(1 for n in thm if n in axr),
           "teoremas_de_usuario": len(thm_user), "teoremas_de_usuario_no_axr": sum(1 for n in thm_user if n in axr),
           "teoremas_so_sandbox": sorted(n for n in thm if n not in axr), "c73": len(c73),
           "c73_teoremas": sum(1 for n in c73 if enum_[n][2] == "thm"), "c73_fora": sum(1 for n in c73 if not set(ax[n]) <= TRIO),
           "dist73_teoremas": dist73, "core_sha256": hashlib.sha256(raw).hexdigest()}
    json.dump(res, open(os.path.join(KH, "D2_consolidado.json"), "w", encoding="utf-8"), ensure_ascii=False)
    print({k: v for k, v in res.items() if k not in ("teoremas_so_sandbox",)})


def final():
    E = json.load(open(os.path.join(KH, "enumeracao.json"), encoding="utf-8"))
    D = json.load(open(os.path.join(KH, "D2_consolidado.json"), encoding="utf-8"))
    raw = open(CORE, "rb").read()
    axr = json.loads(raw.decode("utf-8"))["core"]["kernel_formalization"]["axiom_report"]
    m73 = [m["modulo"] for m in json.load(open(M73, encoding="utf-8"))["modulos"]]
    por_mod = collections.defaultdict(list)
    for c in E["constantes"]:
        por_mod[c[0]].append(c)
    zero_any = sorted(m for m, cs in por_mod.items() if any(c[2] == "thm" for c in cs) and not any(c[1] in axr for c in cs))
    kinds = collections.Counter(c[2] for c in E["constantes"])
    cov = collections.Counter(c[2] for c in E["constantes"] if c[1] in axr)
    regex_nao_le = [c for c in E["constantes"] if not re.fullmatch(r"[\w.']+", c[1])]
    res = {"core_sha256": hashlib.sha256(raw).hexdigest(), "modulos_no_fecho": len(E["modulos"]), "constantes": len(E["constantes"]),
           "por_tipo": dict(kinds), "no_axiom_report_v391_por_tipo": dict(cov), "fora_do_axiom_report": len(E["constantes"]) - sum(cov.values()),
           "modulos_com_teorema_e_zero_entradas": zero_any, "n_zero": len(zero_any), "dos_73_em_zero": len(set(m73) & set(zero_any)),
           "zero_fora_dos_73": sorted(set(zero_any) - set(m73)), "dos_73_fora_de_zero": sorted(set(m73) - set(zero_any)),
           "sandbox_cobertas": D["n"], "sandbox_fora_do_trio": len(D["fora_do_trio"]), "distribuicao": D["distribuicao"],
           "nomes_que_a_regex_do_umpy_nao_le": regex_nao_le}
    for m in res["zero_fora_dos_73"]:
        res.setdefault("detalhe_zero_extra", {})[m] = dict(collections.Counter(c[2] for c in por_mod[m]))
    json.dump(res, open(os.path.join(KH, "KH_N1_final.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in res.items() if k != "modulos_com_teorema_e_zero_entradas"}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    fase = sys.argv[1]
    {"enum": enum, "merge": merge, "final": final}.get(fase, lambda: blocos(int(sys.argv[2])))()
