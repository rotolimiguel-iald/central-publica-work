# -*- coding: utf-8 -*-
"""_r5ag_12_esperados_v410.py -- R5 (D100 e D101): gerar_esperados_v410.py: o estatuto dos nomes novos e' RATIFICADOS (o avesso da checagem antiga) no manifesto do candidato e nos values do ensaio; o manifesto traz a ratificacao D101, os teoremas e auxiliares da R5, os pendentes, a instancia da clausula e o pino do runner do ACOM Mirror;
os values do ensaio trazem a clausula do Tetelestai (c13), a clausula R5 do texto e a ratificacao D101 verificadas."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _r5ag_lib_v410 import aplicar

T = []
T.append(('''and CA["estatuto_dos_nomes_novos"] == DL.ESTATUTO_NOMES_NOVOS_AESCALA and "RATIFICADO" not in CA["estatuto_dos_nomes_novos"].upper() \\
    and CA["ratificacao_pendente"] == DL.RATIFICACAO_PENDENTE_AESCALA''',
          '''and CA["estatuto_dos_nomes_novos"] == DL.ESTATUTO_NOMES_NOVOS_AESCALA and "RATIFICADOS pelo operador em 10/11/2026" in CA["estatuto_dos_nomes_novos"] and "a ratificar" not in CA["estatuto_dos_nomes_novos"] \\
    and CA["ratificacao_pendente"] == DL.RATIFICACAO_PENDENTE_AESCALA''', 1))
T.append(('''assert set(CA["falas"]) <= set(CM["cunhagens"]), "uma fala da AEscala nao esta' entre as falas embutidas do candidato"''',
          '''assert set(CA["falas"]) <= set(CM["cunhagens"]), "uma fala da AEscala nao esta' entre as falas embutidas do candidato"
# (R5, D100 e D101) a ratificacao de 10/11, os teoremas e auxiliares da R5, a instancia da clausula e o pino citado do runner do ACOM Mirror, no manifesto do candidato
assert CA["ratificacao_D101"]["sha256"] == DL.RATIFICACAO_D101_SHA256 and CA["ratificacao_D101"]["decisao"] == "D101" and CA["ratificacao_D101"]["decisao"] in DL.DECISOES_V410 and "D100" in DL.DECISOES_V410 and list(CA["nomes_ratificados_d101"]) == list(DL.NOMES_RATIFICADOS_D101_AESCALA) and list(CA["campos_ratificados_d101"]) == list(DL.CAMPOS_RATIFICADOS_D101_AESCALA) \\
    and list(CA["nomes_pendentes"]) == list(DL.NOMES_PENDENTES_AESCALA) == list(DL.AUXILIARES_R5_AESCALA) and list(CA["teoremas_r5"]) == list(DL.TEOREMAS_R5_AESCALA) and list(CA["auxiliares_r5"]) == list(DL.AUXILIARES_R5_AESCALA) and CA["tetelestai"] == DL.TETELESTAI_AESCALA and CA["acom_mirror_runner"] == DL.ACOM_MIRROR_RUNNER \\
    and CA["acom_mirror_runner"]["sha256"][:16] in open(DL.ADENDO5_ARQ, encoding="utf-8").read(), "o manifesto da AEscala no candidato nao traz a ratificacao D101, os teoremas da R5, os pendentes, a instancia da clausula ou o pino do runner (delta_v410)"''', 1))
T.append(('''assert PA["values"].get("estatuto_dos_nomes_novos") == DL.ESTATUTO_NOMES_NOVOS_AESCALA and "RATIFICADO" not in str(PA["values"].get("estatuto_dos_nomes_novos")).upper() and''',
          '''assert PA["values"].get("estatuto_dos_nomes_novos") == DL.ESTATUTO_NOMES_NOVOS_AESCALA and "RATIFICADOS pelo operador em 10/11/2026" in str(PA["values"].get("estatuto_dos_nomes_novos")) and "a ratificar" not in str(PA["values"].get("estatuto_dos_nomes_novos")) and''', 1))
T.append(('''_bl = AV["bell"]   # o projetor de Bell 4x4:''',
          '''# (R5, D100 e D101) a clausula do Tetelestai em 1 - beta (a c13, com beta de runtime), a clausula R5 do texto e a ratificacao D101, nos values do ensaio
assert (AV["tetelestai"] or {}).get("ok") is True and AV["tetelestai"]["controle_negativo_violado"] is True and (AV["tetelestai"]["contraexemplo"] or {}).get("limiar_negativo") is True and AV["tetelestai"]["beta_entre_0_e_1"] is True and all(AV["tetelestai"]["checagens"].values()) and AV["clausula_r5"]["ok"] is True and not AV["clausula_r5"]["folhas_que_anunciam_sem_a_forma"] \\
    and not AV["clausula_r5"]["acom_mirror_sem_ressalva"] and not AV["clausula_r5"]["acom_mirror_com_desempenho"] and AV["ratificacao_d101"]["ok"] is True and AV["ratificacao_d101"]["fala_sha256"] == DL.RATIFICACAO_D101_SHA256 and list(AV["ratificacao_d101"]["pendentes"]) == list(DL.NOMES_PENDENTES_AESCALA) \\
    and set(AV["teoremas_r5"]) == set(DL.TEOREMAS_R5_AESCALA) | set(DL.AUXILIARES_R5_AESCALA) and all(AV["teoremas_r5"].values()), "o a_escala_v410 do ensaio nao traz a clausula do Tetelestai (c13), a clausula R5 do texto ou a ratificacao D101 verificadas"
_bl = AV["bell"]   # o projetor de Bell 4x4:''', 1))
aplicar("gerar_esperados_v410.py", T)
