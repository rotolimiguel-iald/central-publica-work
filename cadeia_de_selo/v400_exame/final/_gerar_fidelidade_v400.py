# -*- coding: utf-8 -*-
"""_gerar_fidelidade_v400.py -- gera fidelidade_v400.py a partir do meu fidelidade_v399.py (substituicoes com contagem exata)."""
import ast, os
F9 = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v399_exame\final"
F10 = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v400_exame\final"
s = open(os.path.join(F9, "fidelidade_v399.py"), encoding="utf-8").read()


def sub(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:100], s.count(a), n)
    s = s.replace(a, b)


sub('"""fidelidade_v398.py -- exame final v398 (c1, 23/10/2026), item 3:', '"""fidelidade_v400.py -- exame final v400 (c1, 24/10/2026; molde: o meu fidelidade_v399.py), item 5:')
sub('V = r"C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v399"', 'V = r"C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v400"')
sub('CAND = os.path.join(V, "um_v399_candidato.py")', 'CAND = os.path.join(V, "um_v400_candidato.py")')
sub('"textos_v399_strings": "\\n\\n".join(sorted(strings(open(os.path.join(V, "pos_rito", "textos_v399.py"), "rb").read().decode("utf-8"))))}',
    '"textos_v400_strings": "\\n\\n".join(sorted(strings(open(os.path.join(V, "pos_rito", "textos_v400.py"), "rb").read().decode("utf-8"))))}')
sub('for nome, p, tit in (("artigo_pt_v399", os.path.join(V, "dry_v399", "dry_v399_pt.txt"), "O testemunho de dois: o selo pela própria tecnologia"), ("artigo_en_v399", os.path.join(V, "dry_v399", "dry_v399_en.txt"), "The testimony of two: sealing by its own technology")):',
    'for nome, p, tit in (("artigo_pt_v400", os.path.join(V, "dry_v400", "dry_v400_pt.txt"), "O testemunho de dois: o selo pela própria tecnologia"), ("artigo_en_v400", os.path.join(V, "dry_v400", "dry_v400_en.txt"), "The testimony of two: sealing by its own technology")):')
sub('t = open(os.path.join(V, "dry_v399", "um_absoluto_forma_canonica.md"), encoding="utf-8", errors="replace").read()\nSUP["md_ensaio_v399"] = "\\n\\n".join(x for x in re.split(r"\\n\\s*\\n", t) if re.search(r"v399|testemunho de dois|própria tecnologia", x))',
    't = open(os.path.join(V, "dry_v400", "um_absoluto_forma_canonica.md"), encoding="utf-8", errors="replace").read()\nSUP["md_ensaio_v400"] = "\\n\\n".join(x for x in re.split(r"\\n\\s*\\n", t) if re.search(r"v400|v399|testemunho de dois|própria tecnologia", x))')
sub('for p in sorted(glob.glob(os.path.join(H, "textos_renderizados_v399", "*.txt"))):', 'for p in sorted(glob.glob(os.path.join(H, "textos_renderizados_v400", "*.txt"))):')
sub('for nome, p in (("handoff_sb5_memory", os.path.join(H, "..", "sb5", "memory", "handoff-v399-custodia.md")), ("handoff_sb5_nos", os.path.join(H, "..", "sb5", "nos", "HANDOFF_v399_CUSTODIA.md"))):',
    'for nome, p in (("handoff_sb6_memory", os.path.join(H, "sb6", "memory", "handoff-v400-custodia.md")), ("handoff_sb6_nos", os.path.join(H, "sb6", "nos", "HANDOFF_v400_CUSTODIA.md"))):')
# as checagens especificas da v398/v399 (sexta inscricao, ratificacoes) saem; entram as da v400 (a errata: assinatura, atribuicao, a frase do alfa unico)
i = s.index("# a sexta inscricao rotulada; as ratificacoes na forma admitida")
j = s.index("W = \"\".join(map(chr, [67, 79, 78, 70, 73, 82, 77, 69, 68]))")
s = s[:i] + '''# v400: a errata (assinatura em nome proprio da gerencia; atribuicao do defeito a ADAPTACAO da gerencia, nao ao bloco do operador; a v399 fica selada como esta) e a frase do alfa unico
todo = "\\n".join(SUP.values()); tn = norm(todo)
ERR = re.compile(r"Errata ao lado \\(v400|Erratum beside it \\(v400|Errata ao lado \\(em nome pr[oó]prio da ger[eê]ncia c1", re.I)
R["errata_v400"] = {}
for k, v in SUP.items():
    vn = norm(v); hs = [m.start() for m in ERR.finditer(vn)]
    if not hs: continue
    R["errata_v400"][k] = {"ocorrencias": len(hs),
                           "assinada_em_nome_proprio_da_gerencia_a_200": sum(1 for h in hs if re.search(r"em nome pr[oó]prio da ger[eê]ncia|in the management'?s own name|assinad[ao] pela ger[eê]ncia", vn[h: h + 200], re.I)),
                           "atribui_a_adaptacao_da_gerencia_a_900": sum(1 for h in hs if re.search(r"adapta[cç][aã]o da ger[eê]ncia|c[oó]digo da ger[eê]ncia|management'?s code|na adapta[cç][aã]o da ger[eê]ncia", vn[h: h + 900], re.I)),
                           "diz_que_o_bloco_do_operador_nao_muda_a_1500": sum(1 for h in hs if re.search(r"bloco do operador[^.]{0,80}(n[aã]o muda|NAO muda|não no bloco)|n[aã]o no bloco do operador|operator'?s block[^.]{0,80}(does not change|not in)", vn[h: h + 1500], re.I)),
                           "diz_que_a_v399_fica_selada_a_900": sum(1 for h in hs if re.search(r"v399 fica selada|v399 stays sealed|ficam como registro", vn[h: h + 900], re.I))}
R["frase_alfa_unico"] = {k: [norm(v)[max(0, m.start() - 70): m.end() + 70] for m in re.finditer(r"uma s[oó] (declara[cç][aã]o|linha) de (α|\\$\\\\alpha\\$|alfa)|single (declaration|line) of|UMA s[oó] (declara[cç][aã]o|linha) de alfa", norm(v), re.I)][:3] for k, v in SUP.items() if re.search(r"uma s[oó] (declara[cç][aã]o|linha) de|single (declaration|line) of|UMA s[oó] (declara[cç][aã]o|linha) de alfa", norm(v), re.I)}
R["v399_dita_nao_selada_ou_invalida"] = {k: [norm(v)[max(0, m.start() - 90): m.end() + 60] for m in re.finditer(r"v399[^.]{0,60}(n[aã]o (foi )?selad|inv[aá]lid|not sealed|invalid)", norm(v), re.I)] for k, v in SUP.items() if re.search(r"v399[^.]{0,60}(n[aã]o (foi )?selad|inv[aá]lid|not sealed|invalid)", norm(v), re.I)}
''' + s[j:]
sub('json.dump(R, open(os.path.join(H, "FIDELIDADE_v399_%s.json" % R["candidato_sha16"]), "w", encoding="utf-8"), ensure_ascii=False, indent=1)',
    'json.dump(R, open(os.path.join(H, "FIDELIDADE_v400_%s.json" % R["candidato_sha16"]), "w", encoding="utf-8"), ensure_ascii=False, indent=1)')
ast.parse(s)
open(os.path.join(F10, "fidelidade_v400.py"), "w", encoding="utf-8").write(s)
print("ok")
