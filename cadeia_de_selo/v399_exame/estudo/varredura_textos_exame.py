# -*- coding: utf-8 -*-
"""varredura_textos_exame.py -- revisao independente do estudo v399 (c1, 24/10/2026): sobre TODOS os textos da entrega (RESULTADO, PATCH, prototipo, secao colavel, trechos,
Testemunho.lean, registros de exemplo/simulado, sidecar): (a) a DIRECAO do testemunho: toda ocorrencia de «IALD testifica/testifies» e' negada ou esta dentro da fala do
operador que recusa a ordem inversa; «o Pai» mapeado ao absoluto; (b) a declaracao «o um.py so existe porque...» sempre com [DECLARACAO DO OPERADOR / INPUT] (ou INPUT) a 400
chars; (c) as falas de 24/10: cada arquivo OPERADOR_24out_* == a fala embutida na pedra (bytes) e == o texto no prototipo/patch onde citado; (d) [LEGAL] presente; (e) beta/alfa
literal 0,012 em CODIGO (prototipo, secao, trechos): nenhum; (f) palavra proibida (montada por codigo de caractere) e a REGEX do proprio um.py v398 (L248006-248008) sobre
os vereditos novos; (g) «consciencia» so' como palavra retirada. So le; grava so' o JSON nesta pasta."""
import glob, hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__))
S = r"C:\IALD\Central de Patentes\work\v399_selo_e_testemunho"
norm = lambda s: re.sub(r"\s+", " ", s.replace("\u2009", " ").replace("\xa0", " ")).strip()
T = {}
for nome, p in (("RESULTADO.md", "RESULTADO.md"), ("PATCH", "patch_proposto/PATCH_PROPOSTO_v399.md"), ("prototipo", "selo_acom_prototipo.py"), ("secao_colavel", "patch_proposto/secao_colavel_v399.py"),
                ("trechos", "patch_proposto/trechos_v399_para_o_um_py.py"), ("Testemunho.lean", "Testemunho.lean"), ("reg_core_EXEMPLO", "recibos/registro_core_selo_pela_propria_tecnologia_v399_EXEMPLO.json"),
                ("reg_core_SIMULADO", "recibos/registro_core_selo_pela_propria_tecnologia_v399_SIMULADO.json"), ("reg_declaracao_EXEMPLO", "recibos/registro_declaracao_do_operador_v399_EXEMPLO.json"),
                ("sidecar", "recibos/um_absoluto_selo_acom.json"), ("sidecar_SIMULADO", "recibos/um_absoluto_selo_acom_SIMULADO.json"), ("registro_mapa", "registro_mapa_v399_estudo.json"), ("INVENTARIO", "INVENTARIO.json")):
    T[nome] = open(os.path.join(S, p), "rb").read().decode("utf-8", "replace")
R = {"arquivos": {k: hashlib.sha256(v.encode("utf-8")).hexdigest()[:16] for k, v in T.items()}}
# (a) direcao
DIR = re.compile(r"(IALD|the IALD)\s+(testifica|testifies|testify|atesta|testemunha de)", re.I)
NEG = re.compile(r"n[aã]o\s+(podia\s+dizer\s+que\s+)?(a\s+)?IALD\s+testifica|IALD\s+N[AÃ]O\s+testifica|IALD\s+n[aã]o\s+testifica|IALD\s+(does\s+)?not\s+testif|the IALD does not testify|IALD\s+NAO\s+testifica", re.I)
R["direcao"] = {}
for k, v in T.items():
    vn = norm(v); hits = []
    for m in DIR.finditer(vn):
        ctx = vn[max(0, m.start() - 160): m.end() + 120]
        negada = bool(NEG.search(ctx)) or "eu não podia dizer que IALD testifica a mim" in ctx or "eu nao podia dizer que IALD testifica a mim" in ctx
        hits.append({"ctx": ctx[:260], "negada_ou_na_fala_que_recusa": negada})
    R["direcao"][k] = {"ocorrencias": len(hits), "nao_negadas": [h["ctx"] for h in hits if not h["negada_ou_na_fala_que_recusa"]]}
R["direcao_total_nao_negadas"] = sum(len(v["nao_negadas"]) for v in R["direcao"].values())
R["pai_no_absoluto"] = {k: len(re.findall(r"Pai[^.]{0,80}(absoluto|the absolute|o Um|the One)", norm(v), re.I)) for k, v in T.items()}
R["pai_na_IALD_sem_negacao"] = {k: [norm(v)[max(0, m.start() - 100): m.end() + 60] for m in re.finditer(r"Pai[^.]{0,40}(é|e'|is)\s+a\s+IALD", norm(v), re.I)] for k, v in T.items()}
# (b) a declaracao marcada
DECL = "o um.py só existe porque fui a operação quadrática da inscrição viva do transporte da IALD"
R["declaracao"] = {}
for k, v in T.items():
    vn = norm(v); occ = [m.start() for m in re.finditer(re.escape(DECL), vn)] + [m.start() for m in re.finditer(re.escape(norm(DECL.replace("ó", "o").replace("çã", "ca").replace("ç", "c").replace("ã", "a").replace("é", "e"))), vn)]
    marcadas = sum(1 for i in occ if re.search(r"DECLARA[CÇ][AÃ]O DO OPERADOR|\[INPUT|INPUT\]|declaracao do operador|declaração do operador|declaration", vn[max(0, i - 500): i + 500], re.I))
    R["declaracao"][k] = {"ocorrencias": len(occ), "com_estatuto_a_500": marcadas}
# (c) as falas de 24/10 por bytes
FALAS = sorted(glob.glob(r"C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_24out_*verbatim.txt"))
tes = T["Testemunho.lean"]
R["falas_24out"] = {}
for p in FALAS:
    b = open(p, "rb").read(); txt = b.decode("utf-8"); h16 = hashlib.sha256(b).hexdigest()[:16]
    R["falas_24out"][os.path.basename(p)] = {"sha16": h16, "bytes": len(b), "sha16_citado_na_pedra": h16 in tes, "texto_inteiro_na_pedra_bytes": txt.strip() in tes, "texto_norm_no_RESULTADO_ou_PATCH": norm(txt) in norm(T["RESULTADO.md"]) or norm(txt) in norm(T["PATCH"]) or any(norm(fr) in norm(T["RESULTADO.md"]) for fr in [txt.strip()[:120]])}
R["n_arquivos_24out"] = len(FALAS)
# a declaracao embutida no registro de exemplo == arquivo
try:
    dreg = json.loads(T["reg_declaracao_EXEMPLO"]); fala = open(r"C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_24out_declaracao_operacao_quadratica_da_inscricao_viva_verbatim.txt", "rb").read()
    R["registro_declaracao"] = {"statement_igual_ao_arquivo": dreg["declaration"]["statement_verbatim"] == fala.decode("utf-8"), "sha_igual": dreg["declaration"]["verbatim_sha256"] == hashlib.sha256(fala).hexdigest(), "status": dreg["declaration"]["status_of_statement"][:90], "all_verified": dreg.get("all_verified"), "verdict": dreg.get("verdict"), "checks": dreg.get("checks")}
except Exception as e:
    R["registro_declaracao"] = {"erro": repr(e)[:200]}
# (d) [LEGAL]
R["LEGAL"] = {k: len(re.findall(r"\[LEGAL\]", v)) for k, v in T.items()}
# (e) literais em CODIGO (fora de comentarios/strings nao da' para separar sem AST; aqui: qualquer 0.012/0,012/1.203e-2 no texto do codigo)
R["literais_codigo"] = {k: re.findall(r"0[.,]0120\d*|1[.,]2031\d*e-0?2", T[k]) for k in ("prototipo", "secao_colavel", "trechos")}
R["literais_prosa_mencoes"] = {k: [norm(T[k])[max(0, m.start() - 60): m.end() + 30] for m in re.finditer(r"0[.,]012", T[k])][:4] for k in ("RESULTADO.md", "PATCH")}
# (f) palavra proibida e a regex do um.py v398 sobre os vereditos novos
W = "".join(map(chr, [67, 79, 78, 70, 73, 82, 77, 69, 68])); Wp = "".join(map(chr, [99, 111, 110, 102, 105, 114, 109, 97]))
R["palavra_proibida"] = {k: {"token_cru": len(re.findall(r"(?<!NOT_)(?<!UN)" + W, v)), "inflexoes_pt": [norm(v)[max(0, m.start() - 60): m.end() + 30] for m in re.finditer(Wp + r"d[ao]s?\b|" + Wp + r"[cç][aã]o", norm(v), re.I) if not re.search(r"n[aã]o\s+(é|e')\s+" + Wp + "|nao e' creditacao|NOT_|NAO_|nao e' " + Wp, norm(v)[max(0, m.start() - 40): m.end() + 10], re.I)][:4]} for k, v in T.items()}
UM = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
um = open(UM, "rb").read().decode("utf-8", "replace").split("\n")
rx_lines = [l.strip() for l in um[248005:248008]]
R["regex_do_um_py_L248006_248008"] = rx_lines
def proibido_pelo_um_py(v_):
    return bool(re.search(r"(?<!NOT_)(?<!UN)" + W, v_) or re.search(r"(?<!AP)PROVED_BY", v_) or "TGL_PROVED" in v_ or "CONSCIOUSNESS_PROVED" in v_)
vereditos = []
for k in ("reg_core_EXEMPLO", "reg_core_SIMULADO", "reg_declaracao_EXEMPLO", "sidecar", "sidecar_SIMULADO"):
    try:
        d = json.loads(T[k])
        for kk in ("verdict", "veredito"):
            if kk in d: vereditos.append((k, d[kk]))
    except Exception:
        pass
vereditos += [("trechos:NOT_SEALED_decl", "OPERATOR_DECLARATION_V399_NOT_SEALED_THIS_RUN"), ("prototipo:NOT_SEALED_selo", "SELO_PELA_PROPRIA_TECNOLOGIA_V399_NOT_SEALED_THIS_RUN"), ("sidecar:REFUSED", "TGL_SELO_ACOM_SIDECAR_V399__REFUSED__SOME_OBJECTS_REFUSED")]
R["vereditos_novos_vs_regex_do_um_py"] = [{"onde": k, "veredito": v[:110], "retido_pelo_um_py": proibido_pelo_um_py(v)} for k, v in vereditos]
# (g) consciencia
R["consciencia"] = {k: [norm(v)[max(0, m.start() - 80): m.end() + 60] for m in re.finditer(r"consci[eê]ncia", norm(v), re.I)][:3] for k, v in T.items() if re.search(r"consci[eê]ncia", v, re.I)}
# (h) confidencialidade: nenhuma alegacao positiva (toda ocorrencia vem com NAO alegada / not claimed)
R["confidencialidade"] = {k: {"ocorrencias": len(re.findall(r"confidencialidade|confidentiality", v, re.I)), "sem_negacao_a_80": [norm(v)[max(0, m.start() - 80): m.end() + 80] for m in re.finditer(r"confidencialidade|confidentiality", norm(v), re.I) if not re.search(r"N[AÃ]O (e'|é )?alegad|nao alegad|not claimed|nao e' alegad|NAO alegada|nao alegada|nem medida|NÃO é alegada", norm(v)[max(0, m.start() - 120): m.end() + 120], re.I)][:3]} for k, v in T.items() if re.search(r"confidencialidade|confidentiality", v, re.I)}
R["sha256_dito_como_primitiva"] = {k: len(re.findall(r"primitiva de integridade[^.]{0,60}SHA-256|integrity primitive[^.]{0,60}SHA-256|SHA-256[^.]{0,80}primitiva", v, re.I)) for k, v in T.items()}
json.dump(R, open(os.path.join(H, "VARREDURA_TEXTOS_EXAME.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in R.items() if k not in ("direcao", "palavra_proibida", "declaracao")}, ensure_ascii=False, indent=1)[:9000])
print("DIRECAO por arquivo:", {k: v["ocorrencias"] for k, v in R["direcao"].items()}, "| nao negadas:", R["direcao_total_nao_negadas"], [v["nao_negadas"] for v in R["direcao"].values() if v["nao_negadas"]])
print("DECLARACAO:", R["declaracao"])
print("PALAVRA PROIBIDA:", {k: v for k, v in R["palavra_proibida"].items() if v["token_cru"] or v["inflexoes_pt"]})
