# -*- coding: utf-8 -*-
"""fidelidade_v400.py -- exame final v400 (c1, 24/10/2026; molde: o meu fidelidade_v399.py), item 5: fidelidade de citacao POR BYTES. Corpus do OPERADOR (OPERADOR_*/CUNHAGEM_OPERADOR_* verbatim; NUNCA o texto
da gerencia) e, a parte, o texto da GERENCIA (19eca91e e qualquer GERENCIA_*). Superficies: as STRINGS NOVAS do candidato (constantes do AST que nao existem no um.py instalado,
fora do kernel embutido), as strings de pos_rito\\textos_v398.py, os paragrafos novos (v398) do artigo PT/EN (.txt do ensaio) e do .md, os textos do pos-rito RENDERIZADOS
(textos_renderizados_v398\\*.txt, se existirem) e o handoff do meu sandbox (sb4, se existir). Para cada citacao «...», ``...'', “...” (e '...' em linha que fala do operador):
VERBATIM_OPERADOR / GERENCIA (e se o contexto a rotula como da gerencia) / ATLAS / TEX / NAO_ENCONTRADA. Forma proibida: «o operador disse/said X». Forma admitida das
ratificacoes: a leitura ratificada vem com o sha da fala e o da ratificacao. So le; grava so' o JSON nesta pasta."""
import ast, glob, hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__))
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v400"
CAND = os.path.join(V, "um_v400_candidato.py"); NOS_UM = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
norm = lambda s: re.sub(r"\s+", " ", s.replace("\u2009", " ").replace("\xa0", " ")).strip()
OP = {}
for p in glob.glob(r"C:\IALD\Central de Patentes\work\cunhagens_*\OPERADOR_*_verbatim.txt") + glob.glob(r"C:\IALD\PROGRAMA_IALD\OPERADOR_*_verbatim.txt") + glob.glob(r"C:\IALD\Central de Patentes\work\*\CUNHAGEM_OPERADOR_*_verbatim.txt") + glob.glob(r"C:\IALD\Central de Patentes\work\*\OPERADOR_*_verbatim.txt"):
    OP[os.path.basename(p)] = norm(open(p, "rb").read().decode("utf-8"))
GER = {os.path.basename(p): norm(open(p, "rb").read().decode("utf-8")) for p in glob.glob(r"C:\IALD\Central de Patentes\work\cunhagens_*\GERENCIA_*_verbatim.txt")}
ATL = norm(open(r"C:\IALD\Central de Patentes\memory\TGL_ATLAS.md", "rb").read().decode("utf-8", "replace").replace("**", "").replace("*", ""))
TEX = norm(open(r"C:\IALD\Artigo\the_boundary\Genesis da Unificação\Artigos_fundadores\A_ultima_corda_v3.tex", "rb").read().decode("utf-8")) + " " + norm(open(r"C:\IALD\projetos_pyhton\acom\A_fronteira_v4.tex", "rb").read().decode("utf-8"))
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
SUP = {"candidato_strings_novas": "\n\n".join(novas), "textos_v400_strings": "\n\n".join(sorted(strings(open(os.path.join(V, "pos_rito", "textos_v400.py"), "rb").read().decode("utf-8"))))}
KW = re.compile(r"v398|Sônico|sônico|Sonic|afinação|tuning|cordas|strings|oitava|octave|Matsubara|zeta|Bernoulli|gerência|management|23/10/2026|Token|psibit", re.I)
def secao_v398(t, titulo):
    """a secao NOVA do artigo (do titulo da secao v398 ate o proximo titulo de secao) + o quadro do topo"""
    i = [m.start() for m in re.finditer(re.escape(titulo), t)]
    ini = i[-1] if i else -1
    if ini < 0: return ""
    m = re.search(r"\n\n[^\n]{6,90}\n==+\n", t[ini + len(titulo):])
    fim = ini + len(titulo) + (m.start() if m else 9000)
    q = t.find("O Teste da Única Palavra") if "O Teste da Única Palavra" in t else t.find("The Test of the Only Word")
    return t[ini:fim] + "\n\n" + (t[q:q + 2600] if q >= 0 else "")
for nome, p, tit in (("artigo_pt_v400", os.path.join(V, "dry_v400", "dry_v400_pt.txt"), "O testemunho de dois: o selo pela própria tecnologia"), ("artigo_en_v400", os.path.join(V, "dry_v400", "dry_v400_en.txt"), "The testimony of two: sealing by its own technology")):
    t = open(p, encoding="utf-8", errors="replace").read(); SUP[nome] = secao_v398(t, tit)
    if not SUP[nome]: print("AVISO: secao nao achada em", nome)
t = open(os.path.join(V, "dry_v400", "um_absoluto_forma_canonica.md"), encoding="utf-8", errors="replace").read()
SUP["md_ensaio_v400"] = "\n\n".join(x for x in re.split(r"\n\s*\n", t) if re.search(r"v400|v399|testemunho de dois|própria tecnologia", x))
for p in sorted(glob.glob(os.path.join(H, "textos_renderizados_v400", "*.txt"))):
    SUP["render_" + os.path.basename(p)[:-4]] = open(p, encoding="utf-8").read()
for nome, p in (("handoff_sb6_memory", os.path.join(H, "sb6", "memory", "handoff-v400-custodia.md")), ("handoff_sb6_nos", os.path.join(H, "sb6", "nos", "HANDOFF_v400_CUSTODIA.md"))):
    if os.path.exists(p): SUP[nome] = open(p, encoding="utf-8", errors="replace").read()
QRX = [(r"«([^«»]{3,700})»", "«»"), (r"``([^`']{3,500})''", "``''"), (r"“([^“”]{3,500})”", "“”")]
ATRIB = re.compile(r"operador|operator|verbatim|fala d|his saying|nas palavras|in his words", re.I)
PROIB = re.compile(r"(o operador|the operator)\s+(disse|falou|escreveu|said|wrote|stated)\b", re.I)
GERL = re.compile(r"ger[eê]ncia|management|GERENCIA", re.I)
R = {"candidato_sha16": hashlib.sha256(cb.encode("utf-8")).hexdigest()[:16], "corpus_operador_n": len(OP), "corpus_gerencia": sorted(GER), "n_strings_novas": len(novas), "superficies": {}, "nao_encontradas_atribuidas": [], "gerencia_sem_rotulo": [], "forma_proibida": [], "gerencia_citada": 0}
for nome, t in SUP.items():
    n_q = n_v = n_g = n_a = n_t = 0; paras = [p for p in re.split(r"\n\s*\n", t) if p.strip()]
    for p in paras:
        pn = norm(p)
        for rx, tipo in QRX:
            for m in re.finditer(rx, p):
                q = norm(m.group(1))
                if not re.search(r"[A-Za-zÀ-ú]{3}", q) or "{…}" in q or "%s" in q or "%(" in q: continue
                n_q += 1; ctx = pn[max(0, pn.find(q) - 300): pn.find(q) + len(q) + 200]
                if any(q in c for c in OP.values()): n_v += 1; continue
                if any(q in c for c in GER.values()):
                    n_g += 1; R["gerencia_citada"] += 1
                    if not GERL.search(ctx): R["gerencia_sem_rotulo"].append({"superficie": nome, "citacao": q[:160], "contexto": ctx[:400]})
                    continue
                if q in ATL: n_a += 1; continue
                if q in TEX: n_t += 1; continue
                if ATRIB.search(ctx): R["nao_encontradas_atribuidas"].append({"superficie": nome, "citacao": q[:160], "contexto": ctx[:420]})
        for m in PROIB.finditer(pn):
            seg = pn[m.end(): m.end() + 420]
            qs = [norm(x) for rx, _ in QRX for x in re.findall(rx, seg)]
            # «o operador disse X»: so' e' forma PROIBIDA se X (a primeira citacao logo depois) NAO estiver nos bytes do operador, ou se nao houver citacao (parafrase)
            if not qs or not any(q in c for c in OP.values() for q in qs[:1]):
                R["forma_proibida"].append({"superficie": nome, "trecho": pn[max(0, m.start() - 120): m.end() + 260], "citacao_logo_depois": qs[:1]})
    R["superficies"][nome] = {"paragrafos": len(paras), "citacoes": n_q, "verbatim_operador": n_v, "gerencia": n_g, "atlas": n_a, "tex": n_t}
# v400: a errata (assinatura em nome proprio da gerencia; atribuicao do defeito a ADAPTACAO da gerencia, nao ao bloco do operador; a v399 fica selada como esta) e a frase do alfa unico
todo = "\n".join(SUP.values()); tn = norm(todo)
ERR = re.compile(r"Errata ao lado \(v400|Erratum beside it \(v400|Errata ao lado \(em nome pr[oó]prio da ger[eê]ncia c1", re.I)
R["errata_v400"] = {}
for k, v in SUP.items():
    vn = norm(v); hs = [m.start() for m in ERR.finditer(vn)]
    if not hs: continue
    R["errata_v400"][k] = {"ocorrencias": len(hs),
                           "assinada_em_nome_proprio_da_gerencia_a_200": sum(1 for h in hs if re.search(r"em nome pr[oó]prio da ger[eê]ncia|in the management'?s own name|assinad[ao] pela ger[eê]ncia", vn[h: h + 200], re.I)),
                           "atribui_a_adaptacao_da_gerencia_a_900": sum(1 for h in hs if re.search(r"adapta[cç][aã]o da ger[eê]ncia|c[oó]digo da ger[eê]ncia|management'?s code|na adapta[cç][aã]o da ger[eê]ncia", vn[h: h + 900], re.I)),
                           "diz_que_o_bloco_do_operador_nao_muda_a_1500": sum(1 for h in hs if re.search(r"bloco do operador[^.]{0,80}(n[aã]o muda|NAO muda|não no bloco)|n[aã]o no bloco do operador|operator'?s block[^.]{0,80}(does not change|not in)", vn[h: h + 1500], re.I)),
                           "diz_que_a_v399_fica_selada_a_900": sum(1 for h in hs if re.search(r"v399 fica selada|v399 stays sealed|ficam como registro", vn[h: h + 900], re.I))}
R["frase_alfa_unico"] = {k: [norm(v)[max(0, m.start() - 70): m.end() + 70] for m in re.finditer(r"uma s[oó] (declara[cç][aã]o|linha) de (α|\$\\alpha\$|alfa)|single (declaration|line) of|UMA s[oó] (declara[cç][aã]o|linha) de alfa", norm(v), re.I)][:3] for k, v in SUP.items() if re.search(r"uma s[oó] (declara[cç][aã]o|linha) de|single (declaration|line) of|UMA s[oó] (declara[cç][aã]o|linha) de alfa", norm(v), re.I)}
R["v399_dita_nao_selada_ou_invalida"] = {k: [norm(v)[max(0, m.start() - 90): m.end() + 60] for m in re.finditer(r"v399[^.]{0,60}(n[aã]o (foi )?selad|inv[aá]lid|not sealed|invalid)", norm(v), re.I)] for k, v in SUP.items() if re.search(r"v399[^.]{0,60}(n[aã]o (foi )?selad|inv[aá]lid|not sealed|invalid)", norm(v), re.I)}
W = "".join(map(chr, [67, 79, 78, 70, 73, 82, 77, 69, 68])); Wp = "".join(map(chr, [99, 111, 110, 102, 105, 114, 109, 97]))
R["palavra_proibida_por_superficie"] = {k: {"token": len(re.findall(r"(?<!NOT_)" + W, v)), "inflexoes": [norm(v)[max(0, m.start() - 80): m.end() + 40] for m in re.finditer(Wp, norm(v), re.I) if "NOT_A_" not in norm(v)[max(0, m.start() - 12): m.start()]][:4]} for k, v in SUP.items()}
R["literais_beta_alfa_por_superficie"] = {k: re.findall(r"0[.,]0120313\d*|0[.,]00729735\d*|1[.,]6487212\d*|137[.,]035999\d*", v)[:4] for k, v in SUP.items()}
DIR = re.compile(r"(IALD|the IALD)\s+(testifica|testifies|testify|atesta)", re.I)
NEG = re.compile(r"n[aã]o\s+(podia\s+dizer\s+que\s+)?(a\s+)?IALD\s+testifica|IALD\s+N[AÃ]O\s+testifica|IALD\s+n[aã]o\s+testifica|IALD\s+(does\s+)?not\s+testif|IALD\s+NAO\s+testifica|the IALD does not testify", re.I)
R["direcao"] = {}
for k, v in SUP.items():
    vn = norm(v); nn = []
    for m in DIR.finditer(vn):
        ctx = vn[max(0, m.start() - 160): m.end() + 120]
        if not (NEG.search(ctx) or "podia dizer que IALD testifica a mim" in ctx): nn.append(ctx[:240])
    R["direcao"][k] = {"ocorrencias": len(list(DIR.finditer(vn))), "nao_negadas": nn}
R["direcao_nao_negadas_total"] = sum(len(v["nao_negadas"]) for v in R["direcao"].values())
R["pai_e_a_IALD"] = {k: [norm(v)[max(0, m.start() - 80): m.end() + 40] for m in re.finditer(r"Pai[^.]{0,40}(é|e'|is)\s+a\s+IALD", norm(v), re.I)] for k, v in SUP.items() if re.search(r"Pai[^.]{0,40}(é|e'|is)\s+a\s+IALD", norm(v), re.I)}
DECL = "o um.py só existe porque fui a operação quadrática da inscrição viva do transporte da IALD"
R["declaracao_marcada"] = {k: {"ocorrencias": len(list(re.finditer(re.escape(DECL), norm(v)))), "com_estatuto_a_600": sum(1 for m in re.finditer(re.escape(DECL), norm(v)) if re.search(r"DECLARA[CÇ][AÃ]O DO OPERADOR|\[INPUT|INPUT\]|declaration of|Operator'?s declaration|declaração do operador|declaracao do operador", norm(v)[max(0, m.start() - 600): m.end() + 600], re.I))} for k, v in SUP.items() if DECL in norm(v)}
R["confidencialidade_sem_negacao"] = {k: [norm(v)[max(0, m.start() - 90): m.end() + 90] for m in re.finditer(r"confidencialidade|confidentiality", norm(v), re.I) if not re.search(r"N[AÃ]O (e'|é )?alegad|nao alegad|not claimed|nao e' alegad|NAO alegada|nao alegada|nem medida|NÃO é alegada|sem alegação|nenhuma alegação|no cryptographic|is not claimed|não atestada|nao atestada|não é alegada|nao e alegada", norm(v)[max(0, m.start() - 160): m.end() + 160], re.I)] for k, v in SUP.items() if re.search(r"confidencialidade|confidentiality", v, re.I)}
R["sha256_primitiva"] = {k: len(re.findall(r"primitiva de integridade[^.]{0,80}SHA-256|integrity primitive[^.]{0,80}SHA-256|SHA-256[^.]{0,60}primitiva", v, re.I)) for k, v in SUP.items()}
R["legal"] = {k: len(re.findall(r"\[LEGAL\]|LEGAL:", v)) for k, v in SUP.items()}
json.dump(R, open(os.path.join(H, "FIDELIDADE_v400_%s.json" % R["candidato_sha16"]), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in R.items() if k not in ("nao_encontradas_atribuidas", "gerencia_sem_rotulo", "forma_proibida")}, ensure_ascii=False, indent=1))
print("FORMA PROIBIDA:", len(R["forma_proibida"]), json.dumps(R["forma_proibida"][:5], ensure_ascii=False)[:1500])
print("GERENCIA SEM ROTULO:", len(R["gerencia_sem_rotulo"]), json.dumps(R["gerencia_sem_rotulo"][:5], ensure_ascii=False)[:1500])
print("NAO ENCONTRADAS ATRIBUIDAS:", len(R["nao_encontradas_atribuidas"]))
for x in R["nao_encontradas_atribuidas"]: print("  -", x["superficie"], "|", x["citacao"][:150], "| CTX:", x["contexto"][:380])
