# -*- coding: utf-8 -*-
"""_r2ag_10_ensaio_v410.py -- R2 (D99): ensaio_a_seco_v410.py: (a) a lista das decisoes NAO e' contigua (D97 e D98 fora do um.py); (b) cinco controles negativos novos do registro a_escala_v410 (a clausula do limite retirada de todo o texto, a EN, de um so' campo; B1 a ancora nova tirada do contrato;
B3 os seis nomes) e a expectativa precisa do controle do nome novo inexistente (a c2, pela igualdade B1, e a c11); (c) o artigo PT/EN: a clausula na secao A Escala, ao lado do teorema, a definicao de Z(s) na primeira ocorrencia, os seis nomes, a costura do tempo, nada de Unicode cru
fora do modo matematico, com controle negativo (a mesma checagem recusa a secao sem a formula); (d) a linha do .md: a clausula, os seis nomes e a costura do tempo."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _r2ag_lib_v410 import aplicar

T = []
# (a) contiguidade
T.append(('''== set(DL.DECISOES_V410) == {"D%d" % i_ for i_ in range(63, 63 + len(DL.DECISOES_V410))} and _xn10.get("n_modulos")''',
          '''== set(DL.DECISOES_V410) and not (set(DL.DECISOES_FORA_DO_UMPY) & set(_xn10.get("decisoes") or {})) and DL.DECISOES_V410[0] == "D63" and DL.DECISOES_V410[-1] == "D99" and _xn10.get("n_modulos")''', 1))   # (R2: a lista e' D63 a D96 mais D99; D97 e D98 NAO existem no um.py)

# (b) o controle do nome novo inexistente: a c2 (a igualdade B1) e a c11
T.append(('''_detA["nome_novo_inexistente_na_pedra"] = {"falhos": _falhos6(rr_), "ok": _recusa6(rr_, "MECHANICS_CHECK_FAILED") and _falhos6(rr_) == ["c11"]}''',
          '''_detA["nome_novo_inexistente_na_pedra"] = {"falhos": _falhos6(rr_), "ok": _recusa6(rr_, "MECHANICS_CHECK_FAILED") and _falhos6(rr_) == ["c2", "c11"]}   # (R2, B1: o nome novo sem ancora quebra tambem a igualdade ancoras novas == nomes novos, na c2; a falta da declaracao na pedra, na c11)''', 1))

NEW_CTRL = '''# (R2, D99; ADENDO 4) a clausula do limite do teorema do Tetelestai: retirada de todo o texto (PT), retirada da EN, retirada de UM so' campo (diz); (B1) uma ancora nova tirada do contrato; (B3) a frase dos seis nomes retirada do texto
um._V410_AESCALA_TEXT = json.loads(_tpjA.replace(DL.CLAUSULA_Z_PT, "(retirada)"))
try:
    rr_ = um.a_escala_v410(_rapidoA())
finally:
    um._V410_AESCALA_TEXT = _TPA
_detA["clausula_do_limite_retirada_do_texto"] = {"falhos": _falhos6(rr_), "ok": _tpjA.count(DL.CLAUSULA_Z_PT) >= 3 and _recusa6(rr_, "MECHANICS_CHECK_FAILED") and _falhos6(rr_) == ["c8"]}
um._V410_AESCALA_TEXT = json.loads(_tpjA.replace(DL.CLAUSULA_Z_EN, "(removed)"))
try:
    rr_ = um.a_escala_v410(_rapidoA())
finally:
    um._V410_AESCALA_TEXT = _TPA
_detA["clausula_do_limite_em_ingles_retirada"] = {"falhos": _falhos6(rr_), "ok": _tpjA.count(DL.CLAUSULA_Z_EN) >= 3 and _recusa6(rr_, "MECHANICS_CHECK_FAILED") and _falhos6(rr_) == ["c8"]}
_dz4A = _TPA["diz"]; _d4oA = list(_dz4A); _dz4A[:] = [x_.replace(DL.CLAUSULA_Z_PT, "(retirada)") for x_ in _d4oA]
try:
    rr_ = um.a_escala_v410(_rapidoA())
finally:
    _dz4A[:] = _d4oA
_detA["clausula_do_limite_retirada_de_um_campo"] = {"falhos": _falhos6(rr_), "ok": any(DL.CLAUSULA_Z_PT in x_ for x_ in _d4oA) and any(DL.CLAUSULA_Z_PT in x_ for x_ in _TPA["limites"]) and _TPA["escopo"].count(DL.CLAUSULA_Z_PT) >= 1 and _recusa6(rr_, "MECHANICS_CHECK_FAILED") and _falhos6(rr_) == ["c8"]}
_aN0A = list(_CPA["ancoras_novas"]); _CPA["ancoras_novas"] = _aN0A[1:]   # (B1: uma ancora nova tirada do contrato)
try:
    rr_ = um.a_escala_v410(_rapidoA())
finally:
    _CPA["ancoras_novas"] = _aN0A
_detA["ancora_nova_tirada_do_contrato"] = {"falhos": _falhos6(rr_), "ok": len(_aN0A) == _CPA["n_nomes_novos"] == len(_CPA["nomes_novos_a_ratificar"]) and _recusa6(rr_, "MECHANICS_CHECK_FAILED") and _falhos6(rr_) == ["c2"]}
um._V410_AESCALA_TEXT = json.loads(_tpjA.replace(DL.FRASE_SEIS_NOMES_PT, "(retirada)"))   # (B3: a frase dos seis nomes retirada)
try:
    rr_ = um.a_escala_v410(_rapidoA())
finally:
    um._V410_AESCALA_TEXT = _TPA
_detA["seis_nomes_retirados_do_texto"] = {"falhos": _falhos6(rr_), "ok": _tpjA.count(DL.FRASE_SEIS_NOMES_PT) >= 2 and _recusa6(rr_, "MECHANICS_CHECK_FAILED") and _falhos6(rr_) == ["c11"]}
_dA_ok = um.a_escala_v410(cs())'''
T.append(('''_dA_ok = um.a_escala_v410(cs())''', NEW_CTRL, 1))
T.append(('''\'forma_do_tempo_retirada_do_texto\', \'teorema_da_r4_fora_das_ancoras\'))''',
          '''\'forma_do_tempo_retirada_do_texto\', \'teorema_da_r4_fora_das_ancoras\', \'clausula_do_limite_retirada_do_texto\', \'clausula_do_limite_em_ingles_retirada\', \'clausula_do_limite_retirada_de_um_campo\', \'ancora_nova_tirada_do_contrato\', \'seis_nomes_retirados_do_texto\'))''', 1))

# (c) o artigo: DEVE (a costura do tempo, aceita sem afrouxar: o rotulo e a frase com so' a primeira letra em maiuscula) e as checagens novas
T.append(('''DEVE = {"pt": ["parede de montagem do dado", DL.FRASE_H0DN_PODER_PT, DL.FRASE_TEMPO_PT]''', '''DEVE = {"pt": ["parede de montagem do dado", DL.FRASE_H0DN_PODER_PT, DL.ROTULO_TEMPO + " " + DL.FRASE_TEMPO_PT_COSTURADA]''', 1))
T.append(('''"en": ["a wall in assembling the data", DL.FRASE_H0DN_PODER_EN, DL.FRASE_TEMPO_EN]''', '''"en": ["a wall in assembling the data", DL.FRASE_H0DN_PODER_EN, DL.ROTULO_TEMPO + " " + DL.FRASE_TEMPO_EN_COSTURADA]''', 1))

CHECK_FN = '''

def _checagens_r2_do_artigo(tex_, lang_):
    """(R2, D99; ADENDO 4; B3) o que o LaTeX da secao A Escala e a primeira ocorrencia de Z(s) tem de trazer: a clausula do limite EXATA do adendo (a formula em modo matematico), ao lado do teorema (logo depois de «linear nos bits»), a frase dos seis nomes, a definicao de Z(s) na
    primeira ocorrencia do artigo, e nenhum Unicode cru (Sigma, menos, ponto) na secao; a forma comparavel (delta_v410.comparavel) ignora so' o que o LaTeX acrescenta (cifrao, barras, chaves, parenteses, espacos)"""
    ta_ = TA410 if lang_ == "pt" else TA410E; th_ = TH410 if lang_ == "pt" else TH410E
    i0_ = tex_.find("section*{" + ta_ + "}"); i1_ = tex_.find("section*{" + th_ + "}", i0_ + 1)
    sec_ = tex_[i0_:i1_] if 0 <= i0_ < i1_ else ""
    clz_ = DL.comparavel(DL.CLAUSULA_Z_PT if lang_ == "pt" else DL.CLAUSULA_Z_EN); seis_ = DL.comparavel(DL.FRASE_SEIS_NOMES_PT if lang_ == "pt" else DL.FRASE_SEIS_NOMES_EN)
    mk_ = "linear nos bits" if lang_ == "pt" else "linear in the bits"; ib_ = sec_.find(mk_); iz_ = tex_.find("Z(s)")
    return {"secao_da_escala_achada": bool(sec_), "clausula_do_limite_na_secao": bool(sec_ and clz_ in DL.comparavel(sec_)), "clausula_ao_lado_do_teorema": bool(ib_ >= 0 and clz_ in DL.comparavel(sec_[ib_:ib_ + 1400])),
            "seis_nomes_na_secao": bool(sec_ and seis_ in DL.comparavel(sec_)), "z_definida_na_primeira_ocorrencia": bool(iz_ >= 0 and DL.comparavel(r"Z(s)=\\sum_x e^{-s\\cdot c(x)}") in DL.comparavel(tex_[iz_:iz_ + 320])),
            "unicode_cru_na_secao": [ch_ for ch_ in "\\u03a3\\u2212\\u00b7" if ch_ in sec_], "tempo_costurado_na_secao": bool(sec_ and DL.ROTULO_TEMPO in sec_ and (DL.FRASE_TEMPO_PT_COSTURADA if lang_ == "pt" else DL.FRASE_TEMPO_EN_COSTURADA) in sec_)}

'''
T.append(('''\n\ndef compilar(cv, nome, lang, duas=True):''', CHECK_FN + '''\ndef compilar(cv, nome, lang, duas=True):''', 1))
T.append(('''"toc_faltam": [w for w in TOC[lang] if w not in toc]}
    # O QUADRO no topo''',
          '''"toc_faltam": [w for w in TOC[lang] if w not in toc]}
    rep["artigo"][lang]["r2"] = _checagens_r2_do_artigo(tex, lang)   # (R2, D99) a clausula, Z(s), os seis nomes, a costura do tempo
    _neg_ = tex.replace(r"\\sum_x e^{-s\\cdot c(x)}", "x")   # o controle negativo: a mesma checagem recusa o artigo sem a formula da clausula
    rep["artigo"][lang]["r2_controle_negativo_sem_a_formula_recusa"] = bool(_neg_ != tex and not _checagens_r2_do_artigo(_neg_, lang)["clausula_do_limite_na_secao"] and not _checagens_r2_do_artigo(_neg_, lang)["clausula_ao_lado_do_teorema"] and not _checagens_r2_do_artigo(_neg_, lang)["z_definida_na_primeira_ocorrencia"])
    # O QUADRO no topo''', 1))
T.append(('''or v["toc_faltam"] or v["nd_na_secao"] or not v["quadro_logo_depois_do_resumo"]]''',
          '''or v["toc_faltam"] or v["nd_na_secao"] or not v["quadro_logo_depois_do_resumo"]
       or not all(v["r2"][k_] for k_ in ("secao_da_escala_achada", "clausula_do_limite_na_secao", "clausula_ao_lado_do_teorema", "seis_nomes_na_secao", "z_definida_na_primeira_ocorrencia", "tempo_costurado_na_secao")) or v["r2"]["unicode_cru_na_secao"] or not v["r2_controle_negativo_sem_a_formula_recusa"]]''', 1))

# (d) a linha do .md
T.append(('''"a_escala_v410_com_a_forma_da_d83_e_a_frase_canonica_na_linha": ''',
          '''"a_escala_v410_com_a_clausula_do_limite_os_seis_nomes_e_a_costura_do_tempo_na_linha": (lambda ln_: bool(DL.CLAUSULA_Z_PT in ln_ and ln_.find("linear nos bits") < ln_.find(DL.CLAUSULA_Z_PT) < ln_.find(DL.ROTULO_TEMPO + " " + DL.FRASE_TEMPO_PT_COSTURADA) and DL.costura_maiuscula(DL.FRASE_SEIS_NOMES_PT) in ln_ and ln_.count(DL.CLAUSULA_Z_PT) == 1))(md.split(DL.MD_ROTULO_ESCALA, 1)[-1].split("\\n", 1)[0]) if DL.MD_ROTULO_ESCALA in md else False,
                   "a_escala_v410_com_a_forma_da_d83_e_a_frase_canonica_na_linha": ''', 1))
aplicar("ensaio_a_seco_v410.py", T)
