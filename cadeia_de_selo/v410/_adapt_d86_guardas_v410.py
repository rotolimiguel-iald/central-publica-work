# -*- coding: utf-8 -*-
"""_adapt_d86_guardas_v410.py -- D86/D87 (parte 2) nas guardas ESTATICAS: guarda_ordem_de_chamada_v410.py (o a_escala_v410 em FUNCOES_NOVAS_V410, MECANICA_DE, COMUNS_DE, INSUMOS_EXIGIDOS; controle (17) sem a chamada),
comparar_v409_v410.py (os nos novos da AEscala; o patch N00_main_iald2_aescala_h0dn_hms13; o .md com QUATRO linhas; o selo com CINCO chaves; o a_escala entre o iald2 e o h0dn) e _prevoo_gerador_v410.py (o contrato da AEscala, o runtime emendado, os nomes novos, os snippets, os sha16).
Backup de bytes; trocas exatas; ast.parse; idempotente por arquivo."""
import ast, datetime, hashlib, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def aplica(nome, marca, trocas, regex=()):
    p = os.path.join(HERE, nome); b0 = open(p, "rb").read(); t = b0.decode("utf-8")
    if marca in t:
        print(nome, ": ja' aplicado"); return
    open(p + ".bak_" + TS + "_d86", "wb").write(b0); assert open(p + ".bak_" + TS + "_d86", "rb").read() == b0
    for a, b in trocas:
        c = t.count(a); assert c == 1, (nome, c, a[:120]); t = t.replace(a, b)
    for rx, rep in regex:
        t, n = re.subn(rx, rep, t, flags=re.S); assert n == 1, (nome, rx[:80], n)
    assert marca in t
    nb = t.encode("utf-8"); ast.parse(nb)
    open(p + ".tmp", "wb").write(nb); assert os.path.getsize(p + ".tmp") == len(nb); os.replace(p + ".tmp", p)
    print(nome, len(b0), "->", len(nb), "| sha16", hashlib.sha256(nb).hexdigest()[:16])


# ---- guarda_ordem_de_chamada_v410.py
aplica("guarda_ordem_de_chamada_v410.py", "aescala_sem_chamada_no_main_reprova", [
    ('FUNCOES_NOVAS_V410 = ("iald2_v410", "h0dn_bg1_v410", "h0dn_fontes_hms13_v410")', 'FUNCOES_NOVAS_V410 = ("iald2_v410", "a_escala_v410", "h0dn_bg1_v410", "h0dn_fontes_hms13_v410")'),
    ('MECANICA_DE["h0dn_bg1_v410"] = "_v410_h0dn_mechanics"   # (v410, D72)\n', 'MECANICA_DE["h0dn_bg1_v410"] = "_v410_h0dn_mechanics"   # (v410, D72)\nMECANICA_DE["a_escala_v410"] = "_v410_aescala_mechanics"   # (v410, D86: a pedra AEscala, na MESMA instrucao do iald2, logo depois dele)\n'),
    ('             "h0dn_fontes_hms13_v410": ("_v398_beta",)}', '             "h0dn_fontes_hms13_v410": ("_v398_beta",),\n             "a_escala_v410": ("_v398_beta",)}   # (v410, D86) o miolo comum do a_escala: le kernel_formalization, external_ladder, qg_closure e beta (todos do run_um)'),
    ('                    "iald2_v410": ("traducao_turing_v409",', '                    "a_escala_v410": ("traducao_turing_v409", "_v409_rodar_specs", "tetelestai_terminal_v408", "_v408_rodar_specs", "psion_canto_v407", "_v407_rodar_specs", "fechamento_v406", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "witness_layers"),   # (v410, D86) os mesmos do iald2: chamado na MESMA instrucao, logo depois dele (a ordem DENTRO da instrucao e\' medida pelo ensaio e pelo exame_pontos)\n'
     '                    "iald2_v410": ("traducao_turing_v409",'),
    ('    f15_ = r15["funcoes"].get("h0dn_fontes_hms13_v410") or {}\n',
     '    f15_ = r15["funcoes"].get("h0dn_fontes_hms13_v410") or {}\n'
     '    # (17) [v410, D86] a chamada do a_escala_v410 sai do main (a linha traz comentario: troca por prefixo)\n'
     '    _la = [i for i, l in enumerate(linhas) if re.match(r"\\s+_a410 = a_escala_v410\\(core\\)", l)]; assert len(_la) == 1, ("a linha da chamada do a_escala_v410 nao foi achada uma vez", _la)\n'
     '    m17_ = list(linhas); m17_[_la[0]] = m17_[_la[0]].replace("a_escala_v410(core)", "{}", 1)\n'
     '    r16 = ordem_de_chamada("\\n".join(m17_), ("a_escala_v410",))\n'),
    ('"hms13_antes_do_h0dn_reprova": bool(not r15["ok"] and "h0dn_bg1_v410" in (f15_.get("insumos_exigidos_ausentes") or []))}',
     '"hms13_antes_do_h0dn_reprova": bool(not r15["ok"] and "h0dn_bg1_v410" in (f15_.get("insumos_exigidos_ausentes") or [])),\n'
     '         "aescala_sem_chamada_no_main_reprova": bool(not r16["ok"] and "erro" in (r16["funcoes"].get("a_escala_v410") or {}))}'),
])
# ---- comparar_v409_v410.py
aplica("comparar_v409_v410.py", "_V410_AESCALA_TEXT", [
    ('"main": "N00/N02: a chamada do `iald2_v410`, a do `h0dn_bg1_v410`', '"main": "N00/N02: a chamada do `iald2_v410`, a do `a_escala_v410` (D86: a pedra AEscala, na MESMA instrucao, logo depois do iald2), a do `h0dn_bg1_v410`'),
    ('e as chaves novas do selo (iald2_v410, h0dn_bg1_v410, h0dn_fontes_hms13_v410, registros_v410); nada do que existia muda"', 'e as chaves novas do selo (iald2_v410, a_escala_v410, h0dn_bg1_v410, h0dn_fontes_hms13_v410, registros_v410); nada do que existia muda"'),
    ('"W09: as linhas «IALD2 (v410, 06/11/2026)», «H0DN × BG1 pré-registrado (v410, 09/11/2026)» (com a obrigacao D72) e', '"W09: as linhas «IALD2 (v410, 06/11/2026)», a da Escala (v410, 09/11/2026; D82 a D87), «H0DN × BG1 pré-registrado (v410, 09/11/2026)» (com a obrigacao D72) e'),
    ('"N00_main_iald2_h0dn_hms13": ["main"]', '"N00_main_iald2_aescala_h0dn_hms13": ["main"]'),
    ('"_V410_HMS13_CONTRACT", "_V410_HMS13_TEXT", "_V410_HMS13_INSUMOS"}', '"_V410_HMS13_CONTRACT", "_V410_HMS13_TEXT", "_V410_HMS13_INSUMOS", "_v410_aescala_bell", "_v410_aescala_mechanics", "_V410_AESCALA_RECUSA", "_V410_AESCALA_CONTRACT", "_V410_AESCALA_TEXT"}'),
    ('ops[0][4] - ops[0][3] == 3   # (09/11, D72 e D80: TRES linhas', 'ops[0][4] - ops[0][3] == 4   # (09/11, D72, D80 e D86: QUATRO linhas'),
    ('return {"tres_linhas_inseridas_e_nada_removido": ok1,', 'return {"quatro_linhas_inseridas_e_nada_removido": ok1, "traz_o_texto_da_aescala_com_a_forma_canonica": ("A Escala (v410" in txt) and (DL.FRASE_CLAY_CANONICA_PT in txt) and (DL.FRASE_D83_OBRIGATORIA_PT in txt), "a_linha_da_aescala_vem_entre_a_da_iald2_e_a_do_h0dn": 0 <= txt.find("IALD2 (v410") < txt.find("A Escala (v410") < txt.find("H0DN × BG1 pré-registrado (v410"),'),
    ('"as_duas_instrucoes_chamam_iald2_h0dn_hms13_e_os_specs_nesta_ordem": "iald2_v410(core)" in txt and "h0dn_bg1_v410(core)" in txt and "h0dn_fontes_hms13_v410(core)" in txt and "_v410_rodar_specs(core)" in txt and 0 <= txt.find("iald2_v410(core)") < txt.find("h0dn_bg1_v410(core)")',
     '"as_duas_instrucoes_chamam_iald2_aescala_h0dn_hms13_e_os_specs_nesta_ordem": "iald2_v410(core)" in txt and "a_escala_v410(core)" in txt and "h0dn_bg1_v410(core)" in txt and "h0dn_fontes_hms13_v410(core)" in txt and "_v410_rodar_specs(core)" in txt and 0 <= txt.find("iald2_v410(core)") < txt.find("a_escala_v410(core)") < txt.find("h0dn_bg1_v410(core)")'),
    ('"o_selo_so_ganha_as_quatro_chaves_da_v410": bool(sel) and sel["chaves_da_base_preservadas_na_ordem"] and sel["valores_da_base_iguais"] and sorted(sel["chaves_novas"]) == sorted(["iald2_v410", "h0dn_bg1_v410", "h0dn_fontes_hms13_v410", "registros_v410"])',
     '"o_selo_so_ganha_as_cinco_chaves_da_v410": bool(sel) and sel["chaves_da_base_preservadas_na_ordem"] and sel["valores_da_base_iguais"] and sorted(sel["chaves_novas"]) == sorted(["iald2_v410", "a_escala_v410", "h0dn_bg1_v410", "h0dn_fontes_hms13_v410", "registros_v410"])'),
])
# ---- _prevoo_gerador_v410.py
aplica("_prevoo_gerador_v410.py", "registros_aescala_v410 as RA", [
    ('import registros_hms13_v410 as RF  # noqa: E402   (D80)\n', 'import registros_hms13_v410 as RF  # noqa: E402   (D80)\nimport registros_aescala_v410 as RA  # noqa: E402   (D86/D87)\n'),
    ('CONTR_F = RF.contrato_hms13(core0, selo0, CONTR_H); TXT_F = RF.texto_hms13(); INS_F = RF.insumos_embutidos_hms13()\n',
     'CONTR_F = RF.contrato_hms13(core0, selo0, CONTR_H); TXT_F = RF.texto_hms13(); INS_F = RF.insumos_embutidos_hms13()\n'
     'CONTR_A = RA.contrato_aescala(FJ, FORMAL_MAP, E409, sha256(raw), core0, selo0); TXT_A = RA.texto_aescala()\n'
     'chk("contrato AEscala (D86/D87): 12 checagens, 38 ancoras, 44 nomes RATIFICADOS, 8 falas, a escada, o gate, as bandeiras das duas series somam o FLAGS", CONTR_A["n_checks"] == DL.N_CHECKS_AESCALA == 12 and CONTR_A["n_ancoras"] == 38 and CONTR_A["n_nomes"] == 44 and CONTR_A["nomes_ratificados"] is True and len(CONTR_A["falas"]) == 8 and CONTR_A["expected_ladder"] == CONTR["expected_ladder"] == E409 + FJ["n_flags"] and CONTR_A["baseline"]["gate_verdict"] == selo0.get("qg_closure_verdict") and CONTR_A["n_flags"] + CONTR["n_flags"] == FJ["n_flags"])\n'
     'chk("P18 CRUA no texto da AEscala (sem as falas embutidas) e a guarda das frases (F58 do Clay)", not GP.violacoes(json.dumps({k_: TXT_A[k_] for k_ in ("estatuto", "escopo", "limites", "diz", "nao_diz")}, ensure_ascii=False)) and not GF.violacoes(json.dumps(TXT_A, ensure_ascii=False)), (GP.violacoes(json.dumps({k_: TXT_A[k_] for k_ in ("estatuto", "escopo", "limites", "diz", "nao_diz")}, ensure_ascii=False)) + GF.violacoes(json.dumps(TXT_A, ensure_ascii=False)))[:3])\n'),
    ('+ open(os.path.join(HERE, "runtime_hms13_v410.py"), encoding="utf-8").read()\n', '+ open(os.path.join(HERE, "runtime_hms13_v410.py"), encoding="utf-8").read().rstrip("\\n") + "\\n\\n\\n" + open(os.path.join(HERE, "runtime_aescala_v410.py"), encoding="utf-8").read()\n'),
    ('json.dumps([CONTR, TXT, specs, CONTR_H, TXT_H, CONTR_F, TXT_F, ', 'json.dumps([CONTR, TXT, specs, CONTR_H, TXT_H, CONTR_F, TXT_F, CONTR_A, TXT_A, '),
    ('_controles([CONTR, TXT, specs, fontes, CONTR_H, TXT_H, CONTR_F, TXT_F, RUNTIME_SRC], "x")', '_controles([CONTR, TXT, specs, fontes, CONTR_H, TXT_H, CONTR_F, TXT_F, CONTR_A, TXT_A, RUNTIME_SRC], "x")'),
    ('for nome in ("artigo_pt_v410.pysnip", "artigo_en_v410.pysnip", "artigo_pt_h0dn_v410.pysnip", "artigo_en_h0dn_v410.pysnip"):', 'for nome in ("artigo_pt_v410.pysnip", "artigo_en_v410.pysnip", "artigo_pt_aescala_v410.pysnip", "artigo_en_aescala_v410.pysnip", "artigo_pt_h0dn_v410.pysnip", "artigo_en_h0dn_v410.pysnip"):'),
    ('"registros_hms13_v410.py", "runtime_hms13_v410.py", "guarda_frases_v410.py"', '"registros_hms13_v410.py", "runtime_hms13_v410.py", "registros_aescala_v410.py", "runtime_aescala_v410.py", "guarda_frases_v410.py"'),
], regex=[(r'(NOVOS = \([^\n]*?"h0dn_fontes_hms13_v410")\)', r'\1, "_v410_aescala_bell", "_v410_aescala_mechanics", "_V410_AESCALA_RECUSA", "a_escala_v410")')])
print("ok")
