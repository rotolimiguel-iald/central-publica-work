# -*- coding: utf-8 -*-
"""comparar_verdade_v392.py -- compara os dois dumps do kernel (Meta_verdade_*.lean: tipo e valor de cada constante do modulo TGLExt.Verdade, em duas serializacoes
SA = De Bruijn sem nomes de binder, SN = com nomes) entre a Verdade ORIGINAL de 13/10 (sha 2b7639ba) e a CORRIGIDA (docstrings + renomeacao + a ponte). Mapa de nomes:
Verdade.dephased_det -> Verdade.identityProj_dephased_det. Saida: COMPARACAO_VERDADE_v392.json."""
import json, sys, hashlib
sys.stdout.reconfigure(encoding="utf-8")
MAP = [("Verdade.dephased_det", "Verdade.identityProj_dephased_det")]
def mp(s):
    for a, b in MAP: s = s.replace(a, b)
    return s
def carregar(p, mapear):
    d = {}
    for l in open(p, encoding="utf-8"):
        l = l.rstrip("\n")
        if not l or l.startswith("MODULO"): continue
        c = l.split("\t")
        tag, nome = c[0], c[1]
        if mapear: nome = mp(nome); c = [c[0], nome] + [mp(x) for x in c[2:]]
        d[(tag, nome)] = c[2:]
    return d
O = carregar(r"C:\t\k392\meta_verdade_old.txt", True); N = carregar(r"C:\t\k392\meta_verdade_new.txt", False)
nomes_o = {k[1] for k in O if k[0] == "DECL"}; nomes_n = {k[1] for k in N if k[0] == "DECL"}
removidas = sorted(nomes_o - nomes_n); novas = sorted(nomes_n - nomes_o); comuns = sorted(nomes_o & nomes_n)
res = {"constantes_antigas": len(nomes_o), "constantes_novas": len(nomes_n), "removidas": removidas, "novas": novas, "renomeacao_aplicada": MAP}
difs = {"TYPEA": [], "TYPEN": [], "VALA": [], "VALN": [], "DECL_exceto_doc": [], "DOC": []}
for n in comuns:
    for tag in ("TYPEA", "TYPEN", "VALA", "VALN"):
        if O[(tag, n)] != N[(tag, n)]: difs[tag].append(n)
    do, dn = O[("DECL", n)], N[("DECL", n)]
    if do[:-1] != dn[:-1]: difs["DECL_exceto_doc"].append(n)
    if do[-1] != dn[-1]: difs["DOC"].append(n)
res["diferencas"] = {k: v for k, v in difs.items()}
res["n_comuns"] = len(comuns)
res["veredito"] = ("TIPOS_E_TERMOS_IGUAIS_NOS_ENUNCIADOS_ANTIGOS" if not (difs["TYPEA"] or difs["VALA"] or difs["DECL_exceto_doc"] or removidas) else "HA_DIFERENCA")
res["so_nome_de_binder_SN"] = sorted(set(difs["TYPEN"]) | set(difs["VALN"]))
res["fonte_antiga_sha16"] = "2b7639bab440005a"; res["fonte_nova_sha16"] = hashlib.sha256(open(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v392\pedras_corrigidas\Verdade.lean","rb").read()).hexdigest()[:16]
json.dump(res, open(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v392\pedras_corrigidas\COMPARACAO_VERDADE_v392.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: (v if not isinstance(v, (list, dict)) else (len(v) if k!="novas" and k!="removidas" else v)) for k, v in res.items()}, ensure_ascii=False, indent=1))
print({k: v for k, v in difs.items()})
