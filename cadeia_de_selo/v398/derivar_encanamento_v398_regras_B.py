# -*- coding: utf-8 -*-
# regras (lote B) de derivar_encanamento_v398.py: o ENSAIO A SECO (ensaio_a_seco_v398.py) e o COMPARAR (comparar_v397_v398.py). As ancoras `old` sao escritas como o texto da v397 (copiado do arquivo) e passam por `bump()`, de modo que casam
# exatamente com o que o mapa mecanico produz (inclusive os rotulos que o mapa subiu e nao devia: cada regra os corrige); os `new` sao escritos direto para a v398. Contagem exata em cada regra; nada e' executado.
# O ensaio e' CUMULATIVO: os casos de unidade do registro do Teste da Unica Palavra e do quadro (v397) seguem, e entram os casos dos DOIS registros com funcao (sonico_v398 e afinacao_das_cordas_v398), com controles negativos
# (bandeira falsa, axioma fora do trio, proveniencia, fonte, escada, beta, inscricao adulterada, numero adulterado).
# Nomes no ensaio bumpado (o mapa sobe os nomes de VARIAVEL): T398/T398E = o titulo da secao v397 e do QUADRO do topo; T397/T397E = o da v396; TS398/TS398E = o da v398; V397N = os registros v396 (conteudo protegido).


def _seg(src, ini, fim):
    """O trecho EXATO da v397 entre `ini` e `fim` (inclusive), para servir de ancora (passa por bump())."""
    tx = open(os.path.join(V5, src), encoding="utf-8").read()
    a = tx.index(ini); b = tx.index(fim, a) + len(fim)
    return tx[a:b]


_UNIT_V398 = r'''# (6c) [v398] os DOIS registros com FUNCAO: tudo certo, os numeros RECALCULADOS aqui por outro caminho, e cada elo recusa visivelmente (controles negativos)
import math as _math
from fractions import Fraction as _Fr
_FN = {"sonico": um.sonico_v398, "afinacao": um.afinacao_das_cordas_v398}
_CT = {"sonico": um._V398_SONICO_CONTRACT, "afinacao": um._V398_AFINACAO_CONTRACT}
_TX = {"sonico": um._V398_SONICO_TEXT, "afinacao": um._V398_AFINACAO_TEXT}
_GUARDA98 = re.compile("(?<!NOT_)(?<!UN)" + "CONF" + "IRMED|(?<!AP)PRO" + "VED_BY|TGL_PRO" + "VED")
RF = {}
for k_ in ("sonico", "afinacao"):
    fn_, ct_, tx_ = _FN[k_], _CT[k_], _TX[k_]
    r_ = fn_(cs()); RF[k_] = r_
    U[k_ + "_tudo_certo"] = bool(r_["all_verified"] is True and r_["verdict"] == tx_["veredito_ok"] and r_["runtime_executed"] is True and r_["does_not_gate_core"] is True and all(ck_["ok"] for ck_ in r_["mechanics"]["checks"]) and r_["mechanics"]["n_checks"] >= 7
                                 and r_["exact_ladder"] is True and r_["embedded_source_ok"] is True and r_["unconditional"]["in_kernel"] is True and all(r_["formal_theorems"].values()) and all(r_["support_theorems"].values()) and all(r_["inscriptions"].values()))
    U[k_ + "_veredito_e_textos_sem_palavra_proibida"] = bool(not guarda_txt(r_) and not _GUARDA98.search(r_["verdict"]) and not um._v392_guarda_texto(json.dumps(r_["mechanics"]["checks"], ensure_ascii=False)) and not r_["guarda_p18_violacoes"])
    ok_ = True
    for th_, fl_ in ct_["theorems"].items():   # bandeira falsa de CADA teorema do contrato
        c_ = cs(); c_["kernel_formalization"][fl_] = False; rr_ = fn_(c_)
        ok_ = ok_ and rr_["all_verified"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"] and rr_["formal_theorems"][th_] is False
    U[k_ + "_bandeira_falsa_de_cada_teorema_do_contrato_recusa"] = bool(ok_)
    ok_ = True
    for th_ in list(ct_["theorems"]) + list(ct_["support"]) + list(ct_["cited_outside"]):   # axioma fora do trio em CADA termo lido
        c_ = cs(); c_["kernel_formalization"]["axiom_report"][th_] = ["propext", "sorryAx"]; rr_ = fn_(c_)
        ok_ = ok_ and rr_["all_verified"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"]
    U[k_ + "_axioma_fora_do_trio_em_cada_termo_lido_recusa"] = bool(ok_)
    ok_ = True
    for th_ in [ct_["unconditional"]["theorem"]] + list(ct_["support"]):   # proveniencia errada (o compilador diz outro modulo)
        c_ = cs(); c_["kernel_formalization"]["declaration_sources_v394"][th_] = "TGLExt/Outro.lean"; rr_ = fn_(c_)
        ok_ = ok_ and rr_["all_verified"] is False and "FORMAL_OR_SOURCE_EVIDENCE" in rr_["verdict"]
    U[k_ + "_proveniencia_errada_recusa"] = bool(ok_)
    c_ = cs(); c_["kernel_formalization"]["formal_files_sha256"][ct_["stone"]["path"]] = "0" * 64; rr_ = fn_(c_)
    ef_ = dict(um._EMBEDDED_KERNEL_FILES); um._EMBEDDED_KERNEL_FILES[ct_["stone"]["path"]] += " "
    try:
        rr2_ = fn_(cs())
    finally:
        um._EMBEDDED_KERNEL_FILES.clear(); um._EMBEDDED_KERNEL_FILES.update(ef_)
    U[k_ + "_fonte_da_pedra_adulterada_recusa"] = bool(rr_["all_verified"] is False and rr_["embedded_source_ok"] is False and rr2_["all_verified"] is False and rr2_["embedded_source_ok"] is False)
    c_ = cs(); c_["external_ladder"]["n_theorems_clean"] = int(c_["external_ladder"]["n_theorems_clean"]) - 1; rr_ = fn_(c_)
    c2_ = cs(); c2_["kernel_formalization"]["all_verified"] = False; rr2_ = fn_(c2_)
    U[k_ + "_escada_errada_ou_kernel_nao_verificado_recusa"] = bool(rr_["all_verified"] is False and rr_["exact_ladder"] is False and rr2_["all_verified"] is False)
    ok_ = True
    for ch_ in ct_["verbatins"]:
        _ant = dict(um._V398_VERBATINS2[ch_]); um._V398_VERBATINS2[ch_]["text"] += " "
        try:
            rr_ = fn_(cs()); ok_ = ok_ and rr_["all_verified"] is False and rr_["inscriptions"][ch_] is False
        finally:
            um._V398_VERBATINS2[ch_] = _ant
    U[k_ + "_inscricao_adulterada_recusa"] = bool(ok_)
# o SONICO: beta e numero adulterado
_rs = RF["sonico"]; _v = _rs["values"]
_b = um.SEALED_CODATA_ALPHA * _math.sqrt(_math.e); _th = _math.asin(_math.sqrt(_b)); _c2 = _math.cos(_th) ** 2; _s2 = _math.sin(_th) ** 2; _hn = -(_c2 * _math.log(_c2) + _s2 * _math.log(_s2))
U["sonico_numeros_recalculados_aqui"] = bool(abs(_v["beta"] - _b) <= 1e-15 and abs(_v["theta_M_rad"] - _th) <= 1e-15 and abs(_v["collapse_entropy_theta_M_nats"] - _hn) <= 1e-15 and abs(_v["collapse_entropy_theta_M_octaves"] - _hn / _math.log(2.0)) <= 1e-15
                                  and 0.0 < _hn < _math.log(2.0) and abs(_v["ln2"] - _math.log(2.0)) == 0.0 and abs(_v["exp_ln2"] - 2.0) <= 1e-15 and abs(_v["fair_bit_entropy"] - _math.log(2.0)) <= 1e-15 and _v["pin_minus_half_nat"] > 0.19)
c_ = cs(); c_["beta"] = c_["beta"] * 1.001; _rb = um.sonico_v398(c_)
_a0 = um.SEALED_CODATA_ALPHA; um.SEALED_CODATA_ALPHA = _a0 * 1.001
try:
    _ra = um.sonico_v398(cs())
finally:
    um.SEALED_CODATA_ALPHA = _a0
U["sonico_beta_adulterado_recusa"] = bool(_rb["all_verified"] is False and "BETA_IS_NOT_ALPHA_SQRT_E" in _rb["verdict"] and _ra["all_verified"] is False and "BETA_IS_NOT_ALPHA_SQRT_E" in _ra["verdict"])
_h20 = um._v398_h2; um._v398_h2 = lambda p_: _h20(p_) * 1.001
try:
    _rn = um.sonico_v398(cs())
finally:
    um._v398_h2 = _h20
U["sonico_numero_adulterado_recusa"] = bool(_rn["all_verified"] is False and "MECHANICS_CHECK_FAILED" in _rn["verdict"] and any(not ck_["ok"] for ck_ in _rn["mechanics"]["checks"]))
# a AFINACAO: a aritmetica recalculada aqui por outro caminho, a hipotese e a geometria ditas, o kappa do core, e o numero adulterado
_ra_ = RF["afinacao"]; _w = _ra_["values"]
U["afinacao_aritmetica_recalculada_aqui"] = bool(_w["zeta_minus_one"] == str(_Fr(-1, 12)) and _w["hurwitz_zeta_minus_one_half"] == str(_Fr(1, 24)) and _w["bosonic_critical_dimension"] == 26 and _w["superstring_critical_dimension"] == 10 and _w["wrong_fermion_sign_dimension"] == 26
                                                 and _w["house_spatial_dimension"] == 9 and _w["boson_direction"] == str(_Fr(-1, 24)) and _w["ns_fermion_direction"] == str(_Fr(-1, 48)) and _w["ns_direction_sum"] == str(_Fr(-1, 16))
                                                 and [d_ for d_ in range(200) if _Fr(-(d_ - 2), 24) == -1] == [26] and [d_ for d_ in range(200) if _Fr(-(d_ - 2), 16) == _Fr(-1, 2)] == [10])
U["afinacao_hipotese_geometria_e_kappa_ditos"] = bool((_ra_["hypothesis"] == {"name": "MasslessFirstLevel", "status": "KNOWN", "named_not_proved": True}) and _ra_["geometry"] == "OPEN" and _ra_["derives_strings_from_the_axiom"] is False and _w["kappa_from_core"] is None
                                                      and "kappa_is_input" in " ".join(_ra_["limites"]) and "MasslessFirstLevel" in _ra_["estatuto"] and "[KNOWN]" in _ra_["estatuto"] and "[OPEN]" in _ra_["estatuto"] and "nada aqui deriva a teoria das cordas do axioma" in " ".join(_ra_["limites"])
                                                      and len(_ra_["auxiliaries_outside_the_composition"]) == 5 and all(_ra_["auxiliaries_outside_the_composition"].values()))
_bn0 = um._v398_bernoulli
def _bern_ruim(n_):
    b_ = _bn0(n_); b_[2] = _Fr(1, 5); return b_
um._v398_bernoulli = _bern_ruim
try:
    _rz = um.afinacao_das_cordas_v398(cs())
finally:
    um._v398_bernoulli = _bn0
U["afinacao_numero_adulterado_recusa"] = bool(_rz["all_verified"] is False and "ARITHMETIC_CHECK_FAILED" in _rz["verdict"] and any(not ck_["ok"] for ck_ in _rz["mechanics"]["checks"]))
rep["sonico_registro"] = {"verdict": RF["sonico"]["verdict"], "all_verified": RF["sonico"]["all_verified"], "n_checks": RF["sonico"]["mechanics"]["n_checks"], "values": RF["sonico"]["values"], "unconditional": RF["sonico"]["unconditional"]}
rep["afinacao_registro"] = {"verdict": RF["afinacao"]["verdict"], "all_verified": RF["afinacao"]["all_verified"], "n_checks": RF["afinacao"]["mechanics"]["n_checks"], "values": RF["afinacao"]["values"], "unconditional": RF["afinacao"]["unconditional"],
                            "hypothesis": RF["afinacao"]["hypothesis"], "geometry": RF["afinacao"]["geometry"]}
'''

_VARIANTE_NOVA = r'''cv = dict(copy.deepcopy(c)); [cv.pop(k, None) for k in ("teste_de_veracidade_fase9_v397", "cunhagens_v397", "kh_n1_cobertura_v397")]
cv8 = dict(copy.deepcopy(c)); [cv8.pop(k, None) for k in ("sonico_v398", "afinacao_das_cordas_v398", "cunhagens_v398", "kh_n1_cobertura_v398")]
rep["variante"] = {}
for lang in ("pt", "en"):
    _t, _x, _r2, _l = compilar(cv, "dry_v398_var_%s" % lang, lang, duas=False); fl = re.sub(r"\s+", " ", _x)
    _t8, _x8, _r28, _l8 = compilar(cv8, "dry_v398_var8_%s" % lang, lang, duas=False); fl8 = re.sub(r"\s+", " ", _x8)
    rep["variante"][lang] = {"rc": _r2, "frase_guarda": ("NÃO selou" in fl) if lang == "pt" else ("did NOT seal" in fl),
                             "rc_v398": _r28, "frase_guarda_v398": ("NÃO selaram todos" in fl8) if lang == "pt" else ("did NOT all seal" in fl8)}
print("variante:", rep["variante"])
mau_var = [k for k, v in rep["variante"].items() if v["rc"] != [0] or not v["frase_guarda"] or v["rc_v398"] != [0] or not v["frase_guarda_v398"]]
'''

_EXPL_V398 = """EXPLICACOES = {
    "UM_VERSION": "W01: a constante unica de versao v397 -> v398",
    "_EMBEDDED_KERNEL_FILES": "K00/K01: +2 modulos (TGLExt/Sonico.lean e TGLExt/AfinacaoDasCordas.lean) e a raiz TGLExt.lean e o TGL/Audit.lean com os dois imports",
    "_LEAN_THEOREM_FLAGS": "V01: +bandeiras so' de declaracao nomeada das pedras Sonico e AfinacaoDasCordas (FLAGS_v398.json)",
    "prove_external_ladder": "V02: a lista ext_flags ganha as mesmas bandeiras (a escada sobe)",
    "_ESQUELETO_STONES": "V03: o ledger de pedras ganha a Sonico e a AfinacaoDasCordas (os 5 nomeados da afinacao fora da composicao listados como tais)",
    "_V394_FORMAL_CONTRACT": "C12: so' o numero expected_ladder (a escada desta versao); o consumidor exige a igualdade exata com a escada do rito",
    "_V394_QUADRATIC_CONTRACT": "C12: so' o numero expected_ladder",
    "_V394_NETWORK_CONTRACT": "C12: so' o numero expected_ladder",
    "_V395_PSIBIT_CONTRACT": "C12: so' o numero expected_ladder (o psibit_v395 exige a igualdade exata com a escada do rito)",
    "_V396_TESTEMUNHA_CONTRACT": "C12: so' o numero expected_ladder (a testemunha_estatica_v396 exige a igualdade exata com a escada do rito)",
    "_V397_SPECS": "C13: kh_n1_cobertura_v397 passa a piso em h2, h3, h6 e a tamanho minimo em h8 (+ errata assinada); o outro spec nao muda",
    "main": "N00/N01/N02: as chamadas de sonico_v398 e afinacao_das_cordas_v398 na fractalizacao do Um (logo depois do bloco testemunha_estatica_v396), a chamada dos registros por spec da v398 e o selo (sonico_v398, afinacao_das_cordas_v398, registros_v398)",
    "build_pt": "W04: a secao v398 do artigo PT, antes da v397 (o quadro «O Teste da Unica Palavra» do topo NAO muda)",
    "build_en": "W05: a secao v398 do artigo EN, antes da v397 (o quadro «The Test of the Only Word» do topo NAO muda)",
    "emit_canonical_md": "W09: a linha da v398 no .md canonico (o quadro do topo NAO muda)",
}
"""

# ------------------------------------------------------------------------------------------- comparar (AST): nada da v397 perdido
entrada("comparar_v396_v397.py", regras=[
    (bump(_seg("comparar_v396_v397.py", "EXPLICACOES = {", "\n}\n")), _EXPL_V398, 1),
])

# ------------------------------------------------------------------------------------------- ensaio a seco
_ENS = "ensaio_a_seco_v397.py"
entrada(_ENS, regras=[
    (bump('(8) artigo PT/EN, pdflatex x2, E o QUADRO NO TOPO com os numeros == os do resultado pinado; (9) .md (o quadro no topo) e manifesto; (10) o conferidor de citacoes; (11) simular_arvore_do_nos; (12) exame_pontos."""'),
     '(8) artigo PT/EN, pdflatex x2, a secao v398 E o QUADRO NO TOPO (v397, intocado) com os numeros == os do resultado pinado; (9) .md (o quadro no topo) e manifesto; (10) o conferidor de citacoes; (11) simular_arvore_do_nos; (12) exame_pontos; (6c) [v398] os DOIS registros com funcao (sonico_v398 e afinacao_das_cordas_v398): tudo certo, numeros recalculados por outro caminho e controles negativos."""', 1),
    (bump("import quadro_v397 as QV  # noqa: E402"), "import quadro_v397 as QV  # noqa: E402   # (v398: copia do quadro da v397, intocado)", 1),
    (bump('assert "testemunha_estatica_v396" in core0 and "teste_de_veracidade_fase9_v397" not in core0 and selo0["um_version"] == "v396"'),
     'assert "teste_de_veracidade_fase9_v397" in core0 and "sonico_v398" not in core0 and "afinacao_das_cordas_v398" not in core0 and selo0["um_version"] == "v397"', 1),
    (bump('or "v395" in l or "v396" in l or "v397" in l}'), 'or "v395" in l or "v396" in l or "v397" in l or "v398" in l}', 1),
    (bump('V396N = ["testemunha_estatica_v396"] + list(um._V396_NOMES_REGISTROS)\nfor _k in V393N + V394N + V395N + V396N:\n    core_s.pop(_k, None)   # o fluxo os recria; comparam-se depois com os da v396 selada'),
     'V396N = ["testemunha_estatica_v396"] + list(um._V396_NOMES_REGISTROS)\nV397N = ["teste_de_veracidade_fase9_v397"] + list(um._V397_NOMES_REGISTROS)\nfor _k in V393N + V394N + V395N + V396N + V397N:\n    core_s.pop(_k, None)   # o fluxo os recria; comparam-se depois com os da v397 selada', 1),
    (bump('"<main:v393+v394+v395+v396+v397>"'), '"<main:v393+v394+v395+v396+v397+v398>"', 1),
    (bump('NOVAS397 = ["teste_de_veracidade_fase9_v397"] + list(um._V397_NOMES_REGISTROS)'), 'NOVAS398 = ["sonico_v398", "afinacao_das_cordas_v398"] + list(um._V398_NOMES_REGISTROS)', 1),
    (bump('for k in V393N + V394N + V395N + V396N}'), 'for k in V393N + V394N + V395N + V396N + V397N}', 1),
    (bump('"recriados_v393_a_v396": recriados,'),
     '"registros_v398": {n_: {"all_verified": (c.get(n_) or {}).get("all_verified"), "verdict": (c.get(n_) or {}).get("verdict")} for n_ in um._V398_NOMES_REGISTROS}, '
     '"sonico_v398": {x: (c.get("sonico_v398") or {}).get(x) for x in ("verdict", "all_verified", "beta_ok")}, "afinacao_das_cordas_v398": {x: (c.get("afinacao_das_cordas_v398") or {}).get(x) for x in ("verdict", "all_verified")}, "recriados_v393_a_v397": recriados,', 1),
    (bump('and tv0.get("all_verified") is True and all((c.get(n_) or {}).get("all_verified") is True for n_ in um._V397_NOMES_REGISTROS)'),
     'and tv0.get("all_verified") is True and all((c.get(n_) or {}).get("all_verified") is True for n_ in list(um._V397_NOMES_REGISTROS) + list(um._V398_NOMES_REGISTROS) + ["sonico_v398", "afinacao_das_cordas_v398"])', 1),
    (bump('RES_P = os.path.join(HERE, "insumos", "fase9", "RESULTADO_FASE9_V2_C1_20261023_122926.json")'), "RES_P = os.path.join(DL.F9_DIR_DURAVEL, DL.F9_RESULTADO_NOME)", 1),
    ("# o indice qualificado: chamada REAL sobre o core do ensaio", _UNIT_V398 + "# o indice qualificado: chamada REAL sobre o core do ensaio", 1),
    (bump('for sp_ in list(um._V394_SPECS) + list(um._V395_SPECS) + list(um._V396_SPECS) + [VER] + list(um._V397_SPECS):'), 'for sp_ in list(um._V394_SPECS) + list(um._V395_SPECS) + list(um._V396_SPECS) + [VER] + list(um._V397_SPECS) + list(um._V398_SPECS):', 1),
    (bump('U["registros_por_spec_recusam"] = RU_ok and len(RU) == len(um._V394_SPECS) + len(um._V395_SPECS) + len(um._V396_SPECS) + 1 + len(um._V397_SPECS)'),
     'U["registros_por_spec_recusam"] = RU_ok and len(RU) == len(um._V394_SPECS) + len(um._V395_SPECS) + len(um._V396_SPECS) + 1 + len(um._V397_SPECS) + len(um._V398_SPECS)', 1),
    (bump('and seal.get("qg_closure_verdict") == selo0.get("qg_closure_verdict") and all(k in mud_selo for k in ("teste_de_veracidade_fase9_v397", "registros_v397", "um_version"))'),
     'and (seal.get("sonico_v398") or {}).get("all_verified") is True and (seal.get("afinacao_das_cordas_v398") or {}).get("all_verified") is True and all(((seal.get("registros_v398") or {}).get(n_) or {}).get("all_verified") is True for n_ in um._V398_NOMES_REGISTROS)\n'
     '           and seal.get("qg_closure_verdict") == selo0.get("qg_closure_verdict") and all(k in mud_selo for k in ("sonico_v398", "afinacao_das_cordas_v398", "registros_v398", "um_version"))', 1),
    (bump('"registros_v397": seal.get("registros_v397")}'),
     '"registros_v397": seal.get("registros_v397"), "sonico_v398_no_selo": {x: (seal.get("sonico_v398") or {}).get(x) for x in ("verdict", "all_verified")}, "afinacao_v398_no_selo": {x: (seal.get("afinacao_das_cordas_v398") or {}).get(x) for x in ("verdict", "all_verified")}, "registros_v398": seal.get("registros_v398")}', 1),
    (bump('T397 = "O Teste da Única Palavra"; T397E = "The Test of the Only Word"'),
     'TS398 = "Sônico e a afinação das cordas"; TS398E = "Sonic and the tuning of the strings"\nT398 = "O Teste da Única Palavra"; T398E = "The Test of the Only Word"   # (v397: o titulo da secao v397 e do QUADRO do topo; T397 = o da v396)', 1),
    (bump('DEVE = {"pt": [T397, "O que entra.",'), 'DEVE = {"pt": [TS398, "Sônico.", "As falas sobre o sônico.", "Afinação das cordas.", "A fala sobre as cordas.", T398, "O que entra.",', 1),
    (bump('"en": [T397E, "What enters.",'), '"en": [TS398E, "Sonic.", "The sayings on the sonic stone.", "Tuning of the strings.", "The saying on the strings.", T398E, "What enters.",', 1),
    (bump('TOC = {"pt": [T397, T396, "v384 a v39"], "en": [T397E, T396E, "v384 to v39"]}'), 'TOC = {"pt": [TS398, T398, T397, "v384 a v39"], "en": [TS398E, T398E, T397E, "v384 to v39"]}', 1),
    (bump('h0 = T397 if lang == "pt" else T397E; h1 = T396 if lang == "pt" else T396E'), 'hq = T398 if lang == "pt" else T398E; h0 = TS398 if lang == "pt" else TS398E; h1 = T398 if lang == "pt" else T398E', 1),
    (bump(r'qc["tex_antes_do_resumo"] = bool(0 <= tex.find(h0) < tex.find(r"\begin{abstract}"))'), r'qc["tex_antes_do_resumo"] = bool(0 <= tex.find(hq) < tex.find(r"\begin{abstract}"))', 1),
    (bump(_seg(_ENS, 'cv = dict(copy.deepcopy(c));', 'mau_var = [k for k, v in rep["variante"].items() if v["rc"] != [0] or not v["frase_guarda"]]\n')), _VARIANTE_NOVA, 1),
    (bump('"token_v397": "O Teste da Única Palavra e a pedra Token (v397, 23/10/2026)" in md, "testemunha_v396_fica": "A testemunha estática (v396, 22/10/2026)" in md,'),
     '"sonico_v398": "Sônico e a afinação das cordas (v398, 23/10/2026)" in md, "token_v397_fica": "O Teste da Única Palavra e a pedra Token (v397, 23/10/2026)" in md, "testemunha_v396_fica": "A testemunha estática (v396, 22/10/2026)" in md,', 1),
    (bump('_regs_sim = ("teste_de_veracidade_fase9_v397", '), '_regs_sim = ("sonico_v398", "afinacao_das_cordas_v398", "cunhagens_v398", "kh_n1_cobertura_v398", "teste_de_veracidade_fase9_v397", ', 1),
    (bump('_kh = [s_ for s_ in um._V397_SPECS if s_["nome"] == "kh_n1_cobertura_v397"][0]'), '_kh = [s_ for s_ in um._V398_SPECS if s_["nome"] == "kh_n1_cobertura_v398"][0]', 1),
    (bump('"ponto_psibit": _ej.get("ponto_psibit"), "ponto_testemunha": _ej.get("ponto_testemunha"), "ponto_veracidade": _ej.get("ponto_veracidade")}'),
     '"ponto_psibit": _ej.get("ponto_psibit"), "ponto_testemunha": _ej.get("ponto_testemunha"), "ponto_sonico": _ej.get("ponto_sonico"), "ponto_afinacao": _ej.get("ponto_afinacao"), "ponto_veracidade": _ej.get("ponto_veracidade")}', 1),
])
