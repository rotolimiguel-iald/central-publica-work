# -*- coding: utf-8 -*-
"""Nomes e Verdade, PARTE 1: tabela de invariancia lida do KERNEL. Para cada par (modulo antigo, modulo novo) compara, constante por
constante, o que Meta_*.lean gravou (tipo e valor em SA = De Bruijn sem nomes de binder, e SN = com nomes de binder; kind, lps,
hints, axiomas, hash da docstring). As cadeias do modulo ANTIGO passam pelo mapa de nomes (prefixo do modulo + renomeacoes
listadas); depois a comparacao e de CADEIAS INTEIRAS. Falha visivel (exit 1) se qualquer tipo ou termo diferir em SA.
Uso: comparar.py"""
import json, os, re, sys, hashlib, datetime

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = "C:/t/nm1/meta/"
TRIO = {"propext", "Classical.choice", "Quot.sound"}
PARES = [
    {"nome": "Posto", "velho": "rank_old", "novo": "posto_new",
     "pref": {"TGLExt.TheUnitIsTheRank": "TGLExt.Posto"},
     "ren": {"reading_weights_are_truth_and_cost": "rhoStar_and_Q0_traces_of_diag_one_sub_b_b",
             "inscription_at_thetaMiguel": "dephasing_acts_and_endpoint_entry_at_thetaMiguel"},
     "modulo_velho": "TGLExt.TheUnitIsTheRank", "modulo_novo": "TGLExt.Posto"},
    {"nome": "Santo", "velho": "time_old", "novo": "santo_new",
     "pref": {"TGLExt.TheTimeIsNotAPost": "TGLExt.Santo"},
     "ren": {"the_two_regimes_of_time": "isometry_dephasing_and_clock_conjunction",
             "the_face_lands": "dephase_tendsto_expectation_reexport",
             "face_clock_has_no_period": "decay_clock_has_no_period",
             "face_has_a_limit": "orbit_tendsto_center_reexport",
             "face_distinguishes_instants": "diagFlow_distinguishes_instants_reexport"},
     "modulo_velho": "TGLExt.TheTimeIsNotAPost", "modulo_novo": "TGLExt.Santo"},
    {"nome": "IALD", "velho": "iald_old", "novo": "iald_new",
     "pref": {"TGLExt.TheUnitIsTheRank": "TGLExt.Posto", "TGLExt.TheTimeIsNotAPost": "TGLExt.Santo"},
     "ren": {},
     "modulo_velho": "TGLExt.IALD", "modulo_novo": "TGLExt.IALD"},
]


def h(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def ler(p):
    d = {}
    ordem = []
    cab = None
    with open(p, encoding="utf-8") as fh:
        for ln in fh:
            ln = ln.rstrip("\n")
            if not ln:
                continue
            parts = ln.split("\t")
            tag = parts[0]
            if tag == "MODULO":
                cab = parts
                continue
            n = parts[1]
            if tag == "DECL":
                kind, internal, lps, extra, axs, doc = parts[2:8]
                d[n] = {"kind": kind, "internal": internal == "true", "lps": lps, "extra": extra,
                        "axiomas": [x for x in axs.split(",") if x], "doc_hash": doc}
                ordem.append(n)
            else:
                d[n][tag] = "\t".join(parts[2:])
    return cab, ordem, d


def mapa(s, par):
    for a, b in par["pref"].items():
        s = s.replace(a, b)
        # nomes de binder higienicos (so na leitura SN) carregam o modulo como componente de nome entre aspas
        s = s.replace('"' + a.split(".")[-1] + '"', '"' + b.split(".")[-1] + '"')
    for a, b in par["ren"].items():
        s = s.replace('"' + a + '"', '"' + b + '"')
    for a, b in par["ren"].items():
        s = re.sub(r"(?<![A-Za-z0-9_'])" + re.escape(a) + r"(?![A-Za-z0-9_'])", b, s)
    return s


saida = {"quando_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
         "metodo": ("Meta_*.lean le, no kernel do MESMO sandbox C:/t/nm1, cada constante do modulo (env.header.moduleData[idx].constNames): "
                    "tipo e valor serializados SA (De Bruijn, sem nomes de binder, mdata ignorado) e SN (com nome e info de cada binder e marca de mdata). "
                    "As cadeias do modulo antigo passam pelo mapa de nomes (prefixo do modulo e renomeacoes); a comparacao e de CADEIAS INTEIRAS "
                    "(sha256 so para leitura humana). Axiomas = Lean.collectAxioms de CADA constante do modulo."),
         "pares": {}}
falha_global = False
for par in PARES:
    c1, o1, d1 = ler(M + "meta_" + par["velho"] + ".txt")
    c2, o2, d2 = ler(M + "meta_" + par["novo"] + ".txt")
    linhas = []
    falhas = []
    nome_novo_de = {}
    for n in o1:
        nn = mapa(n, par)
        nome_novo_de[n] = nn
    so_novo = [n for n in d2 if n not in set(nome_novo_de.values())]
    for n in o1:
        nn = nome_novo_de[n]
        a = d1[n]
        b = d2.get(nn)
        reg = {"nome_antigo": n, "nome_novo": nn, "renomeada": n != nn and nn.split(".")[-1] != n.split(".")[-1]}
        if b is None:
            reg["ausente_no_novo"] = True
            falhas.append(n)
            linhas.append(reg)
            continue
        ok = True
        for campo in ("kind", "internal", "lps", "extra"):
            if mapa(str(a[campo]), par) != str(b[campo]):
                ok = False
                reg[campo + "_difere"] = [a[campo], b[campo]]
        reg["axiomas"] = b["axiomas"]
        reg["axiomas_no_trio"] = set(b["axiomas"]) <= TRIO
        reg["axiomas_iguais"] = a["axiomas"] == b["axiomas"]
        ok = ok and reg["axiomas_no_trio"] and reg["axiomas_iguais"]
        for campo in ("TYPEA", "VALA"):
            reg[campo + "_igual"] = mapa(a[campo], par) == b[campo]
            ok = ok and reg[campo + "_igual"]
        for campo in ("TYPEN", "VALN"):
            reg[campo + "_igual"] = mapa(a[campo], par) == b[campo]
        reg["so_nome_de_binder"] = (reg["TYPEA_igual"] and reg["VALA_igual"]) and not (reg["TYPEN_igual"] and reg["VALN_igual"])
        reg["docstring_mudou"] = a["doc_hash"] != b["doc_hash"]
        reg["IDENTICA_tipo_e_termo_SA"] = ok
        if not ok:
            falhas.append(n)
        linhas.append(reg)
    ren = [r for r in linhas if r.get("renomeada")]
    # categorias
    def cat(r):
        if r.get("ausente_no_novo"):
            return "AUSENTE"
        if r["nome_antigo"].endswith(tuple(".eq_%d" % i for i in range(1, 9))) or re.search(r"\.eq_\d+$", r["nome_antigo"]):
            return "lema_de_equacao"
        if "._" in r["nome_antigo"] or r["nome_antigo"].split(".")[-1].startswith("_"):
            return "interna"
        return "publica"
    cont = {}
    for r in linhas:
        k = cat(r)
        cont[k] = cont.get(k, 0) + 1
    saida["pares"][par["nome"]] = {
        "modulo_antigo": par["modulo_velho"], "modulo_novo": par["modulo_novo"],
        "meta_antigo": {"arquivo": M + "meta_" + par["velho"] + ".txt", "sha256": hashlib.sha256(open(M + "meta_" + par["velho"] + ".txt", "rb").read()).hexdigest(), "cabecalho": c1},
        "meta_novo": {"arquivo": M + "meta_" + par["novo"] + ".txt", "sha256": hashlib.sha256(open(M + "meta_" + par["novo"] + ".txt", "rb").read()).hexdigest(), "cabecalho": c2},
        "mapa_de_prefixos": par["pref"], "renomeacoes": par["ren"],
        "n_constantes_antigo": len(d1), "n_constantes_novo": len(d2), "mesma_ordem_no_modulo": [nome_novo_de[n] for n in o1] == o2,
        "mesmo_conjunto_de_nomes": sorted(nome_novo_de[n] for n in o1) == sorted(o2),
        "so_no_novo": so_novo,
        "contagem_por_categoria": cont,
        "n_identicas_tipo_e_termo_SA": sum(1 for r in linhas if r.get("IDENTICA_tipo_e_termo_SA")),
        "n_identicas_tipo_e_termo_SN": sum(1 for r in linhas if r.get("TYPEN_igual") and r.get("VALN_igual")),
        "n_so_nome_de_binder": sum(1 for r in linhas if r.get("so_nome_de_binder")),
        "so_nome_de_binder_em": [r["nome_antigo"] for r in linhas if r.get("so_nome_de_binder")],
        "n_docstring_mudou": sum(1 for r in linhas if r.get("docstring_mudou")),
        "docstring_mudou_em": [r["nome_novo"] for r in linhas if r.get("docstring_mudou")],
        "n_axiomas_fora_do_trio_novo": sum(1 for r in linhas if r.get("axiomas_no_trio") is False),
        "n_sem_axioma": sum(1 for r in linhas if r.get("axiomas") == []),
        "renomeadas": [[r["nome_antigo"], r["nome_novo"], r["IDENTICA_tipo_e_termo_SA"]] for r in ren],
        "falhas": falhas,
        "VEREDITO": "INVARIANTE" if not falhas and not so_novo and sorted(nome_novo_de[n] for n in o1) == sorted(o2) else "DIFERE",
        "constantes": linhas}
    if saida["pares"][par["nome"]]["VEREDITO"] != "INVARIANTE":
        falha_global = True
saida["VEREDITO_GERAL"] = "INVARIANTE_100_POR_CENTO" if not falha_global else "DIFERE"
dest = os.path.join(AQUI, "TABELA_INVARIANCIA.json")
json.dump(saida, open(dest, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
resumo = {k: {kk: vv for kk, vv in v.items() if kk not in ("constantes", "meta_antigo", "meta_novo", "renomeadas", "docstring_mudou_em", "so_nome_de_binder_em")}
          for k, v in saida["pares"].items()}
print(json.dumps(resumo, ensure_ascii=False, indent=1))
print("VEREDITO_GERAL", saida["VEREDITO_GERAL"])
sys.exit(0 if not falha_global else 1)
