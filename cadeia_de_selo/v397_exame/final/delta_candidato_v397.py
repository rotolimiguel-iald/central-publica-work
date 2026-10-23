# -*- coding: utf-8 -*-
"""delta_candidato_v397.py -- exame final v397 (c1, 23/10/2026): o DELTA entre o candidato examinado (A = 0ac860f4...) e o candidato regerado (B) depois da correcao das
citacoes: (1) por AST, quais nos mudaram e se SO' mudaram constantes de TEXTO (nenhum numero, nenhuma funcao); (2) o kernel embutido, as bandeiras, a escada e os pinos (h8 de
kh_n1_cobertura_v397, sha da pedra) IGUAIS; (3) os textos mudados, linha a linha; (4) ESPERADOS_v397.json: so' candidato_sha16/bytes/ensaio e os vereditos dos registros
que carregam texto podem mudar; os numeros do quadro iguais. So le. uso: python -I -B -X utf8 delta_candidato_v397.py <A.py> <B.py> <saida.json>"""
import ast, json, sys, hashlib, difflib, os
A_, B_, S_ = sys.argv[1:4]
sa, sb = open(A_, "rb").read().decode("utf-8"), open(B_, "rb").read().decode("utf-8")
TA, TB = ast.parse(sa), ast.parse(sb)
def top(T):
    d = {}
    for n in T.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name): d[n.targets[0].id] = n
        elif isinstance(n, (ast.FunctionDef, ast.ClassDef)): d[n.name] = n
    return d
dA, dB = top(TA), top(TB)
R = {"A_sha16": hashlib.sha256(sa.encode("utf-8")).hexdigest()[:16], "B_sha16": hashlib.sha256(sb.encode("utf-8")).hexdigest()[:16], "A_bytes": len(sa.encode("utf-8")), "B_bytes": len(sb.encode("utf-8"))}
mud = sorted(k for k in dA if k in dB and ast.dump(dA[k]) != ast.dump(dB[k]))
R["nos_mudados"] = mud; R["nos_novos"] = sorted(set(dB) - set(dA)); R["nos_removidos"] = sorted(set(dA) - set(dB))
def consts(n):
    s, num = [], []
    for x in ast.walk(n):
        if isinstance(x, ast.Constant):
            (s if isinstance(x.value, str) else num if isinstance(x.value, (int, float)) and not isinstance(x.value, bool) else []).append(x.value)
    return s, num
R["detalhe"] = {}
for k in mud:
    sA, nA = consts(dA[k]); sB, nB = consts(dB[k])
    strip = lambda n: ast.dump(ast.parse(ast.unparse(n))).replace("Constant(value='", "C(").replace('Constant(value="', "C(")
    import re
    # estrutura sem o conteudo das strings
    skel = lambda n: re.sub(r"Constant\(value='(?:[^'\\]|\\.)*'\)", "STR", re.sub(r'Constant\(value="(?:[^"\\]|\\.)*"\)', "STR", ast.dump(n)))
    R["detalhe"][k] = {"so_texto_mudou": skel(dA[k]) == skel(dB[k]) and sorted(map(repr, nA)) == sorted(map(repr, nB)), "numeros_iguais": sorted(map(repr, nA)) == sorted(map(repr, nB)),
                       "strings_so_A": [x[:300] for x in sA if x not in sB][:12], "strings_so_B": [x[:300] for x in sB if x not in sA][:12]}
# o que NAO pode mudar
lit = lambda d, k: ast.literal_eval(d[k].value)
R["kernel_embutido_igual"] = lit(dA, "_EMBEDDED_KERNEL_FILES") == lit(dB, "_EMBEDDED_KERNEL_FILES")
R["bandeiras_iguais"] = lit(dA, "_LEAN_THEOREM_FLAGS") == lit(dB, "_LEAN_THEOREM_FLAGS")
R["esqueleto_igual"] = lit(dA, "_ESQUELETO_STONES") == lit(dB, "_ESQUELETO_STONES")
for c in ("_V394_FORMAL_CONTRACT", "_V394_QUADRATIC_CONTRACT", "_V394_NETWORK_CONTRACT", "_V395_PSIBIT_CONTRACT", "_V396_TESTEMUNHA_CONTRACT", "_V397_FONTES", "_V397_VERBATINS2", "_V396_SPECS", "_V397_CHAVES_NUM", "_V397_FRASE_444"):
    if c in dA and c in dB:
        R["igual_" + c] = lit(dA, c) == lit(dB, c)
# as falas embutidas: as antigas iguais; cada fala NOVA = os bytes do arquivo do operador (sha256 do texto == sha256 declarado == sha256 do arquivo; trechos sao substrings)
def det_dict(c):
    if c not in dA or c not in dB:
        return {"ausente_em": [x for x, d in (("A", dA), ("B", dB)) if c not in d]}
    xa, xb = lit(dA, c), lit(dB, c)
    o = {"so_A": sorted(set(xa) - set(xb)), "so_B": sorted(set(xb) - set(xa)), "mudadas": sorted(k for k in set(xa) & set(xb) if xa[k] != xb[k]), "novas": {}}
    for k in o["so_B"]:
        e = xb[k]; t = e.get("text"); arq = e.get("arquivo"); sh = e.get("sha256")
        r = {"sha256_declarado16": (sh or "")[:16]}
        if t is not None:
            r["sha256_do_texto_igual"] = hashlib.sha256(t.encode("utf-8")).hexdigest() == sh
            r["trechos_substrings"] = all(x in t for x in e.get("trechos", [])) if e.get("trechos") else None
            r["texto"] = t[:200]
        if arq and os.path.exists(arq):
            fb = open(arq, "rb").read(); r["arquivo_sha256_igual"] = hashlib.sha256(fb).hexdigest() == sh
            if t is not None:
                r["texto_igual_aos_bytes_do_arquivo"] = fb.decode("utf-8") == t
        else:
            r["arquivo_existe"] = False
        r["chaves"] = sorted(e.keys()); o["novas"][k] = r
    return o
R["inscricoes_V397_VERBATINS2"] = det_dict("_V397_VERBATINS2")
R["fontes_V397_FONTES"] = {k: v for k, v in det_dict("_V397_FONTES").items() if k != "novas"}
# o spec de veracidade: so' os textos (limites/diz/nao_diz/leituras/extras) podem mudar; checks e fontes iguais
vA, vB = lit(dA, "_V397_VERACIDADE_SPEC"), lit(dB, "_V397_VERACIDADE_SPEC")
R["veracidade_spec"] = {"checks_iguais": vA["checks"] == vB["checks"], "fontes_iguais": vA["fontes"] == vB["fontes"], "verbatins_iguais": vA["verbatins"] == vB["verbatins"], "veredito_igual": (vA["veredito_prefixo"], vA["veredito_sufixo"]) == (vB["veredito_prefixo"], vB["veredito_sufixo"]),
                        "chaves_de_texto_mudadas": sorted(k for k in set(vA) | set(vB) if vA.get(k) != vB.get(k))}
pA = {s["nome"]: s for s in lit(dA, "_V397_SPECS")}; pB = {s["nome"]: s for s in lit(dB, "_V397_SPECS")}
R["specs_v397"] = {n: {"checks_iguais": pA[n]["checks"] == pB[n]["checks"], "chaves_mudadas": sorted(k for k in set(pA[n]) | set(pB[n]) if pA[n].get(k) != pB[n].get(k))} for n in pA if n in pB}
def dchecks(ca, cb):
    ia = {c.get("id"): c for c in ca}; ib = {c.get("id"): c for c in cb}
    return {"ids_so_A": sorted(set(ia) - set(ib), key=str), "ids_so_B": sorted(set(ib) - set(ia), key=str), "ids_mudados": sorted((k for k in set(ia) & set(ib) if ia[k] != ib[k]), key=str),
            "novos": [ib[k] for k in sorted(set(ib) - set(ia), key=str)][:8], "mudados_detalhe": [{"id": k, "A": ia[k], "B": ib[k]} for k in sorted((k for k in set(ia) & set(ib) if ia[k] != ib[k]), key=str)][:8]}
R["veracidade_checks_delta"] = dchecks(vA["checks"], vB["checks"])
R["specs_checks_delta"] = {n: dchecks(pA[n]["checks"], pB[n]["checks"]) for n in pA if n in pB and pA[n]["checks"] != pB[n]["checks"]}
R["veracidade_verbatins_lista"] = {"A": vA.get("verbatins"), "B": vB.get("verbatins")}
R["specs_verbatins_lista"] = {n: {"A": pA[n].get("verbatins"), "B": pB[n].get("verbatins")} for n in pA if n in pB and pA[n].get("verbatins") != pB[n].get("verbatins")}
pin = lambda P: next((c["valor"] for c in P["kh_n1_cobertura_v397"]["checks"] if c.get("caminho") == ["formal_files_sha256"]), None)
R["h8_pino_igual"] = pin(pA) == pin(pB); R["h8_n"] = len(pin(pB) or {})
# linhas do diff fora do kernel embutido
emb = dB["_EMBEDDED_KERNEL_FILES"]; la, lb = sa.splitlines(), sb.splitlines()
sm = difflib.SequenceMatcher(None, la, lb, autojunk=False); dl = []
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag != "equal":
        dl.append({"tag": tag, "A": [l[:260] for l in la[i1:i2]][:6], "B": [l[:260] for l in lb[j1:j2]][:6], "linhas_B": [j1 + 1, j2]})
R["diff_linhas"] = dl[:40]; R["n_blocos_diff"] = len(dl)
# ESPERADOS
V = os.path.dirname(B_)
try:
    EA = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ESPERADOS_v397_candidato_A.json"), encoding="utf-8")); EB = json.load(open(os.path.join(V, "ESPERADOS_v397.json"), encoding="utf-8"))
    J = lambda x: json.dumps(x, sort_keys=True, ensure_ascii=False)
    R["esperados"] = {"chaves_mudadas": sorted(k for k in set(EA) | set(EB) if J(EA.get(k)) != J(EB.get(k))), "quadro_igual": J(EA.get("quadro")) == J(EB.get("quadro")), "veracidade_igual": J(EA.get("veracidade")) == J(EB.get("veracidade")),
                      "h8_entradas": EB.get("h8_entradas"), "escada": EB.get("escada"), "pedras_sha256_igual": J(EA.get("pedras_sha256")) == J(EB.get("pedras_sha256")), "qg_closure_igual": EA.get("qg_closure_verdict") == EB.get("qg_closure_verdict")}
except Exception as e:
    R["esperados"] = {"erro": repr(e)[:200]}
json.dump(R, open(S_, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in R.items() if k != "diff_linhas"}, ensure_ascii=False, indent=1)[:12000])
print("DIFF (fora do kernel):", json.dumps(R["diff_linhas"], ensure_ascii=False, indent=1)[:9000])
