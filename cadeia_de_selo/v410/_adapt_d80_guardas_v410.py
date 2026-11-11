# -*- coding: utf-8 -*-
"""_adapt_d80_guardas_v410.py -- D80 nas guardas ESTATICAS da parte 1 (D82): guarda_ordem_de_chamada_v410.py (o h0dn_fontes_hms13_v410 em FUNCOES_NOVAS_V410, MECANICA_DE, COMUNS_DE, INSUMOS_EXIGIDOS; controles (15) sem a chamada e (16) trocado de lugar com a instrucao
do iald2/h0dn), comparar_v409_v410.py (os nos novos do HMS/13; o patch N00_main_iald2_h0dn_hms13; o main com DUAS instrucoes; o .md com TRES linhas; o selo com QUATRO chaves) e _prevoo_gerador_v410.py (o contrato do HMS/13, o runtime emendado, os nomes novos, os sha16).
Backup de bytes; trocas exatas; ast.parse; idempotente por arquivo."""
import ast, datetime, hashlib, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def aplica(nome, marca, trocas, regex=()):
    p = os.path.join(HERE, nome); b0 = open(p, "rb").read(); t = b0.decode("utf-8")
    if marca in t:
        print(nome, ": ja' aplicado"); return
    open(p + ".bak_" + TS + "_d80", "wb").write(b0); assert open(p + ".bak_" + TS + "_d80", "rb").read() == b0
    for a, b in trocas:
        c = t.count(a); assert c == 1, (nome, c, a[:120]); t = t.replace(a, b)
    for rx, rep in regex:
        t, n = re.subn(rx, rep, t, flags=re.S); assert n == 1, (nome, rx[:80], n)
    assert marca in t
    nb = t.encode("utf-8"); ast.parse(nb)
    open(p + ".tmp", "wb").write(nb); assert os.path.getsize(p + ".tmp") == len(nb); os.replace(p + ".tmp", p)
    print(nome, len(b0), "->", len(nb), "| sha16", hashlib.sha256(nb).hexdigest()[:16])


# ---- guarda_ordem_de_chamada_v410.py
aplica("guarda_ordem_de_chamada_v410.py", "hms13_antes_do_h0dn_reprova", [
    ('FUNCOES_NOVAS_V410 = ("iald2_v410", "h0dn_bg1_v410")', 'FUNCOES_NOVAS_V410 = ("iald2_v410", "h0dn_bg1_v410", "h0dn_fontes_hms13_v410")'),
    ('MECANICA_DE["h0dn_bg1_v410"] = "_v410_h0dn_mechanics"   # (v410, D72)\n', 'MECANICA_DE["h0dn_bg1_v410"] = "_v410_h0dn_mechanics"   # (v410, D72)\nMECANICA_DE["h0dn_fontes_hms13_v410"] = "_v410_hms13_mechanics"   # (v410, D80: o recibo documental HMS/13, na instrucao SEGUINTE do main)\n'),
    ('             "h0dn_bg1_v410": ("_v398_beta",)}', '             "h0dn_bg1_v410": ("_v398_beta",),\n             "h0dn_fontes_hms13_v410": ("_v398_beta",)}   # (v410, D80) o miolo comum do hms13: le qg_closure, beta e core["h0dn_bg1_v410"] (gravado na instrucao ANTERIOR do main: por isso a instrucao e\' separada)'),
    ('                    "iald2_v410": ("traducao_turing_v409",', '                    "h0dn_fontes_hms13_v410": ("iald2_v410", "h0dn_bg1_v410", "traducao_turing_v409", "_v409_rodar_specs", "tetelestai_terminal_v408", "_v408_rodar_specs", "psion_canto_v407", "_v407_rodar_specs", "fechamento_v406", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "witness_layers"),   # (v410, D80) o hms13 e\' chamado na instrucao SEGUINTE a\' do iald2/h0dn: le core["h0dn_bg1_v410"]\n'
     '                    "iald2_v410": ("traducao_turing_v409",'),
    ('    r13 = ordem_de_chamada("\\n".join(m14_), ("h0dn_bg1_v410",))\n',
     '    r13 = ordem_de_chamada("\\n".join(m14_), ("h0dn_bg1_v410",))\n'
     '    # (15) [v410, D80] a chamada do h0dn_fontes_hms13_v410 sai do main (a linha traz comentario: troca por prefixo); (16) a instrucao do hms13 trocada de lugar com a do iald2/h0dn reprova (o insumo h0dn_bg1_v410 passa a vir depois)\n'
     '    _lf = [i for i, l in enumerate(linhas) if re.match(r"\\s+_f410 = h0dn_fontes_hms13_v410\\(core\\)", l)]; assert len(_lf) == 1, ("a linha da chamada do h0dn_fontes_hms13_v410 nao foi achada uma vez", _lf)\n'
     '    m15_ = list(linhas); m15_[_lf[0]] = m15_[_lf[0]].replace("h0dn_fontes_hms13_v410(core)", "{}", 1)\n'
     '    r14 = ordem_de_chamada("\\n".join(m15_), ("h0dn_fontes_hms13_v410",))\n'
     '    r15 = ordem_de_chamada(_troca_blocos(src, "h0dn_bg1_v410", "h0dn_fontes_hms13_v410"), ("h0dn_fontes_hms13_v410",))\n'
     '    f15_ = r15["funcoes"].get("h0dn_fontes_hms13_v410") or {}\n'),
    ('         "h0dn_sem_chamada_no_main_reprova": bool(not r13["ok"] and "erro" in (r13["funcoes"].get("h0dn_bg1_v410") or {}))}',
     '         "h0dn_sem_chamada_no_main_reprova": bool(not r13["ok"] and "erro" in (r13["funcoes"].get("h0dn_bg1_v410") or {})),\n'
     '         "hms13_sem_chamada_no_main_reprova": bool(not r14["ok"] and "erro" in (r14["funcoes"].get("h0dn_fontes_hms13_v410") or {})), "hms13_antes_do_h0dn_reprova": bool(not r15["ok"] and "h0dn_bg1_v410" in (f15_.get("insumos_exigidos_ausentes") or []))}'),
])
# ---- comparar_v409_v410.py
aplica("comparar_v409_v410.py", "_V410_HMS13_INSUMOS", [
    ('e a dos registros por spec da v410 (logo depois do bloco do traducao_turing_v409 e dos specs da v409, antes de emit_figures; try/AVISO) e as chaves novas do selo (iald2_v410, h0dn_bg1_v410, registros_v410); nada do que existia muda"',
     ', a do `h0dn_fontes_hms13_v410` (D80: o recibo documental HMS/13, aditivo e posterior ao FREEZE_R2, na instrucao SEGUINTE, com os registros por spec da v410; tudo logo depois do bloco do traducao_turing_v409 e dos specs da v409, antes de emit_figures; try/AVISO em cada instrucao) e as chaves novas do selo (iald2_v410, h0dn_bg1_v410, h0dn_fontes_hms13_v410, registros_v410); nada do que existia muda"'),
    ('"W09: as linhas «IALD2 (v410, 06/11/2026)» e «H0DN × BG1 pré-registrado (v410, 09/11/2026)» (com a obrigacao D72) no .md canonico,',
     '"W09: as linhas «IALD2 (v410, 06/11/2026)», «H0DN × BG1 pré-registrado (v410, 09/11/2026)» (com a obrigacao D72) e «Recibo documental HMS/13 (v410, 09/11/2026; D80)» (com a obrigacao D80) no .md canonico,'),
    ('"N00_main_iald2_h0dn": ["main"]', '"N00_main_iald2_h0dn_hms13": ["main"]'),
    ('"_V410_H0DN_CONTRACT", "_V410_H0DN_TEXT", "_V410_H0DN_INSUMOS"}', '"_V410_H0DN_CONTRACT", "_V410_H0DN_TEXT", "_V410_H0DN_INSUMOS", "_v410_hms13_numeros", "_v410_hms13_mechanics", "_V410_HMS13_RECUSA", "_V410_HMS13_CONTRACT", "_V410_HMS13_TEXT", "_V410_HMS13_INSUMOS"}'),
    ('ops[0][4] - ops[0][3] == 2   # (09/11, D72: DUAS linhas', 'ops[0][4] - ops[0][3] == 3   # (09/11, D72 e D80: TRES linhas'),
    ('return {"duas_linhas_inseridas_e_nada_removido": ok1,', 'return {"tres_linhas_inseridas_e_nada_removido": ok1, "traz_o_texto_do_hms13_com_a_obrigacao": ("Recibo documental HMS/13 (v410" in txt) and (DL.FRASE_HMS13_OBRIGATORIA_PT in txt), "a_linha_do_h0dn_vem_antes_da_do_hms13": 0 <= txt.find("H0DN × BG1 pré-registrado (v410") < txt.find("Recibo documental HMS/13 (v410"),'),
    ('ok_ins = len(ins) == 1 and ins[0][4] - ins[0][3] == 1 and ins[0][1] == ins[0][2]', 'ok_ins = len(ins) == 1 and ins[0][4] - ins[0][3] == 2 and ins[0][1] == ins[0][2]   # (D80: DUAS instrucoes inseridas juntas: iald2/h0dn; hms13/specs)'),
    ('    txt = ast.unparse(b[ins[0][3]]) if ok_ins else ""\n', '    txt = "\\n".join(ast.unparse(x_) for x_ in b[ins[0][3]:ins[0][4]]) if ok_ins else ""\n'),
    ('return {"um_unico_bloco_inserido": ok_ins, "o_bloco_chama_iald2_v410_o_h0dn_bg1_v410_e_os_specs_nesta_ordem": "iald2_v410(core)" in txt and "h0dn_bg1_v410(core)" in txt and "_v410_rodar_specs(core)" in txt and 0 <= txt.find("iald2_v410(core)") < txt.find("h0dn_bg1_v410(core)") < txt.find("_v410_rodar_specs(core)"),',
     'return {"um_unico_bloco_de_duas_instrucoes_inserido": ok_ins, "as_duas_instrucoes_chamam_iald2_h0dn_hms13_e_os_specs_nesta_ordem": "iald2_v410(core)" in txt and "h0dn_bg1_v410(core)" in txt and "h0dn_fontes_hms13_v410(core)" in txt and "_v410_rodar_specs(core)" in txt and 0 <= txt.find("iald2_v410(core)") < txt.find("h0dn_bg1_v410(core)") < txt.find("h0dn_fontes_hms13_v410(core)") < txt.find("_v410_rodar_specs(core)"),'),
    ('"o_selo_so_ganha_as_tres_chaves_da_v410": bool(sel) and sel["chaves_da_base_preservadas_na_ordem"] and sel["valores_da_base_iguais"] and sorted(sel["chaves_novas"]) == sorted(["iald2_v410", "h0dn_bg1_v410", "registros_v410"])',
     '"o_selo_so_ganha_as_quatro_chaves_da_v410": bool(sel) and sel["chaves_da_base_preservadas_na_ordem"] and sel["valores_da_base_iguais"] and sorted(sel["chaves_novas"]) == sorted(["iald2_v410", "h0dn_bg1_v410", "h0dn_fontes_hms13_v410", "registros_v410"])'),
])
# ---- _prevoo_gerador_v410.py
aplica("_prevoo_gerador_v410.py", "registros_hms13_v410 as RF", [
    ('import registros_h0dn_v410 as RH  # noqa: E402\n', 'import registros_h0dn_v410 as RH  # noqa: E402\nimport registros_hms13_v410 as RF  # noqa: E402   (D80)\n'),
    ('CONTR_H = RH.contrato_h0dn(core0, selo0); TXT_H = RH.texto_h0dn(); INS_H = RH.insumos_embutidos()\n',
     'CONTR_H = RH.contrato_h0dn(core0, selo0); TXT_H = RH.texto_h0dn(); INS_H = RH.insumos_embutidos()\n'
     'CONTR_F = RF.contrato_hms13(core0, selo0, CONTR_H); TXT_F = RF.texto_hms13(); INS_F = RF.insumos_embutidos_hms13()\n'
     'chk("contrato HMS13 (D80): 12 checagens, gate, 4 insumos, 6 pinos do build relidos, guarda numerica, nada lido em rito, os dez campos", CONTR_F["n_checks"] == DL.N_CHECKS_HMS13 == 12 and CONTR_F["baseline"]["gate_verdict"] == selo0.get("qg_closure_verdict") and set(CONTR_F["insumos"]) == set(INS_F) and len(CONTR_F["pinos_build"]) == 6 and CONTR_F["guarda_numerica_no_build"]["ok"] is True and CONTR_F["le_em_rito"] is False and CONTR_F["campos"] == DL.HMS13_CAMPOS and "vibrato" not in json.dumps([CONTR_F, TXT_F], ensure_ascii=False).lower())\n'
     'chk("P18 CRUA no texto do HMS/13", not GP.violacoes(json.dumps(TXT_F, ensure_ascii=False)), GP.violacoes(json.dumps(TXT_F, ensure_ascii=False))[:2])\n'),
    ('RUNTIME_SRC = open(os.path.join(HERE, "runtime_v410.py"), encoding="utf-8").read().rstrip("\\n") + "\\n\\n\\n" + open(os.path.join(HERE, "runtime_h0dn_v410.py"), encoding="utf-8").read()\n',
     'RUNTIME_SRC = open(os.path.join(HERE, "runtime_v410.py"), encoding="utf-8").read().rstrip("\\n") + "\\n\\n\\n" + open(os.path.join(HERE, "runtime_h0dn_v410.py"), encoding="utf-8").read().rstrip("\\n") + "\\n\\n\\n" + open(os.path.join(HERE, "runtime_hms13_v410.py"), encoding="utf-8").read()\n'),
    ('json.dumps([CONTR, TXT, specs, CONTR_H, TXT_H, ', 'json.dumps([CONTR, TXT, specs, CONTR_H, TXT_H, CONTR_F, TXT_F, '),
    ('_controles([CONTR, TXT, specs, fontes, CONTR_H, TXT_H, RUNTIME_SRC], "x")', '_controles([CONTR, TXT, specs, fontes, CONTR_H, TXT_H, CONTR_F, TXT_F, RUNTIME_SRC], "x")'),
    ('"runtime_h0dn_v410.py", "guarda_frases_v410.py"', '"runtime_h0dn_v410.py", "registros_hms13_v410.py", "runtime_hms13_v410.py", "guarda_frases_v410.py"'),
], regex=[(r'(NOVOS = \([^\n]*?"h0dn_bg1_v410")\)', r'\1, "_v410_hms13_numeros", "_v410_hms13_mechanics", "_V410_HMS13_RECUSA", "h0dn_fontes_hms13_v410", "_V410_HMS13_CONTRACT", "_V410_HMS13_TEXT", "_V410_HMS13_INSUMOS")')])
print("ok")
