# -*- coding: utf-8 -*-
"""_adapt_h0dn_pos_v410.py -- (claude-construtor-v410, 09/11/2026, retomada; D72 e o AVISO da gerencia sobre a pasta do Kimi) leva o SEGUNDO registro com funcao da v410, h0dn_bg1_v410, aos tres scripts que o fork B adaptou em 06/11 ANTES de a D72 existir,
e o VETO explicito a pasta vedada ao espelho da casa:
  (1) simular_arvore_do_nos_v410.py: o h0dn_bg1_v410 roda na ordem do main (logo depois do iald2_v410, antes dos specs da v410) e entra na lista dos registros conferidos;
  (2) exame_pontos_v410.py: o ponto (4h) do h0dn_bg1_v410 (na MESMA instrucao do main do iald2, logo depois dele, antes dos specs), o registro no selo, o falso `ponto_h0dn`;
  (3) guarda_ordem_de_chamada_v410.py: o h0dn_bg1_v410 entra em FUNCOES_NOVAS_V410 (mecanica _v410_h0dn_mechanics, miolo _v398_beta, os mesmos insumos exigidos do iald2) e ganha o controle negativo (14): a chamada retirada reprova;
  (4) pos_rito/harness_fechar_sandbox_v410.py: a pasta VEDADA (DL.H0DN_PASTA_VEDADA, lida do delta real importado) nunca entra no espelho da casa nem na copia da memoria; um acesso medido sob ela e' FALHA VISIVEL.
Backup de bytes; trocas exatas com contagem; fim de linha de cada arquivo preservado; ast.parse."""
import ast, datetime, hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def troca_arquivo(rel, trocas, marca=None):
    P = os.path.join(HERE, rel); b0 = open(P, "rb").read(); nl = "\r\n" if b0.count(b"\r\n") else "\n"
    bk = P + ".bak_" + TS + "_h0dn"; open(bk, "wb").write(b0); assert open(bk, "rb").read() == b0
    t = b0.decode("utf-8")
    for v, n, k in trocas:
        v2, n2 = v.replace("\n", nl), n.replace("\n", nl); c = t.count(v2); assert c == k, (rel, c, k, v[:140]); t = t.replace(v2, n2)
    if marca:
        lin = t.split(nl); assert lin[0].startswith("# -*- coding"), rel; lin.insert(1, marca); t = nl.join(lin)
    nb = t.encode("utf-8"); ast.parse(nb); tmp = P + ".tmp_" + TS; open(tmp, "wb").write(nb); assert os.path.getsize(tmp) == len(nb); os.replace(tmp, P)
    print(rel, len(b0), "->", len(nb), "| sha16", hashlib.sha256(nb).hexdigest()[:16], "| trocas", len(trocas))


# (1) simular_arvore_do_nos_v410.py
troca_arquivo("simular_arvore_do_nos_v410.py", [
    ("um.iald2_v410(core); um._v410_rodar_specs(core)   # (v410: o iald2_v410 vem logo depois dos specs da v409",
     "um.iald2_v410(core); um.h0dn_bg1_v410(core); um._v410_rodar_specs(core)   # (v410, D72: o h0dn_bg1_v410 -- pré-registrado; nenhum dado observado lido -- vem na mesma instrucao do main, logo depois do iald2_v410 e antes dos specs da v410; o iald2_v410 vem logo depois dos specs da v409", 1),
    ('for k in ("iald2_v410", "cunhagens_v410", "kh_n1_cobertura_v410",', 'for k in ("iald2_v410", "h0dn_bg1_v410", "cunhagens_v410", "kh_n1_cobertura_v410",', 1),
], marca="# [ADAPTADO v410, 09/11/2026, claude-construtor-v410 (retomada), por _adapt_h0dn_pos_v410.py] D72: o SEGUNDO registro com funcao, h0dn_bg1_v410 (pré-registrado; nenhum dado observado lido), roda na ordem do main (logo depois do iald2_v410, antes dos specs da v410) e entra nos registros conferidos na arvore simulada")

# (2) exame_pontos_v410.py
troca_arquivo("exame_pontos_v410.py", [
    ('out["core.iald2_v410"] = {"all_verified": ia.get("all_verified"), "verdict": str(ia.get("verdict"))[:300], "falhas": R["ponto_iald2"]["mecanica"]["falhos"]}\n',
     'out["core.iald2_v410"] = {"all_verified": ia.get("all_verified"), "verdict": str(ia.get("verdict"))[:300], "falhas": R["ponto_iald2"]["mecanica"]["falhos"]}\n'
     "# (4h) [v410, D72] o PONTO DE CHAMADA REAL do h0dn_bg1_v410 (executado dentro do bloco acima, na MESMA instrucao do main que chama o iald2_v410, LOGO DEPOIS dele e ANTES dos specs da v410): o registro pre-registrado -- pré-registrado; nenhum dado observado lido --, as 12 checagens,\n"
     "#      o veredito pre-registrado, beta em runtime, o gate congelado, nenhum caminho tocado sob a pasta vedada (a entrega do Kimi) nem com nome vedado (medido pela c7 do proprio registro)\n"
     'hb = core.get("h0dn_bg1_v410") or {}; hbv = hb.get("values") or {}\n'
     "_CPH = um._V410_H0DN_CONTRACT\n"
     "_uia = unp[iia]; _tem_h = \"h0dn_bg1_v410(core)\" in _uia\n"
     'R["ponto_h0dn"] = {"indice_no_main": iia, "linha": main.body[iia].lineno, "na_mesma_instrucao_do_iald2": _tem_h, "logo_depois_do_iald2_na_instrucao": (_uia.find("iald2_v410(core)") < _uia.find("h0dn_bg1_v410(core)")) if _tem_h else False, "antes_dos_specs_v410_na_instrucao": (_uia.find("h0dn_bg1_v410(core)") < _uia.find("_v410_rodar_specs(core)")) if _tem_h else False,\n'
     '                   "dentro_do_bloco_executado": i0 <= iia < i1, "verdict": hb.get("verdict"), "veredito_ok_do_contrato": _CPH["veredito_ok"], "all_verified": hb.get("all_verified"), "runtime_executed": hb.get("runtime_executed"), "observed_vector_read": hb.get("observed_vector_read"), "does_not_gate_core": hb.get("does_not_gate_core"), "beta_ok": hb.get("beta_ok"),\n'
     '                   "mecanica": {"passed": (hb.get("mechanics") or {}).get("passed"), "n_checks": (hb.get("mechanics") or {}).get("n_checks"), "falhos": [c_.get("id") for c_ in ((hb.get("mechanics") or {}).get("checks") or []) if not c_.get("ok")]},\n'
     '                   "n_pinos": hbv.get("n_pinos"), "n_pinos_freeze": hbv.get("n_pinos_freeze"), "n_embutidos": hbv.get("n_embutidos"), "ramos_vistos": hbv.get("ramos_vistos"), "n_vetores_c6": len(hbv.get("vetores_c6") or []), "gate_verdict": hbv.get("gate_verdict"), "veredito_h0dn_source_sha256": hb.get("veredito_h0dn_source_sha256"),\n'
     '                   "n_caminhos_tocados": hbv.get("n_caminhos_tocados"), "sob_pasta_vedada": hbv.get("sob_pasta_vedada"), "com_nome_vedado": hbv.get("com_nome_vedado"), "pasta_vedada": hbv.get("pasta_vedada"),\n'
     '                   "contrato": {"n_checks_do_DL": DL.N_CHECKS_H0DN, "n_pinos_esperados": len(_CPH["insumos"]) + len(_CPH["pinos_freeze_r2_so_no_disco"]), "n_pinos_freeze": _CPH["n_pinos_freeze"], "n_vetores_c6": len(_CPH["vetores_c6"]), "pasta_vedada": _CPH["pasta_vedada"]}}\n'
     'out["core.h0dn_bg1_v410"] = {"all_verified": hb.get("all_verified"), "verdict": str(hb.get("verdict"))[:300], "falhas": R["ponto_h0dn"]["mecanica"]["falhos"]}\n', 1),
    ('"iald2_v410": {x: (seal.get("iald2_v410") or {}).get(x) for x in ("verdict", "all_verified")}, "registros_v410":',
     '"iald2_v410": {x: (seal.get("iald2_v410") or {}).get(x) for x in ("verdict", "all_verified")}, "h0dn_bg1_v410": {x: (seal.get("h0dn_bg1_v410") or {}).get(x) for x in ("verdict", "all_verified")}, "registros_v410":', 1),
    ('        or any(v_ is not False for v_ in pia["fica_false_por_teorema"].values()) or (pia.get("alcance") or {}).get("frase") != DL.FRASE_D64_PT): falsos.append("ponto_iald2")\n',
     '        or any(v_ is not False for v_ in pia["fica_false_por_teorema"].values()) or (pia.get("alcance") or {}).get("frase") != DL.FRASE_D64_PT): falsos.append("ponto_iald2")\n'
     'phb = R["ponto_h0dn"]   # (4h) o SEGUNDO ponto NOVO da v410 (D72): pré-registrado; nenhum dado observado lido; na mesma instrucao do iald2, logo depois dele\n'
     'if (phb.get("all_verified") is not True or phb.get("runtime_executed") is not True or phb.get("observed_vector_read") is not False or not phb.get("dentro_do_bloco_executado") or not phb.get("na_mesma_instrucao_do_iald2") or not phb.get("logo_depois_do_iald2_na_instrucao") or not phb.get("antes_dos_specs_v410_na_instrucao")\n'
     '        or phb.get("verdict") != phb.get("veredito_ok_do_contrato") or phb.get("verdict") != DL.VEREDITO_H0DN_OK or (phb.get("mecanica") or {}).get("passed") is not True or (phb.get("mecanica") or {}).get("n_checks") != DL.N_CHECKS_H0DN or (phb.get("mecanica") or {}).get("falhos")\n'
     '        or phb.get("n_pinos") != phb["contrato"]["n_pinos_esperados"] or phb.get("n_pinos_freeze") != DL.N_PINOS_FREEZE_R2 or phb.get("ramos_vistos") != [1, 2, 3, 4, 5, 6] or phb.get("n_vetores_c6") != phb["contrato"]["n_vetores_c6"] or phb.get("does_not_gate_core") is not True or phb.get("beta_ok") is not True\n'
     '        or phb.get("sob_pasta_vedada") != [] or phb.get("com_nome_vedado") != [] or not isinstance(phb.get("n_caminhos_tocados"), int) or phb.get("n_caminhos_tocados") < 1 or phb.get("pasta_vedada") != DL.H0DN_PASTA_VEDADA or phb.get("gate_verdict") != pia.get("gate_verdict")\n'
     '        or not isinstance(phb.get("veredito_h0dn_source_sha256"), str) or len(phb.get("veredito_h0dn_source_sha256") or "") != 64): falsos.append("ponto_h0dn")\n', 1),
], marca="# [ADAPTADO v410, 09/11/2026, claude-construtor-v410 (retomada), por _adapt_h0dn_pos_v410.py] D72: o ponto (4h) do h0dn_bg1_v410 (pré-registrado; nenhum dado observado lido), na MESMA instrucao do main do iald2_v410, logo depois dele e antes dos specs da v410; o registro no selo; o falso `ponto_h0dn`")

# (3) guarda_ordem_de_chamada_v410.py
troca_arquivo("guarda_ordem_de_chamada_v410.py", [
    ('FUNCOES_NOVAS_V410 = ("iald2_v410",)                               # a v410 e\' um BUNDLE de um modulo de kernel (IALD2): o UNICO registro com funcao novo e\' o iald2_v410',
     'FUNCOES_NOVAS_V410 = ("iald2_v410", "h0dn_bg1_v410")              # a v410 e\' um BUNDLE de um modulo de kernel (IALD2) e traz DOIS registros com funcao novos: o iald2_v410 e, na MESMA instrucao do main, logo depois dele, o h0dn_bg1_v410 (D72: o teste pre-registrado da razao de Hubble; pré-registrado; nenhum dado observado lido)', 1),
    ('MECANICA_DE["iald2_v410"] = "v410_iald2_mechanics"\n', 'MECANICA_DE["iald2_v410"] = "v410_iald2_mechanics"\nMECANICA_DE["h0dn_bg1_v410"] = "_v410_h0dn_mechanics"   # (v410, D72)\n', 1),
    ('             "iald2_v410": ("_v410_formal", "_v398_beta")}   # (v410) o miolo comum do iald2 (nao le chave de testemunha: nenhuma chave antiga muda)',
     '             "iald2_v410": ("_v410_formal", "_v398_beta"),   # (v410) o miolo comum do iald2 (nao le chave de testemunha: nenhuma chave antiga muda)\n'
     '             "h0dn_bg1_v410": ("_v398_beta",)}   # (v410, D72) o miolo comum do h0dn (le hubble_ratio_v387, qg_closure e beta, todos do run_um: nenhuma chave antiga muda)', 1),
    ('INSUMOS_EXIGIDOS = {"iald2_v410": ("traducao_turing_v409", "_v409_rodar_specs", "tetelestai_terminal_v408", "_v408_rodar_specs", "psion_canto_v407", "_v407_rodar_specs", "fechamento_v406", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "witness_layers"),',
     'INSUMOS_EXIGIDOS = {"h0dn_bg1_v410": ("traducao_turing_v409", "_v409_rodar_specs", "tetelestai_terminal_v408", "_v408_rodar_specs", "psion_canto_v407", "_v407_rodar_specs", "fechamento_v406", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "witness_layers"),   # (v410, D72) os mesmos do iald2: o h0dn e\' chamado na MESMA instrucao do main, logo depois do iald2 (a ordem DENTRO da instrucao e\' medida pelo ensaio e pelo exame_pontos)\n'
     '                    "iald2_v410": ("traducao_turing_v409", "_v409_rodar_specs", "tetelestai_terminal_v408", "_v408_rodar_specs", "psion_canto_v407", "_v407_rodar_specs", "fechamento_v406", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "witness_layers"),', 1),
    ("    (12) [v410] o iald2_v410 chamado ANTES do traducao_turing_v409 reprova, e o motivo e' o insumo exigido ausente; (13) [v410] o iald2_v410 sem a chamada no main reprova. Rodado sobre o texto: nada executa.\"\"\"",
     "    (12) [v410] o iald2_v410 chamado ANTES do traducao_turing_v409 reprova, e o motivo e' o insumo exigido ausente; (13) [v410] o iald2_v410 sem a chamada no main reprova; (14) [v410, D72] o h0dn_bg1_v410 sem a chamada no main reprova (a linha traz comentario: a troca e' por prefixo). Rodado sobre o texto: nada executa.\"\"\"", 1),
    ('    r12 = ordem_de_chamada(_sem_chamada(src, "iald2_v410", "_r410"), ("iald2_v410",))\n',
     '    r12 = ordem_de_chamada(_sem_chamada(src, "iald2_v410", "_r410"), ("iald2_v410",))\n'
     '    # (14) [v410, D72] a chamada do h0dn_bg1_v410 sai do main (a linha do candidato traz um comentario depois da chamada: a troca e\' por prefixo, nao por fullmatch)\n'
     '    _lh = [i for i, l in enumerate(linhas) if re.match(r"\\s+_h410 = h0dn_bg1_v410\\(core\\)", l)]; assert len(_lh) == 1, ("a linha da chamada do h0dn_bg1_v410 nao foi achada uma vez", _lh)\n'
     '    m14_ = list(linhas); m14_[_lh[0]] = m14_[_lh[0]].replace("h0dn_bg1_v410(core)", "{}", 1)\n'
     '    r13 = ordem_de_chamada("\\n".join(m14_), ("h0dn_bg1_v410",))\n', 1),
    ('         "iald2_antes_da_traducao_reprova": bool(not r11["ok"] and "traducao_turing_v409" in (f11_.get("insumos_exigidos_ausentes") or [])), "iald2_sem_chamada_no_main_reprova": bool(not r12["ok"] and "erro" in (r12["funcoes"].get("iald2_v410") or {}))}',
     '         "iald2_antes_da_traducao_reprova": bool(not r11["ok"] and "traducao_turing_v409" in (f11_.get("insumos_exigidos_ausentes") or [])), "iald2_sem_chamada_no_main_reprova": bool(not r12["ok"] and "erro" in (r12["funcoes"].get("iald2_v410") or {})),\n'
     '         "h0dn_sem_chamada_no_main_reprova": bool(not r13["ok"] and "erro" in (r13["funcoes"].get("h0dn_bg1_v410") or {}))}', 1),
], marca="# [ADAPTADO v410, 09/11/2026, claude-construtor-v410 (retomada), por _adapt_h0dn_pos_v410.py] D72: o h0dn_bg1_v410 entra em FUNCOES_NOVAS_V410 (mecanica _v410_h0dn_mechanics; miolo _v398_beta; os insumos exigidos do iald2) e o controle negativo (14): a chamada retirada reprova")

# (4) pos_rito/harness_fechar_sandbox_v410.py: o VETO explicito a pasta da entrega do Kimi
troca_arquivo("pos_rito/harness_fechar_sandbox_v410.py", [
    ('def mk_memoria_copia(dst):\n    """COPIA do diretorio de memoria:',
     'def mk_memoria_copia(dst):\n    """(AVISO da gerencia, 09/11) a pasta VEDADA da entrega do Kimi (DL.H0DN_PASTA_VEDADA, lida do delta real) nunca entra na copia: a exclusao e\' explicita, por medida (_sob_vedado), mesmo que ela nao viva sob a memoria. COPIA do diretorio de memoria:', 1),
    ('    shutil.rmtree(dst, ignore_errors=True); os.makedirs(dst)\n    n = tot = 0\n    for f in sorted(os.listdir(MEM_REAL)):\n        p = os.path.join(MEM_REAL, f)\n        if os.path.isfile(p) and ".bak" not in f and ".tmp" not in f and "v410" not in f:\n',
     '    shutil.rmtree(dst, ignore_errors=True); os.makedirs(dst)\n    _ved = globals().get("_sob_vedado") or (lambda p_: False)   # (AVISO 09/11) VEDADO: nada da pasta da entrega do Kimi entra na copia\n    n = tot = 0\n    for f in sorted(os.listdir(MEM_REAL)):\n        p = os.path.join(MEM_REAL, f)\n        if os.path.isfile(p) and ".bak" not in f and ".tmp" not in f and "v410" not in f and not _ved(p):\n', 1),
    ('            if f == "fila.lock" or ".tmp" in f or f == "PAUSA_VIGIA.json":\n                continue\n',
     '            if f == "fila.lock" or ".tmp" in f or f == "PAUSA_VIGIA.json" or _ved(os.path.join(r, f)):   # (VEDADO: a pasta do Kimi, explicitamente)\n                continue\n', 1),
    ("_CEN_REAL = os.path.dirname(os.path.dirname(PKG))\n",
     "_CEN_REAL = os.path.dirname(os.path.dirname(PKG))\n"
     "# (AVISO da gerencia, 09/11) O VETO A PASTA DA ENTREGA DO KIMI: a pasta e' lida do delta REAL ja' importado (_dm.H0DN_PASTA_VEDADA = work\\\\h0dn_bg1_v410_09nov\\\\kimi); nenhum acesso MEDIDO na importacao do delta pode cair sob ela (se cair, FALHA VISIVEL: a v410 pre-registra e NAO abre),\n"
     "# o espelho da casa a exclui EXPLICITAMENTE (abaixo) e a copia da memoria tambem (mk_memoria_copia): a exclusao e' por medida, nao por promessa\n"
     "_VEDADO = os.path.normcase(os.path.abspath(_dm.H0DN_PASTA_VEDADA))\n"
     "_sob_vedado = lambda p_: (lambda q_: q_ == _VEDADO or q_.startswith(_VEDADO + os.sep))(os.path.normcase(os.path.abspath(p_)))\n"
     "_ACESSOS_VEDADOS = sorted(p_ for p_ in _ACESSOS if _sob_vedado(p_))\n"
     'assert not _ACESSOS_VEDADOS, ("VEDADO: a importacao do delta tocou a pasta da entrega do Kimi (a v410 pre-registra e NAO abre)", _ACESSOS_VEDADOS)\n'
     'assert not _sob_vedado(MEM_REAL) and not _sob_vedado(PKG) and not _sob_vedado(SB), "VEDADO: a memoria, o pacote ou o sandbox estariam sob a pasta vedada"\n', 1),
    ("for _p_a in sorted(_ACESSOS):\n    if not (_p_a.startswith(_CEN_REAL + os.sep) and os.path.isfile(_p_a)):\n        continue\n",
     "for _p_a in sorted(_ACESSOS):\n    if _sob_vedado(_p_a):\n        raise AssertionError((\"VEDADO: o espelho da casa nao copia nada da pasta da entrega do Kimi\", _p_a))   # (AVISO 09/11; nunca alcancado se o assert acima passou: fica como a segunda trava)\n    if not (_p_a.startswith(_CEN_REAL + os.sep) and os.path.isfile(_p_a)):\n        continue\n", 1),
    ('"n_acessos_medidos": len(_ACESSOS), "n_falas_excluidas_nao_copiadas_nem_nomeadas": _ESP_EXCL_N,',
     '"n_acessos_medidos": len(_ACESSOS), "pasta_vedada_kimi": {"pasta": _dm.H0DN_PASTA_VEDADA, "acessos_medidos_sob_ela": _ACESSOS_VEDADOS, "excluida_explicitamente_do_espelho_e_da_copia_da_memoria": True}, "n_falas_excluidas_nao_copiadas_nem_nomeadas": _ESP_EXCL_N,', 1),
], marca="# [ADAPTADO v410, 09/11/2026, claude-construtor-v410 (retomada), por _adapt_h0dn_pos_v410.py] AVISO da gerencia (09/11): a pasta VEDADA da entrega do Kimi (DL.H0DN_PASTA_VEDADA, lida do delta real importado) e' excluida EXPLICITAMENTE do espelho da casa e da copia da memoria; um acesso medido sob ela na importacao do delta e' FALHA VISIVEL")
print("ok")
