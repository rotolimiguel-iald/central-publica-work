# -*- coding: utf-8 -*-
"""_adapt_exame_v408.py -- adapta exame_pontos_v408.py (subida mecanica) a v408: o ponto do psion_canto_v407 passa a HERDADO (os numeros dele saem do DL.D7 e do FLAGS_v407.json) e vem IMEDIATAMENTE antes do ponto NOVO (4e) do tetelestai_terminal_v408, que vem IMEDIATAMENTE antes de emit_figures;
o ponto novo e' conferido (posicao, registro, 16 checagens, nenhuma chave antiga mudada, o insumo purgado); o selo e os nao-verdes ganham as chaves da v408. Trocas de contagem EXATA; backup de bytes; retira a marca. Escrito pela ferramenta Write."""
import ast, datetime, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "exame_pontos_v408.py")
raw = open(P, "rb").read(); open(P + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_adapt", "wb").write(raw)
t = raw.decode("utf-8"); assert "\r\n" not in t


def sub(old, new, n=1):
    global t
    assert t.count(old) == n, (old[:100], t.count(old), n); t = t.replace(old, new)


t = re.sub(r"(?m)^# \[A ADAPTAR v408\][^\n]*\n", "", t, count=1)
t = re.sub(r"(?m)^# ADAPTADO a v408 \(03/11/2026, claude-prep-v408\):[^\n]*\n", "# ADAPTADO a v408 (04/11/2026, claude-construtor-v408): molde v407/exame_pontos_v407.py; o ponto NOVO e' o do `tetelestai_terminal_v408` (a instrucao do main que chama tambem `_v408_rodar_specs`, IMEDIATAMENTE depois do psion_canto_v407 e IMEDIATAMENTE antes de emit_figures); o ponto do psion_canto_v407 e o do fechamento_v406 sao HERDADOS e seguem conferidos; nenhuma chave antiga muda.\n", t, count=1)
sub(" (4d) [v407] o PONTO DE CHAMADA REAL do `psion_canto_v407`: a instrucao do main (um `try` que chama tambem `_v407_rodar_specs`) que vem IMEDIATAMENTE depois do fechamento_v406 e IMEDIATAMENTE antes de `_figs = emit_figures(core)`,",
    " (4d) [v407, HERDADO na v408] o PONTO DE CHAMADA REAL do `psion_canto_v407`: a instrucao do main (um `try` que chama tambem `_v407_rodar_specs`) que vem IMEDIATAMENTE depois do fechamento_v406 e IMEDIATAMENTE antes do ponto do tetelestai_terminal_v408 (4e);\n (4e) [v408] o PONTO DE CHAMADA REAL do `tetelestai_terminal_v408`: a instrucao do main (um `try` que chama tambem `_v408_rodar_specs`) que vem IMEDIATAMENTE depois do psion_canto_v407 e IMEDIATAMENTE antes de `_figs = emit_figures(core)`, executada dentro do bloco (4b); confere o registro (16 checagens), que nenhuma chave antiga mudou e o insumo purgado;")
sub('assert len(ipc) == 1 and ipc[0] == ifch + 1 and ipc[0] + 1 == i1, ("a instrucao do psion_canto_v407 nao e\' unica, nao vem IMEDIATAMENTE depois do fechamento_v406 ou nao vem IMEDIATAMENTE antes de emit_figures", ipc, ifch, i1)',
    'itt = [i for i, s_ in enumerate(unp) if "tetelestai_terminal_v408(core)" in s_]\n'
    'assert len(ipc) == 1 and ipc[0] == ifch + 1 and len(itt) == 1 and itt[0] == ipc[0] + 1 and itt[0] + 1 == i1, ("a instrucao do psion_canto_v407 nao e\' unica, nao vem IMEDIATAMENTE depois do fechamento_v406, ou a do tetelestai_terminal_v408 nao e\' unica, nao vem IMEDIATAMENTE depois do psion ou nao vem IMEDIATAMENTE antes de emit_figures", ipc, ifch, itt, i1)\n'
    'itt = itt[0]')
sub('"logo_antes_do_emit_figures": ipc + 1 == i1, "chama_tambem_os_specs_v408": "_v407_rodar_specs(core)" in unp[ipc],', '"logo_antes_do_tetelestai_terminal_v408": ipc + 1 == itt, "chama_tambem_os_specs_v407": "_v407_rodar_specs(core)" in unp[ipc],')
sub('"n_flags_no_FLAGS_json": (len(json.load(open(A.flags, encoding="utf-8"))["flags"]) if A.flags and os.path.exists(A.flags) else None), "n_checks_do_DL": DL.N_CHECKS_FECHO, "ancora_lema": _CP["ancora_lema"], "ancora_par": _CP["ancora_par"]},',
    '"n_flags_no_FLAGS_json": len(json.load(open(os.path.join(DL.V407, DL.D7.KERNEL_DIR, "FLAGS_v407.json"), encoding="utf-8"))["flags"]), "n_checks_do_DL": DL.D7.N_CHECKS_FECHO, "ancora_lema": _CP["ancora_lema"], "ancora_par": _CP["ancora_par"]},   # (v408: o FLAGS da v407 e o DL.D7, porque o ponto e\' HERDADO)')
sub('out["core.psion_canto_v407"] = {"all_verified": pc.get("all_verified"), "verdict": str(pc.get("verdict"))[:300], "falhas": R["ponto_psion_canto"]["mecanica"]["falhos"]}\n',
    'out["core.psion_canto_v407"] = {"all_verified": pc.get("all_verified"), "verdict": str(pc.get("verdict"))[:300], "falhas": R["ponto_psion_canto"]["mecanica"]["falhos"]}\n'
    '# (4e) [v408] o PONTO DE CHAMADA REAL do tetelestai_terminal_v408 (executado dentro do bloco acima): a posicao no main (IMEDIATAMENTE depois do psion_canto_v407, IMEDIATAMENTE antes de emit_figures), o registro, nenhuma chave antiga mudada, o insumo purgado\n'
    'tt = core.get("tetelestai_terminal_v408") or {}; ttv = tt.get("values") or {}\n'
    '_CP8 = um._V408_TERMINAL_CONTRACT; _TP8 = um._V408_TERMINAL_TEXT\n'
    'R["ponto_tetelestai"] = {"indice_no_main": itt, "linha": main.body[itt].lineno, "antes_do_bloco_v393": itt < i0, "logo_depois_do_psion_canto_v407": itt == ipc + 1, "logo_antes_do_emit_figures": itt + 1 == i1, "chama_tambem_os_specs_v408": "_v408_rodar_specs(core)" in unp[itt],\n'
    '                         "instrucao_anterior": unp[itt - 1][:160].replace("\\n", " | "), "dentro_do_bloco_executado": i0 <= itt < i1, "verdict": tt.get("verdict"), "veredito_ok_do_contrato": _TP8["veredito_ok"], "all_verified": tt.get("all_verified"), "runtime_executed": tt.get("runtime_executed"),\n'
    '                         "mecanica": {"passed": (tt.get("mechanics") or {}).get("passed"), "n_checks": (tt.get("mechanics") or {}).get("n_checks"), "falhos": [c_.get("id") for c_ in ((tt.get("mechanics") or {}).get("checks") or []) if not c_.get("ok")]},\n'
    '                         "n_ancoras_ok": ttv.get("n_ancoras_ok"), "n_ancoras": ttv.get("n_ancoras"), "n_modulos_ok": ttv.get("n_modulos_ok"), "n_modulos": ttv.get("n_modulos"), "n_flags_true": ttv.get("n_flags_true"), "n_flags": ttv.get("n_flags"), "escada": ttv.get("escada"), "gate_verdict": ttv.get("gate_verdict"), "respostas_ok": ttv.get("respostas_ok"),\n'
    '                         "does_not_gate_core": tt.get("does_not_gate_core"), "embedded_sources_n_ok": tt.get("embedded_sources_n_ok"), "contrato": {"n_ancoras": len(_CP8["ancoras"]), "n_modulos": _CP8["bundle"]["n"], "n_flags": _CP8["n_flags"], "n_flags_no_FLAGS_json": (len(json.load(open(A.flags, encoding="utf-8"))["flags"]) if A.flags and os.path.exists(A.flags) else None), "n_checks_do_DL": DL.N_CHECKS_FECHO, "ancora_principal": _CP8["ancora_principal"]},\n'
    '                         "ancora_principal": tt.get("ancora_principal"), "ancoras_principais": tt.get("ancoras_principais"), "nome_provisorio": tt.get("nome_provisorio"), "chaves_antigas_que_mudam": tt.get("chaves_antigas_que_mudam"), "chave_do_lema_segue_true": tef.get("linked_to_the_corner_by_a_lemma"), "insumo_purgado": tt.get("insumo_purgado"), "podado": tt.get("podado"),\n'
    '                         "fica_false_por_teorema": {"qg_closure.gate.full_static_witness_exists": ((core.get("qg_closure") or {}).get("gate") or {}).get("full_static_witness_exists"), "witness_rigidity.trivial_inhabitant_exists": (core.get("witness_rigidity") or {}).get("trivial_inhabitant_exists")}, "fica_aberto": tt.get("fica_aberto")}\n'
    'out["core.tetelestai_terminal_v408"] = {"all_verified": tt.get("all_verified"), "verdict": str(tt.get("verdict"))[:300], "falhas": R["ponto_tetelestai"]["mecanica"]["falhos"]}\n')
sub('                   "v408_psion_canto_e_specs": [k for k in list(um._V407_REGISTROS_FUNCAO) + list(um._V407_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],\n',
    '                   "v407_psion_canto_e_specs": [k for k in list(um._V407_REGISTROS_FUNCAO) + list(um._V407_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],   # (os da v407: HERDADOS na v408)\n'
    '                   "v408_tetelestai_e_specs": [k for k in list(um._V408_REGISTROS_FUNCAO) + list(um._V408_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],\n')
sub('"registros_v407": {n_: ((seal.get("registros_v407") or {}).get(n_) or {}).get("all_verified") for n_ in um._V407_NOMES_REGISTROS}}',
    '"registros_v407": {n_: ((seal.get("registros_v407") or {}).get(n_) or {}).get("all_verified") for n_ in um._V407_NOMES_REGISTROS},\n'
    '                 "tetelestai_terminal_v408": {x: (seal.get("tetelestai_terminal_v408") or {}).get(x) for x in ("verdict", "all_verified")}, "registros_v408": {n_: ((seal.get("registros_v408") or {}).get(n_) or {}).get("all_verified") for n_ in um._V408_NOMES_REGISTROS}}')
sub('ppc = R["ponto_psion_canto"]   # (4d) o ponto NOVO da v408', 'ppc = R["ponto_psion_canto"]   # (4d) o ponto da v407, HERDADO na v408 (os numeros dele: DL.D7 e o FLAGS da v407)')
sub('        or not ppc.get("logo_depois_do_fechamento_v407") or not ppc.get("logo_antes_do_emit_figures") or not ppc.get("chama_tambem_os_specs_v408") or ppc.get("verdict") != ppc.get("veredito_ok_do_contrato")',
    '        or not ppc.get("logo_depois_do_fechamento_v407") or not ppc.get("logo_antes_do_tetelestai_terminal_v408") or not ppc.get("chama_tambem_os_specs_v407") or ppc.get("verdict") != ppc.get("veredito_ok_do_contrato")')
sub('        or (ppc.get("mecanica") or {}).get("passed") is not True or (ppc.get("mecanica") or {}).get("n_checks") != DL.N_CHECKS_FECHO or (ppc.get("mecanica") or {}).get("falhos")',
    '        or (ppc.get("mecanica") or {}).get("passed") is not True or (ppc.get("mecanica") or {}).get("n_checks") != DL.D7.N_CHECKS_FECHO or (ppc.get("mecanica") or {}).get("falhos")')
sub('or ppc.get("n_modulos_ok") != DL.N_BUNDLE or ppc.get("n_modulos") != DL.N_BUNDLE or', 'or ppc.get("n_modulos_ok") != DL.D7.N_BUNDLE or ppc.get("n_modulos") != DL.D7.N_BUNDLE or')
sub('        or ppc.get("does_not_gate_core") is not True or ppc.get("embedded_sources_n_ok") != DL.N_BUNDLE or ppc.get("lemma") != DL.ANCORA_LEMA or ppc.get("pair_theorem") != DL.ANCORA_PAR',
    '        or ppc.get("does_not_gate_core") is not True or ppc.get("embedded_sources_n_ok") != DL.D7.N_BUNDLE or ppc.get("lemma") != DL.D7.ANCORA_LEMA or ppc.get("pair_theorem") != DL.D7.ANCORA_PAR')
sub('if R["troca_dita_v408"]["ok"] is not True: falsos.append("troca_dita_v408")\n',
    'ptt = R["ponto_tetelestai"]   # (4e) o ponto NOVO da v408\n'
    'if (ptt.get("all_verified") is not True or ptt.get("runtime_executed") is not True or not ptt.get("dentro_do_bloco_executado") or not ptt.get("logo_depois_do_psion_canto_v407") or not ptt.get("logo_antes_do_emit_figures") or not ptt.get("chama_tambem_os_specs_v408") or ptt.get("verdict") != ptt.get("veredito_ok_do_contrato")\n'
    '        or not str(ptt.get("verdict") or "").startswith(DL.VEREDITO_OK_PREFIXO) or not str(ptt.get("verdict") or "").endswith(DL.VEREDITO_SUFIXO) or (ptt.get("mecanica") or {}).get("passed") is not True or (ptt.get("mecanica") or {}).get("n_checks") != DL.N_CHECKS_FECHO or (ptt.get("mecanica") or {}).get("falhos")\n'
    '        or ptt.get("n_ancoras_ok") != ptt.get("n_ancoras") or ptt.get("n_ancoras") != ptt["contrato"]["n_ancoras"] or ptt["contrato"]["n_ancoras"] != len(DL.ANCORAS) or ptt.get("n_modulos_ok") != DL.N_BUNDLE or ptt.get("n_modulos") != DL.N_BUNDLE or ptt.get("n_flags_true") != ptt.get("n_flags") or ptt.get("n_flags") != ptt["contrato"]["n_flags"] or (ptt["contrato"]["n_flags_no_FLAGS_json"] is not None and ptt["contrato"]["n_flags"] != ptt["contrato"]["n_flags_no_FLAGS_json"])\n'
    '        or ptt.get("does_not_gate_core") is not True or ptt.get("embedded_sources_n_ok") != DL.N_BUNDLE or ptt.get("ancora_principal") != DL.ANCORA_PRINCIPAL or ptt.get("ancoras_principais") != list(DL.ANCORAS_PRINCIPAIS) or ptt.get("nome_provisorio") is not None or ptt.get("chaves_antigas_que_mudam") != [] or ptt.get("chave_do_lema_segue_true") is not True or ptt.get("respostas_ok") is not True\n'
    '        or any(v_ is not False for v_ in ptt["fica_false_por_teorema"].values()) or (ptt.get("insumo_purgado") or {}).get("integra_pinada") is not False or (ptt.get("insumo_purgado") or {}).get("integra_fora_do_espelho") is not True): falsos.append("ponto_tetelestai")\n'
    'if R["troca_dita_v408"]["ok"] is not True: falsos.append("troca_dita_v408")\n')
assert "[A ADAPTAR" not in t
ast.parse(t); open(P, "wb").write(t.encode("utf-8")); print("ok exame", len(t))
