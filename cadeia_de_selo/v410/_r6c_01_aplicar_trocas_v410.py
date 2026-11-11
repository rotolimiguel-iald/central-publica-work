# -*- coding: utf-8 -*-
"""_r6c_01_aplicar_trocas_v410.py -- o CONSERTO UNICO da v410 (ordem da gerencia de 10/11/2026; D106 a D123), passos 0 e 1: aplica POR SCRIPT, sem interpretar, as trocas exatas da ESPEC_CONSERTO_R3_v2_FINAL.json
(sha256 conferido), no fim de linha de cada arquivo (no arquivo misto, o da linha tocada). Antes: confere os bytes de partida (delta e candidato) e tira o retrato (sha256) da pasta; backup de BYTES de cada arquivo tocado
(<arquivo>.bak_<TS>_r6c). Depois: cada trecho novo contado, cada trecho atual contado, ast.parse dos .py e dos .pysnip, comparacao LETRA A LETRA com o aplicado em memoria pelo conferidor do cetico (_cetico\\_aplicado.json),
e o retrato de novo (so' os arquivos da ESPEC mudaram). Escreve por temporario + os.replace. NAO roda duas vezes: se o delta ja' nao tem o sha16 de partida, recusa.   uso: python -I -B -X utf8 _r6c_01_aplicar_trocas_v410.py [--seco]"""
import ast, hashlib, json, os, re, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); TS = time.strftime("%Y%m%d_%H%M%S"); SECO = "--seco" in sys.argv
ESPEC = os.path.join(HERE, "conserto_r3", "ESPEC_CONSERTO_R3_v2_FINAL.json"); ESPEC_SHA = "8ecf4082e657bd69887c52e0e7d8efbcdbfc85eb4d739679227c9b11f5c23f19"   # (o sha256 da ESPEC e' o da ORDEM da gerencia e o do ADENDO 7; conferido abaixo contra o arquivo E contra o adendo)
CETICO = os.path.join(os.environ.get("TEMP", ""), "claude", "b4ca26c934d2167f", "6da8f00d-d44f-4888-a88d-fc9f73eead3d", "scratchpad", "conserto_r3", "v2", "_cetico", "_aplicado.json")
sha = lambda b: hashlib.sha256(b).hexdigest()
rd = lambda p: open(p, "rb").read()
P = lambda rel: os.path.join(HERE, *rel.split("/"))
assert sha(rd(ESPEC)) == ESPEC_SHA, "a ESPEC em disco nao tem o sha256 da ordem"
AD7 = rd(P("DESENHO_v410_ADENDO_7_POS_CANDIDATO_10nov.md")).decode("utf-8"); assert ESPEC_SHA in AD7, "o ADENDO 7 nao traz o sha256 da ESPEC"
D = json.loads(rd(ESPEC).decode("utf-8")); ITS = D["itens"]
assert sha(rd(P("delta_v410.py")))[:16] == D["base"]["delta_v410_de_hoje_sha16"] == "8dc927fc07320460", "o delta nao esta' nos bytes de partida (a aplicacao nao roda duas vezes)"
assert sha(rd(P("um_v410_candidato.py")))[:16] == D["candidato_revisado_sha16"] == "8a713e5e644af09b", "o candidato nao e' o revisado"
TROCAS = [i for i in ITS if i["tipo"] == "TROCA_EXATA"]; INSTR = [i for i in ITS if i["tipo"] == "INSTRUCAO"]
assert len(TROCAS) == D["n_trocas_exatas"] == 290 and len(INSTR) == D["n_instrucoes"] == 8 and len(ITS) == D["n_itens"] == 298
ARQS = sorted({i["arquivo_rel"] for i in TROCAS}); assert len(ARQS) == 23, len(ARQS)
assert all(os.path.normcase(os.path.abspath(i["arquivo"])) == os.path.normcase(os.path.abspath(P(i["arquivo_rel"]))) for i in TROCAS), "arquivo e arquivo_rel divergem"


def retrato():
    out = {}
    for sub in ("", "pos_rito", "insumos", "pedra", "pedra/origem", "kernel", "revisao_terceiro", "conserto_r3"):
        d = P(sub) if sub else HERE
        if not os.path.isdir(d):
            continue
        for n in os.listdir(d):
            f = os.path.join(d, n)
            if os.path.isfile(f):
                out[(sub + "/" if sub else "") + n] = sha(rd(f))
    return out


R0 = retrato()
aplicado_cetico = json.load(open(CETICO, encoding="utf-8")) if os.path.exists(CETICO) else None
res = {"contrato": "R6c_TROCAS_v410", "quando": time.strftime("%d/%m/%Y %H:%M:%S"), "espec_sha256": ESPEC_SHA, "seco": SECO, "arquivos": {}, "itens": {}, "problemas": []}
novos_bytes = {}
for rel in ARQS:
    b0 = rd(P(rel)); raw = b0.decode("utf-8"); lf = raw.replace("\r\n", "\n"); assert "\r" not in lf, ("CR solto", rel)
    n_crlf = raw.count("\r\n"); n_lf = raw.count("\n"); eol_arq = "CRLF" if (n_crlf == n_lf and n_lf) else ("LF" if n_crlf == 0 else "MISTO")
    spans = []
    for it in [i for i in TROCAS if i["arquivo_rel"] == rel]:
        a = it["trecho_atual"]; nv = it["trecho_novo"]; k = it["ocorrencias"]
        assert "\r" not in a and "\r" not in nv and a != nv and k >= 1, ("item malformado", it["n"])
        assert lf.count(a) == k, ("contagem do trecho atual", it["n"], lf.count(a), k)
        rx = re.compile(r"\r?\n".join(re.escape(x) for x in a.split("\n")))
        ms = list(rx.finditer(raw)); assert len(ms) == k, ("ocorrencias no texto cru", it["n"], len(ms), k)
        for m in ms:
            g = m.group(0)
            if "\r\n" in g:
                eol = "\r\n"; assert g.count("\r\n") == g.count("\n"), ("fim de linha misto DENTRO do trecho", it["n"])
            elif "\n" in g:
                eol = "\n"
            else:   # o trecho atual cabe numa linha: vale o fim de linha da LINHA TOCADA (a que contem o trecho)
                q = raw.find("\n", m.end())
                if q < 0:
                    q = raw.rfind("\n", 0, m.start())
                eol = "\r\n" if (q > 0 and raw[q - 1] == "\r") else "\n"
            spans.append((m.start(), m.end(), nv.replace("\n", eol), it["n"]))
    spans.sort()
    for x, y in zip(spans, spans[1:]):
        assert y[0] >= x[1], ("sobreposicao", rel, x[3], y[3])
    t = raw
    for s0, s1, nv_raw, n_ in sorted(spans, reverse=True):
        t = t[:s0] + nv_raw + t[s1:]
    t_lf = t.replace("\r\n", "\n"); assert "\r" not in t_lf, ("CR solto depois de aplicar", rel)
    n_crlf1 = t.count("\r\n"); n_lf1 = t.count("\n"); eol_dep = "CRLF" if (n_crlf1 == n_lf1 and n_lf1) else ("LF" if n_crlf1 == 0 else "MISTO")
    assert eol_dep == eol_arq, ("o fim de linha do arquivo mudou", rel, eol_arq, eol_dep)
    if eol_arq == "MISTO":   # as linhas LF de antes continuam sendo exatamente as que ja' eram LF: nenhuma linha CRLF virou LF nem o contrario fora dos trechos tocados (o numero de linhas LF so' pode mudar por trecho novo posto numa linha LF)
        res["arquivos"].setdefault(rel, {})["linhas_LF_antes_depois"] = [n_lf - n_crlf, n_lf1 - n_crlf1]
    try:
        if rel.endswith(".py"):
            ast.parse(t_lf)
        elif rel.endswith(".pysnip"):
            try:
                ast.parse(t_lf)
            except SyntaxError:
                ast.parse("if True:\n" + t_lf)
    except SyntaxError as e:
        res["problemas"].append(["sintaxe", rel, str(e)])
    if aplicado_cetico is not None:
        if aplicado_cetico.get(rel) != t_lf:
            res["problemas"].append(["difere do aplicado em memoria pelo cetico", rel])
    for it in [i for i in TROCAS if i["arquivo_rel"] == rel]:
        cn = t_lf.count(it["trecho_novo"]); ca = t_lf.count(it["trecho_atual"]); contem = it["trecho_atual"] in it["trecho_novo"]
        res["itens"][str(it["n"])] = {"arquivo": rel, "ocorrencias": it["ocorrencias"], "novo_no_arquivo": cn, "atual_no_arquivo": ca, "novo_contem_o_atual": contem}
        if cn < it["ocorrencias"]:
            res["problemas"].append(["trecho novo ausente ou a menos", it["n"], cn, it["ocorrencias"]])
    novos_bytes[rel] = (b0, t.encode("utf-8"))
    res["arquivos"].setdefault(rel, {}).update({"fim_de_linha": eol_arq, "n_trocas": sum(i["ocorrencias"] for i in TROCAS if i["arquivo_rel"] == rel), "n_itens": sum(1 for i in TROCAS if i["arquivo_rel"] == rel), "sha16_antes": sha(b0)[:16], "sha16_depois": sha(t.encode("utf-8"))[:16], "bytes_antes": len(b0), "bytes_depois": len(t.encode("utf-8"))})
res["n_itens_aplicados"] = len(res["itens"]); res["n_trocas_aplicadas"] = sum(v["n_trocas"] for v in res["arquivos"].values()); res["comparado_com_o_cetico"] = aplicado_cetico is not None
res["novo_mais_vezes_que_o_item"] = {n: v for n, v in res["itens"].items() if v["novo_no_arquivo"] != v["ocorrencias"]}
res["atual_que_ficou"] = {n: v for n, v in res["itens"].items() if v["atual_no_arquivo"] and not v["novo_contem_o_atual"]}
assert not res["problemas"], res["problemas"]
if not SECO:
    for rel, (b0, b1) in novos_bytes.items():
        p = P(rel); bak = p + ".bak_" + TS + "_r6c"; assert not os.path.exists(bak)
        open(bak, "wb").write(b0); assert rd(bak) == b0
        tmp = p + ".tmp_r6c"; open(tmp, "wb").write(b1); assert os.path.getsize(tmp) == len(b1) > 0; os.replace(tmp, p); assert rd(p) == b1
        res["arquivos"][rel]["backup"] = os.path.basename(bak)
    R1 = retrato()
    mud = sorted(k for k in R0 if R1.get(k) != R0[k]); nov = sorted(k for k in R1 if k not in R0)
    res["mudaram_de_sha256"] = mud; res["arquivos_novos"] = nov
    assert mud == ARQS, ("mudou arquivo fora da ESPEC, ou faltou mudar algum", sorted(set(mud) ^ set(ARQS)))
    assert all(".bak_" + TS + "_r6c" in n for n in nov), ("arquivo novo que nao e' backup", nov)
    out = P("_r6c_TROCAS_v410.json"); tmp = out + ".tmp"; open(tmp, "w", encoding="utf-8", newline="\n").write(json.dumps(res, ensure_ascii=False, indent=1)); os.replace(tmp, out)
print("ESPEC", ESPEC_SHA[:16], "| itens de troca:", res["n_itens_aplicados"], "| trocas (com as repetidas):", res["n_trocas_aplicadas"], "| arquivos:", len(res["arquivos"]), "| comparado letra a letra com o aplicado do cetico:", res["comparado_com_o_cetico"], "| problemas:", res["problemas"], "| seco:", SECO)
print("trecho novo com contagem diferente da do item:", {n: (v["novo_no_arquivo"], v["ocorrencias"]) for n, v in res["novo_mais_vezes_que_o_item"].items()})
print("trecho atual que ficou (sem o novo conte-lo):", {n: v["atual_no_arquivo"] for n, v in res["atual_que_ficou"].items()})
for rel, v in sorted(res["arquivos"].items()):
    print(" ", rel, v["fim_de_linha"], v["n_itens"], "itens", v["sha16_antes"], "->", v["sha16_depois"], v.get("linhas_LF_antes_depois", ""))
