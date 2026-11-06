# -*- coding: utf-8 -*-
"""Revisor terceiro v409 (R1): (1) roda as guardas (P18 + frases v409, as da cadeia) sobre TODOS os textos publicos: pysnips, delta/registros/runtime, pedras, textos rendidos do harness (C:/t/h409), artigo PT/EN do ensaio,
.md canonico do ensaio, rascunho da custodia, textos do handoff; (2) controle negativo das guardas; (3) PROXIMIDADE: cada ocorrencia de «P = nP»/«P=nP» tem, num raio de 700 caracteres, o qualificador «relativ(a|o) ao leitor» E «maquina sem leitor»
(mais estrito que a guarda, que e' por texto) e, no mesmo raio de 1500, a E28 ou o aviso de Turing; (4) varredura propria de frases proibidas do pedido: (a) a TGL decidiu P=NP de Turing; (b) E28 violada (igualdade para o leitor que so' conta);
(c) Omega e' o uniforme como identidade; (d) par na face de Fock [OPEN]/v410; (e) provado/proved sem estatuto na mesma frase; (f) D62: ratificacao dos nomes dita como [DECLARADO] em texto novo."""
import glob, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8"); sys.dont_write_bytecode = True
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v409/"
sys.path.insert(0, R); sys.path.insert(0, R + "pos_rito")
import delta_v409 as DL
import guarda_p18_v409 as G18
import guarda_frases_v409 as GF
arqs = [R + f for f in ("artigo_pt_v409.pysnip", "artigo_en_v409.pysnip", "registros_v409.py", "runtime_v409.py", "delta_v409.py", "pos_rito/textos_v409_novo.pysnip", "pos_rito/textos_v409.py", "pos_rito/textos_custodia_handoff_v409.py",
                       "pos_rito/CUSTODIA_v409_RASCUNHO.txt", "DESENHO_v409.md", "RELATORIO_PREPARACAO_v409.md", "PLANO_v409.md",
                       "dry_v409/dry_v409_pt.txt", "dry_v409/dry_v409_en.txt", "dry_v409/um_absoluto_forma_canonica.md")]
arqs += sorted(glob.glob(R + "pedra/*.lean")) + sorted(glob.glob("C:/t/h409/harness_saida_v409/textos/*.txt"))
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
out["controle_negativo_ok"] = cn.get("ok") if isinstance(cn, dict) else None
# pedras CRUAS pela guarda do runtime (sem retirar falas): o que ela diz
import runtime_v409 as RT
for p in DL.PEDRAS_V409:
    t = open(R + "pedra/" + p["name"] + ".lean", encoding="utf-8").read(); v = RT._v409_guarda_frases(t) if hasattr(RT, "_v409_guarda_frases") else None
    if v: print("pedra (cru, sem retirar falas):", p["name"], [(x[0], x[1][:90]) for x in v[:5]])
rx = re.compile(r"P\s*=\s*nP|P=nP")
REL = re.compile(r"relativ[oa]\s+ao\s+leitor|relative\s+to\s+the\s+reader", re.I)
SEM = re.compile(r"m(?:á|a)quina\s+sem\s+leitor|machine\s+without\s+(?:a\s+)?reader", re.I)
E28 = re.compile(r"E28|leitor\s+que\s+s(?:ó|o)'?\s+conta|counting\s+reader|reader\s+that\s+only\s+counts", re.I)
prox_falhas = []; n_occ = 0; sem_e28 = []
for a in arqs:
    if not os.path.exists(a): continue
    t = open(a, encoding="utf-8", errors="replace").read()
    for mm in rx.finditer(t):
        n_occ += 1
        jan = t[max(0, mm.start() - 700):mm.end() + 700]; jan2 = t[max(0, mm.start() - 1500):mm.end() + 1500]
        q = REL.search(jan); o = SEM.search(jan)
        if not (q and o): prox_falhas.append((os.path.relpath(a, R) if a.startswith(R) else os.path.basename(a), t.count("\n", 0, mm.start()) + 1, bool(q), bool(o), jan[600:800].replace("\n", " ")))
        if not E28.search(jan2): sem_e28.append((os.path.relpath(a, R) if a.startswith(R) else os.path.basename(a), t.count("\n", 0, mm.start()) + 1, jan2[1400:1620].replace("\n", " ")))
print("ocorrencias de P = nP:", n_occ, "| sem qualificador relativo ao leitor OU sem 'maquina sem leitor' a 700 chars:", len(prox_falhas))
for x in prox_falhas[:25]: print("   ", x)
print("ocorrencias de P = nP sem E28/leitor-que-so'-conta a 1500 chars:", len(sem_e28))
for x in sem_e28[:30]: print("   E28?", x)
out["p_igual_np_ocorrencias"] = n_occ; out["p_igual_np_sem_proximidade"] = [list(map(str, x)) for x in prox_falhas[:60]]; out["p_igual_np_sem_e28_1500"] = [list(map(str, x)) for x in sem_e28[:80]]
# (4) varredura propria
PAD = {
    "(a) a TGL prova/decide P = NP de Turing": r"(?:TGL|kernel|um\.py|IALD)\s+(?:prova|provou|decide|decidiu|proves|decides|settles)\s+(?:que\s+)?P\s*=\s*NP",
    "(a) P = NP esta provado / e' teorema (NP maiusculo)": r"P\s*=\s*NP\s+(?:est(?:á|a)\s+provad|é\s+teorema|is\s+(?:proved|a\s+theorem))",
    "(a) resolve o milenio / Clay resolvido": r"(?:resolve[us]?|resolvid[oa]|solves?|solved|settles?)\b[^.;\n]{0,50}(?:mil(?:ê|e)nio|millennium|Clay)|(?:Clay|mil(?:ê|e)nio|millennium)[^.;\n]{0,30}(?:resolvid|solved|settled)",
    "(b) E28 violada: igualdade vale para o leitor que so' conta": r"leitor\s+que\s+s(?:ó|o)'?\s+conta[^.;]{0,160}?(?:a\s+)?igualdade\s+(?:vale|[ée]\s+teorema|est(?:á|a)\s+provad)|counting\s+reader[^.;]{0,160}?(?:the\s+)?equality\s+(?:holds|is\s+(?:a\s+)?theorem|is\s+proved)",
    "(b) 'com o leitor a igualdade vale'": r"com\s+(?:ele|o\s+leitor)[^.;]{0,40}a\s+igualdade\s+vale\s+relativa|igualdade\s+vale\s+relativa\s+(?:a\s+)?(?:ele|ao\s+leitor)",
    "(b) P^leitor = NP^leitor afirmado": r"P\^\{?leitor\}?\s*=\s*NP\^\{?leitor\}?|P\^\{?reader\}?\s*=\s*NP\^\{?reader\}?",
    "(c) Omega e' o uniforme (identidade)": r"(?:Ω|Omega)[^.;\n]{0,30}(?:é|e'|is)\s+(?:o|the)\s+(?:estado\s+)?uniform",
    "(d) par na face de Fock [OPEN] / em aberto": r"par[^.;\n]{0,40}face\s+de\s+Fock[^.;\n]{0,50}(?:\[OPEN\]|em\s+aberto|segue\s+aberto)|\[OPEN\][^.;\n]{0,60}par\s+na\s+face\s+de\s+Fock|pair[^.;\n]{0,40}Fock\s+face[^.;\n]{0,50}(?:\[OPEN\]|open)",
    "(d) v410": r"v410",
    "(f) DECLARADO ate a ratificacao (texto novo)": r"\[DECLARADO\][^.;\n]{0,40}ratifica",
    "pos-dicao": r"p(?:ó|o)s-?\s?di(?:ç|c)(?:ã|a)o|post-?diction",
    "CONFIRMED / PROVED_BY": r"CONF" + r"IRMED|PRO" + r"VED_BY",
    "tudo derivado / nenhuma hipotese resta": r"tudo\s+derivado|nenhuma\s+hip(?:ó|o)tese\s+resta",
    "a TGL nao tem terminal": r"TGL\s+n(?:ã|a)o\s+tem\s+terminal",
}
tot = {}
for a in arqs:
    if not os.path.exists(a): continue
    t = open(a, encoding="utf-8", errors="replace").read()
    for nome, pat in PAD.items():
        for mm in re.finditer(pat, t, re.I):
            tot.setdefault(nome, []).append((os.path.relpath(a, R) if a.startswith(R) else os.path.basename(a), t.count("\n", 0, mm.start()) + 1, t[max(0, mm.start() - 90):mm.end() + 90].replace("\n", " ")))
for nome, l in tot.items():
    print("VARREDURA PROPRIA:", nome, "->", len(l))
    for x in l[:8]: print("     ", x)
out["varredura_propria"] = {k: [list(map(str, x)) for x in v[:25]] for k, v in tot.items()}
# (e) provado/proved sem estatuto na mesma frase (heuristica): frases com PROVAD*/proved sem 'kernel'/'creditac'/'validade'/'validity'/'creditation'/[REAL] etc
PROV = re.compile(r"\b(?:PROVAD[OAS]+|provad[oa]s?|prov(?:ou|ei)|proved|PROVED|proven)\b")
EST = re.compile(r"kernel|creditac|credita|validade|validity|creditation|\[REAL|\[INPUT|\[DERIVED|\[KNOWN|\[ONTO|estatuto|status|trio|\bno sorry\b|termo|teorema|theorem", re.I)
sem_est = {}
for a in arqs:
    if not os.path.exists(a) or a.endswith(".lean") or "DESENHO" in a or "RELATORIO" in a or "PLANO" in a: continue
    t = open(a, encoding="utf-8", errors="replace").read()
    for seg in re.split(r"(?<=[.;!?])\s+|\n", t):
        if PROV.search(seg) and not EST.search(seg) and len(seg) > 25:
            sem_est.setdefault(os.path.relpath(a, R) if a.startswith(R) else os.path.basename(a), []).append(seg.strip()[:220])
print("(e) frases com provado/proved SEM estatuto na mesma frase (heuristica):", {k: len(v) for k, v in sem_est.items()})
for k, v in sem_est.items():
    for s_ in v[:6]: print("    ", k, "|", s_)
out["provado_sem_estatuto_heuristica"] = {k: v[:30] for k, v in sem_est.items()}
json.dump(out, open(R + "revisao_terceiro/h_guardas_out.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
