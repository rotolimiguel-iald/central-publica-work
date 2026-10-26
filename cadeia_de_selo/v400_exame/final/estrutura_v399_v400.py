# -*- coding: utf-8 -*-
"""estrutura_v399_v400.py -- exame final v400 (c1, modelo forte, 24/10/2026): comparacao ESTRUTURAL e TEXTUAL entre a v399 instalada (A = Nos, so' lido)
e o candidato v400 (B), mais o censo do alfa (a contagem do esboco R3.5 pinado, com as regexes DELE, e o meu censo por AST de toda ligacao dos nomes
ALPHA_FINE_CODATA_2018 e SEALED_CODATA_ALPHA), o bloco do operador nos dois arquivos e as varreduras das linhas novas (beta/sqrt(e)/alfa literais, a palavra
proibida montada por codigo de caractere, atribuicao ao gate). So' le; escreve so' o json e o diff de saida.
uso: python -I -B -X utf8 estrutura_v399_v400.py <A.py> <B.py> <saida.json> <diff.txt>"""
import ast, json, re, sys, hashlib, difflib, importlib.util, os
A_, B_, S_, D_ = sys.argv[1:5]
ESB = r"C:\IALD\Central de Patentes\work\bancada_vinculo_12out\R3_5\sincronizar_bancada.py"
ESB_SHA16 = "02b22ba5c6d35c71"
rawA, rawB = open(A_, "rb").read(), open(B_, "rb").read()
sha = lambda b: hashlib.sha256(b).hexdigest()
R = {"A": {"path": A_, "sha16": sha(rawA)[:16], "bytes": len(rawA)}, "B": {"path": B_, "sha16": sha(rawB)[:16], "bytes": len(rawB)}}
sa, sb = rawA.decode("utf-8"), rawB.decode("utf-8")
# ---------------------------------------------------------------- 1. o esboco pinado e as regexes DELE (nada copiado)
eb = open(ESB, "rb").read()
assert sha(eb)[:16] == ESB_SHA16, "esboco R3.5 diverge do pino"
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("esboco_r35_exame", ESB); MOD = importlib.util.module_from_spec(spec); spec.loader.exec_module(MOD)
def contagem_do_esboco(raw):
    t = raw.decode("utf-8-sig")          # a MESMA decodificacao de ler_nos
    out = {"alfa_coluna0": len(MOD.RE_ALPHA_LINHAS.findall(t)), "alfa_indentada": len(MOD.RE_ALPHA_INDENTADA.findall(t)),
           "versao_coluna0": len(MOD.RE_VERSAO_LINHAS.findall(t)), "versao_indentada": len(MOD.RE_VERSAO_INDENTADA.findall(t))}
    out["linhas_alfa_coluna0"] = [t[:m.start()].count("\n") + 1 for m in MOD.RE_ALPHA_LINHAS.finditer(t)]
    a = MOD.RE_ALPHA.search(t); v = MOD.RE_VERSAO.search(t)
    out["primeira_linha_alfa_lida"] = (t[:a.start()].count("\n") + 1, a.group(1)) if a else None
    out["versao_lida"] = v.group(1) if v else None
    return out
R["esboco"] = {"path": ESB, "sha16": sha(eb)[:16], "revisao": MOD.REVISAO, "regex_alfa_linhas": MOD.RE_ALPHA_LINHAS.pattern, "regex_alfa_indentada": MOD.RE_ALPHA_INDENTADA.pattern}
R["contagem_do_esboco"] = {"A_v399": contagem_do_esboco(rawA), "B_v400": contagem_do_esboco(rawB)}
# ---------------------------------------------------------------- 2. AST
TA, TB = ast.parse(sa), ast.parse(sb)
def top(T):
    d, anon = {}, []
    for n in T.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name): d.setdefault(n.targets[0].id, []).append(n)
        elif isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name): d.setdefault(n.target.id, []).append(n)
        elif isinstance(n, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)): d.setdefault(n.name, []).append(n)
        else: anon.append(n)
    return d, anon
(dA, anA), (dB, anB) = top(TA), top(TB)
dumpsA = {k: [ast.dump(x) for x in v] for k, v in dA.items()}; dumpsB = {k: [ast.dump(x) for x in v] for k, v in dB.items()}
mud = sorted(k for k in dA if k in dB and dumpsA[k] != dumpsB[k])
uA, uB = [ast.unparse(n) for n in anA], [ast.unparse(n) for n in anB]
R["nos"] = {"n_nomeados_A": len(dA), "n_nomeados_B": len(dB), "iguais": sum(1 for k in dA if k in dB and dumpsA[k] == dumpsB[k]), "mudados": mud,
            "novos": sorted(set(dB) - set(dA)), "removidos": sorted(set(dA) - set(dB)),
            "nomes_com_mais_de_uma_ligacao_de_topo": {"A": sorted(k for k, v in dA.items() if len(v) > 1), "B": sorted(k for k, v in dB.items() if len(v) > 1)},
            "n_anonimos_A": len(uA), "n_anonimos_B": len(uB),
            "anonimos_so_A": [s[:400] for s in uA if s not in uB], "anonimos_so_B": [s[:400] for s in uB if s not in uA]}
DECLARADOS = {"UM_VERSION", "emit_canonical_md", "build_pt", "build_en", "_beta_runtime", "registro_core_v399", "selo_acom_v399"}
# o ALPHA_FINE_CODATA_2018 de topo: o top() junta as ligacoes por NOME; na A sao 2 (l.5584 e a redeclaracao da secao ACOM), na B tem de ser 1 == a 1a da A
_aA, _aB = dumpsA.get("ALPHA_FINE_CODATA_2018", []), dumpsB.get("ALPHA_FINE_CODATA_2018", [])
R["nos"]["alpha_A_2_ligacoes_B_1_igual_a_1a_da_A"] = len(_aA) == 2 and len(_aB) == 1 and _aB[0] == _aA[0]
R["nos"]["mudados_sem_o_alpha"] = sorted(set(mud) - {"ALPHA_FINE_CODATA_2018"})
R["nos"]["mudados_sao_exatamente_os_7_declarados"] = set(mud) - {"ALPHA_FINE_CODATA_2018"} == DECLARADOS and R["nos"]["alpha_A_2_ligacoes_B_1_igual_a_1a_da_A"]
# o ALPHA_FINE_CODATA_2018 de topo: na A sao 2 ligacoes (l.5584 e a redeclaracao); na B, 1 -- o top() junta por nome, entao o "removido" aparece como "mudado" se a 1a ligacao continua
R["nos"]["alpha_ligacoes_de_topo"] = {"A": [(n.lineno, ast.unparse(n)[:120]) for n in dA.get("ALPHA_FINE_CODATA_2018", [])], "B": [(n.lineno, ast.unparse(n)[:120]) for n in dB.get("ALPHA_FINE_CODATA_2018", [])]}
# os nos mudados: diff do unparse (build_pt/build_en/emit_canonical_md por linhas)
diffs = {}
for k in mud:
    la = "\n".join(ast.unparse(x) for x in dA[k]).splitlines(); lb = "\n".join(ast.unparse(x) for x in dB[k]).splitlines()
    dd = [l for l in difflib.unified_diff(la, lb, lineterm="", n=0) if l[:1] in "+-" and not l.startswith(("+++", "---"))]
    diffs[k] = {"n_menos": sum(1 for l in dd if l.startswith("-")), "n_mais": sum(1 for l in dd if l.startswith("+")), "linhas": [l[:700] for l in dd[:60]]}
R["diff_dos_nos_mudados"] = diffs
# ---------------------------------------------------------------- 3. censo por AST de TODA ligacao de alfa (topo e aninhada)
def censo(T, nomes=("ALPHA_FINE_CODATA_2018", "SEALED_CODATA_ALPHA")):
    out = {n: [] for n in nomes}
    for node in ast.walk(T):
        alvos = []
        if isinstance(node, ast.Assign): alvos = node.targets
        elif isinstance(node, (ast.AnnAssign, ast.AugAssign)): alvos = [node.target]
        elif isinstance(node, ast.NamedExpr): alvos = [node.target]
        elif isinstance(node, (ast.For, ast.AsyncFor, ast.comprehension)): alvos = [node.target]
        elif isinstance(node, (ast.With, ast.AsyncWith)): alvos = [it.optional_vars for it in node.items if it.optional_vars is not None]
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            for al in node.names:
                if (al.asname or al.name.split(".")[0]) in nomes: out[al.asname or al.name.split(".")[0]].append({"tipo": "import", "linha": node.lineno})
        elif isinstance(node, (ast.Global, ast.Nonlocal)):
            for nm in node.names:
                if nm in nomes: out[nm].append({"tipo": type(node).__name__, "linha": node.lineno})
        elif isinstance(node, ast.arg) and node.arg in nomes: out[node.arg].append({"tipo": "parametro", "linha": node.lineno})
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.name in nomes: out[node.name].append({"tipo": "def", "linha": node.lineno})
        for a in alvos:
            for m in ast.walk(a):
                if isinstance(m, ast.Name) and m.id in nomes and isinstance(m.ctx, ast.Store):
                    out[m.id].append({"tipo": type(node).__name__, "linha": node.lineno, "coluna": node.col_offset, "valor": ast.unparse(node)[:140]})
    # escrita indireta: globals()[...] / setattr(..., "ALPHA...") / vars()
    ind = []
    for node in ast.walk(T):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and node.value in nomes:
            ind.append(node.lineno)
    return out, ind
cA, iA = censo(TA); cB, iB = censo(TB)
R["censo_alfa_ast"] = {"A_v399": cA, "B_v400": cB, "literal_do_nome_em_string_A": iA, "literal_do_nome_em_string_B": iB}
# ---------------------------------------------------------------- 4. o bloco do operador (texto LF do primeiro INICIO ao marcador de FIM do acom_crypto), nos dois
def bloco(s):
    t = s.replace("\r\n", "\n"); i = t.index("# >>> ACOM_EMBUTIDO_INICIO"); mk = "# <<< ACOM_EMBUTIDO_FIM: skygrid_sim/acom_crypto.py <<<\n"; f = t.index(mk) + len(mk)
    return t[i:f]
bA, bB = bloco(sa), bloco(sb)
R["bloco_do_operador"] = {"sha256_A": sha(bA.encode("utf-8")), "sha256_B": sha(bB.encode("utf-8")), "igual_A_B": bA == bB, "linhas": bB.count("\n"),
                          "B_igual_ao_declarado_afc80b740f71ca0a": sha(bB.encode("utf-8")).startswith("afc80b740f71ca0a"),
                          "n_marcadores_inicio_B": sb.count("# >>> ACOM_EMBUTIDO_INICIO"), "n_marcadores_fim_B": sb.count("# <<< ACOM_EMBUTIDO_FIM")}
# ---------------------------------------------------------------- 5. o diff textual completo e as varreduras das linhas novas
LA, LB = sa.splitlines(), sb.splitlines()
ud = list(difflib.unified_diff(LA, LB, "v399_instalada", "v400_candidato", lineterm="", n=2))
open(D_, "w", encoding="utf-8").write("\n".join(ud) + "\n")
mais = [l[1:] for l in ud if l.startswith("+") and not l.startswith("+++")]
menos = [l[1:] for l in ud if l.startswith("-") and not l.startswith("---")]
R["diff_texto"] = {"linhas_A": len(LA), "linhas_B": len(LB), "n_mais": len(mais), "n_menos": len(menos), "arquivo": D_}
PAL = "".join(chr(c) for c in (67, 79, 78, 70, 73, 82, 77, 69, 68))
GUARDA = re.compile("(?<!NOT_)(?<!UN)" + PAL + "|(?<!AP)PRO" + "VED_BY|TGL_PRO" + "VED|CONSCIOUSNESS_PRO" + "VED")
RX = {"beta_literal": re.compile(r"0[.,]01203\d*|0[.,]012031|1[.,]2031\d*e-0?2"), "sqrt_e_literal": re.compile(r"1[.,]6487\d+"), "alfa_literal": re.compile(r"0[.,]0072973\d*|7[.,]29735\d*e-0?3|137[.,]035\d+"),
      "palavra_proibida_case": re.compile(PAL), "palavra_proibida_i": re.compile(PAL, re.I), "guarda_do_um_py": GUARDA,
      "gate_atribuicao": re.compile(r"qg_closure_verdict\s*=|\bgate\w*\s*\[[^\]]+\]\s*=|_FLAG\w*\s*=\s*True"), "assert_alfa": re.compile(r"assert\s+SEALED_CODATA_ALPHA")}
R["varredura_linhas_novas"] = {k: [l.strip()[:220] for l in mais if rx.search(l)] for k, rx in RX.items()}
R["varredura_linhas_removidas"] = {k: [l.strip()[:220] for l in menos if rx.search(l)] for k, rx in RX.items() if k in ("alfa_literal", "assert_alfa", "beta_literal")}
R["veredito"] = {"7_nos_declarados": R["nos"]["mudados_sao_exatamente_os_7_declarados"], "novos_0": R["nos"]["novos"] == [],
                 "alfa_esboco_B_1_linha_0_indentada": R["contagem_do_esboco"]["B_v400"]["alfa_coluna0"] == 1 and R["contagem_do_esboco"]["B_v400"]["alfa_indentada"] == 0,
                 "alfa_esboco_A_2_linhas": R["contagem_do_esboco"]["A_v399"]["alfa_coluna0"] == 2,
                 "versao_B_1_linha": R["contagem_do_esboco"]["B_v400"]["versao_coluna0"] == 1 and R["contagem_do_esboco"]["B_v400"]["versao_indentada"] == 0 and R["contagem_do_esboco"]["B_v400"]["versao_lida"] == "v400",
                 "censo_ast_B_alpha_1_ligacao": len(cB["ALPHA_FINE_CODATA_2018"]) == 1, "censo_ast_B_sealed_1_ligacao": len(cB["SEALED_CODATA_ALPHA"]) == 1,
                 "bloco_igual_e_afc80b74": R["bloco_do_operador"]["igual_A_B"] and R["bloco_do_operador"]["B_igual_ao_declarado_afc80b740f71ca0a"],
                 "sem_beta_literal_novo": not R["varredura_linhas_novas"]["beta_literal"] and not R["varredura_linhas_novas"]["sqrt_e_literal"],
                 "sem_alfa_literal_novo": not R["varredura_linhas_novas"]["alfa_literal"], "sem_palavra_proibida_nova": not R["varredura_linhas_novas"]["palavra_proibida_case"] and not R["varredura_linhas_novas"]["guarda_do_um_py"],
                 "sem_atribuicao_ao_gate_nova": not R["varredura_linhas_novas"]["gate_atribuicao"]}
json.dump(R, open(S_, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print(json.dumps(R["veredito"], ensure_ascii=False, indent=1))
print("mudados:", mud); print("novos:", R["nos"]["novos"], "removidos:", R["nos"]["removidos"]); print("anonimos so A:", len(R["nos"]["anonimos_so_A"]), "so B:", len(R["nos"]["anonimos_so_B"]))
print("contagem esboco:", json.dumps(R["contagem_do_esboco"], ensure_ascii=False)); print("censo ast B:", json.dumps(cB, ensure_ascii=False)[:800])
print("diff texto:", R["diff_texto"]); print("palavra proibida (i) nas novas:", R["varredura_linhas_novas"]["palavra_proibida_i"][:5])
