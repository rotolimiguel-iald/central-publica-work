# -*- coding: utf-8 -*-
"""fidelidade_v402.py -- exame final v402 (27/10/2026; molde: fidelidade_v401.py), item 4: fidelidade de citacao POR BYTES e as regras de texto da v402.
Corpus do OPERADOR (OPERADOR_*/CUNHAGEM_OPERADOR_* verbatim) + as cunhagens VERBATIM do ADENDO de 03-04/09 (itens numerados «...» do adendo do Nos, lidos do arquivo).
Superficies: as STRINGS NOVAS do candidato (fora do kernel embutido), as strings de pos_rito\\textos_v402.py, a secao v402 do artigo PT/EN e as linhas v402 do .md (do Nos EMULADO sb8,
que e o dry_v402), os textos do pos-rito RENDERIZADOS (textos_renderizados_v402) e o handoff do meu sandbox sb8. So le; grava so o JSON nesta pasta."""
import ast, glob, hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__))
W = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "work")
V = os.path.join(W, "cadeia_de_selo", "v402")
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
CAND = os.path.join(V, "um_v402_candidato.py"); NOS_UM = os.path.join(NOS, "um.py")
SB = os.path.join(H, "sb8")
norm = lambda s: re.sub(r"\s+", " ", s.replace(" ", " ").replace("\xa0", " ")).strip()
OP = {}
for p in glob.glob(os.path.join(W, "cunhagens_*", "OPERADOR_*_verbatim.txt")) + glob.glob(os.path.join("C:" + os.sep, "IALD", "PROGRAMA_IALD", "OPERADOR_*_verbatim.txt")) + glob.glob(os.path.join(W, "*", "CUNHAGEM_OPERADOR_*_verbatim.txt")) + glob.glob(os.path.join(W, "*", "OPERADOR_*_verbatim.txt")):
    OP[os.path.basename(p)] = norm(open(p, "rb").read().decode("utf-8"))
ADENDO_RAW = open(os.path.join(NOS, "ADENDO_A_INSCRICAO_INTERROMPE_A_INERCIA.md"), "rb").read()
ADENDO_SHA16 = hashlib.sha256(ADENDO_RAW).hexdigest()[:16]
ADENDO_CUNH = [norm(m.group(1)) for m in re.finditer(r"^\d+\. \(\d\d/\d\d\) «([^»]+)»", ADENDO_RAW.decode("utf-8"), re.M)]
GER = {os.path.basename(p): norm(open(p, "rb").read().decode("utf-8")) for p in glob.glob(os.path.join(W, "cunhagens_*", "GERENCIA_*_verbatim.txt"))}
ATL = norm(open(os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "memory", "TGL_ATLAS.md"), "rb").read().decode("utf-8", "replace").replace("**", "").replace("*", ""))
ADN = norm(ADENDO_RAW.decode("utf-8").replace("**", ""))
KERN = norm(" ".join(open(p, "rb").read().decode("utf-8", "replace") for p in glob.glob(os.path.join("C:" + os.sep, "t", "k402c", "final", "TGLExt", "*.lean")) + glob.glob(os.path.join("C:" + os.sep, "t", "k402c", "final", "TGL", "*.lean"))))
CASA = norm(open(os.path.join("C:" + os.sep, "IALD", "CLAUDE.md"), "rb").read().decode("utf-8", "replace").replace("**", ""))


def strings(src):
    out = set()
    for n in ast.walk(ast.parse(src)):
        if isinstance(n, ast.Constant) and isinstance(n.value, str): out.add(n.value)
        elif isinstance(n, ast.JoinedStr): out.add("".join(v.value if isinstance(v, ast.Constant) else "{…}" for v in n.values))
    return out


cb = open(CAND, "rb").read().decode("utf-8"); nb = open(NOS_UM, "rb").read().decode("utf-8")
emb = set()
for n in ast.parse(cb).body:
    if isinstance(n, ast.Assign) and len(n.targets) == 1 and getattr(n.targets[0], "id", None) in ("_EMBEDDED_KERNEL_FILES", "_LEAN_THEOREM_FLAGS", "_BENCH_ARCHIVE_V361_INDEX"):
        emb |= {x.value for x in ast.walk(n) if isinstance(x, ast.Constant) and isinstance(x.value, str)}
novas = sorted(strings(cb) - strings(nb) - emb)
SUP = {"candidato_strings_novas": "\n\n".join(novas), "textos_v402_strings": "\n\n".join(sorted(strings(open(os.path.join(V, "pos_rito", "textos_v402.py"), "rb").read().decode("utf-8"))))}


def secao(t, titulo):
    i = [m.start() for m in re.finditer(re.escape(titulo), t)]
    ini = i[-1] if i else -1
    if ini < 0: return ""
    m = re.search(r"\n== [^\n]{6,140} ==\n", t[ini + len(titulo) + 10:])
    fim = ini + len(titulo) + 10 + (m.start() if m else 20000)
    return t[ini:fim]


for nome, p, tit in (("artigo_pt_v402", os.path.join(SB, "nos", "um_absoluto_pt.txt"), "A ponte da escala dual, a queda sem geometria e a esperança condicional"),
                     ("artigo_en_v402", os.path.join(SB, "nos", "um_absoluto_en.txt"), "The dual-scale bridge, the fall without geometry and the conditional expectation")):
    t = open(p, encoding="utf-8", errors="replace").read(); SUP[nome] = secao(t, tit)
    if not SUP[nome]: print("AVISO: secao nao achada em", nome)
t = open(os.path.join(SB, "nos", "um_absoluto_forma_canonica.md"), encoding="utf-8", errors="replace").read()
SUP["md_v402"] = "\n\n".join(x for x in re.split(r"\n\s*\n", t) if re.search(r"v402|ponte da escala|queda sem geometria|esperança condicional", x))
for p in sorted(glob.glob(os.path.join(H, "textos_renderizados_v402", "*.txt"))):
    SUP["render_" + os.path.basename(p)[:-4]] = open(p, encoding="utf-8").read()
for nome, p in (("handoff_sb8_memory", os.path.join(SB, "memory", "handoff-v402-custodia.md")), ("handoff_sb8_nos", os.path.join(SB, "nos", "HANDOFF_v402_CUSTODIA.md"))):
    if os.path.exists(p): SUP[nome] = open(p, encoding="utf-8", errors="replace").read()
QRX = [(r"«([^«»]{3,700})»", "«»"), (r"``([^`']{3,500})''", "``''"), (r"“([^“”]{3,500})”", "“”")]
ATRIB = re.compile(r"operador|operator|verbatim|fala d|his saying|nas palavras|in his words", re.I)
PROIB = re.compile(r"(o operador|the operator)\s+(disse|falou|escreveu|said|wrote|stated)\b", re.I)
GERL = re.compile(r"ger[eê]ncia|management|GERENCIA", re.I)
R = {"candidato_sha16": hashlib.sha256(cb.encode("utf-8")).hexdigest()[:16], "corpus_operador_n": len(OP), "adendo_sha16": ADENDO_SHA16, "adendo_cunhagens": ADENDO_CUNH,
     "n_strings_novas": len(novas), "superficies": {}, "nao_encontradas_atribuidas": [], "gerencia_sem_rotulo": [], "forma_proibida": [], "gerencia_citada": 0}
for nome, t in SUP.items():
    n_q = n_v = n_ad = n_g = n_a = n_k = n_c = 0; paras = [p for p in re.split(r"\n\s*\n", t) if p.strip()]
    for p in paras:
        pn = norm(p)
        for rx, tipo in QRX:
            for m in re.finditer(rx, p):
                q = norm(m.group(1))
                if not re.search(r"[A-Za-zÀ-ú]{3}", q) or "{…}" in q or "%s" in q or "%(" in q: continue
                n_q += 1; ctx = pn[max(0, pn.find(q) - 300): pn.find(q) + len(q) + 200]
                if any(q in c for c in OP.values()): n_v += 1; continue
                if any(q in c for c in ADENDO_CUNH): n_ad += 1; continue
                if any(q in c for c in GER.values()):
                    n_g += 1; R["gerencia_citada"] += 1
                    if not GERL.search(ctx): R["gerencia_sem_rotulo"].append({"superficie": nome, "citacao": q[:160], "contexto": ctx[:400]})
                    continue
                if q in ATL or q in ADN: n_a += 1; continue
                if q in KERN: n_k += 1; continue
                if q in CASA: n_c += 1; continue
                if ATRIB.search(ctx): R["nao_encontradas_atribuidas"].append({"superficie": nome, "citacao": q[:160], "contexto": ctx[:420]})
        for m in PROIB.finditer(pn):
            seg = pn[m.end(): m.end() + 420]
            qs = [norm(x) for rx, _ in QRX for x in re.findall(rx, seg)]
            if not qs or not any(q in c for c in list(OP.values()) + ADENDO_CUNH for q in qs[:1]):
                R["forma_proibida"].append({"superficie": nome, "trecho": pn[max(0, m.start() - 120): m.end() + 260], "citacao_logo_depois": qs[:1]})
    R["superficies"][nome] = {"paragrafos": len(paras), "citacoes": n_q, "verbatim_operador": n_v, "verbatim_adendo": n_ad, "gerencia": n_g, "atlas_ou_adendo_texto": n_a, "kernel": n_k, "memoria_da_casa": n_c}
# ---- as regras da v402
LOR_PROIB = re.compile(r"Lorentz vem da queda da fase|Lorentz comes from the fall of the phase", re.I)
LOR_OK = "Lorentz vem do potencial da fase de queda, uma fase cai após a comutação que produz a torção"
R["lorentz_forma_curta"] = {}
for k, v in SUP.items():
    vn = norm(v); hs = []
    for m in LOR_PROIB.finditer(vn):
        ctx = vn[max(0, m.start() - 300): m.end() + 200]
        hs.append({"ctx": ctx[:500], "dita_do_escriba_nao_do_operador": bool(re.search(r"escriba|scribe|t[ií]tulo|title|n[aã]o (é |e' )?(a palavra )?do operador|not the operator", ctx, re.I)),
                   "rotulada_como_do_operador": bool(re.search(r"(operador|operator)[^.«]{0,60}«?Lorentz vem da queda", ctx, re.I)) and not re.search(r"escriba|scribe", ctx, re.I)})
    if hs: R["lorentz_forma_curta"][k] = hs
R["lorentz_forma_curta_como_do_operador"] = sum(1 for v in R["lorentz_forma_curta"].values() for h in v if not h["dita_do_escriba_nao_do_operador"])
R["lorentz_forma_do_operador_por_bytes"] = {k: norm(v).count(LOR_OK) for k, v in SUP.items() if LOR_OK in norm(v)}
R["lorentz_forma_do_operador_no_adendo"] = LOR_OK in ADENDO_CUNH
FALAS = {"5d3976cd0cc10dc8": "OPERADOR_26out_esperanca_condicional_e_nome_verbatim.txt", "36cfa0027565dcff": "OPERADOR_26out_o_um_se_poe_e_cai_a_queda_sem_geometria_verbatim.txt", "a1c4bae4a87aa173": "OPERADOR_26out_e_isso_faca_a_prova_prossiga_verbatim.txt"}
R["falas_26out_sha"] = {h: hashlib.sha256(open(os.path.join(W, "cunhagens_13out", f), "rb").read()).hexdigest()[:16] == h for h, f in FALAS.items()}
PR = re.compile(r"o Um posto tem dire[cç][aã]o|does the posited One have a direction|has the posited One a direction|the posited One have direction|Um posto tem direcao", re.I)
R["pergunta_e_resposta"] = {k: [{"declarado_a_500": bool(re.search(r"DECLARADO|DECLARED", norm(v)[max(0, m.start() - 500): m.end() + 500])), "ctx": norm(v)[max(0, m.start() - 160): m.end() + 200]} for m in PR.finditer(norm(v))] for k, v in SUP.items() if PR.search(norm(v))}
R["pergunta_e_resposta_sem_declarado"] = sum(1 for v in R["pergunta_e_resposta"].values() for x in v if not x["declarado_a_500"])
DRX = re.compile(r"\bD1[1-6]\b")
R["decisoes"] = {k: {"n": len(DRX.findall(v)), "D11_a_D16": sorted(set(DRX.findall(v))), "gerencia_a_400": sum(1 for m in DRX.finditer(norm(v)) if re.search(r"ger[eê]ncia|management|gerencia", norm(v)[max(0, m.start() - 400): m.end() + 400], re.I)),
                     "ratificavel_no_texto": bool(re.search(r"ratific[aá]ve|ratifiab|ratific", v, re.I))} for k, v in SUP.items() if DRX.search(v)}
ERX = re.compile(r"\bE[1-4]\b")
R["erratas_E"] = {k: {"E1_a_E4": sorted(set(ERX.findall(v))), "assinada_gerencia_c1_em_nome_proprio": len(re.findall(r"ger[eê]ncia c1, em nome pr[oó]prio|management c1, in its own name|gerencia c1, em nome proprio|c1 management, in its own name", v, re.I))}
                  for k, v in SUP.items() if re.search(r"\bE1\b", v) and re.search(r"\bE4\b", v)}
HT = re.compile(r"H_\\tau|H_tau|H_τ")
R["H_tau"] = {}
for k, v in SUP.items():
    vn = norm(v); hs = list(HT.finditer(vn))
    if not hs: continue
    R["H_tau"][k] = {"n": len(hs), "refutada_a_300": sum(1 for m in hs if re.search(r"REFUTAD|refuted|REFUTED|refutad", vn[max(0, m.start() - 300): m.end() + 300])),
                     "dita_aberta_sem_refutada_a_300": [vn[max(0, m.start() - 150): m.end() + 150] for m in hs if re.search(r"\[OPEN\]|ABERTA|open", vn[max(0, m.start() - 60): m.end() + 120]) and not re.search(r"REFUTAD|refuted|REFUTED|refutad|dizia|said|v401", vn[max(0, m.start() - 300): m.end() + 300])][:3]}
R["E2_vetor_zero"] = {k: len(re.findall(r"VETOR ZERO|vetor zero|zero vector|ZERO VECTOR", v)) for k, v in SUP.items() if re.search(r"Inertial|inercial|inertial", v)}
R["E3_nunca_mc2_composta"] = {k: [norm(v)[max(0, m.start() - 160): m.end() + 120] for m in re.finditer(r"E\s*=\s*mc\^?2|E = mc²|E=mc2", norm(v)) if not re.search(r"nunca|never|n[aã]o|not|E3|premissas|premises|condicionad|conditional", norm(v)[max(0, m.start() - 200): m.end() + 200], re.I)][:3] for k, v in SUP.items() if re.search(r"E\s*=\s*mc", v)}
R["E4_proveniencia"] = {k: ("8a3a1c0baa8b7faf" in v, "9f6efcb2a0987e18" in v) for k, v in SUP.items() if re.search(r"\bE4\b", v)}
PROV = re.compile(r"PonteDaEscalaDual|QuedaSemGeometria|EsperancaCondicional")
R["nomes_provisorios"] = {k: {"mencoes": len(PROV.findall(v)), "provisorio_no_texto": bool(re.search(r"provis[oó]ri|provisional|PROVISORI", v, re.I))} for k, v in SUP.items() if PROV.search(v)}
R["nomes_sem_provisorio"] = [k for k, x in R["nomes_provisorios"].items() if not x["provisorio_no_texto"]]
R["ordem_025"] = {k: {"ocorrencias": len(re.findall(r"ORDEM 025", v)), "com_pendencia_a_400": sum(1 for m in re.finditer(r"ORDEM 025", norm(v)) if re.search(r"PARCIAL|parcial|partial|PARTIAL|pend[eê]ncia|pending|\[OPEN\]|H_BW|errata|E1", norm(v)[max(0, m.start() - 400): m.end() + 400], re.I))} for k, v in SUP.items() if "ORDEM 025" in v}
R["ordem_025_sem_pendencia"] = {k: x for k, x in R["ordem_025"].items() if x["com_pendencia_a_400"] < x["ocorrencias"]}
W8 = "".join(map(chr, [67, 79, 78, 70, 73, 82, 77, 69, 68])); Wp = "".join(map(chr, [99, 111, 110, 102, 105, 114, 109, 97]))
R["palavra_proibida_por_superficie"] = {k: {"token": len(re.findall(r"(?<!NOT_)" + W8, v)), "inflexoes": [norm(v)[max(0, m.start() - 80): m.end() + 40] for m in re.finditer(Wp, norm(v), re.I) if "NOT_A_" not in norm(v)[max(0, m.start() - 12): m.start()]][:4]} for k, v in SUP.items()}
R["palavra_proibida_total_token"] = sum(x["token"] for x in R["palavra_proibida_por_superficie"].values())
R["palavra_proibida_inflexoes"] = {k: x["inflexoes"] for k, x in R["palavra_proibida_por_superficie"].items() if x["inflexoes"]}
R["pos_dicao_como_demerito"] = {k: [norm(v)[max(0, m.start() - 120): m.end() + 80] for m in re.finditer(r"p[óo]s-?di[cç][cç]?[ãa]o|postdiction", norm(v), re.I)] for k, v in SUP.items() if re.search(r"p[óo]s-?di[cç][cç]?[ãa]o|postdiction", v, re.I)}
R["literais_beta_alfa_por_superficie"] = {k: re.findall(r"0[.,]0120313\d*|0[.,]00729735\d*|1[.,]6487212\d*|137[.,]035999\d*", v)[:4] for k, v in SUP.items() if re.findall(r"0[.,]0120313\d*|0[.,]00729735\d*|1[.,]6487212\d*|137[.,]035999\d*", v)}
CODE = {"textos_v402.py": os.path.join(V, "pos_rito", "textos_v402.py"), "leitura_v402.py": os.path.join(V, "pos_rito", "leitura_v402.py"), "fechar_v402.py": os.path.join(V, "pos_rito", "fechar_v402.py"),
        "superficies_v402.py": os.path.join(V, "pos_rito", "superficies_v402.py"), "registrar_mapa_v402.py": os.path.join(V, "pos_rito", "registrar_mapa_v402.py"), "delta_v402.py": os.path.join(V, "delta_v402.py"), "registros_v402.py": os.path.join(V, "registros_v402.py"), "runtime_v402.py": os.path.join(V, "runtime_v402.py")}
R["literais_beta_alfa_no_codigo"] = {k: re.findall(r"0[.,]0120313\d*|0[.,]0120\d{3}|0[.,]00729735\d*|1[.,]6487212\d*|137[.,]035999\d*", open(p, encoding="utf-8").read()) for k, p in CODE.items()}
DIR = re.compile(r"(IALD|the IALD)\s+(testifica|testifies|testify|atesta)", re.I)
NEG = re.compile(r"n[aã]o\s+(podia\s+dizer\s+que\s+)?(a\s+)?IALD\s+testifica|IALD\s+N[AÃ]O\s+testifica|IALD\s+n[aã]o\s+testifica|IALD\s+(does\s+)?not\s+testif|IALD\s+NAO\s+testifica|the IALD does not testify", re.I)
R["direcao"] = {}
for k, v in SUP.items():
    vn = norm(v); nn = []
    for m in DIR.finditer(vn):
        ctx = vn[max(0, m.start() - 160): m.end() + 120]
        if not (NEG.search(ctx) or "podia dizer que IALD testifica a mim" in ctx): nn.append(ctx[:240])
    if list(DIR.finditer(vn)): R["direcao"][k] = {"ocorrencias": len(list(DIR.finditer(vn))), "nao_negadas": nn}
R["direcao_nao_negadas_total"] = sum(len(v["nao_negadas"]) for v in R["direcao"].values())
R["pai_e_a_IALD"] = {k: [norm(v)[max(0, m.start() - 80): m.end() + 40] for m in re.finditer(r"Pai[^.]{0,40}(é|e'|is)\s+a\s+IALD", norm(v), re.I)] for k, v in SUP.items() if re.search(r"Pai[^.]{0,40}(é|e'|is)\s+a\s+IALD", norm(v), re.I)}
R["confidencialidade_sem_negacao"] = {k: [norm(v)[max(0, m.start() - 90): m.end() + 90] for m in re.finditer(r"confidencialidade|confidentiality", norm(v), re.I) if not re.search(r"N[AÃ]O (e'|é )?alegad|nao alegad|not claimed|nao e' alegad|NAO alegada|nao alegada|nem medida|NÃO é alegada|sem alegação|nenhuma alegação|no cryptographic|is not claimed|não atestada|nao atestada|não é alegad|nenhuma alegacao|no claim", norm(v)[max(0, m.start() - 200): m.end() + 200], re.I)][:3] for k, v in SUP.items() if re.search(r"confidencialidade|confidentiality", v, re.I)}
R["confidencialidade_sem_negacao"] = {k: v for k, v in R["confidencialidade_sem_negacao"].items() if v}
R["legal"] = {k: len(re.findall(r"\[LEGAL\]|LEGAL:", v)) for k, v in SUP.items() if re.findall(r"\[LEGAL\]|LEGAL:", v)}
R["chao_e_o_posto"] = {k: {"posto": bool(re.search(r"POSTO|posto|the post", v)), "infimo_0_negado": bool(re.search(r"nunca o [ií]nfimo|never the infimum|NUNCA o [ií]nfimo|nunca o infimo", v, re.I))} for k, v in SUP.items() if re.search(r"ch[aã]o|floor", v, re.I) and re.search(r"v402|queda|fall", v, re.I)}
json.dump(R, open(os.path.join(H, "FIDELIDADE_v402_%s.json" % R["candidato_sha16"]), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
resumo = {k: v for k, v in R.items() if k not in ("nao_encontradas_atribuidas", "gerencia_sem_rotulo", "forma_proibida", "superficies", "palavra_proibida_por_superficie", "lorentz_forma_curta", "pergunta_e_resposta", "adendo_cunhagens")}
print(json.dumps(resumo, ensure_ascii=False, indent=1)[:9000])
print("SUPERFICIES:", len(R["superficies"]), "citacoes:", sum(x["citacoes"] for x in R["superficies"].values()), "verbatim operador:", sum(x["verbatim_operador"] for x in R["superficies"].values()), "adendo:", sum(x["verbatim_adendo"] for x in R["superficies"].values()))
print("LORENTZ curta:", json.dumps(R["lorentz_forma_curta"], ensure_ascii=False)[:1500])
print("PERGUNTA/RESPOSTA:", json.dumps(R["pergunta_e_resposta"], ensure_ascii=False)[:1200])
print("FORMA PROIBIDA:", len(R["forma_proibida"]), json.dumps(R["forma_proibida"][:5], ensure_ascii=False)[:1500])
print("GERENCIA SEM ROTULO:", len(R["gerencia_sem_rotulo"]))
print("NAO ENCONTRADAS ATRIBUIDAS:", len(R["nao_encontradas_atribuidas"]))
for x in R["nao_encontradas_atribuidas"]: print("  -", x["superficie"], "|", x["citacao"][:150], "| CTX:", x["contexto"][:300])
