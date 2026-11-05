# -*- coding: utf-8 -*-
"""Revisor terceiro v408 (R1): (1) roda as guardas (P18 + frases v408, as da cadeia) sobre TODOS os textos publicos: pysnips, delta/registros/runtime, pedras, textos rendidos do harness (C:/t/h408), artigo PT/EN do ensaio,
.md canonico do ensaio, rascunho da custodia, textos do handoff, template da ordem ao app; (2) controle negativo das guardas; (3) PROXIMIDADE: cada ocorrencia de «P = nP»/«P=nP» tem, num raio de 700 caracteres,
o qualificador do dicionario do operador E a ressalva [OPEN] da traducao (mais estrito que a guarda, que e' por texto); (4) varredura propria de frases proibidas do pedido, item 4; (5) as RESSALVAS_V408 inteiras nos textos rendidos."""
import glob, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8"); sys.dont_write_bytecode = True
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v408/"
sys.path.insert(0, R); sys.path.insert(0, R + "pos_rito")
import delta_v408 as DL
import guarda_p18_v408 as G18
import guarda_frases_v408 as GF
arqs = [R + f for f in ("artigo_pt_v408.pysnip", "artigo_en_v408.pysnip", "registros_v408.py", "runtime_v408.py", "delta_v408.py", "pos_rito/textos_v408_novo.pysnip", "pos_rito/textos_v408.py", "pos_rito/textos_custodia_handoff_v408.py",
                       "pos_rito/CUSTODIA_v408_RASCUNHO.txt", "orquestrador/ORDEM_RELEASE_APP_TEMPLATE.md", "DESENHO_v408.md", "RELATORIO_PREPARACAO_v408.md", "PLANO_v408.md",
                       "dry_v408/dry_v408_pt.txt", "dry_v408/dry_v408_en.txt", "dry_v408/um_absoluto_forma_canonica.md")]
arqs += sorted(glob.glob(R + "pedra/*.lean")) + sorted(glob.glob("C:/t/h408/harness_saida_v408/textos/*.txt"))
out = {"guardas": {}}; achados = 0
for a in arqs:
    if not os.path.exists(a): print("AUSENTE", a); continue
    t = open(a, encoding="utf-8", errors="replace").read()
    v1 = G18.violacoes(t); v2 = GF.violacoes(t)
    out["guardas"][os.path.relpath(a, R) if a.startswith(R) else a] = {"p18": [list(x) for x in v1[:6]], "frases": [list(x) for x in v2[:6]]}
    if v1 or v2:
        achados += 1; print("GUARDA ACHOU em", os.path.basename(a), "P18:", v1[:3], "| frases:", v2[:3])
print("arquivos varridos:", len(arqs), "| com achado:", achados)
ped = GF.pedras(); print("pedras():", {k: (len(v["violacoes"]), v["falas_retiradas"], v["apontadas"]) for k, v in ped.items()})
out["pedras"] = ped
cn = GF.controle_negativo(); print("controle_negativo():", cn["ok"] if isinstance(cn, dict) else cn)
# pedras CRUAS pela guarda do runtime (sem retirar falas): o que ela diz
import runtime_v408 as RT
for p in DL.PEDRAS_V408:
    t = open(p["src"], encoding="utf-8").read(); v = RT._v408_guarda_frases(t)
    if v: print("pedra (cru, sem retirar falas):", p["name"], [(x[0], x[1][:90]) for x in v[:5]])
# (3) proximidade de «P = nP»
rx = re.compile(r"P\s*=\s*nP|P=nP")
prox_falhas = []; n_occ = 0
textos = [a for a in arqs if os.path.exists(a) and not a.endswith(".lean") or a.endswith(".lean")]
for a in textos:
    if not os.path.exists(a): continue
    t = open(a, encoding="utf-8", errors="replace").read()
    for mm in rx.finditer(t):
        n_occ += 1
        jan = t[max(0, mm.start() - 700):mm.end() + 700]
        q = re.search(r"dicion(?:á|a)rio|dictionary", jan, re.I); o = re.search(r"\[OPEN\]", jan)
        if not (q and o): prox_falhas.append((os.path.relpath(a, R) if a.startswith(R) else os.path.basename(a), t.count("\n", 0, mm.start()) + 1, bool(q), bool(o), jan[600:800].replace("\n", " ")))
print("ocorrencias de P = nP:", n_occ, "| sem qualificador ou sem [OPEN] a 700 chars:", len(prox_falhas))
for x in prox_falhas[:25]: print("   ", x)
out["p_igual_np_ocorrencias"] = n_occ; out["p_igual_np_sem_proximidade"] = [list(map(str, x)) for x in prox_falhas[:60]]
# (4) varredura propria do item 4 do pedido
PAD = {"a TGL prova/decide P = NP de Turing": r"(?:TGL|kernel|um\.py|IALD)\s+(?:prova|provou|decide|decidiu|proves|decides)\s+(?:que\s+)?P\s*=\s*NP",
       "P = NP esta provado (sem do dicionario)": r"P\s*=\s*NP\s+(?:est(?:á|a)\s+provad|é\s+teorema|is\s+(?:proved|a\s+theorem))",
       "nao trata das classes": r"n(?:ã|a)o\s+trata\s+(?:d[ae]s?\s+)?classes",
       "relacao sem peso como existente": r"(?:h(?:á|a)|existe)\s+rela(?:ç|c)(?:ã|a)o\s+sem\s+peso",
       "a TGL nao tem terminal": r"TGL\s+n(?:ã|a)o\s+tem\s+terminal",
       "impedancia como termo": r"imped(?:â|a)ncia\s+(?:é|e)\s+(?:um\s+)?termo",
       "CONFIRMED / PROVED_BY": r"CONF" + r"IRMED|PRO" + r"VED_BY",
       "tudo derivado / nenhuma hipotese resta": r"tudo\s+derivado|nenhuma\s+hip(?:ó|o)tese\s+resta",
       "pos-dicao": r"p(?:ó|o)s-?\s?di(?:ç|c)(?:ã|a)o|post-?diction"}
tot = {}
for a in arqs:
    if not os.path.exists(a) or a.endswith(".lean") and False: continue
    t = open(a, encoding="utf-8", errors="replace").read()
    for nome, pat in PAD.items():
        for mm in re.finditer(pat, t, re.I):
            tot.setdefault(nome, []).append((os.path.relpath(a, R) if a.startswith(R) else os.path.basename(a), t.count("\n", 0, mm.start()) + 1, t[max(0, mm.start() - 70):mm.end() + 70].replace("\n", " ")))
for nome, l in tot.items():
    print("VARREDURA PROPRIA:", nome, "->", len(l))
    for x in l[:6]: print("     ", x)
out["varredura_propria"] = {k: [list(map(str, x)) for x in v[:15]] for k, v in tot.items()}
json.dump(out, open(R + "revisao_terceiro/h_guardas_out.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
