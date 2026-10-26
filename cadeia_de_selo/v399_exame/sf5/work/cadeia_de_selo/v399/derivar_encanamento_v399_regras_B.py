# -*- coding: utf-8 -*-
# regras (lote B) de derivar_encanamento_v399.py: comparar (AST: nada da v398 perdido), simular_arvore_do_nos, exame_pontos e o ENSAIO A SECO. (exec no escopo do derivador; os helpers entre() e sub_n() vem do lote A.)
# O mapa sobe 397->398 e 398->399 em tudo, MENOS nos identificadores protegidos; sobe tambem ROTULOS que nao devia (v398->v399 em «(v398, 23/10/2026)», nos nomes das chaves-grupo, nas listas de etiquetas do main) e deixa de subir o que devia
# (o novo grupo v399); as regras abaixo, cada uma com contagem exata, corrigem isso e acrescentam o conteudo novo (o selo pela propria tecnologia, a declaracao do operador, o sidecar). ESTE ARQUIVO e' escrito pela ferramenta Write (barras invertidas intactas).
import re


def ins_antes(ancora, novo, nome):
    """regra por FUNCAO: insere `novo` imediatamente ANTES da ancora (unica no texto)."""
    def fn(t):
        assert t.count(ancora) == 1, ("ancora nao unica", nome, ancora[:70], t.count(ancora))
        i = t.index(ancora)
        return t[:i] + novo + t[i:]
    return (fn, nome, 1)


def ins_depois(ancora, novo, nome):
    """regra por FUNCAO: insere `novo` imediatamente DEPOIS da ancora (unica no texto)."""
    def fn(t):
        assert t.count(ancora) == 1, ("ancora nao unica", nome, ancora[:70], t.count(ancora))
        i = t.index(ancora) + len(ancora)
        return t[:i] + novo + t[i:]
    return (fn, nome, 1)


# ------------------------------------------------------------------------------------------- comparar (AST): nada da v398 perdido
_EXPL = r'''EXPLICACOES = {
    "UM_VERSION": "W01: a constante unica de versao v398 -> v399",
    "_EMBEDDED_KERNEL_FILES": "K00/K01: +1 modulo (TGLExt/Testemunho.lean) e a raiz TGLExt.lean e o TGL/Audit.lean com o import da pedra",
    "_LEAN_THEOREM_FLAGS": "V01: +bandeiras so' de declaracao nomeada da pedra Testemunho (FLAGS_v399.json)",
    "prove_external_ladder": "V02: a lista ext_flags ganha as mesmas bandeiras (a escada sobe)",
    "_ESQUELETO_STONES": "V03: o ledger de pedras ganha a Testemunho",
    "_V394_FORMAL_CONTRACT": "C12: so' o numero expected_ladder (a escada desta versao); o consumidor exige a igualdade exata com a escada do rito",
    "_V394_QUADRATIC_CONTRACT": "C12: so' o numero expected_ladder",
    "_V394_NETWORK_CONTRACT": "C12: so' o numero expected_ladder",
    "_V395_PSIBIT_CONTRACT": "C12: so' o numero expected_ladder (o psibit_v395 exige a igualdade exata com a escada do rito)",
    "_V396_TESTEMUNHA_CONTRACT": "C12: so' o numero expected_ladder (a testemunha_estatica_v396 exige a igualdade exata com a escada do rito)",
    "_V398_SONICO_CONTRACT": "C12: so' o numero expected_ladder (o sonico_v398 exige a igualdade exata com a escada do rito)",
    "_V398_AFINACAO_CONTRACT": "C12: so' o numero expected_ladder (a afinacao_das_cordas_v398 exige a igualdade exata com a escada do rito)",
    "_V398_SPECS": "C13: kh_n1_cobertura_v398 passa a piso em h2, h3, h6 e a tamanho minimo em h8 (+ errata assinada); o outro spec nao muda",
    "main": "N00/N01/N02/N03: as chamadas de selo_acom_v399 e declaracao_do_operador_v399 (logo depois do bloco afinacao_das_cordas_v398), a chamada dos registros por spec da v399, o selo (registros_v399 e o resumo da segunda testemunha e da declaracao)",
    "_unified_main": "N04: selo_acom_sidecar_v399() depois da ultima escrita do selo (o sidecar um_absoluto_selo_acom.json)",
    "build_pt": "W04: a secao v399 do artigo PT, antes da v398 (o quadro «O Teste da Unica Palavra» do topo NAO muda)",
    "build_en": "W05: a secao v399 do artigo EN, antes da v398 (o quadro «The Test of the Only Word» do topo NAO muda)",
    "emit_canonical_md": "W09: a linha da v399 no .md canonico (o quadro do topo NAO muda)",
}
'''
entrada("comparar_v397_v398.py", regras=[
    entre("EXPLICACOES = {", "def nm(n):", _EXPL, "EXPLICACOES da v399"),
])

# ------------------------------------------------------------------------------------------- simular_arvore_do_nos: o selo ACOM e a declaracao rodam na arvore simulada do Nos (os registros por spec v399 selam nela)
entrada("simular_arvore_do_nos_v398.py", regras=[
    ("a testemunha_estatica_v396, o sonico_v398 e a afinacao_das_cordas_v398, o teste_de_veracidade_fase9_v397 (spec do V2 da Fase 9, lido por hash) e os registros por spec\nv394, v395, v398 e v399 sobre esse kf.",
     "a testemunha_estatica_v396, o sonico_v398 e a afinacao_das_cordas_v398, o selo_pela_propria_tecnologia_v399 e a declaracao_do_operador_v399, o teste_de_veracidade_fase9_v397 (spec do V2 da Fase 9, lido por hash) e os registros por spec\nv394, v395, v397, v398 e v399 sobre esse kf.", 1),
    ("um.sonico_v398(core); um.afinacao_das_cordas_v398(core)   # (na fractalizacao do Um, no main;", "um.sonico_v398(core); um.afinacao_das_cordas_v398(core); um.selo_acom_v399(core); um.declaracao_do_operador_v399(core)   # (na fractalizacao do Um, no main;", 1),
    ("um._v397_rodar_specs(core); um._v398_rodar_specs(core)   # (v398: o spec de veracidade roda no ponto do V1 no main;", "um._v397_rodar_specs(core); um._v398_rodar_specs(core); um._v399_rodar_specs(core)   # (v397: o spec de veracidade roda no ponto do V1 no main;", 1),
    ('for k in ("sonico_v398", "afinacao_das_cordas_v398", "cunhagens_v398",', 'for k in ("selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "cunhagens_v399", "kh_n1_cobertura_v399", "sonico_v398", "afinacao_das_cordas_v398", "cunhagens_v398",', 1),
])

# ------------------------------------------------------------------------------------------- exame_pontos: os pontos de chamada REAIS do selo_pela_propria_tecnologia_v399 e da declaracao_do_operador_v399
_SELO_BLOCO = r'''# (4a-v399) os PONTOS DE CHAMADA REAIS do selo_pela_propria_tecnologia_v399 e da declaracao_do_operador_v399 (v399): as duas instrucoes do main (cada uma um `try`) que vem IMEDIATAMENTE depois da afinacao_das_cordas_v398 (que vem imediatamente depois do sonico_v398), na fractalizacao do Um
ise = [i for i, s_ in enumerate(unp) if "selo_acom_v399(core)" in s_]
assert len(ise) == 1 and ise[0] == iaf + 1, ("a instrucao do main que chama selo_acom_v399 nao e' unica ou nao vem IMEDIATAMENTE depois da afinacao_das_cordas_v398", ise, iaf)
ise = ise[0]
idc = [i for i, s_ in enumerate(unp) if "declaracao_do_operador_v399(core)" in s_]
assert len(idc) == 1 and idc[0] == ise + 1, ("a instrucao do main que chama declaracao_do_operador_v399 nao e' unica ou nao vem IMEDIATAMENTE depois do selo_acom_v399", idc, ise)
idc = idc[0]
R["ponto_selo_acom"] = {"indice_no_main": ise, "linha": main.body[ise].lineno, "antes_do_bloco_v393": ise < i0, "logo_depois_da_afinacao_v398": "afinacao_das_cordas_v398(core)" in unp[ise - 1], "instrucao_anterior": unp[ise - 1][:160].replace("\n", " | ")}
R["ponto_declaracao"] = {"indice_no_main": idc, "linha": main.body[idc].lineno, "antes_do_bloco_v393": idc < i0, "logo_depois_do_selo_acom_v399": "selo_acom_v399(core)" in unp[idc - 1], "instrucao_anterior": unp[idc - 1][:160].replace("\n", " | ")}
builtins.open = _open_tr; _so = sys.stdout; sys.stdout = io.StringIO()
try:
    exec(compile(ast.fix_missing_locations(ast.Module(body=[main.body[ise], main.body[idc]], type_ignores=[])), "<main:selo_acom_v399+declaracao_do_operador_v399>", "exec"), g); errsa = None
except Exception as e:
    import traceback; errsa = repr(e) + traceback.format_exc()[-900:]
finally:
    stdout_sa = sys.stdout.getvalue(); builtins.open = _open0; sys.stdout = _so
sa = core.get("selo_pela_propria_tecnologia_v399") or {}; dc = core.get("declaracao_do_operador_v399") or {}
_decl_arquivo = hashlib.sha256(open(DL.VERBATIM_ORIGEM[DL.DECLARACAO_IDX], "rb").read()).hexdigest()
R["ponto_selo_acom"].update({"erro": errsa, "stdout": stdout_sa.splitlines(), "avisos": [l for l in stdout_sa.splitlines() if "AVISO" in l], "verdict": sa.get("verdict"), "all_verified": sa.get("all_verified"), "perfil": (sa.get("values") or {}).get("perfil"),
                             "controles": [(sa.get("controles_negativos") or {}).get("n_controles"), (sa.get("controles_negativos") or {}).get("todos_recusados")], "sha256_do_um_py": (sa.get("selo") or {}).get("sha256"), "checks": [[d_, v_] for d_, v_ in (sa.get("checks") or [])]})
R["ponto_declaracao"].update({"erro": errsa, "avisos": [l for l in stdout_sa.splitlines() if "AVISO" in l], "verdict": dc.get("verdict"), "all_verified": dc.get("all_verified"), "verbatim_sha256": (dc.get("declaration") or {}).get("verbatim_sha256"),
                              "verbatim_sha256_igual_ao_arquivo": (dc.get("declaration") or {}).get("verbatim_sha256") == _decl_arquivo, "checks": [[d_, v_] for d_, v_ in (dc.get("checks") or [])]})
out["core.selo_pela_propria_tecnologia_v399"] = {"all_verified": sa.get("all_verified"), "verdict": str(sa.get("verdict"))[:300], "falhas": [d_ for d_, v_ in (sa.get("checks") or []) if not v_]}
out["core.declaracao_do_operador_v399"] = {"all_verified": dc.get("all_verified"), "verdict": str(dc.get("verdict"))[:300], "falhas": [d_ for d_, v_ in (dc.get("checks") or []) if not v_]}
'''
_SELO_FALSO = r'''psa = R["ponto_selo_acom"]
if psa.get("erro") or psa.get("avisos") or psa.get("all_verified") is not True or not psa.get("antes_do_bloco_v393") or not psa.get("logo_depois_da_afinacao_v398") or psa.get("perfil") != "ACOM-INT-C96-Q8" or psa.get("controles") != [13, True]: falsos.append("ponto_selo_acom")
pdc = R["ponto_declaracao"]
if pdc.get("erro") or pdc.get("avisos") or pdc.get("all_verified") is not True or not pdc.get("antes_do_bloco_v393") or not pdc.get("logo_depois_do_selo_acom_v399") or pdc.get("verbatim_sha256_igual_ao_arquivo") is not True: falsos.append("ponto_declaracao")
'''
entrada("exame_pontos_v398.py", regras=[
    ("(4) [v399: + os pontos do sonico_v398 e da afinacao_das_cordas_v398, logo depois da testemunha]",
     "(4) [v398: + os pontos do sonico_v398 e da afinacao_das_cordas_v398, logo depois da testemunha; v399: + os pontos do selo_pela_propria_tecnologia_v399 e da declaracao_do_operador_v399, logo depois da afinacao]", 1),
    ('+ ["teste_de_veracidade_fase9_v397"] + list(um._V397_NOMES_REGISTROS):\n    core.pop(n_, None)', '+ ["teste_de_veracidade_fase9_v397"] + list(um._V397_NOMES_REGISTROS) + ["sonico_v398", "afinacao_das_cordas_v398"] + list(um._V398_NOMES_REGISTROS):\n    core.pop(n_, None)', 1),
    ("(4a'') os PONTOS DE CHAMADA REAIS do sonico_v398 e da afinacao_das_cordas_v398 (v399):", "(4a'') os PONTOS DE CHAMADA REAIS do sonico_v398 e da afinacao_das_cordas_v398 (v398):", 1),
    ("# (4a') o PONTO DE CHAMADA REAL do teste_de_veracidade_fase9_v397 (v398): a instrucao do main (um `try` + o `print` [v398])", _SELO_BLOCO + "# (4a') o PONTO DE CHAMADA REAL do teste_de_veracidade_fase9_v397 (v397): a instrucao do main (um `try` + o `print` [v397])", 1),
    ('assert "[v398]" in unp[iv + 1] and "teste_de_veracidade_fase9_v397" in unp[iv + 1]', 'assert "[v397]" in unp[iv + 1] and "teste_de_veracidade_fase9_v397" in unp[iv + 1]', 1),
    ('"v398": [k for k in ["teste_de_veracidade_fase9_v397"] + list(um._V397_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],', '"v397": [k for k in ["teste_de_veracidade_fase9_v397"] + list(um._V397_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],', 1),
    ('"v399": [k for k in ["sonico_v398", "afinacao_das_cordas_v398"] + list(um._V398_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],',
     '"v398": [k for k in ["sonico_v398", "afinacao_das_cordas_v398"] + list(um._V398_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],\n'
     '                   "v399": [k for k in ["selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399"] + list(um._V399_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],', 1),
    ('seal = gs["seal"]; S0 = json.load(open(SELO0P, encoding="utf-8"))', 'seal = gs["seal"]; seal.update(gs["resumos_do_selo_v399"](core)); S0 = json.load(open(SELO0P, encoding="utf-8"))', 1),
    ('"registros_v398": {n_: ((seal.get("registros_v398") or {}).get(n_) or {}).get("all_verified") for n_ in um._V398_NOMES_REGISTROS}}',
     '"registros_v398": {n_: ((seal.get("registros_v398") or {}).get(n_) or {}).get("all_verified") for n_ in um._V398_NOMES_REGISTROS},\n'
     '                 "selo_pela_propria_tecnologia_v399": {x: (seal.get("selo_pela_propria_tecnologia_v399") or {}).get(x) for x in ("verdict", "all_verified", "perfil", "controles_negativos")}, "declaracao_do_operador_v399": {x: (seal.get("declaracao_do_operador_v399") or {}).get(x) for x in ("verdict", "all_verified", "verbatim_sha256")},\n'
     '                 "registros_v399": {n_: ((seal.get("registros_v399") or {}).get(n_) or {}).get("all_verified") for n_ in um._V399_NOMES_REGISTROS}}', 1),
    ('pv = R["ponto_veracidade"]\nif (pv.get("erro")', _SELO_FALSO + 'pv = R["ponto_veracidade"]\nif (pv.get("erro")', 1),
])

# ------------------------------------------------------------------------------------------- ensaio a seco
_ENS_DOC = r'''"""ensaio_a_seco_v399.py -- ENSAIO A SECO da v399 (molde: ensaio_a_seco_v398.py), SEM a GPU do rito e SEM rodar o rito. Chama NO PONTO DE CHAMADA REAL todo veredito novo ou alterado.
uso: python -B -X utf8 ensaio_a_seco_v399.py <candidato.py> <rotulo>
(1) copia o candidato; materializa o kernel embutido e confere BYTE A BYTE contra o sandbox construido; (2) importa (o rito NAO roda); UM_VERSION v399;
(3) o core da v398 SELADA + o kernel REAL: verify_tgl_kernel_formalization() de ponta a ponta com o lake simulado devolvendo os logs CRUS do sandbox (build = lake_build.log, audit = audit.log);
(4) os registros vizinhos RECOMPUTADOS (v387, v389, v390, v391, pedras_v392, varredura_v392 e os por spec da v392): iguais, ou a TROCA DITA (so' numeros); (5) o FLUXO PRINCIPAL v393+v394+v395+v396+v397+v398+v399 (as instrucoes
etiquetadas do main, na ordem do arquivo: a do psibit_v395 e a da testemunha_estatica_v396 NA FRACTALIZACAO DO UM, depois o sonico, a afinacao, o selo pela propria tecnologia e a declaracao do operador; a do teste_de_veracidade_fase9_v397 logo depois do bloco do V1);
(6) unidade: o registro do Teste da Unica Palavra recusa visivelmente (sha do resultado errado, recibo ausente, numero adulterado com sha repinado, beta, alfa, cadeia dos recibos, veredito...), o QUADRO (regra da ordem do 4,44), os specs, a cobertura;
(6c) [v398] os DOIS registros com funcao (sonico_v398 e afinacao_das_cordas_v398): tudo certo, numeros recalculados por outro caminho e controles negativos; (6d) [v399] o selo pela propria tecnologia (o round trip recalculado so' das tres partes cruas, os 13 controles,
o SHA-256 ao lado, a recusa que so' registra, o tempo) e a declaracao do operador (as dez ancoras e a pedra no kernel do rito, a fala por sha256, a trava, a direcao do testemunho) com controles negativos; (6e) [v399] o SIDECAR um_absoluto_selo_acom.json sobre o core e o selo deste ensaio;
(7) o selo (a instrucao `seal = {...}` do main + o resumo da v399) e o indice (chamada real); (8) artigo PT/EN, pdflatex x2, a secao v399 E o QUADRO NO TOPO (v397, intocado) com os numeros == os do resultado pinado; (9) .md (o quadro no topo) e manifesto;
(10) o conferidor de citacoes; (11) simular_arvore_do_nos; (12) exame_pontos."""
'''
_ENS_6D = r'''# (6d) [v399] os DOIS registros com FUNCAO da v399 (selo_pela_propria_tecnologia_v399 e declaracao_do_operador_v399): tudo certo, o round trip RECALCULADO aqui por outro caminho, a direcao do testemunho, e cada elo recusa visivelmente (controles negativos)
import time as _tm, tempfile as _tf, numpy as _np
import acom_conferencias_v399 as AC  # noqa: E402
_UMB = open(os.path.join(DRY, "um.py"), "rb").read(); _UMH = hashlib.sha256(_UMB).hexdigest()
_t0 = _tm.perf_counter(); r9s = um.selo_acom_v399(cs()); t_selo9 = _tm.perf_counter() - _t0
_s9 = r9s["selo"]; _a9 = _s9["acom"]; _ct9 = r9s["controles_negativos"]
U["selo_acom_tudo_certo"] = bool(r9s["all_verified"] is True and r9s["verdict"].startswith("TGL_SELO_PELA_PROPRIA_TECNOLOGIA_V399__") and r9s["does_not_gate_core"] is True and r9s["values"]["perfil"] == "ACOM-INT-C96-Q8" and _ct9["n_controles"] == 13 and _ct9["todos_recusados"] is True
                                and _s9["sha256"] == _UMH and _s9["bytes"] == len(_UMB) and _a9["prova_de_reconstrucao"]["igual_ao_objeto_byte_a_byte"] is True and _a9["prova_de_reconstrucao"]["bytes_divergentes"] == 0 and len(r9s["checks"]) == 6 and all(v_ for _, v_ in r9s["checks"]))
# o round trip RECALCULADO aqui, so' das tres partes cruas (a formula da Dobra + o arredondamento ao reticulado inteiro + o centro), sem as funcoes de reconstrucao do selo
_sl, _pp = um.selar(_UMB, "um.py", devolver_partes=True); _kp = _sl["acom"]["kappa"]["campos"]; _n9 = _kp["n_elements"]; _m9 = _kp["m_max_abs"]
_st9 = um._unpack2bits(_pp["psi_raw"], _n9); _th9 = _np.frombuffer(_pp["theta_raw"], dtype=_np.uint8)
_real9 = (_math.sqrt(_m9) * _np.sin(_th9.astype(_np.float64) / 255 * (_math.pi / 2))) ** 2
_rec9 = (_np.where(_st9 >= 2, -1, 1) * _np.rint(_real9).astype(_np.int64) + 96).astype(_np.uint8).tobytes()
U["selo_acom_round_trip_recalculado_aqui_so_das_tres_partes_cruas"] = bool(_rec9 == _UMB and _sl["acom"]["psi"]["sha256"] == _a9["psi"]["sha256"] and _sl["acom"]["theta"]["sha256"] == _a9["theta"]["sha256"] and _sl["acom"]["kappa"]["sha256"] == _a9["kappa"]["sha256"])
_erro_dobra9 = float(_np.abs(_real9 - _np.abs(_np.frombuffer(_UMB, dtype=_np.uint8).astype(_np.int64) - 96)).max())
U["selo_acom_dobra_pura_nao_e_exata_e_o_rint_e_dito"] = bool(0.0 < _erro_dobra9 < 0.5 and "rint" in _a9["prova_de_reconstrucao"]["metodo"] and "NAO e' da patente" in " ".join(r9s["statuses"].values()))
del _real9, _rec9, _st9, _th9
U["selo_acom_orcamento_de_tempo"] = bool(t_selo9 <= 10.0)   # medido ~1,4 s com os 13 controles; o limite folgado evita falso negativo em maquina ocupada
U["selo_acom_os_13_controles_recusados_na_ordem"] = bool([c_["id"] for c_ in _ct9["controles"]] == ["N%d" % i_ for i_ in range(1, 14)] and all(c_["ok"] and c_["obtido"].startswith("RECUSOU:") for c_ in _ct9["controles"])
                                                         and any("A_SEGUNDA_TESTEMUNHA_DETECTA_SOZINHA" in c_["obtido"] for c_ in _ct9["controles"] if c_["id"] == "N9") and next(c_.get("sem_hash_a_reconstrucao_nao_muda") for c_ in _ct9["controles"] if c_["id"] == "N5") is True)
_txt9 = json.dumps({k_: r9s.get(k_) for k_ in ("theorem", "direcao_do_testemunho", "statuses", "verdict")}, ensure_ascii=False)
U["selo_acom_textos_sem_palavra_proibida_e_sem_alegar_confidencialidade"] = bool(not um._v392_guarda_texto(_txt9) and not _GUARDA98.search(r9s["verdict"]) and "NAO alegada" in r9s["statuses"]["confidencialidade"] and not re.search(r"(?i)(inviol|indecifr|quantum[- ]safe|seguranca criptografica garantida)", _txt9))
U["selo_acom_direcao_do_testemunho_dita"] = bool("o operador testifica DA IALD" in r9s["direcao_do_testemunho"] and "a IALD nao testifica do operador" in r9s["direcao_do_testemunho"] and "Jo 8,18" in r9s["direcao_do_testemunho"])
# controles negativos do registro do selo: SHA-256 do codigo diferente; bloco embutido adulterado; a recusa so' REGISTRA (e o rito nao cai)
_rr = um.registro_core_v399(_UMB[:300000], sha256_do_codigo="0" * 64, amostra=1 << 16)
U["selo_acom_sha256_do_codigo_diferente_recusa"] = bool(_rr["all_verified"] is False and _rr["verdict"].endswith("_NOT_SEALED_THIS_RUN") and any((not v_) for _, v_ in _rr["checks"]))
_ap0 = um.ACOM_PROVENIENCIA["bloco_embutido_sha256"]; um.ACOM_PROVENIENCIA["bloco_embutido_sha256"] = "0" * 64
try:
    _rb = um.registro_core_v399(_UMB[:300000], amostra=1 << 16); _cbe = um.conferir_bloco_embutido()
finally:
    um.ACOM_PROVENIENCIA["bloco_embutido_sha256"] = _ap0
U["selo_acom_bloco_embutido_adulterado_recusa"] = bool(_rb["all_verified"] is False and _cbe["confere"] is False)
_sel0 = um.selar


def _selar_recusa(*a_, **k_):
    raise um.SeloRecusado("RECONSTRUCAO_DIVERGE")


um.selar = _selar_recusa
try:
    _rz = um.selo_acom_v399(cs()); _sc0 = um.sidecar([("x", b"abc" * 100)], quem="ensaio")
finally:
    um.selar = _sel0
U["selo_acom_recusa_so_registra_e_nao_derruba"] = bool(_rz["all_verified"] is False and _rz["selo"] is None and _rz["erro"] and _rz["verdict"].endswith("_NOT_SEALED_THIS_RUN") and _sc0["recusas"] and "REFUSED" in _sc0["veredito"] and not _sc0["objetos"])
_ns_stmts = [st_ for st_ in main.body if isinstance(st_, ast.Assign) and any(isinstance(t_, ast.Name) and t_.id in ("_not_sealed", "_recusas", "_formais", "_computacao") for t_ in st_.targets)]
_gns = dict(vars(um)); _gns["core"] = dict(cs(), selo_pela_propria_tecnologia_v399=_rz)
exec(compile(ast.fix_missing_locations(ast.Module(body=_ns_stmts, type_ignores=[])), "<not_sealed>", "exec"), _gns)
U["selo_acom_recusado_entra_em_not_sealed_this_run_formais"] = bool(len(_ns_stmts) >= 5 and "selo_pela_propria_tecnologia_v399" in _gns["_formais"] and "selo_pela_propria_tecnologia_v399" not in _gns["_recusas"])
# a DECLARACAO DO OPERADOR
d9 = um.declaracao_do_operador_v399(cs())
_dtxt = open(DL.VERBATIM_ORIGEM[DL.DECLARACAO_IDX], "rb").read()
U["declaracao_tudo_certo"] = bool(d9["all_verified"] is True and d9["verdict"].startswith("TGL_OPERATOR_DECLARATION_OF_24OCT_REGISTERED__") and d9["does_not_gate_core"] is True and d9["declaration"]["statement_verbatim"].encode("utf-8") == _dtxt and d9["declaration"]["verbatim_sha256"] == hashlib.sha256(_dtxt).hexdigest()
                                  and len(d9["declaration"]["kernel_anchors_REAL"]) == 10 and all(a_["no_kernel_do_rito"] and a_["axiomas_no_trio"] for a_ in d9["declaration"]["kernel_anchors_REAL"]) and len(d9["declaration"]["pedra_instalada"]) == 2
                                  and all(a_["no_kernel_do_rito"] and a_["axiomas_no_trio"] for a_ in d9["declaration"]["pedra_instalada"]) and "[DECLARACAO DO OPERADOR / INPUT]" in d9["declaration"]["status_of_statement"] and len(d9["declaration"]["not_declared"]) == 4)
_anc = [a_["termo"] for a_ in d9["declaration"]["kernel_anchors_REAL"]]; _ped = [a_["termo"] for a_ in d9["declaration"]["pedra_instalada"]]
ok_ = True
for t_ in _anc + _ped:   # ancora ou declaracao da pedra AUSENTE do axiom_report do rito: recusa
    c_ = cs(); c_["kernel_formalization"]["axiom_report"].pop(t_); rr_ = um.declaracao_do_operador_v399(c_)
    ok_ = ok_ and rr_["all_verified"] is False and rr_["verdict"].startswith("OPERATOR_DECLARATION_V399_NOT_SEALED")
U["declaracao_ancora_ou_pedra_ausente_do_kernel_recusa"] = bool(ok_)
ok_ = True
for t_ in _anc + _ped:   # axioma fora do trio em cada termo lido
    c_ = cs(); c_["kernel_formalization"]["axiom_report"][t_] = ["propext", "sorryAx"]; ok_ = ok_ and um.declaracao_do_operador_v399(c_)["all_verified"] is False
U["declaracao_axioma_fora_do_trio_em_cada_termo_recusa"] = bool(ok_)
_t0_ = um._V399_DECLARACAO_TXT; um._V399_DECLARACAO_TXT = _t0_ + " "
try:
    rr_ = um.declaracao_do_operador_v399(cs())
finally:
    um._V399_DECLARACAO_TXT = _t0_
_s0_ = um._V399_DECLARACAO_SHA256; um._V399_DECLARACAO_SHA256 = "0" * 64
try:
    rr2_ = um.declaracao_do_operador_v399(cs())
finally:
    um._V399_DECLARACAO_SHA256 = _s0_
U["declaracao_fala_adulterada_ou_sha256_pinado_errado_recusa"] = bool(rr_["all_verified"] is False and rr2_["all_verified"] is False)
_f0_ = um.__file__; _tmpf_ = os.path.join(DRY, "sem_trava.txt"); open(_tmpf_, "w", encoding="utf-8").write("nada aqui\n"); um.__file__ = _tmpf_
try:
    rr3_ = um.declaracao_do_operador_v399(cs())
finally:
    um.__file__ = _f0_
U["declaracao_sem_a_trava_EXECUTION_LOCKED_NOT_ONE_recusa"] = bool(rr3_["all_verified"] is False)
_txtd = json.dumps({k_: d9.get(k_) for k_ in ("declaration", "statuses", "verdict")}, ensure_ascii=False)
_RX_INV = re.compile(r"IALD\s+testifica\s+(?:a\s+mim|do\s+operador|de\s+mim)")


def _tem_inversao(txt_):
    """a IALD no papel de quem testifica DO operador, fora da citacao em que ele a RECUSA («eu nao podia dizer que IALD testifica a mim»)."""
    for m_ in _RX_INV.finditer(txt_):
        ant_ = txt_[max(0, m_.start() - 40):m_.start()].lower()
        if not (ant_.endswith("nao ") or ant_.endswith("não ") or "podia dizer que " in ant_):
            return True
    return False


U["declaracao_texto_sem_palavra_proibida_e_sem_inverter_a_direcao"] = bool(not um._v392_guarda_texto(_txtd) and not _GUARDA98.search(d9["verdict"]) and not _tem_inversao(_txtd) and not _tem_inversao(_txt9)
                                                                          and d9["declaration"]["direcao_do_testemunho"]["a_IALD"].startswith("NAO testifica do operador") and d9["declaration"]["direcao_do_testemunho"]["o_um_py"].startswith("testifica EM HASH"))
U["declaracao_diz_o_que_nao_declara"] = bool(any("o kernel prove a declaracao" in x_ for x_ in d9["declaration"]["not_declared"]) and any("diagFlow" in x_ for x_ in d9["declaration"]["not_declared"]) and any("creditado" in x_ for x_ in d9["declaration"]["not_declared"]) and any("gate" in x_ for x_ in d9["declaration"]["not_declared"]))
_rs9 = um.resumos_do_selo_v399(dict(cs(), selo_pela_propria_tecnologia_v399=r9s, declaracao_do_operador_v399=d9))
U["selo_resumos_so_veredito_bandeira_e_hashes_sem_o_selo_acom_inteiro"] = bool(set(_rs9) == {"selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399"} and _rs9["selo_pela_propria_tecnologia_v399"]["all_verified"] is True and _rs9["declaracao_do_operador_v399"]["all_verified"] is True
                                                                            and "acom" not in _rs9["selo_pela_propria_tecnologia_v399"] and _rs9["selo_pela_propria_tecnologia_v399"]["sha256_do_um_py"] == _UMH and _rs9["declaracao_do_operador_v399"]["verbatim_sha256"] == hashlib.sha256(_dtxt).hexdigest())
_blk9 = AC.extrair_bloco(open(os.path.join(DRY, "um.py"), "rb").read().decode("utf-8")); _emb9, _hemb9, _ = AC.bloco_das_fontes()
_prov9 = um.ACOM_PROVENIENCIA; _fo9 = os.path.join(HERE, "insumos", "acom", "fontes_operador")
_pins9 = {"acom_mirror.py": _prov9["codigo_embutido_de"][0]["sha256"], "acom_crypto.py": _prov9["codigo_embutido_de"][1]["sha256"], "Acom_v17_mirror_crypto.py": _prov9["origem_funcional_do_operador"]["sha256"], "run_tests.py": _prov9["testes_do_operador"]["sha256"], "tgl_core.py": _prov9["tgl_core"]["sha256"], "ACOM_Mirror_Crypto_PI_INPI.tex": _prov9["patentes"][1]["sha256"]}
U["C1_bloco_embutido_do_um_py_igual_ao_refeito_das_fontes_do_operador"] = bool(_blk9 == _emb9 and _hemb9 == _prov9["bloco_embutido_sha256"] and _cbe["calculado"] != "0" * 64)
U["C2_pinos_das_seis_fontes_do_operador_igual_ao_disco"] = bool(all(hashlib.sha256(open(os.path.join(_fo9, n_), "rb").read()).hexdigest() == h_ for n_, h_ in _pins9.items()))
rep["selo_acom_registro"] = {"verdict": r9s["verdict"], "all_verified": r9s["all_verified"], "perfil": r9s["values"]["perfil"], "bloco_embutido_sha256": r9s["values"]["bloco_embutido_sha256"], "tempo_total_s": r9s["values"]["tempo_total_s"], "selagem_total_s": t_selo9, "sha256_do_um_py": _s9["sha256"], "bytes": _s9["bytes"],
                             "psi": _a9["psi"], "theta": _a9["theta"], "kappa": {"sha256": _a9["kappa"]["sha256"], "bytes": _a9["kappa"]["bytes"]}, "lut_sha256": _a9["kappa"]["campos"]["lut_sha256"], "m_max_abs": _a9["kappa"]["campos"]["m_max_abs"], "f_exp": _a9["estrutura"]["f_exp"], "entropia_dos_estados_bits": _a9["estrutura"]["entropia_dos_estados_bits"],
                             "erro_real_maximo_antes_do_rint": _a9["prova_de_reconstrucao"]["erro_real_maximo_antes_do_rint"], "erro_dobra_pura_recalculado_aqui": _erro_dobra9, "controles": [[c_["id"], c_["obtido"]] for c_ in _ct9["controles"]], "checks": [[d_, v_] for d_, v_ in r9s["checks"]], "auditoria_de_separacao": {k_: _a9["auditoria_de_separacao"][k_] for k_ in ("fracao_de_L_negativo", "psi_redundante", "basta")}}
rep["declaracao_registro"] = {"verdict": d9["verdict"], "all_verified": d9["all_verified"], "verbatim_sha256": d9["declaration"]["verbatim_sha256"], "checks": [[d_, v_] for d_, v_ in d9["checks"]], "ancoras": _anc, "pedra": _ped, "linhas_da_trava": d9["declaration"]["termos_para_a_leitura"]["EXECUTION_LOCKED_NOT_ONE"]}
'''
_ENS_6E = r'''# (6e) [v399] o SIDECAR um_absoluto_selo_acom.json sobre o core e o selo DESTE ensaio (as copias de dry): os tres objetos selados e verificados, o SHA-256 ao lado, deterministico (dois ritos seguidos), a honestidade e o tempo
_td = tempfile.mkdtemp(prefix="v399_sidecar_"); _oo = um.OUT
try:
    shutil.copyfile(os.path.join(DRY, "core_ensaio.json"), os.path.join(_td, "um_absoluto.json")); shutil.copyfile(os.path.join(DRY, "selo_ensaio.json"), os.path.join(_td, "um_absoluto_selo.json"))
    um.OUT = _td
    _t0 = _tm.perf_counter(); _sc1 = um.selo_acom_sidecar_v399(); t_side = _tm.perf_counter() - _t0
    _b1 = open(os.path.join(_td, "um_absoluto_selo_acom.json"), "rb").read()
    _sc2 = um.selo_acom_sidecar_v399(); _b2 = open(os.path.join(_td, "um_absoluto_selo_acom.json"), "rb").read()
    _sj9 = json.loads(_b1.decode("utf-8"))
    _bytes_obj = {"um.py": _UMB, "um_absoluto.json": open(os.path.join(_td, "um_absoluto.json"), "rb").read(), "um_absoluto_selo.json": open(os.path.join(_td, "um_absoluto_selo.json"), "rb").read()}
    _ver9 = {o_["nome"]: um.verificar(_bytes_obj[o_["nome"]], o_) for o_ in _sj9["objetos"]}
finally:
    um.OUT = _oo; shutil.rmtree(_td, ignore_errors=True)
U["sidecar_tres_objetos_selados_e_verificados_com_o_sha256_ao_lado"] = bool(_sj9["veredito"].startswith("TGL_SELO_ACOM_SIDECAR_V399__ALL_OBJECTS_SEALED") and [o_["nome"] for o_ in _sj9["objetos"]] == ["um.py", "um_absoluto.json", "um_absoluto_selo.json"] and not _sj9["recusas"]
                                                                       and all(_ver9[n_]["ok"] for n_ in _ver9) and all(o_["sha256"] == hashlib.sha256(_bytes_obj[o_["nome"]]).hexdigest() and o_["bytes"] == len(_bytes_obj[o_["nome"]]) for o_ in _sj9["objetos"])
                                                                       and all(o_["acom"]["prova_de_reconstrucao"]["igual_ao_objeto_byte_a_byte"] is True for o_ in _sj9["objetos"]) and _sj9["esquema"] == "um_absoluto_selo_acom/v1 (v399)")
U["sidecar_deterministico_dois_ritos_seguidos"] = bool(_b1 == _b2)
U["sidecar_orcamento_de_tempo"] = bool(t_side <= 15.0)
_hn = _sj9["honestidade"]
U["sidecar_honestidade_sha256_e_a_primitiva_e_nenhuma_confidencialidade"] = bool("SHA-256" in _hn["primitiva_de_integridade"] and "NAO alegada" in _hn["confidencialidade"] and "NAO acrescenta resistencia criptografica independente" in _hn["o_que_a_segunda_testemunha_acrescenta"]
                                                                                 and "rint" in _hn["dobra"] and "[LEGAL]" in _hn["estatuto"] and "ofuscacao" in _hn["ofuscacao_xor"].lower() and not um._v392_guarda_texto(json.dumps(_hn, ensure_ascii=False)) and not _tem_inversao(json.dumps(_sj9, ensure_ascii=False)))
rep["sidecar"] = {"veredito": _sj9["veredito"], "objetos": [{"nome": o_["nome"], "bytes": o_["bytes"], "sha256": o_["sha256"], "psi": o_["acom"]["psi"]["sha256"], "theta": o_["acom"]["theta"]["sha256"], "kappa": o_["acom"]["kappa"]["sha256"]} for o_ in _sj9["objetos"]], "bytes_do_sidecar": len(_b1), "sha256_do_sidecar_do_ensaio": hashlib.sha256(_b1).hexdigest(),
                  "tempo_s": t_side, "verificacao": {n_: _ver9[n_]["ok"] for n_ in _ver9}}
'''
_ENS_ART = r'''TN399 = "O testemunho de dois: o selo pela própria tecnologia"; TN399E = "The testimony of two: sealing by its own technology"
'''
_ENS_MD = r'''rep["markdown"] = {"carimbo": "**Versão v399**" in md, "testemunho_v399": "O testemunho de dois: o selo pela própria tecnologia (v399, 24/10/2026)" in md, "sonico_v398_fica": "Sônico e a afinação das cordas (v398, 23/10/2026)" in md, "token_v397_fica": "O Teste da Única Palavra e a pedra Token (v397, 23/10/2026)" in md,
                   "testemunha_v396_fica": "A testemunha estática (v396, 22/10/2026)" in md, "psibit_v395_fica": "O modo psiônico na fractalização do Um (v395, 21/10/2026)" in md, "v394_fica": "A integração do Codex e as cunhagens (v394, 19/10/2026)" in md, "v393_fica": "A regra e o coração (v393, 14/10/2026)" in md}
'''
entrada("ensaio_a_seco_v398.py", regras=[
    entre('"""ensaio_a_seco_v399.py', "import hashlib, copy, io, json, os, re, shutil, subprocess, sys, ast, tempfile, textwrap", _ENS_DOC, "docstring"),
    ("# (v399: copia do quadro da v398, intocado)", "# (copia do quadro da v397, intocada pela v398 e pela v399)", 1),
    ('assert "teste_de_veracidade_fase9_v397" in core0 and "sonico_v398" not in core0 and "afinacao_das_cordas_v398" not in core0 and selo0["um_version"] == "v398"',
     'assert "teste_de_veracidade_fase9_v397" in core0 and "sonico_v398" in core0 and "afinacao_das_cordas_v398" in core0 and "selo_pela_propria_tecnologia_v399" not in core0 and "declaracao_do_operador_v399" not in core0 and "cunhagens_v399" not in core0 and selo0["um_version"] == "v398"', 1),
    ("# (5) o fluxo principal: as instrucoes etiquetadas v393, v394, v395, v398 e v399 do main (a ordem do arquivo)", "# (5) o fluxo principal: as instrucoes etiquetadas v393, v394, v395, v396, v397, v398 e v399 do main (a ordem do arquivo)", 1),
    ('or "v396" in l or "v398" in l or "v399" in l}', 'or "v396" in l or "v397" in l or "v398" in l or "v399" in l}', 1),
    ('V397N = ["teste_de_veracidade_fase9_v397"] + list(um._V397_NOMES_REGISTROS)\n', 'V397N = ["teste_de_veracidade_fase9_v397"] + list(um._V397_NOMES_REGISTROS)\nV398N = ["sonico_v398", "afinacao_das_cordas_v398"] + list(um._V398_NOMES_REGISTROS)\n', 1),
    ("for _k in V393N + V394N + V395N + V396N + V397N:", "for _k in V393N + V394N + V395N + V396N + V397N + V398N:", 1),
    ('"<main:v393+v394+v395+v396+v398+v399>"', '"<main:v393+v394+v395+v396+v397+v398+v399>"', 1),
    ('NOVAS399 = ["sonico_v398", "afinacao_das_cordas_v398"] + list(um._V398_NOMES_REGISTROS)', 'NOVAS399 = ["selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399"] + list(um._V399_NOMES_REGISTROS)', 1),
    ("for k in V393N + V394N + V395N + V396N + V397N}", "for k in V393N + V394N + V395N + V396N + V397N + V398N}", 1),
    ('"recriados_v393_a_v398": recriados,', '"registros_v399": {n_: {"all_verified": (c.get(n_) or {}).get("all_verified"), "verdict": (c.get(n_) or {}).get("verdict")} for n_ in um._V399_NOMES_REGISTROS}, "selo_pela_propria_tecnologia_v399": {x: (c.get("selo_pela_propria_tecnologia_v399") or {}).get(x) for x in ("verdict", "all_verified")}, "declaracao_do_operador_v399": {x: (c.get("declaracao_do_operador_v399") or {}).get(x) for x in ("verdict", "all_verified")}, "recriados_v393_a_v398": recriados,', 1),
    ('for n_ in um._V397_NOMES_REGISTROS + um._V396_NOMES_REGISTROS + um._V395_NOMES_REGISTROS', 'for n_ in list(um._V399_NOMES_REGISTROS) + list(um._V398_NOMES_REGISTROS) + um._V397_NOMES_REGISTROS + um._V396_NOMES_REGISTROS + um._V395_NOMES_REGISTROS', 1),
    ('all((c.get(n_) or {}).get("all_verified") is True for n_ in list(um._V397_NOMES_REGISTROS) + list(um._V398_NOMES_REGISTROS) + ["sonico_v398", "afinacao_das_cordas_v398"])',
     'all((c.get(n_) or {}).get("all_verified") is True for n_ in list(um._V397_NOMES_REGISTROS) + list(um._V398_NOMES_REGISTROS) + list(um._V399_NOMES_REGISTROS) + ["sonico_v398", "afinacao_das_cordas_v398", "selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399"])', 1),
    ("# (6c) [v399] os DOIS registros com FUNCAO: tudo certo,", "# (6c) [v398] os DOIS registros com FUNCAO: tudo certo,", 1),
    ("# o indice qualificado: chamada REAL sobre o core do ensaio", _ENS_6D + "# o indice qualificado: chamada REAL sobre o core do ensaio", 1),
    ("-- v394, v395, v398 e v399 (mais o spec de veracidade)", "-- v394, v395, v396, v397, v398 e v399 (mais o spec de veracidade)", 1),
    ("+ [VER] + list(um._V397_SPECS) + list(um._V398_SPECS):", "+ [VER] + list(um._V397_SPECS) + list(um._V398_SPECS) + list(um._V399_SPECS):", 1),
    ("+ 1 + len(um._V397_SPECS) + len(um._V398_SPECS)", "+ 1 + len(um._V397_SPECS) + len(um._V398_SPECS) + len(um._V399_SPECS)", 1),
    ('seal = _ns2.get("seal") or {}\n', 'seal = _ns2.get("seal") or {}\nseal.update(um.resumos_do_selo_v399(c))   # v399: o resumo da segunda testemunha e da declaracao do operador (a instrucao seal.update do main, que o ensaio nao executa por ser fora do fluxo etiquetado)\n', 1),
    ('"afinacao_v399_no_selo": {x: (seal.get("afinacao_das_cordas_v398") or {}).get(x) for x in ("verdict", "all_verified")}, "registros_v398": seal.get("registros_v398")}',
     '"afinacao_v398_no_selo": {x: (seal.get("afinacao_das_cordas_v398") or {}).get(x) for x in ("verdict", "all_verified")}, "registros_v398": seal.get("registros_v398"), "selo_pela_propria_tecnologia_v399_no_selo": {x: (seal.get("selo_pela_propria_tecnologia_v399") or {}).get(x) for x in ("verdict", "all_verified", "perfil", "controles_negativos")}, "declaracao_do_operador_v399_no_selo": {x: (seal.get("declaracao_do_operador_v399") or {}).get(x) for x in ("verdict", "all_verified", "verbatim_sha256")}, "registros_v399": seal.get("registros_v399")}', 1),
    ('and all(((seal.get("registros_v398") or {}).get(n_) or {}).get("all_verified") is True for n_ in um._V398_NOMES_REGISTROS)\n',
     'and all(((seal.get("registros_v398") or {}).get(n_) or {}).get("all_verified") is True for n_ in um._V398_NOMES_REGISTROS)\n           and (seal.get("selo_pela_propria_tecnologia_v399") or {}).get("all_verified") is True and (seal.get("declaracao_do_operador_v399") or {}).get("all_verified") is True and all(((seal.get("registros_v399") or {}).get(n_) or {}).get("all_verified") is True for n_ in um._V399_NOMES_REGISTROS)\n', 1),
    ('all(k in mud_selo for k in ("sonico_v398", "afinacao_das_cordas_v398", "registros_v398", "um_version"))', 'all(k in mud_selo for k in ("selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "registros_v399", "um_version"))', 1),
    ('rep["unidade"] = U; print("unidade:"', _ENS_6E + 'rep["unidade"] = U; print("unidade:"', 1),
    ('TS399 = "Sônico e a afinação das cordas"; TS399E', _ENS_ART + 'TS399 = "Sônico e a afinação das cordas"; TS399E', 1),
    ('DEVE = {"pt": [TS399,', 'DEVE = {"pt": [TN399, "A direção do testemunho.", "A declaração do operador.", "O selo pela própria tecnologia.", "A pedra Testemunho.", TS399,', 1),
    ('"en": [TS399E, "Sonic."', '"en": [TN399E, "The direction of the testimony.", "The operator\'s declaration.", "Sealing by its own technology.", "The Testemunho stone.", TS399E, "Sonic."', 1),
    ('TOC = {"pt": [TS399, T399, T398, "v384 a v39"], "en": [TS399E, T399E, T398E, "v384 to v39"]}', 'TOC = {"pt": [TN399, TS399, T399, T398, "v384 a v39"], "en": [TN399E, TS399E, T399E, T398E, "v384 to v39"]}', 1),
    ('hq = T399 if lang == "pt" else T399E; h0 = TS399 if lang == "pt" else TS399E; h1 = T399 if lang == "pt" else T399E', 'hq = T399 if lang == "pt" else T399E; h0 = TN399 if lang == "pt" else TN399E; h1 = TS399 if lang == "pt" else TS399E', 1),
    ('cv8 = dict(copy.deepcopy(c)); [cv8.pop(k, None) for k in ("sonico_v398", "afinacao_das_cordas_v398", "cunhagens_v398", "kh_n1_cobertura_v398")]\n',
     'cv8 = dict(copy.deepcopy(c)); [cv8.pop(k, None) for k in ("sonico_v398", "afinacao_das_cordas_v398", "cunhagens_v398", "kh_n1_cobertura_v398")]\ncv9 = dict(copy.deepcopy(c)); [cv9.pop(k, None) for k in ("selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "cunhagens_v399", "kh_n1_cobertura_v399")]\n', 1),
    ('_t8, _x8, _r28, _l8 = compilar(cv8, "dry_v399_var8_%s" % lang, lang, duas=False); fl8 = re.sub(r"\\s+", " ", _x8)\n',
     '_t8, _x8, _r28, _l8 = compilar(cv8, "dry_v399_var8_%s" % lang, lang, duas=False); fl8 = re.sub(r"\\s+", " ", _x8)\n    _t9, _x9, _r29, _l9 = compilar(cv9, "dry_v399_var9_%s" % lang, lang, duas=False); fl9 = re.sub(r"\\s+", " ", _x9)\n', 1),
    ('"rc_v399": _r28, "frase_guarda_v399": ("NÃO selaram todos" in fl8) if lang == "pt" else ("did NOT all seal" in fl8)}',
     '"rc_v398": _r28, "frase_guarda_v398": ("NÃO selaram todos" in fl8) if lang == "pt" else ("did NOT all seal" in fl8), "rc_v399": _r29, "frase_guarda_v399": ("NÃO selaram todos" in fl9) if lang == "pt" else ("did NOT all seal" in fl9)}', 1),
    ('or v["rc_v399"] != [0] or not v["frase_guarda_v399"]]', 'or v["rc_v398"] != [0] or not v["frase_guarda_v398"] or v["rc_v399"] != [0] or not v["frase_guarda_v399"]]', 1),
    entre('rep["markdown"] = {', 'rep["quadro"]["md"] = QV.confere_md', _ENS_MD, "markdown (rotulos das versoes anteriores nao sobem)"),
    ('_kh = [s_ for s_ in um._V398_SPECS if s_["nome"] == "kh_n1_cobertura_v398"][0]', '_kh = [s_ for s_ in um._V399_SPECS if s_["nome"] == "kh_n1_cobertura_v399"][0]', 1),
    ('_regs_sim = ("sonico_v398",', '_regs_sim = ("selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "cunhagens_v399", "kh_n1_cobertura_v399", "sonico_v398",', 1),
    ('"ponto_sonico": _ej.get("ponto_sonico"), "ponto_afinacao": _ej.get("ponto_afinacao"),', '"ponto_sonico": _ej.get("ponto_sonico"), "ponto_afinacao": _ej.get("ponto_afinacao"), "ponto_selo_acom": _ej.get("ponto_selo_acom"), "ponto_declaracao": _ej.get("ponto_declaracao"),', 1),
])
