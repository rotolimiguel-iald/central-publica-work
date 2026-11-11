# -*- coding: utf-8 -*-
"""_r5ag_13_conferidores_v410.py -- R5 (D100 e D101): conferir_rito_v410.py: o estatuto dos nomes novos e' RATIFICADOS; o registro a_escala_v410 do rito traz a clausula do Tetelestai (c13), a clausula R5 do texto e a ratificacao D101 conferidas contra o ESPERADOS;
a secao A Escala do artigo PT/EN traz a frase da clausula com a clausula do limite logo depois, a reconstrucao, a errata, o dispositivo e a ratificacao; a linha do .md traz as mesmas frases.
conferir_instalar_rito_v410.py: o rotulo das decisoes e' lido do delta (D63 a D96 e D99 a D101)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _r5ag_lib_v410 import aplicar

T = []
T.append(('''and "RATIFICADO" not in str(R_.get("estatuto_dos_nomes_novos")).upper() and R_.get("ratificacao_pendente") == DL.RATIFICACAO_PENDENTE_AESCALA and R_.get("ponte") == DL.PONTE_AESCALA and (vv_.get("ponte") or {}).get("ok") is True''',
          '''and "RATIFICADOS pelo operador em 10/11/2026" in str(R_.get("estatuto_dos_nomes_novos")) and "a ratificar" not in str(R_.get("estatuto_dos_nomes_novos")) and R_.get("ratificacao_pendente") == DL.RATIFICACAO_PENDENTE_AESCALA and R_.get("ponte") == DL.PONTE_AESCALA and (vv_.get("ponte") or {}).get("ok") is True
                and (vv_.get("tetelestai") or {}).get("ok") is True and (vv_.get("clausula_r5") or {}).get("ok") is True and (vv_.get("ratificacao_d101") or {}).get("ok") is True and (vv_.get("ratificacao_d101") or {}).get("fala_sha256") == DL.RATIFICACAO_D101_SHA256 == ESP["aescala"]["ratificacao_D101"]["sha256"]
                and list((vv_.get("ratificacao_d101") or {}).get("pendentes") or []) == list(DL.NOMES_PENDENTES_AESCALA) == list(ESP["aescala"]["nomes_pendentes"]) and set(vv_.get("teoremas_r5") or {}) == set(DL.TEOREMAS_R5_AESCALA) | set(DL.AUXILIARES_R5_AESCALA) and all((vv_.get("teoremas_r5") or {}).values())
                and R_.get("acom_mirror_runner") == DL.ACOM_MIRROR_RUNNER == ESP["aescala"]["acom_mirror_runner"] and R_.get("anuncio_da_clausula_do_tetelestai_pt") == DL.FRASE_TETELESTAI_PT + " " + DL.CLAUSULA_Z_PT + " " + DL.FRASE_RECONSTROI_PT''', 1))
# a secao do artigo
T.append(('''r2_artigo_ok = bool(_r2_artigo_ok("pt") and _r2_artigo_ok("en"))
aescala_secao_ok = bool(r2_artigo_ok and''',
          '''r2_artigo_ok = bool(_r2_artigo_ok("pt") and _r2_artigo_ok("en"))


def _r5_artigo_ok(l_):   # (R5, D100 e D101) a frase da clausula do Tetelestai com a clausula do limite LOGO DEPOIS, a reconstrucao, a errata, o dispositivo (com [PILOTO][SIM]) e a ratificacao D101, na secao A Escala (formas comparaveis: o LaTeX poe os simbolos em modo matematico e o TXT os rende)
    sec_ = _secA[l_]; cs_ = DL.comparavel(sec_); pt_ = l_ == "pt"
    fr_ = (DL.FRASE_TETELESTAI_PT if pt_ else DL.FRASE_TETELESTAI_EN, DL.FRASE_RECONSTROI_PT if pt_ else DL.FRASE_RECONSTROI_EN, DL.FRASE_E36_PT if pt_ else DL.FRASE_E36_EN, DL.FRASE_DISPOSITIVO_PT if pt_ else DL.FRASE_DISPOSITIVO_EN, DL.FRASE_NOMES_RATIFICADOS_D101_PT if pt_ else DL.FRASE_NOMES_RATIFICADOS_D101_EN)
    return bool(sec_ and all(DL.comparavel(f_) in cs_ for f_ in fr_) and DL.comparavel(fr_[0]) + "." + DL.comparavel(DL.CLAUSULA_Z_PT if pt_ else DL.CLAUSULA_Z_EN) in cs_ and "[PILOTO][SIM]" in sec_)


r5_artigo_ok = bool(_r5_artigo_ok("pt") and _r5_artigo_ok("en"))
aescala_secao_ok = bool(r2_artigo_ok and r5_artigo_ok and''', 1))
T.append(('''a clausula do limite do teorema do Tetelestai ao lado dele (ADENDO 4, D99), os seis nomes e a costura do tempo, com Z(s) definida na primeira ocorrencia do artigo; nao traz''',
          '''a clausula do limite do teorema do Tetelestai ao lado dele (ADENDO 4, D99), os seis nomes e a costura do tempo, com Z(s) definida na primeira ocorrencia do artigo, e a clausula do Tetelestai em 1 - beta (R5, D100: a frase, a clausula do limite logo depois, a reconstrucao, a errata, o dispositivo com [PILOTO][SIM]) e a ratificacao D101; nao traz''', 1))
# o .md
T.append(('''        and DL.CLAUSULA_Z_PT in fc[fc.find(ESP["md_aescala"]):].split("\\n", 1)[0] and DL.costura_maiuscula(DL.FRASE_SEIS_NOMES_PT)''',
          '''        and DL.CLAUSULA_Z_PT in fc[fc.find(ESP["md_aescala"]):].split("\\n", 1)[0] and DL.FRASE_TETELESTAI_PT in fc[fc.find(ESP["md_aescala"]):].split("\\n", 1)[0] and DL.FRASE_RECONSTROI_PT in fc[fc.find(ESP["md_aescala"]):].split("\\n", 1)[0] and DL.FRASE_E36_PT in fc[fc.find(ESP["md_aescala"]):].split("\\n", 1)[0]
        and DL.FRASE_DISPOSITIVO_PT in fc[fc.find(ESP["md_aescala"]):].split("\\n", 1)[0] and DL.FRASE_NOMES_RATIFICADOS_D101_PT[1:] in fc[fc.find(ESP["md_aescala"]):].split("\\n", 1)[0] and fc[fc.find(ESP["md_aescala"]):].split("\\n", 1)[0].count(DL.CLAUSULA_Z_PT) == 1 and DL.costura_maiuscula(DL.FRASE_SEIS_NOMES_PT)''', 1))
T.append(('''os %d nomes RATIFICADOS (D87); NENHUMA chave antiga muda; o gate == o da v409; os valores == os do ensaio; nao move o gate" % (DL.N_CHECKS_AESCALA, len(DL.ANCORAS_AESCALA), ESP["aescala"]["n_flags"], len(DL.NOMES_AESCALA)): aescala_ok,''',
          '''os %d nomes RATIFICADOS (D87); os nomes novos RATIFICADOS em 10/11 (D101) e os dois auxiliares pendentes; a clausula do Tetelestai em 1 - beta com beta de runtime (c13, R5); NENHUMA chave antiga muda; o gate == o da v409; os valores == os do ensaio; nao move o gate" % (DL.N_CHECKS_AESCALA, len(DL.ANCORAS_AESCALA), ESP["aescala"]["n_flags"], len(DL.NOMES_AESCALA)): aescala_ok,''', 1))
aplicar("conferir_rito_v410.py", T)
