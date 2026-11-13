# -*- coding: utf-8 -*-
"""_adapt_simular_arvore_v411.py -- (claude-construtor-v411, fork C, 12/11/2026) monta simular_arvore_do_nos_v411.py a partir do ORIGINAL ..\\v410\\simular_arvore_do_nos_v410.py (nao da copia bumpada), com trocas
DITAS e cada ancora unica: o delta da v411; o candidato/artefato por DL.CANDIDATO_ARQ; a pasta sim_<sha16> FORA de work (DL.RODADA_PAI); a saida SIMULACAO_ARVORE_NOS_<sha16>.json em DL.saida (com DL.MARCA_ENSAIO); o registro
h0dn_bg1_v411 e os specs da v411 rodam DEPOIS dos specs da v410, como no main; os registros da v410 viram heranca (DL.REGISTROS_FUNCAO_V410); o FORMAL_MAP e o manifesto lidos por DL.FORMAL_MAP_ARQ / DL.MANIFESTO_ARQ;
o h8 da v411 nao traz extras_fora_do_corpo_embutido_no_nos: os residuais do hash tem de estar entre os extras copiados do Nos. Backup de BYTES do destino antes. uso: python -B -X utf8 _adapt_simular_arvore_v411.py"""
import ast, datetime, os
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), "v410", "simular_arvore_do_nos_v410.py")
DST = os.path.join(HERE, "simular_arvore_do_nos_v411.py")
t = open(SRC, "rb").read().decode("utf-8"); assert "\r" not in t
cab = ("# -*- coding: utf-8 -*-\n"
       "# [ADAPTADO v411, 12/11/2026, claude-construtor-v411 (retomada, fork C)] montado por _adapt_simular_arvore_v411.py do ORIGINAL v410/simular_arvore_do_nos_v410.py: o registro com funcao h0dn_bg1_v411 e os specs da v411 (cunhagens_v411, kh_n1_cobertura_v411)\n"
       "# rodam na ordem do main, DEPOIS dos specs da v410; os quatro registros com funcao da v410 (iald2_v410, a_escala_v410, h0dn_bg1_v410, h0dn_fontes_hms13_v410) e os specs da v410 sao HERANCA; nenhum modulo novo; a pasta sim_ FORA de work; saida em DL.saida.\n")
PARES = [
    ("# -*- coding: utf-8 -*-\n", cab),
    ('"""simular_arvore_do_nos_v410.py -- simula', '"""simular_arvore_do_nos_v411.py -- (v411: o kernel e\' o da v410 byte a byte; o registro h0dn_bg1_v411 e os specs da v411 depois dos da v410, herdados) simula'),
    ("import delta_v410 as DL  # noqa: E402\n", "import delta_v411 as DL  # noqa: E402\n"),
    ('ap.add_argument("--candidato", default=os.path.join(H, DL.CANDIDATO))', 'ap.add_argument("--candidato", default=DL.CANDIDATO_ARQ)'),
    ('SIM = os.path.join(H, "sim_" + SHA[:16]); os.makedirs(SIM, exist_ok=True)',
     'SIM = os.path.join(DL.RODADA_PAI, "sim_" + SHA[:16])   # (v411, D135: a copia do kernel por rodada fica FORA de work)\nif os.path.isdir(SIM):\n    shutil.rmtree(SIM)\nos.makedirs(SIM)'),
    ("um.a_escala_v410(core); um.h0dn_bg1_v410(core); um.h0dn_fontes_hms13_v410(core); um._v410_rodar_specs(core)   # (v410, D72:",
     "um.a_escala_v410(core); um.h0dn_bg1_v410(core); um.h0dn_fontes_hms13_v410(core); um._v410_rodar_specs(core); um.h0dn_bg1_v411(core); um._v411_rodar_specs(core)   # (v411: o h0dn_bg1_v411 -- o teste aberto uma vez, recalculado dos bytes embutidos -- e os specs da v411 DEPOIS do bloco da v410, como no main) (v410, D72:"),
    ('for k in tuple(DL.REGISTROS_FUNCAO) + ("cunhagens_v410", "kh_n1_cobertura_v410", "traducao_turing_v409",',
     'for k in tuple(DL.REGISTROS_FUNCAO) + (DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO) + tuple(DL.REGISTROS_FUNCAO_V410) + ("cunhagens_v410", "kh_n1_cobertura_v410", "traducao_turing_v409",'),
    ('# (v410) a arvore simulada contra o FORMAL_MAP_v410.json e contra o h8 do CANDIDATO: os embutidos iguais ao mapa, os residuais do Nos = a diferenca, o total = o do CANDIDATO\n'
     'FM = json.load(open(os.path.join(H, "FORMAL_MAP_v410.json"), encoding="utf-8")); CM = json.load(open(os.path.join(H, "CANDIDATO_v410.json"), encoding="utf-8")); H8 = CM["h8"]',
     '# (v411) a arvore simulada contra o FORMAL_MAP_v411.json e contra o h8 do manifesto: os embutidos iguais ao mapa, os residuais do Nos = a diferenca, o total = o do manifesto\n'
     'FM = json.load(open(DL.FORMAL_MAP_ARQ, encoding="utf-8")); CM = json.load(open(DL.MANIFESTO_ARQ, encoding="utf-8")); H8 = CM["h8"]; assert CM["sha16"] == SHA[:16], ("o manifesto nao e\' deste arquivo", CM["sha16"], SHA[:16])'),
    ('R["formal_map_v410"] = {', 'R["formal_map_v411"] = {'),
    ('"witness_layers_canonical_full_witness_term_constructed": {"da_base_v409_selada": _wl_antes,', '"witness_layers_canonical_full_witness_term_constructed": {"da_base_v410_selada": _wl_antes,'),
    ('R["formal_map_v410"]["ok"] = bool(not R["formal_map_v410"]["diferentes_do_mapa"] and not R["formal_map_v410"]["ausentes_do_mapa_na_arvore"] and R["formal_map_v410"]["a_mais_na_arvore_alem_do_mapa"] == H8["residuais_do_nos"] and len(FM) == H8["embutidas"] == len(emb)\n'
     '                                  and len(_arv) == H8["entradas"] == len(FM) + len(H8["residuais_do_nos"]) and sorted(extras) == sorted(H8["extras_fora_do_corpo_embutido_no_nos"]) and R["formal_map_v410"]["kf_formal_files_sha256_igual_a_arvore"] and R["formal_map_v410"]["witness_layers_canonical_full_witness_term_constructed"]["recomputado_pela_expressao_do_run_um_do_candidato"] is True)',
     'R["formal_map_v411"]["ok"] = bool(not R["formal_map_v411"]["diferentes_do_mapa"] and not R["formal_map_v411"]["ausentes_do_mapa_na_arvore"] and R["formal_map_v411"]["a_mais_na_arvore_alem_do_mapa"] == H8["residuais_do_nos"] and len(FM) == H8["embutidas"] == len(emb)\n'
     '                                  and len(_arv) == H8["entradas"] == len(FM) + len(H8["residuais_do_nos"]) and set(H8["residuais_do_nos"]) <= set(extras) and R["formal_map_v411"]["kf_formal_files_sha256_igual_a_arvore"] and R["formal_map_v411"]["witness_layers_canonical_full_witness_term_constructed"]["recomputado_pela_expressao_do_run_um_do_candidato"] is True)\n'
     'R["registros_v411_selaram"] = {k_: (core.get(k_) or {}).get("all_verified") for k_ in tuple(DL.REGISTROS_FUNCAO) + (DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO)}\n'
     'R["p2_ao_lado_da_v387"] = (core.get(DL.FECHO_REGISTRO) or {}).get("p2_ao_lado_da_v387")\n'
     'R.update(DL.MARCA_ENSAIO)'),
    ('json.dump(R, open(os.path.join(H, "SIMULACAO_ARVORE_NOS_%s.json" % SHA[:16]), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)',
     '_pS = DL.saida("SIMULACAO_ARVORE_NOS_%s.json" % SHA[:16]); open(_pS + ".tmp", "w", encoding="utf-8").write(json.dumps(R, ensure_ascii=False, indent=1, default=str)); os.replace(_pS + ".tmp", _pS)'),
]
for a_, n_ in PARES:
    assert t.count(a_) == 1, (a_[:100], t.count(a_))
    t = t.replace(a_, n_, 1)
t = t.replace('uso: python -B -X utf8 simular_arvore_do_nos_v410.py', 'uso: python -B -X utf8 simular_arvore_do_nos_v411.py')
ast.parse(t)
b0 = open(DST, "rb").read()
bak = DST + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_forkc"; open(bak, "wb").write(b0); assert open(bak, "rb").read() == b0
nb = t.encode("utf-8"); open(DST + ".tmp", "wb").write(nb); assert os.path.getsize(DST + ".tmp") == len(nb); os.replace(DST + ".tmp", DST)
print("ok", DST, len(b0), "->", len(nb))
