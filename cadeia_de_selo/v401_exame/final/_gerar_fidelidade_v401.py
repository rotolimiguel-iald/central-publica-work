# -*- coding: utf-8 -*-
"""_gerar_fidelidade_v401.py -- gera fidelidade_v401.py a partir do meu fidelidade_v400.py (substituicoes com contagem exata) + as checagens da v401."""
import ast, os
F10 = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v400_exame\final"; F11 = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v401_exame\final"
s = open(os.path.join(F10, "fidelidade_v400.py"), encoding="utf-8").read()


def sub(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:100], s.count(a), n); s = s.replace(a, b)


sub('"""fidelidade_v400.py -- exame final v400 (c1, 24/10/2026; molde: o meu fidelidade_v399.py), item 5:', '"""fidelidade_v401.py -- exame final v401 (c1, 25/10/2026; molde: o meu fidelidade_v400.py), item 2:')
sub('V = r"C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v400"', 'V = r"C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v401"')
sub('CAND = os.path.join(V, "um_v400_candidato.py")', 'CAND = os.path.join(V, "um_v401_candidato.py")')
sub('"textos_v400_strings": "\\n\\n".join(sorted(strings(open(os.path.join(V, "pos_rito", "textos_v400.py"), "rb").read().decode("utf-8"))))}', '"textos_v401_strings": "\\n\\n".join(sorted(strings(open(os.path.join(V, "pos_rito", "textos_v401.py"), "rb").read().decode("utf-8"))))}')
sub('for nome, p, tit in (("artigo_pt_v400", os.path.join(V, "dry_v400", "dry_v400_pt.txt"), "O testemunho de dois: o selo pela própria tecnologia"), ("artigo_en_v400", os.path.join(V, "dry_v400", "dry_v400_en.txt"), "The testimony of two: sealing by its own technology")):',
    'for nome, p, tit in (("artigo_pt_v401", os.path.join(V, "dry_v401", "dry_v401_pt.txt"), "A falsidade (simulacro) da inércia"), ("artigo_en_v401", os.path.join(V, "dry_v401", "dry_v401_en.txt"), "The falsity (simulacrum) of inertia")):')
sub('t = open(os.path.join(V, "dry_v400", "um_absoluto_forma_canonica.md"), encoding="utf-8", errors="replace").read()\nSUP["md_ensaio_v400"] = "\\n\\n".join(x for x in re.split(r"\\n\\s*\\n", t) if re.search(r"v400|v399|testemunho de dois|própria tecnologia", x))',
    't = open(os.path.join(V, "dry_v401", "um_absoluto_forma_canonica.md"), encoding="utf-8", errors="replace").read()\nSUP["md_ensaio_v401"] = "\\n\\n".join(x for x in re.split(r"\\n\\s*\\n", t) if re.search(r"v401|falsidade|inércia|simulacro", x))')
sub('for p in sorted(glob.glob(os.path.join(H, "textos_renderizados_v400", "*.txt"))):', 'for p in sorted(glob.glob(os.path.join(H, "textos_renderizados_v401", "*.txt"))):')
sub('for nome, p in (("handoff_sb6_memory", os.path.join(H, "sb6", "memory", "handoff-v400-custodia.md")), ("handoff_sb6_nos", os.path.join(H, "sb6", "nos", "HANDOFF_v400_CUSTODIA.md"))):',
    'for nome, p in (("handoff_sb7_memory", os.path.join(H, "sb7", "memory", "handoff-v401-custodia.md")), ("handoff_sb7_nos", os.path.join(H, "sb7", "nos", "HANDOFF_v401_CUSTODIA.md"))):')
i = s.index("# v400: a errata (assinatura em nome proprio da gerencia"); j = s.index('W = "".join(map(chr, [67, 79, 78, 70, 73, 82, 77, 69, 68]))')
NOVO = r'''# v401: a errata ao lado da leitura do escriba (assinada pela gerencia c1; SUPERADA), a parafrase sem aspas, «ONTO do operador» nunca para a CADEIA, a ORDEM 025 como pendencia externa, o recorte dito como recorte
todo = "\n".join(SUP.values()); tn = norm(todo)
R["errata_v401"] = {}
ERR = re.compile(r"Errata ao lado|Erratum beside|ERRATA AO LADO", re.I)
for k, v in SUP.items():
    vn = norm(v); hs = [m.start() for m in ERR.finditer(vn) if re.search(r"adendo|addendum|escriba|scribe|INÉRCIA|inércia|inertia", vn[m.start(): m.start() + 500], re.I)]
    if not hs: continue
    R["errata_v401"][k] = {"ocorrencias": len(hs), "assinada_gerencia_c1_a_250": sum(1 for h in hs if re.search(r"ger[eê]ncia c1|management, in its own name|gerencia c1|gerência, em nome próprio", vn[h: h + 250], re.I)),
                           "superada_a_900": sum(1 for h in hs if re.search(r"SUPERADA|superseded", vn[h: h + 900], re.I)),
                           "inercia_e_o_zero_a_900": sum(1 for h in hs if re.search(r"zero absoluto|absolute zero|0_abs", vn[h: h + 900], re.I)),
                           "adendo_sha_a_900": sum(1 for h in hs if "1459b477b496e1f0" in vn[h: h + 900])}
PAR = re.compile(r"tende ao (seu )?movimento por si|tends to its (own )?motion by itself", re.I)
R["parafrase"] = {k: [norm(v)[max(0, m.start() - 60): m.end() + 40] for m in PAR.finditer(norm(v))] for k, v in SUP.items() if PAR.search(norm(v))}
R["parafrase_entre_aspas"] = {k: [c for c in vs if re.search(r"[«“\"`]\s*(que )?tende ao (seu )?movimento por si", c)] for k, vs in R["parafrase"].items()}
ONTO = re.compile(r"ONTO (do|da|sua|minha) operador|ONTO do operador|\[ONTO\][^.]{0,80}(cadeia|chain)|(cadeia|chain)[^.]{0,80}\[ONTO\]", re.I)
R["onto_para_a_cadeia"] = {k: [norm(v)[max(0, m.start() - 120): m.end() + 80] for m in ONTO.finditer(norm(v)) if not re.search(r"n[aã]o (fosse|seja|e'|é) ?(\[)?ONTO|not be his \[ONTO\]|nao \[ONTO\]|não \[ONTO\]|DERIVED|derivad|INPUT/ONTO do operador, verbatim", norm(v)[max(0, m.start() - 120): m.end() + 80], re.I)] for k, v in SUP.items() if ONTO.search(norm(v))}
R["ordem_025"] = {k: {"ocorrencias": len(re.findall(r"ORDEM 025", v)), "como_pendencia_externa_a_300": sum(1 for m in re.finditer(r"ORDEM 025", norm(v)) if re.search(r"pend[eê]ncia EXTERNA|pendência externa|external pending|pendencia externa|enfileirada|fila|queued|external", norm(v)[max(0, m.start() - 300): m.end() + 300], re.I))} for k, v in SUP.items() if "ORDEM 025" in v}
R["recorte"] = {k: {"e26364c5": len(re.findall("e26364c5", v)), "dito_recorte_a_300": sum(1 for m in re.finditer("e26364c5", norm(v)) if re.search(r"recorte|excerpt|RECORTE", norm(v)[max(0, m.start() - 300): m.end() + 300], re.I))} for k, v in SUP.items() if "e26364c5" in v}
HT = re.compile(r"H_\\tau|H_tau|H_τ")
R["H_tau_nomeada_open_nao_usada"] = {k: {"H_tau": len(HT.findall(v)), "com_OPEN_a_300": sum(1 for m in HT.finditer(norm(v)) if "OPEN" in norm(v)[max(0, m.start() - 300): m.end() + 300]), "nenhum_teorema_usa_a_300": sum(1 for m in HT.finditer(norm(v)) if re.search(r"nenhum teorema (a )?usa|no theorem uses|nao usada por teorema|unused|não usada", norm(v)[max(0, m.start() - 300): m.end() + 300], re.I))} for k, v in SUP.items() if HT.search(v)}
'''
s = s[:i] + NOVO + s[j:]
sub('json.dump(R, open(os.path.join(H, "FIDELIDADE_v400_%s.json" % R["candidato_sha16"]), "w", encoding="utf-8"), ensure_ascii=False, indent=1)', 'json.dump(R, open(os.path.join(H, "FIDELIDADE_v401_%s.json" % R["candidato_sha16"]), "w", encoding="utf-8"), ensure_ascii=False, indent=1)')
ast.parse(s); open(os.path.join(F11, "fidelidade_v401.py"), "w", encoding="utf-8").write(s); print("gerado")
