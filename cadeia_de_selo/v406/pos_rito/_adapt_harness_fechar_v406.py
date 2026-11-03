# -*- coding: utf-8 -*-
"""_adapt_harness_fechar_v406.py -- as edicoes de harness_fechar_sandbox_v406.py (chamado por adaptar_pos_rito_v406.py): o sandbox leva o que o delta_v406 pina por assert (BUNDLE com o caminho do MANIFEST reescrito, o MANIFEST da integracao, o resultado da Fase 9 V2) e a cadeia de siblings
v405 -> v404 -> ... -> v399; os controles negativos do fechar passam a ser os do fechamento."""

SANDBOX_EXTRA = r'''# v406 (desvio do molde, dito): o delta_v406 PINA POR ASSERT o caminho absoluto do MANIFEST da integracao R3 (BUNDLE_v406.json: origem_integracao == MANIFEST_INTEGRACAO_ARQ, derivado da pasta do pacote) e o sha16 do resultado da Fase 9 V2: o sandbox leva o MANIFEST (copia de bytes) na mesma posicao relativa
# dentro de work\fechamento_02nov, o resultado da Fase 9 V2 em work\fase9_v2_c1_23out\saidas e uma COPIA do BUNDLE_v406.json em que SO' o campo origem_integracao e' reescrito para o caminho do sandbox (sha256_manifesto_integracao fica: o MANIFEST e' o mesmo, byte a byte); a candidata vai em pedra\
_bd_ = rdj(os.path.join(PKG, "BUNDLE_v406.json"))
_man_sb = os.path.join(SB, "work", "fechamento_02nov", os.path.relpath(_dm.MANIFEST_INTEGRACAO_ARQ, _dm.ESTUDO_FECHO))
os.makedirs(os.path.dirname(_man_sb), exist_ok=True); shutil.copyfile(_dm.MANIFEST_INTEGRACAO_ARQ, _man_sb)
_bd_["origem_integracao"] = _man_sb.replace(os.sep, "/")
open(os.path.join(PKS, "BUNDLE_v406.json"), "w", encoding="utf-8").write(json.dumps(_bd_, ensure_ascii=False, indent=1))
os.makedirs(os.path.join(SB, "work", "fase9_v2_c1_23out", "saidas"), exist_ok=True); shutil.copyfile(_dm.FASE9_V2_ARQ, os.path.join(SB, "work", "fase9_v2_c1_23out", "saidas", os.path.basename(_dm.FASE9_V2_ARQ)))
os.makedirs(os.path.join(PKS, "pedra"), exist_ok=True); shutil.copyfile(_dm.TESTEMUNHA["src"], os.path.join(PKS, "pedra", os.path.basename(_dm.TESTEMUNHA["src"])))
for _n_ in ("FORMAL_MAP_v406.json", "CANDIDATO_v406.json"):
    if not os.path.exists(os.path.join(PKS, _n_)):
        shutil.copyfile(os.path.join(PKG, _n_), os.path.join(PKS, _n_))
'''

CONTROLES_1C = r'''_recusa_com_core("fechar_fecho_valor_adulterado", "o numero de modulos ok do fechamento_v406 adulterado no core (300 de 301)", lambda c: c["fechamento_v406"]["values"].__setitem__("n_modulos_ok", 300))
_recusa_com_core("fechar_fecho_chave_false", "a chave rede_fock_v394.whole_certificate_inhabited de volta a False no core (o literal)", lambda c: c["rede_fock_v394"].__setitem__("whole_certificate_inhabited", False))
_recusa_com_core("fechar_fecho_frase_proibida", "uma frase proibida nos limites do fechamento_v406", lambda c: c["fechamento_v406"]["limites"].append("o unico autovetor da luz"))
_recusa_com_core("fechar_psion_adulterado", "numero do Ponto Zero do Psion (recriado) adulterado no core (hbar omega)", lambda c: c["ponto_zero_do_psion_v405"]["values"].__setitem__("hbar_omega_meV", 17.5))
_recusa_com_core("fechar_f2b_adulterado", "numero da errata de F2b adulterado no core (a previsao do par)", lambda c: c["f2b_errata_v404"]["values"].__setitem__("previsao_do_par", 0.1))
_recusa_com_core("fechar_f2b_canal_ainda_awaiting", "o canal F2b ainda AWAITING no core (a retirada nao aconteceu)", lambda c: c["f2b_errata_v404"].__setitem__("F2b_status_now", "AWAITING"))
_recusa_com_core("fechar_v1_reescrito", "o V1 do ramo B reescrito no core (F2b_status do registro da v386)", lambda c: c["ramo_b_preregistration_v386"].__setitem__("F2b_status", "WITHDRAWN"))
_recusa_com_core("fechar_angle_status_reescrito", "o texto antigo de neutrino_mass.angle_status reescrito no core (a errata e' ao lado)", lambda c: c["neutrino_mass"].__setitem__("angle_status", "sin(45deg) agora e DERIVADO"))
_recusa_com_core("fechar_gate_adulterado", "numero do gate (recriado) adulterado no core (17 calculadas)", lambda c: c["bandeiras_do_gate_v403"]["values"].__setitem__("n_calculated", 17))
_recusa_com_core("fechar_bandeira_do_gate_false", "uma bandeira calculada do gate (linearized_spin2_finite_face) False no core", lambda c: c["qg_closure"]["physics_flags"].__setitem__("linearized_spin2_finite_face", False))
_recusa_com_core("fechar_caminho_v405_adulterado", "numero do caminho da v403 (recriado) adulterado no core (energia minima do nucleo)", lambda c: c["caminho_v403"]["values"].__setitem__("min_core_energy", 0.31))
_recusa_com_core("fechar_ponte_v402_adulterada", "numero da ponte da v402 (recriada) adulterado no core", lambda c: c["ponte_da_escala_dual_v402"]["values"].__setitem__("min_null_energy_shift", 0.31))
'''

PORTA_ISOLADA = r'''# a PORTA do paragrafo novo isolada: T.paragrafo_v406() da copia do sandbox tem de LEVANTAR com o numero de modulos adulterado no core (a verificacao compara com os numeros de ESPERADOS e de delta_v406)
cj = json.loads(raw_core.decode("utf-8")); cj["core"]["fechamento_v406"]["values"]["n_modulos_ok"] = 300
open(core_p, "wb").write(json.dumps(cj, ensure_ascii=False).encode("utf-8"))
import importlib.util as _iu1
_sp1 = _iu1.spec_from_file_location("textos_sb1", os.path.join(POS, "textos_v406.py")); _t1 = _iu1.module_from_spec(_sp1); _sp1.loader.exec_module(_t1)
try:
    _t1.paragrafo_v406(); _levanta1 = False
except Exception as _ex1:   # noqa: BLE001
    _levanta1 = isinstance(_ex1, AssertionError)
NEG.append({"controle": "a porta do paragrafo novo (paragrafo_v406, chamada pelo fechar) levanta com o numero de modulos do fechamento_v406 adulterado", "rc": 2 if _levanta1 else 0, "recusou": _levanta1, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v406-custodia.md"))})
open(core_p, "wb").write(raw_core)
'''

CONTROLES_V406 = r'''_recusa_com_core("fechar_direcao_invertida", "a direcao do testemunho invertida no core (a IALD como quem testifica do operador; declaracao da v399 recriada)", lambda c: c["declaracao_do_operador_v399"]["declaration"]["direcao_do_testemunho"].__setitem__("a_IALD", "testifica do operador"))
_recusa_com_core("fechar_inscricao_nao_embutida", "uma inscricao de 02/11 deixou de estar embutida no core (cunhagens_v406)", lambda c: list(c["cunhagens_v406"]["verbatim"].values())[0].__setitem__("embedded_ok", False))
_recusa_com_core("fechar_sem_errata", "falta uma das erratas E14 a E17 (em nome da gerencia) no core", lambda c: c["cunhagens_v406"]["erratas"].pop())
_recusa_com_core("fechar_sem_decisao", "falta uma das decisoes D34 a D40 da gerencia no core", lambda c: c["cunhagens_v406"]["extras"]["decisoes"].pop("D40"))
_recusa_com_core("fechar_leitura_sem_onto", "a leitura de 02/11 dita [REAL] no core (e' ONTO)", lambda c: c["cunhagens_v406"]["extras"]["leituras"].__setitem__("estatuto", "[REAL]"))
_recusa_com_core("fechar_pedra_v403_adulterada", "a pedra selada da v403 (Caminho) adulterada no hash formal do core", lambda c: c["kernel_formalization"]["formal_files_sha256"].__setitem__("TGLExt/Caminho.lean", "0" * 64))
for _nm, _ia in (("topo", 0), ("certificado", 2)):
    _recusa_com_core("fechar_ancora_%s_fora_do_trio" % _nm, "a ancora %s fora do trio no core" % _nm, lambda c, _ia=_ia: c["kernel_formalization"]["axiom_report"].__setitem__(list(_dm.ANCORAS)[_ia], ["propext", "sorryAx"]))
'''

STUB_V_VELHO = "'reg406': {'cunhagens_v405': {'ok': True}}, "
STUB_V_NOVO = "'reg406': {'cunhagens_v406': {'ok': True}}, 'reg405c': {'cunhagens_v405': {'ok': True}}, 'fecho': {'ok': True}, 'ancoras': {}, 'bandeiras': {}, 'chaves': {}, 'fun405c': {}, "


def rodar(A):
    nome = "harness_fechar_sandbox_v406.py"
    txt, crlf, raw = A.le(nome)
    if A.pula(nome, txt):
        return
    t = A.tira_cabecalho(txt)
    for velho, novo in (("B11 (v405) -> B12 (v406)", "B14 (v405) -> B15 (v406)"), ("B11 -> B12", "B14 -> B15"), ("B13 -> B14", "B14 -> B15"), ("(Caminho, Verdade e Vida)", "(o fechamento)"), ("(a massa derivada e a identidade definida)", "(o fechamento)"),
                        ("a NOTA ao lado do paragrafo da v405", "a NOTA ao lado dos paragrafos anteriores"), ("com as TRES pedras novas", "com os 301 modulos novos"), ("(as oito pedras novas)", "(os 301 modulos novos)"), ("diff do kernel traz as %d pedras novas", "diff do kernel traz os %d modulos novos"),
                        ("nem de leitura_v405", "nem de leitura_v406"), ("textos_v406/leitura_v405", "textos_v406/leitura_v406"), ("com um numero da ponte da v405 recriada adulterado", "com um numero do fechamento_v406 adulterado")):
        t = t.replace(velho, novo)
    # ---- os stubs da fila
    t = A.sub(t, "TOPICO_NOVO = 'v406-selada-massa-derivada-e-identidade.md'\nREGS = 'ponte_da_massa_v405 massa_tensao_pura_v405 identidade_v405 observador_terminal_v405 lei_do_diminuto_v405 tonica_do_hamiltoniano_v405 disco_de_euler_v405 ponto_zero_do_psion_v405 cunhagens_v405 campos_fechados_e_leituras_v405 ga_reclassificacao_v405 gap_v405 kh_n1_cobertura_v405'",
              "TOPICO_NOVO = 'v406-selada-o-fechamento.md'\nREGS = 'fechamento_v406 cunhagens_v406 kh_n1_cobertura_v406'")
    t = A.sub(t, '"(handoff-v406-pontes-da-massa-e-espelho-30out.md)" in l]', '"(handoff-v405-custodia.md)" in l and l.startswith("- [")]')
    t = A.sub(t, "(\"linha do handoff de 30/10 da v406 no MEMORY.md da copia\"", "(\"linha do handoff da custodia da v405 no MEMORY.md da copia\"")
    # ---- o sandbox: a cadeia de siblings inclui a v404; o delta pina caminhos absolutos
    t = A.sub(t, 'for _vv in ("v405", "v403", "v402", "v401", "v400", "v399"):', 'for _vv in ("v405", "v404", "v403", "v402", "v401", "v400", "v399"):')
    t = A.sub(t, 'for _vp in ("v405", "v403", "v402", "v401", "v399"):', 'for _vp in ("v405", "v404", "v403", "v402", "v401", "v399"):')
    t = A.sub(t, 'for n in ("guarda_p18_v406.py", "guarda_frases_v406.py", "PINO_DAS_PEDRAS_DETALHE_v406.json", "VERBATIM_CONGELADO_v406.json",', 'for n in ("guarda_p18_v406.py", "guarda_frases_v406.py", "PINO_DAS_PEDRAS_DETALHE_v406.json", "VERBATIM_CONGELADO_v406.json", "FORMAL_MAP_v406.json",')
    ancora = '_dlx = importlib.util.spec_from_file_location("delta_v406_h", os.path.join(PKG, "delta_v406.py")); _dm = importlib.util.module_from_spec(_dlx); _dlx.loader.exec_module(_dm)\n'
    t = A.sub(t, ancora, ancora + SANDBOX_EXTRA)
    # ---- os controles negativos do fechar
    t = A.entre(t, '_recusa_com_core("fechar_ponte_adulterada"', "# a PORTA do paragrafo novo isolada:", CONTROLES_1C)
    t = A.entre(t, "# a PORTA do paragrafo novo isolada:", '_recusa_com_core("fechar_direcao_invertida"', PORTA_ISOLADA)
    t = A.entre(t, '_recusa_com_core("fechar_direcao_invertida"', "sj = json.loads(raw_sc.decode(\"utf-8\")); sj[\"objetos\"][1][\"sha256\"]", CONTROLES_V406)
    # ---- o fechar positivo e o manifesto
    t = A.sub(t, 'for k_ in ("registros_v405", "registros_v404", "registros_v403", "registros_v402", "registros_v401", "registros_v399", "registros_funcao_v406", "campos_fechados_e_leituras_v405", "ga_reclassificacao_v405", "gap_v405", "f2b_errata",',
              'for k_ in ("registros_v406", "registros_v405", "registros_v404", "registros_v403", "registros_v402", "registros_v401", "registros_v399", "registros_funcao_v406", "ancoras_v406", "bandeiras_v406", "chaves_v406", "f2b_errata",', 2)
    # ---- os stubs de leitura
    t = A.sub(t, STUB_V_VELHO, STUB_V_NOVO)
    t = A.sub(t, "TOPICO_NOVO = \\'v406-selada-jo8v32-projecao-transversal.md\\'", "TOPICO_NOVO = \\'v406-selada-o-fechamento.md\\'")
    A.grava(nome, t, crlf, raw)
