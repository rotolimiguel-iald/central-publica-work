# -*- coding: utf-8 -*-
"""exame_artigo_v388.py -- exame do ARTIGO emitido pela v388 (SO LEITURA do Nos): sumario PT/EN, front matter, inventario de «pos-dicao»,
lista de incorporacao item a item (linha do txt), PDF (paginas, mtime). Saida: EXAME_ARTIGO_v388.json."""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
R = {"arquivos": {}, "achados": [], "toc": {}, "incorporacao": {}, "pos_dicao": {}}
def achado(cat, grav, lingua, linha, evid, nota=""):
    R["achados"].append({"categoria": cat, "gravidade": grav, "lingua": lingua, "linha": linha, "evidencia": evid[:400], "nota": nota})
TX = {}
for l in ("pt", "en"):
    for ext in ("txt", "tex", "toc", "pdf"):
        p = os.path.join(NOS, "um_absoluto_%s.%s" % (l, ext)); b = open(p, "rb").read()
        R["arquivos"]["%s.%s" % (l, ext)] = {"sha16": hashlib.sha256(b).hexdigest()[:16], "bytes": len(b), "mtime": os.path.getmtime(p)}
        if ext == "pdf":
            R["arquivos"]["%s.pdf" % l]["paginas_por_Type_Page"] = len(re.findall(rb"/Type\s*/Page(?!s)", b))
    TX[l] = open(os.path.join(NOS, "um_absoluto_%s.txt" % l), encoding="utf-8", errors="replace").read().split("\n")
um_mtime = os.path.getmtime(os.path.join(NOS, "rodada_v388_stdout.txt"))
for k, v in R["arquivos"].items():
    if v["mtime"] < um_mtime - 6 * 3600:
        achado("arquivo_antigo", "CORRIGIR", k[:2], None, "%s mais velho que a rodada v388" % k)
def acha(l, rx, ini=1, fim=None):
    P = re.compile(rx); out = []
    for i, s in enumerate(TX[l][ini - 1: fim], ini):
        m = P.search(s)
        if m:
            out.append((i, s[max(0, m.start() - 90): m.end() + 90]))
    return out
# (1) SUMARIO
for l in ("pt", "en"):
    t = open(os.path.join(NOS, "um_absoluto_%s.toc" % l), encoding="utf-8", errors="replace").read()
    ents = re.findall(r"\\contentsline \{(\w+)\}\{(.*?)\}\{(\d+)\}", t); tits = [e[1] for e in ents]
    req = ({"Ao lado (v388)": r"^Ao lado \(v388\)", "Tres testes (v387)": r"^Os três testes de estresse", "Ao lado (v387)": r"^Ao lado \(v387\)", "Ao lado (v386)": r"^Ao lado \(v386\)",
            "Ao lado (v385)": r"^Ao lado \(v385\)", "Introducao": r"^Introdução", "Nota GPU": r"^Nota: o que se calcula na GPU"} if l == "pt" else
           {"Beside (v388)": r"^Beside \(v388\)", "Three tests (v387)": r"^The three stress tests", "Beside (v387)": r"^Beside \(v387\)", "Beside (v386)": r"^Beside \(v386\)",
            "Beside (v385)": r"^Beside \(v385\)", "Introduction": r"^Introduction", "Note GPU": r"^Note: what is computed on the GPU"})
    R["toc"][l] = {"n_entradas": len(ents), "presentes": {k: [i for i, x in enumerate(tits) if re.search(v, x)] for k, v in req.items()}}
    for k, v in R["toc"][l]["presentes"].items():
        if len(v) != 1:
            achado("sumario", "CORRIGIR", l, None, "%s: %d entradas no .toc" % (k, len(v)))
    # cada \section* com addcontentsline no txt (marcador tocsection) tem de estar no .toc
    secs = [s.split("tocsection", 1)[1].strip() for s in TX[l] if s.startswith("tocsection")]
    R["toc"][l]["tocsection_no_txt"] = len(secs)
    # versao datada nos titulos
    for x in tits:
        if re.search(r"agora \(v38[0-7]\)|now \(v38[0-7]\)", x):
            achado("versao_datada_no_titulo", "CORRIGIR", l, None, x, "o titulo afirma 'agora' com versao anterior a v388")
# (2) FRONT MATTER (ate a Parte A)
for l in ("pt", "en"):
    pa = [i for i, s in enumerate(TX[l], 1) if re.match(r"^(Parte A|Part A) ---", s)]
    fim = pa[0] if pa else 80; R.setdefault("front_matter_ate_linha", {})[l] = fim
    fm = "\n".join(TX[l][:fim])
    R.setdefault("front_matter", {})[l] = {"tem_6154": "6154" in fm, "tem_GPU_ou_GKLS": bool(re.search(r"GPU|GKLS", fm)), "tem_POSTO": bool(re.search(r"\bposto\b|POSTO|\bposited\b|POSITED|\bposed\b", fm)),
                                           "data_da_rodada": TX[l][4] if len(TX[l]) > 4 else None}
    for i, s in acha(l, r"único postulado|single postulate|um só postulado|one postulate", 1, fim):
        achado("front_matter_postulado_vs_POSTO", "CORRIGIR", l, i, s, "o operador decidiu (05/10) a etiqueta [POSTO] para omega(I)=1: posto, nao postulado (imposto); o resumo ainda diz 'postulado'")
    for i, s in acha(l, r"Palavras-chave|Keywords", 1, fim):
        R["front_matter"][l]["palavras_chave_linha"] = i
        R["front_matter"][l]["palavras_chave_tem_GPU_GKLS"] = bool(re.search(r"GPU|GKLS", TX[l][i - 1]))
# (3) POS-DICAO
for l, rx in (("pt", r"p[óo]s-?di[çc]{1,2}[ãa]o|pós-ditad"), ("en", r"post-?diction|postdict")):
    occ = acha(l, rx); R["pos_dicao"][l] = [{"linha": i, "trecho": s} for i, s in occ]
    for i, s in occ:
        if not re.search(r"não é|nunca|is not|never|onde se lia|where it read|retrodição|retrodiction|''", s):
            achado("pos_dicao_como_demerito", "CORRIGIR", l, i, s)
# (4) INCORPORACAO
ITENS = [
 ("livro de cobrancas v383", r"livro de cobranças", r"ledger of charges|charge ledger|ledger"),
 ("pilar quantico v384", r"pilar quântico", r"quantum pillar"),
 ("Axioma / testemunha falsa v385", r"testemunha falsa", r"false witness"),
 ("[POSTO] (posto, nao postulado)", r"\[POSTO\]|POSTO|\bposto\b", r"\[POSTO\]|POSTO|posited"),
 ("Verbo v386 (o Verbo seleciona)", r"Verbo seleciona", r"Verb selects"),
 ("ramo B reaberto", r"ramo B reaberto|ramo B", r"branch B reopened|branch B"),
 ("V1 do ramo B por hash", r"ramo B.{0,400}(hash|sha)", r"branch B.{0,400}(hash|sha)"),
 ("tres testes conjuntos", r"três testes", r"three stress tests|three tests"),
 ("duas probabilidades", r"duas probabilidades|probabilidade conjunta", r"two probabilities|joint probability"),
 ("retrodicao sem ajuste / novidade de uso", r"retrodição sem ajuste", r"retrodiction without adjustment"),
 ("Mercurio", r"Mercúrio", r"Mercury"),
 ("Fase 8: N_eff 0,1195", r"0,1195", r"0\.1195"),
 ("Fase 8: veredito/poder dito", r"poder de hoje é \$?1,00", r"(?i)power today is \$?1\.00|today's power is \$?1\.00"),
 ("Fase 9: ln B 9,17", r"9,17", r"9\.17"),
 ("Fase 9: z_disc 4,28", r"4,28", r"4\.28"),
 ("Fase 9: INCONCLUSIVE", r"FASE9_ RAZAO_ DE_ HUBBLE_ V1_ _ INCONCLUSIVE|FASE9_RAZAO_DE_HUBBLE_V1__INCONCLUSIVE", r"FASE9_ RAZAO_ DE_ HUBBLE_ V1_ _ INCONCLUSIVE|FASE9_RAZAO_DE_HUBBLE_V1__INCONCLUSIVE"),
 ("Fase 9: contrafactual", r"contrafactual", r"counterfactual"),
 ("beta escalar limitado inferiormente", r"limitado inferiormente", r"bounded below"),
 ("beta_0 (constante da fronteira)", r"β_0=α_ ?Thomson|β_0", r"β_0=α_ ?Thomson|β_0"),
 ("Teorema da Escala", r"Teorema da Escala", r"Scale Theorem"),
 ("Zenao (nome)", r"Zen[ãa]o|Zeno", r"Zeno"),
 ("soma das metades (a operacao de Zenao)", r"soma das metades", r"sum of the halves"),
 ("Meia-Nat ponto fixo", r"Meia-Nat é o ponto fixo", r"Half-Nat is the fixed point"),
 ("errata alpha observa-se nao se deriva", r"observa-se, não se deriva", r"is observed, not derived"),
]
for nome, rpt, ren in ITENS:
    R["incorporacao"][nome] = {}
    for l, rx in (("pt", rpt), ("en", ren)):
        occ = acha(l, rx)
        R["incorporacao"][nome][l] = {"n": len(occ), "primeira_linha": occ[0][0] if occ else None, "trecho": occ[0][1] if occ else None}
        if not occ:
            g = "NOTA" if nome.startswith("Zenao (nome)") else "CORRIGIR"
            achado("incorporacao_ausente", g, l, None, nome, "regex %s sem ocorrencia" % rx)
# (5) secoes datadas que dizem 'nada foi aberto' para a Fase 9 (superadas pela v388) -- coerencia entre secoes
for l, rx in (("pt", r"Nada foi aberto"), ("en", r"Nothing was opened|Nothing has been opened")):
    for i, s in acha(l, rx):
        achado("secao_v387_superada_pela_v388", "NOTA", l, i, s, "secao datada (v387); a v388 (acima) registra a abertura; sem remissao cruzada")
R["resumo"] = {}
for a in R["achados"]:
    R["resumo"][a["gravidade"]] = R["resumo"].get(a["gravidade"], 0) + 1
p = os.path.join(HERE, "EXAME_ARTIGO_v388.json")
open(p + ".tmp", "w", encoding="utf-8").write(json.dumps(R, ensure_ascii=False, indent=1, default=str)); os.replace(p + ".tmp", p)
print(json.dumps({"resumo": R["resumo"], "toc": R["toc"], "front_matter": R["front_matter"], "pos_dicao_n": {k: len(v) for k, v in R["pos_dicao"].items()},
                  "incorporacao": {k: {l: (v[l]["n"], v[l]["primeira_linha"]) for l in v} for k, v in R["incorporacao"].items()},
                  "achados": R["achados"]}, ensure_ascii=False, indent=1))
