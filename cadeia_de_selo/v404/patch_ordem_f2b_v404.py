# -*- coding: utf-8 -*-
"""patch_ordem_f2b_v404.py -- gerencia c1, 28/10/2026: corrige a ORDEM DE CHAMADA da errata de F2b na cadeia da v404 (licao da 1a tentativa do rito,
RECIBO_REVERSAO_20261028_201111.json). O bloco da chamada f2b_errata_v404 sai de «logo depois do Jo8v32» e vai para «logo depois da errata ao lado de R6
da v386» (quando ramo_b_preregistration_v386, ledger_errata_v386 e the_ledger_of_charges_v383 ja' estao no core). Toda frase que afirmava o ponto antigo
e' corrigida (o numero corrige a frase); o exame de pontos passa a exigir a ordem nova e a atribuicao previa dos insumos; o ensaio a seco ganha a guarda
estatica (guarda_ordem_de_chamada_v404.py). Backup de BYTES de cada arquivo antes; cada ancora ocorre EXATAMENTE uma vez (senao PARA sem gravar nada)."""
import os, re, sys, time
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__)); TS = time.strftime("%Y%m%d_%H%M%S")
P = lambda *a: os.path.join(H, *a)
NOVOS = {}   # path -> bytes (so' grava no fim, depois de TODOS os asserts)


def ler(p):
    return open(p, "rb").read().decode("utf-8")


def subst1(t, old, new, nome):
    assert t.count(old) == 1, ("ancora nao unica", nome, t.count(old), old[:90])
    return t.replace(old, new)


def preparar(p, t_novo, t_velho):
    assert t_novo != t_velho, ("nada mudou", p)
    NOVOS[p] = t_novo.encode("utf-8")


# ---------------- 1. gerar_candidato_v404.py ----------------
p = P("gerar_candidato_v404.py"); t0 = ler(p); t = t0
i_b = t.index("BLOCO_N00 = r'''"); i_m = t.index("    try:   # v404: a ERRATA AO LADO da cobranca F2b", i_b); i_e = t.index("'''", i_m)
assert t.count("    try:   # v404: a ERRATA AO LADO da cobranca F2b") == 1
f2b_block = t[i_m:i_e]; assert f2b_block.endswith("(_e404c,))\n") and "f2b_errata_v404(core)" in f2b_block
t = t[:i_m] + t[i_e:]
f2b_block = subst1(f2b_block, "lida logo depois do Jo8v32;",
                   "lida logo depois da errata ao lado de R6 da v386 (o V1 do ramo B, a errata da v386 e o livro da v383 ja' no core; licao da 1a tentativa do rito, 28/10/2026: chamada logo depois do Jo8v32 lia um core sem eles e recusava);", "comentario f2b")
m = re.search(r'^edit\(A_FAL\.end\(\), A_FAL\.end\(\), crlf\(BLOCO_N00\), "N00_main_tres_registros", "G_RUNTIME", "[^"]*"\)\n', t, re.M); assert m, "linha edit(N00) nao achada"
novo_edit = ('edit(A_FAL.end(), A_FAL.end(), crlf(BLOCO_N00), "N00_main_projecao_jo8v32", "G_RUNTIME", "main: projecao transversal e jo8v32 (try/AVISO cada), logo depois do bloco bandeiras_do_gate_v403.")\n'
             "A_F2B = linha_unica('^    ' + re.escape('print(\"   [v386] a errata ao lado de R6 e a cobranca F2b (o livro v383 intacto): %s\" % core[\"ledger_errata_v386\"][\"verdict\"])'))   # a ancora da errata de F2b: a ultima instrucao do bloco v386 (ramo B lido por hash + errata de R6)\n"
             "BLOCO_N00B = r'''" + f2b_block + "'''\n"
             'edit(A_F2B.end(), A_F2B.end(), crlf(BLOCO_N00B), "N00b_main_errata_f2b", "G_RUNTIME", "main: a errata de F2b (try/AVISO), logo depois da errata ao lado de R6 da v386: o V1 do ramo B, a errata da v386 e o livro da v383 ja\' estao no core (licao da 1a tentativa do rito, 28/10/2026).")\n')
t = t[:m.start()] + novo_edit + t[m.end():]
t = subst1(t, "(lidos depois das bandeiras do gate)", "(a projecao e o jo8v32 lidos depois das bandeiras do gate; a errata de F2b depois da errata ao lado de R6 da v386)", "print N01")
t = subst1(t, '"projecao_jo8_f2b_v404": "main: IMEDIATAMENTE depois do bloco bandeiras_do_gate_v403 (tres instrucoes try, na ordem projecao transversal, jo8v32, errata de F2b)"',
           '"projecao_jo8_v404": "main: IMEDIATAMENTE depois do bloco bandeiras_do_gate_v403 (duas instrucoes try, na ordem projecao transversal, jo8v32)", "f2b_v404": "main: IMEDIATAMENTE depois da errata ao lado de R6 da v386 (uma instrucao try; ramo_b_preregistration_v386, ledger_errata_v386 e the_ledger_of_charges_v383 ja\' atribuidos ao core; licao da 1a tentativa do rito, 28/10/2026)"', "manifesto ponto_de_chamada")
preparar(p, t, t0)

# ---------------- 2. runtime_v404.py (docstring) ----------------
p = P("runtime_v404.py"); t0 = ler(p)
t = subst1(t0, "lida logo depois do Jo8v32. Le o V1", "lida logo depois da errata ao lado de R6 da v386, quando o V1 do ramo B, a errata da v386 e o livro da v383 ja' estao no core (licao da 1a tentativa do rito v404, 28/10/2026). Le o V1", "docstring runtime")
preparar(p, t, t0)

# ---------------- 3. exame_pontos_v404.py e a regra de derivacao (regrasC), o MESMO texto nos dois ----------------
R1_OLD = '_ANTERIOR_V404C = ["bandeiras_do_gate_v403(core)", "projecao_transversal_v404(core)", "jo8v32_v404(core)"]\n'
R1_NEW = ('_ANTERIOR_V404C = {"projecao": "bandeiras_do_gate_v403(core)", "jo8v32": "projecao_transversal_v404(core)", "f2b": "a errata ao lado de R6 e a cobranca F2b"}\n'
          "# [licao da 1a tentativa do rito v404, 28/10/2026] a errata de F2b vem logo DEPOIS da errata ao lado de R6 da v386 e DEPOIS das tres atribuicoes do core que ela le\n"
          "# (ramo_b_preregistration_v386, ledger_errata_v386, the_ledger_of_charges_v383): chamada logo depois do Jo8v32 ela lia um core sem elas e recusava as 7 checagens\n"
          "_ATRIB_MAIN = {}\n"
          "for _ia, _sta in enumerate(main.body):\n"
          "    for _na in ast.walk(_sta):\n"
          "        if isinstance(_na, ast.Assign):\n"
          "            for _ta in _na.targets:\n"
          '                if isinstance(_ta, ast.Subscript) and isinstance(_ta.value, ast.Name) and _ta.value.id == "core" and isinstance(_ta.slice, ast.Constant) and isinstance(_ta.slice.value, str):\n'
          "                    _ATRIB_MAIN.setdefault(_ta.slice.value, _ia)\n"
          '_INSUMOS_F2B = ("ramo_b_preregistration_v386", "ledger_errata_v386", "the_ledger_of_charges_v383")\n')
R2_OLD = '("f2b", "f2b_errata_v404", 10)):'; R2_NEW = '("f2b", "f2b_errata_v404", None)):'
R3_OLD = '''    assert len(ii_) == 1 and ii_[0] == ifa + off_, ("a instrucao do main que chama %s nao e' unica ou nao vem na ordem, logo depois do bandeiras_do_gate_v403" % fn_, ii_, ifa)\n'''
R3_NEW = ('''    if off_ is not None:\n'''
          '''        assert len(ii_) == 1 and ii_[0] == ifa + off_, ("a instrucao do main que chama %s nao e' unica ou nao vem na ordem, logo depois do bandeiras_do_gate_v403" % fn_, ii_, ifa)\n'''
          '''    else:\n'''
          '''        _ins_ = {k_: _ATRIB_MAIN.get(k_) for k_ in _INSUMOS_F2B}\n'''
          '''        assert len(ii_) == 1 and all(v_ is not None and v_ < ii_[0] for v_ in _ins_.values()) and _ANTERIOR_V404C["f2b"] in unp[ii_[0] - 1], ("a instrucao do main que chama %s nao e' unica, nao vem logo depois da errata ao lado de R6 (v386) ou vem ANTES de um insumo do core que ela le" % fn_, ii_, _ins_)\n''')
R4_OLD = '"logo_depois_da_anterior": _ANTERIOR_V404C[off_ - 8] in unp[ii_ - 1],'; R4_NEW = '"logo_depois_da_anterior": _ANTERIOR_V404C[nome_] in unp[ii_ - 1],'
R5_OLD = '_ANTERIOR_V404C[nome_] in unp[ii_ - 1], "instrucao_anterior": unp[ii_ - 1][:160]'   # unica depois da R4 (os outros pontos de chamada usam a mesma chave)
R5_NEW = '_ANTERIOR_V404C[nome_] in unp[ii_ - 1], "insumos_do_core_atribuidos_antes": ({k_: {"indice": _ATRIB_MAIN.get(k_), "antes": (_ATRIB_MAIN.get(k_) is not None and _ATRIB_MAIN[k_] < ii_)} for k_ in _INSUMOS_F2B} if nome_ == "f2b" else None), "instrucao_anterior": unp[ii_ - 1][:160]'
R6_OLD = "as tres instrucoes do main (cada uma um `try`) que vem IMEDIATAMENTE depois do bandeiras_do_gate_v403, em ordem"
R6_NEW = "as duas instrucoes de pedra do main (cada uma um `try`) que vem IMEDIATAMENTE depois do bandeiras_do_gate_v403, em ordem, e a da errata de F2b, que vem IMEDIATAMENTE depois da errata ao lado de R6 da v386 (depois dos tres insumos do core que ela le)"
for nome in ("exame_pontos_v404.py", "derivar_encanamento_v404_regrasC.py"):
    p = P(nome); t0 = ler(p); t = t0
    for o_, n_, r_ in ((R1_OLD, R1_NEW, "R1"), (R2_OLD, R2_NEW, "R2"), (R3_OLD, R3_NEW, "R3"), (R4_OLD, R4_NEW, "R4"), (R5_OLD, R5_NEW, "R5"), (R6_OLD, R6_NEW, "R6")):
        t = subst1(t, o_, n_, nome + " " + r_)
    preparar(p, t, t0)

# ---------------- 4. ensaio_a_seco_v404.py: a guarda estatica ----------------
p = P("ensaio_a_seco_v404.py"); t0 = ler(p)
GUARDA = ("U = {}\n"
          "# (5b) [LICAO DA 1a TENTATIVA DO RITO v404, 28/10/2026] A ORDEM DE CHAMADA, estatica (guarda_ordem_de_chamada_v404.py): toda chave do core que uma funcao nova LE e que o main ATRIBUI tem de ser atribuida ANTES da chamada.\n"
          "# O fluxo (5) nao pega isto (core_s ja' traz as chaves da v403 selada); o rito real pegou: f2b_errata_v404, chamada logo depois do Jo8v32, leu um core sem ramo_b_preregistration_v386, ledger_errata_v386 e the_ledger_of_charges_v383 e RECUSOU as 7 checagens.\n"
          "import guarda_ordem_de_chamada_v404 as _GOC\n"
          "_ordem = _GOC.ordem_de_chamada(src, _GOC.FUNCOES_V404)\n"
          'rep["ordem_de_chamada_v404"] = _ordem\n'
          'U["v404_ordem_de_chamada_todo_insumo_do_core_atribuido_no_main_antes_da_leitura"] = bool(_ordem["ok"] and set((_ordem["funcoes"].get("f2b_errata_v404") or {}).get("insumos_atribuidos_no_main") or {}) >= set(_GOC.INSUMOS_EXIGIDOS["f2b_errata_v404"]))\n'
          'print("ordem de chamada (guarda estatica, licao da 1a tentativa):", _ordem["ok"], "| f2b lida depois de:", sorted((_ordem["funcoes"].get("f2b_errata_v404") or {}).get("insumos_atribuidos_no_main") or {}))\n')
t = subst1(t0, "\nU = {}\n", "\n" + GUARDA, "ensaio U = {}")
preparar(p, t, t0)

# ---------------- 5. rito_v404.sh (comentario) ----------------
p = P("rito_v404.sh"); t0 = ler(p)
t = subst1(t0, "(chamados no main logo depois do bandeiras_do_gate_v403; a errata de F2b e' AO LADO:",
           "(a projecao e o jo8v32 chamados no main logo depois do bandeiras_do_gate_v403; a errata de F2b logo depois da errata ao lado de R6 da v386, quando o V1 do ramo B e o livro da v383 ja' estao no core -- licao da 1a tentativa, 28/10; a errata de F2b e' AO LADO:", "rito.sh comentario")
preparar(p, t, t0)

# ---------------- 6. os textos do pos-rito exigem os ids dos patches ----------------
for nome in (os.path.join("pos_rito", "textos_v404.py"), os.path.join("pos_rito", "textos_v404_novo.pysnip")):
    p = P(nome); t0 = ler(p)
    t = subst1(t0, '"N00_main_tres_registros", "N01_main_specs"', '"N00_main_projecao_jo8v32", "N00b_main_errata_f2b", "N01_main_specs"', nome + " ids")
    preparar(p, t, t0)

# ---------------- 7. as duas frases descritivas ----------------
p = P("derivar_encanamento_v404.py"); t0 = ler(p)
t = subst1(t0, "lidos no main logo depois do bandeiras_do_gate_v403", "lidos no main (os dois de pedra logo depois do bandeiras_do_gate_v403; a errata de F2b logo depois da errata ao lado de R6 da v386, depois dos insumos que ela le -- licao da 1a tentativa do rito, 28/10)", "derivar_encanamento (c)")
preparar(p, t, t0)
p = P("comparar_v403_v404.py"); t0 = ler(p)
t = subst1(t0, '"main": "N00/N01/N02: as chamadas dos tres registros com funcao (projecao transversal, jo8v32, errata de F2b)', '"main": "N00/N00b/N01/N02: as chamadas dos tres registros com funcao (projecao transversal e jo8v32 depois das bandeiras do gate; a errata de F2b depois da errata ao lado de R6 da v386)', "comparar EXPLICACOES")
preparar(p, t, t0)

# ---------------- gravar: backup de BYTES -> temporario -> conferir -> substituir ----------------
for p, b in NOVOS.items():
    old = open(p, "rb").read(); bak = p + ".bak_" + TS
    open(bak, "wb").write(old); assert open(bak, "rb").read() == old
    tmp = p + ".tmp_" + TS; open(tmp, "wb").write(b); assert open(tmp, "rb").read() == b; os.replace(tmp, p)
    print("GRAVADO %-60s %8d -> %8d B  (backup %s)" % (os.path.relpath(p, H), len(old), len(b), os.path.basename(bak)))
# o que ainda afirma o ponto antigo (fora do candidato velho, dos pinos derivados, das tentativas, dos dry e dos backups)
rest = []
for root, _, fs in os.walk(H):
    if any(x in root for x in ("tentativa_v404", "dry_", "conferidor_import", "harness_saida", "__pycache__", "base_v403", "falso_nos", "arvore_simulada")):
        continue
    for f in fs:
        if f.endswith((".py", ".pysnip", ".sh")) and ".bak_" not in f and f not in ("um_v404_candidato.py", "v404_pins.py", "patch_ordem_f2b_v404.py"):
            try:
                tt = ler(os.path.join(root, f))
            except UnicodeDecodeError:
                continue
            for frase in ("logo depois do bandeiras_do_gate_v403; a errata", "lida logo depois do Jo8v32", "lidos depois das bandeiras do gate)", "N00_main_tres_registros"):
                if frase in tt:
                    rest.append((os.path.relpath(os.path.join(root, f), H), frase))
print("restam afirmando o ponto antigo:", rest if rest else "nenhum")
