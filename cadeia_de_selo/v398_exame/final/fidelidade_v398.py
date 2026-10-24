# -*- coding: utf-8 -*-
"""fidelidade_v398.py -- exame final v398 (c1, 23/10/2026), item 3: fidelidade de citacao POR BYTES. Corpus do OPERADOR (OPERADOR_*/CUNHAGEM_OPERADOR_* verbatim; NUNCA o texto
da gerencia) e, a parte, o texto da GERENCIA (19eca91e e qualquer GERENCIA_*). Superficies: as STRINGS NOVAS do candidato (constantes do AST que nao existem no um.py instalado,
fora do kernel embutido), as strings de pos_rito\\textos_v398.py, os paragrafos novos (v398) do artigo PT/EN (.txt do ensaio) e do .md, os textos do pos-rito RENDERIZADOS
(textos_renderizados_v398\\*.txt, se existirem) e o handoff do meu sandbox (sb4, se existir). Para cada citacao «...», ``...'', “...” (e '...' em linha que fala do operador):
VERBATIM_OPERADOR / GERENCIA (e se o contexto a rotula como da gerencia) / ATLAS / TEX / NAO_ENCONTRADA. Forma proibida: «o operador disse/said X». Forma admitida das
ratificacoes: a leitura ratificada vem com o sha da fala e o da ratificacao. So le; grava so' o JSON nesta pasta."""
import ast, glob, hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__))
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v398"
CAND = os.path.join(V, "um_v398_candidato.py"); NOS_UM = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
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
SUP = {"candidato_strings_novas": "\n\n".join(novas), "textos_v398_strings": "\n\n".join(sorted(strings(open(os.path.join(V, "pos_rito", "textos_v398.py"), "rb").read().decode("utf-8"))))}
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
for nome, p, tit in (("artigo_pt_v398", os.path.join(V, "dry_v398", "dry_v398_pt.txt"), "Sônico e a afinação das cordas"), ("artigo_en_v398", os.path.join(V, "dry_v398", "dry_v398_en.txt"), "Sonic and the tuning of the strings")):
    t = open(p, encoding="utf-8", errors="replace").read(); SUP[nome] = secao_v398(t, tit)
    if not SUP[nome]: print("AVISO: secao nao achada em", nome)
t = open(os.path.join(V, "dry_v398", "um_absoluto_forma_canonica.md"), encoding="utf-8", errors="replace").read()
SUP["md_ensaio_v398"] = "\n\n".join(x for x in re.split(r"\n\s*\n", t) if re.search(r"v398|Sônico|afinação das cordas", x))
for p in sorted(glob.glob(os.path.join(H, "textos_renderizados_v398", "*.txt"))):
    SUP["render_" + os.path.basename(p)[:-4]] = open(p, encoding="utf-8").read()
for nome, p in (("handoff_sb4_memory", os.path.join(H, "..", "sb4", "memory", "handoff-v398-custodia.md")), ("handoff_sb4_nos", os.path.join(H, "..", "sb4", "nos", "HANDOFF_v398_CUSTODIA.md"))):
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
# a sexta inscricao rotulada; as ratificacoes na forma admitida
todo = "\n".join(SUP.values()); tn = norm(todo)
R["sexta_inscricao"] = {"ocorrencias_19eca91e": tn.count("19eca91e"), "ocorrencias_19eca91e_com_rotulo_de_gerencia_a_300": sum(1 for m in re.finditer("19eca91e", tn) if GERL.search(tn[max(0, m.start() - 300): m.end() + 300])),
                        "ocorrencias_19eca91e_ditas_do_operador": [tn[max(0, m.start() - 160): m.end() + 60] for m in re.finditer("19eca91e", tn) if re.search(r"fala do operador[^.]{0,40}19eca91e|19eca91e[^.]{0,40}fala do operador", tn[max(0, m.start() - 160): m.end() + 60], re.I)]}
R["ratificacoes_forma_admitida"] = {"sonico_leitura_ratificada_b4483331_com_e5c2910a_ou_19eca91e_a_400": sum(1 for m in re.finditer("b4483331", tn) if re.search(r"ratific", tn[max(0, m.start() - 400): m.end() + 400], re.I) and re.search(r"e5c2910a|19eca91e", tn[max(0, m.start() - 400): m.end() + 400])),
                                     "afinacao_ratificada_5bccedc9_com_baef998c_a_400": sum(1 for m in re.finditer("5bccedc9", tn) if re.search(r"ratific", tn[max(0, m.start() - 400): m.end() + 400], re.I) and "baef998c" in tn[max(0, m.start() - 400): m.end() + 400]),
                                     "ocorrencias_b4483331": tn.count("b4483331"), "ocorrencias_5bccedc9": tn.count("5bccedc9")}
W = "".join(map(chr, [67, 79, 78, 70, 73, 82, 77, 69, 68])); Wp = "".join(map(chr, [99, 111, 110, 102, 105, 114, 109, 97]))
R["palavra_proibida_por_superficie"] = {k: {"token": len(re.findall(r"(?<!NOT_)" + W, v)), "inflexoes": [norm(v)[max(0, m.start() - 80): m.end() + 40] for m in re.finditer(Wp, norm(v), re.I) if "NOT_A_" not in norm(v)[max(0, m.start() - 12): m.start()]][:4]} for k, v in SUP.items()}
R["literais_beta_alfa_por_superficie"] = {k: re.findall(r"0[.,]0120313\d*|0[.,]00729735\d*|1[.,]6487212\d*|137[.,]035999\d*", v)[:4] for k, v in SUP.items()}
json.dump(R, open(os.path.join(H, "FIDELIDADE_v398_%s.json" % R["candidato_sha16"]), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in R.items() if k not in ("nao_encontradas_atribuidas", "gerencia_sem_rotulo", "forma_proibida")}, ensure_ascii=False, indent=1))
print("FORMA PROIBIDA:", len(R["forma_proibida"]), json.dumps(R["forma_proibida"][:5], ensure_ascii=False)[:1500])
print("GERENCIA SEM ROTULO:", len(R["gerencia_sem_rotulo"]), json.dumps(R["gerencia_sem_rotulo"][:5], ensure_ascii=False)[:1500])
print("NAO ENCONTRADAS ATRIBUIDAS:", len(R["nao_encontradas_atribuidas"]))
for x in R["nao_encontradas_atribuidas"]: print("  -", x["superficie"], "|", x["citacao"][:150], "| CTX:", x["contexto"][:380])
