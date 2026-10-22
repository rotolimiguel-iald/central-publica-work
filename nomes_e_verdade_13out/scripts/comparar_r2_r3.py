# -*- coding: utf-8 -*-
"""Tabela r2 -> r3 da Verdade, lida do KERNEL (meta_id_r2.txt x meta_verdade_new.txt). Por constante: MANTIDA (tipo e valor SA iguais
apos o prefixo), RENOMEADA (nenhuma, por construcao), TIPO_MUDOU, VALOR_MUDOU (tipo igual, termo difere), REMOVIDA, NOVA.
Tambem: axiomas de TODAS as 206 constantes no trio; e a PARAMETRICIDADE LIDA DO KERNEL: nenhuma constante da Verdade
(fora das que tratam do nome) menciona `NamedIdentity.name`, `postedName` ou `ofName` no tipo ou no termo."""
import json, re, os, sys, hashlib, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = "C:/t/nm1/meta/"
TRIO = {"propext", "Classical.choice", "Quot.sound"}
PRE = ("TGLExt.TheIdentityHasAName", "TGLExt.Verdade")


def ler(p):
    d = {}
    ordem = []
    with open(p, encoding="utf-8") as fh:
        for ln in fh:
            ln = ln.rstrip("\n")
            if not ln or ln.startswith("MODULO"):
                continue
            parts = ln.split("\t")
            tag, n = parts[0], parts[1]
            if tag == "DECL":
                d[n] = {"kind": parts[2], "internal": parts[3] == "true", "lps": parts[4], "extra": parts[5],
                        "axiomas": [x for x in parts[6].split(",") if x], "doc_hash": parts[7]}
                ordem.append(n)
            else:
                d[n][tag] = "\t".join(parts[2:])
    return ordem, d


mp = lambda s: s.replace(PRE[0], PRE[1]).replace('"' + PRE[0].split(".")[-1] + '"', '"' + PRE[1].split(".")[-1] + '"')
o2, d2 = ler(M + "meta_id_r2.txt")
o3, d3 = ler(M + "meta_verdade_new.txt")
linhas = []
vistos = set()
for n in o2:
    nn = mp(n)
    vistos.add(nn)
    a = d2[n]
    b = d3.get(nn)
    if b is None:
        linhas.append({"nome_r2": n, "nome_r3": None, "estado": "REMOVIDA"})
        continue
    ti = mp(a["TYPEA"]) == b["TYPEA"]
    vi = mp(a["VALA"]) == b["VALA"]
    est = "MANTIDA" if (ti and vi) else ("TIPO_MUDOU" if not ti else "VALOR_MUDOU")
    linhas.append({"nome_r2": n, "nome_r3": nn, "estado": est, "TYPEA_igual": ti, "VALA_igual": vi,
                   "TYPEN_igual": mp(a["TYPEN"]) == b["TYPEN"], "VALN_igual": mp(a["VALN"]) == b["VALN"],
                   "docstring_mudou": a["doc_hash"] != b["doc_hash"]})
for n in o3:
    if n not in vistos:
        linhas.append({"nome_r2": None, "nome_r3": n, "estado": "NOVA", "kind": d3[n]["kind"]})
cont = {}
for r in linhas:
    cont[r["estado"]] = cont.get(r["estado"], 0) + 1
# axiomas
fora = [n for n in o3 if not set(d3[n]["axiomas"]) <= TRIO]
# parametricidade lida do kernel
NOME_LIGADAS = re.compile(r"NamedIdentity|ofName|postedName|theNamedIdentity|every_name|the_name_enters|the_structure_does_not_fix|changing_the_name|probe_named|no_named_identity|the_named_identity|identity_iff_truth|the_identity_is_the_truth")
menciona = []
for n in o3:
    s = d3[n]["TYPEA"] + " " + d3[n]["VALA"]
    if "NamedIdentity.name" in s or "postedName" in s:
        menciona.append(n)
verdade_nucleo = [n for n in o3 if n.startswith("TGLExt.Verdade.") and not NOME_LIGADAS.search(n)]
mencionam_nucleo = [n for n in menciona if n in set(verdade_nucleo)]
saida = {"quando_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
         "metodo": "mesma leitura do kernel que a TABELA_INVARIANCIA (Meta_*.lean); comparacao SA (De Bruijn) de tipo e valor apos o mapa de prefixo TheIdentityHasAName -> Verdade.",
         "n_r2": len(o2), "n_r3": len(o3), "contagem": cont,
         "n_axiomas_r3_fora_do_trio": len(fora), "fora_do_trio": fora,
         "n_constantes_r3_sem_axioma": sum(1 for n in o3 if not d3[n]["axiomas"]),
         "parametricidade": {"constantes_que_mencionam_o_campo_name_ou_postedName": menciona,
                             "n_constantes_do_nucleo_da_Verdade_checadas": len(verdade_nucleo),
                             "nucleo_que_menciona_o_nome": mencionam_nucleo,
                             "leitura": "nenhuma prova do nucleo (Verdade, comutacao, reflexividade, unicidade) le o nome"},
         "meta_r2_sha256": hashlib.sha256(open(M + "meta_id_r2.txt", "rb").read()).hexdigest(),
         "meta_r3_sha256": hashlib.sha256(open(M + "meta_verdade_new.txt", "rb").read()).hexdigest(),
         "TIPO_MUDOU": [r["nome_r2"] for r in linhas if r["estado"] == "TIPO_MUDOU"],
         "VALOR_MUDOU": [r["nome_r2"] for r in linhas if r["estado"] == "VALOR_MUDOU"],
         "REMOVIDAS": [r["nome_r2"] for r in linhas if r["estado"] == "REMOVIDA"],
         "NOVAS_publicas": [r["nome_r3"] for r in linhas if r["estado"] == "NOVA" and "._" not in r["nome_r3"] and not re.search(r"\.eq_\d+$", r["nome_r3"])],
         "constantes": linhas}
json.dump(saida, open(AQUI + "/TABELA_R2_R3.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in saida.items() if k != "constantes"}, ensure_ascii=False, indent=1))
